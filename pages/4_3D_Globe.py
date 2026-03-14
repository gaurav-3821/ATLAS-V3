from __future__ import annotations

import pandas as pd
import streamlit as st

from utils.chart_factory import create_globe, create_latitude_profile
from utils.data_loader import (
    clear_uploaded_file,
    detect_axes,
    format_variable_label,
    format_variable_units,
    get_active_dataset,
    get_dataset_choice,
    get_dataset_choices,
    get_time_values,
    prepare_map_slice,
    register_dataset_choice,
    register_uploaded_file,
    to_display_array,
    variable_label_map,
    variable_options,
)
from utils.insights_generator import generate_globe_insight
from utils.stats_engine import summarize_values
from utils.style import apply_atlas_theme, render_feature_card, render_info_banner, render_metric_card, render_story_panel


st.set_page_config(page_title="ATLAS | 3D Globe", page_icon=":material/public:", layout="wide")


def main() -> None:
    apply_atlas_theme()
    st.title("3D Globe")

    with st.sidebar:
        st.header("Dataset")
        dataset_choice = st.selectbox("Dataset preset", get_dataset_choices(), index=get_dataset_choices().index(get_dataset_choice()))
        register_dataset_choice(dataset_choice)
        uploaded = st.file_uploader("Upload NetCDF", type=["nc", "nc4", "cdf", "netcdf"])
        if uploaded is not None:
            register_uploaded_file(uploaded)
        if st.button("Use demo dataset"):
            clear_uploaded_file()

    try:
        dataset, label = get_active_dataset()
        render_info_banner(f"Loaded source: {label}")
        variables = variable_options(dataset)
        if not variables:
            st.warning("No plottable climate variables were found in this dataset.")
            return
        labels = variable_label_map(dataset)
        selected_var = st.sidebar.selectbox("Variable", variables, format_func=lambda var: labels.get(var, var))
        data_array = to_display_array(dataset[selected_var], selected_var)
        axes = detect_axes(data_array)
        time_values = get_time_values(data_array, axes)
        selected_time = st.sidebar.select_slider(
            "Time step",
            options=list(time_values),
            value=time_values[-1],
            format_func=lambda ts: pd.Timestamp(ts).strftime("%Y-%m"),
        )
        anomaly_mode = st.sidebar.toggle("Show anomaly mode", value=False)
        marker_size = st.sidebar.slider("Marker size", min_value=3, max_value=8, value=5)

        globe_slice = prepare_map_slice(data_array, axes, pd.Timestamp(selected_time), "Global", anomaly_mode)
        summary = summarize_values(globe_slice)
        units_label = format_variable_units(data_array) or selected_var
        time_label = pd.Timestamp(selected_time).strftime("%B %Y")

        st.markdown("### Orbital View")
        globe_col, context_col = st.columns((1.4, 0.9))
        with globe_col:
            st.plotly_chart(
                create_globe(
                    globe_slice,
                    axes,
                    title=f"{format_variable_label(data_array, selected_var)} - {time_label}",
                    colorscale="RdBu_r" if anomaly_mode else ("YlOrRd" if selected_var == "t2m" else "Viridis"),
                    colorbar_title=units_label,
                    marker_size=marker_size,
                ),
                use_container_width=True,
            )
        with context_col:
            render_story_panel(
                "What judges should notice",
                "This view turns the climate field into a globe-scale story. Start with the warmest band, then call out how values change toward the poles.",
            )
            render_info_banner(
                generate_globe_insight(
                    format_variable_label(data_array, selected_var),
                    units_label,
                    time_label,
                    summary,
                    anomaly_mode,
                )
            )
            render_feature_card(
                "Use it in the pitch",
                "Open this after Story Mode. It works best as the final visual payoff once the climate narrative is already established.",
            )
            st.plotly_chart(
                create_latitude_profile(
                    globe_slice,
                    axes,
                    title="Latitudinal Signature",
                    x_label=units_label,
                ),
                use_container_width=True,
            )

        metric_cols = st.columns(3)
        with metric_cols[0]:
            render_metric_card("Mean", f"{summary['mean']:.2f}", units_label)
        with metric_cols[1]:
            render_metric_card("Max", f"{summary['max']:.2f}", "Current globe maximum")
        with metric_cols[2]:
            render_metric_card("Min", f"{summary['min']:.2f}", "Current globe minimum")
        render_info_banner(
            f"Globe view is showing {format_variable_label(data_array, selected_var)} for "
            f"{time_label} with a mean of {summary['mean']:.2f} "
            f"{units_label}."
        )
        globe_df = globe_slice.to_dataframe(name=selected_var).reset_index()
        st.download_button(
            "Download globe slice CSV",
            data=globe_df.to_csv(index=False).encode("utf-8"),
            file_name=f"atlas_globe_{selected_var}_{pd.Timestamp(selected_time).strftime('%Y_%m')}.csv",
            mime="text/csv",
            use_container_width=True,
        )

    except Exception as exc:
        st.warning(f"3D Globe hit a recoverable issue: {exc}")
        st.info("The globe view is designed to fail gracefully. Use the demo dataset for the best result.")


if __name__ == "__main__":
    main()
