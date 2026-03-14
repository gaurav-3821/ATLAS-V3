from __future__ import annotations

import pandas as pd
import streamlit as st

from utils.chart_factory import create_heatmap
from utils.data_loader import (
    clear_uploaded_file,
    detect_axes,
    format_variable_label,
    format_variable_units,
    get_active_dataset,
    get_dataset_choice,
    get_dataset_choices,
    period_mean,
    register_dataset_choice,
    register_uploaded_file,
    to_display_array,
)
from utils.insights_generator import generate_story_insight
from utils.story_content import STORY_STEPS
from utils.style import apply_atlas_theme, render_feature_card, render_info_banner, render_metric_card, render_story_panel


st.set_page_config(page_title="ATLAS | Story Mode", page_icon=":material/menu_book:", layout="wide")


def main() -> None:
    apply_atlas_theme()
    st.title("The Climate Story")

    try:
        with st.sidebar:
            st.header("Dataset")
            dataset_choice = st.selectbox("Dataset preset", get_dataset_choices(), index=get_dataset_choices().index(get_dataset_choice()))
            register_dataset_choice(dataset_choice)
            uploaded = st.file_uploader("Upload NetCDF", type=["nc", "nc4", "cdf", "netcdf"])
            if uploaded is not None:
                register_uploaded_file(uploaded)
            if st.button("Use demo dataset"):
                clear_uploaded_file()

        dataset, label = get_active_dataset()
        render_info_banner(f"Loaded source: {label}")

        if "atlas_story_step" not in st.session_state:
            st.session_state["atlas_story_step"] = 0

        with st.sidebar:
            step_labels = [f"{idx + 1}. {step['slug']}" for idx, step in enumerate(STORY_STEPS)]
            selected_label = st.selectbox("Jump to chapter", step_labels, index=st.session_state["atlas_story_step"])
            st.session_state["atlas_story_step"] = step_labels.index(selected_label)

        step_index = st.session_state["atlas_story_step"]
        step = STORY_STEPS[step_index]
        data_array = to_display_array(dataset[step["variable"]], step["variable"])
        axes = detect_axes(data_array)

        st.caption("Story arc")
        step_cols = st.columns(len(STORY_STEPS))
        for idx, (col, chapter) in enumerate(zip(step_cols, STORY_STEPS)):
            with col:
                if idx == step_index:
                    render_story_panel(
                        f"{idx + 1}. {chapter['slug']}",
                        f"{chapter['region']} scene currently in focus.",
                    )
                else:
                    render_feature_card(
                        f"{idx + 1}. {chapter['slug']}",
                        f"{chapter['region']} chapter in the narrative.",
                    )

        start_date, end_date = step["year_range"]
        if step["map_type"] == "difference_map":
            before_start, before_end = step["comparison_range"]
            story_map = period_mean(data_array, axes, pd.Timestamp(start_date), pd.Timestamp(end_date), step["region"]) - period_mean(
                data_array,
                axes,
                pd.Timestamp(before_start),
                pd.Timestamp(before_end),
                step["region"],
            )
            colorscale = "RdBu_r"
        elif step["map_type"] == "anomaly_map":
            story_map = period_mean(data_array, axes, pd.Timestamp(start_date), pd.Timestamp(end_date), step["region"]) - period_mean(
                data_array,
                axes,
                pd.Timestamp("1951-01-01"),
                pd.Timestamp("1970-12-01"),
                step["region"],
            )
            colorscale = "RdBu_r"
        else:
            story_map = period_mean(data_array, axes, pd.Timestamp(start_date), pd.Timestamp(end_date), step["region"])
            colorscale = "YlOrRd"

        metric_cols = st.columns(3)
        with metric_cols[0]:
            render_metric_card("Window", start_date[:7], end_date[:7])
        with metric_cols[1]:
            render_metric_card("Region", step["region"], step["map_type"].replace("_", " ").title())
        with metric_cols[2]:
            render_metric_card("Variable", format_variable_label(data_array, step["variable"]), format_variable_units(data_array) or "units")

        text_col, visual_col = st.columns((0.92, 1.28))
        with text_col:
            st.markdown(f"<div class='atlas-story-label'>Step {step_index + 1} of {len(STORY_STEPS)}</div>", unsafe_allow_html=True)
            st.subheader(step["title"])
            render_story_panel("Narrative", step["caption"])
            if step.get("highlight"):
                render_story_panel("Judge Callout", step["highlight"])
            render_info_banner(generate_story_insight(step["title"], step["caption"]))
            st.markdown("### How to narrate this")
            st.write(
                "Call out what changed, why this scene matters, and what the audience should look at first on the map. "
                "This keeps the pitch sharp even under time pressure."
            )
            st.markdown("### Presenter cue")
            if step["slug"] == "Baseline":
                st.write("Tell judges this is the reference world before modern warming accelerated.")
            elif step["slug"] == "El Nino":
                st.write("Use this scene to show that climate stories can capture both long-term trends and short-term shocks.")
            elif step["slug"] == "Arctic":
                st.write("Point to the Arctic band and explain that warming is not spatially uniform.")
            else:
                st.write("Finish strong here: connect the record-breaking map to urgency and real-world impact.")

        with visual_col:
            st.plotly_chart(
                create_heatmap(
                    story_map,
                    axes,
                    title=f"{format_variable_label(data_array, step['variable'])} story view",
                    colorscale=colorscale,
                    colorbar_title=format_variable_units(data_array) or step["variable"],
                ),
                use_container_width=True,
            )
            st.caption(
                f"View mode: {step['map_type'].replace('_', ' ')}. "
                f"Variable: {format_variable_label(data_array, step['variable'])}."
            )

        prev_col, next_col = st.columns(2)
        with prev_col:
            if st.button("Previous", disabled=step_index == 0, use_container_width=True):
                st.session_state["atlas_story_step"] = max(0, step_index - 1)
                st.rerun()
        with next_col:
            if st.button("Next", disabled=step_index == len(STORY_STEPS) - 1, use_container_width=True):
                st.session_state["atlas_story_step"] = min(len(STORY_STEPS) - 1, step_index + 1)
                st.rerun()

    except Exception as exc:
        st.warning(f"Story Mode hit a recoverable issue: {exc}")
        st.info("ATLAS keeps the narrative alive even if a dataset is incomplete. Switch to the demo dataset for the full story.")


if __name__ == "__main__":
    main()
