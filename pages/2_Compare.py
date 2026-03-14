from __future__ import annotations

import pandas as pd
import streamlit as st

from utils.chart_factory import create_heatmap
from utils.data_loader import (
    REGION_BOUNDS,
    clear_uploaded_file,
    detect_axes,
    format_variable_label,
    format_variable_units,
    get_active_dataset,
    get_dataset_choice,
    get_dataset_choices,
    get_time_values,
    period_mean,
    register_dataset_choice,
    register_uploaded_file,
    to_display_array,
    variable_label_map,
    variable_options,
)
from utils.insights_generator import generate_compare_insight
from utils.stats_engine import compute_period_change
from utils.style import apply_atlas_theme, render_info_banner, render_metric_card


st.set_page_config(page_title="ATLAS | Compare", page_icon=":material/compare_arrows:", layout="wide")


def main() -> None:
    apply_atlas_theme()
    st.title("Compare Climate Periods")

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
        region_name = st.sidebar.selectbox("Region", list(REGION_BOUNDS.keys()), index=0)

        time_values = get_time_values(data_array, axes)
        years = sorted(pd.DatetimeIndex(time_values).year.unique().tolist())
        period_a = st.sidebar.select_slider(
            "Period A",
            options=years,
            value=(years[max(len(years) // 8, 0)], years[max(len(years) // 4, 0)]),
        )
        period_b = st.sidebar.select_slider(
            "Period B",
            options=years,
            value=(years[max(len(years) // 2, 0)], years[-1]),
        )
        year_a_start, year_a_end = period_a
        year_b_start, year_b_end = period_b

        before_slice = period_mean(
            data_array,
            axes,
            pd.Timestamp(f"{year_a_start}-01-01"),
            pd.Timestamp(f"{year_a_end}-12-01"),
            region_name,
        )
        after_slice = period_mean(
            data_array,
            axes,
            pd.Timestamp(f"{year_b_start}-01-01"),
            pd.Timestamp(f"{year_b_end}-12-01"),
            region_name,
        )
        difference = after_slice - before_slice
        change = compute_period_change(before_slice, after_slice)
        label_a = f"{year_a_start}-{year_a_end}"
        label_b = f"{year_b_start}-{year_b_end}"

        metric_cols = st.columns(3)
        with metric_cols[0]:
            render_metric_card("Period A Mean", f"{change['before_mean']:.2f}", label_a)
        with metric_cols[1]:
            render_metric_card("Period B Mean", f"{change['after_mean']:.2f}", label_b)
        with metric_cols[2]:
            render_metric_card("Net Change", f"{change['delta']:+.2f}", format_variable_units(data_array) or selected_var)

        row_a, row_b = st.columns(2)
        with row_a:
            st.plotly_chart(
                create_heatmap(
                    before_slice,
                    axes,
                    title=f"{format_variable_label(data_array, selected_var)} - {label_a}",
                    colorscale="YlOrRd",
                    colorbar_title=format_variable_units(data_array) or selected_var,
                ),
                use_container_width=True,
            )
        with row_b:
            st.plotly_chart(
                create_heatmap(
                    after_slice,
                    axes,
                    title=f"{format_variable_label(data_array, selected_var)} - {label_b}",
                    colorscale="YlOrRd",
                    colorbar_title=format_variable_units(data_array) or selected_var,
                ),
                use_container_width=True,
            )

        st.plotly_chart(
            create_heatmap(
                difference,
                axes,
                title=f"Difference Map ({label_b} minus {label_a})",
                colorscale="RdBu_r",
                colorbar_title=format_variable_units(data_array) or selected_var,
            ),
            use_container_width=True,
        )

        export_cols = st.columns(2)
        with export_cols[0]:
            diff_df = difference.to_dataframe(name=selected_var).reset_index()
            st.download_button(
                "Download difference map CSV",
                data=diff_df.to_csv(index=False).encode("utf-8"),
                file_name=f"atlas_compare_{selected_var}_{label_a}_vs_{label_b}.csv",
                mime="text/csv",
                use_container_width=True,
            )
        with export_cols[1]:
            summary_csv = (
                "period,mean\n"
                f"{label_a},{change['before_mean']:.4f}\n"
                f"{label_b},{change['after_mean']:.4f}\n"
                f"delta,{change['delta']:.4f}\n"
            )
            st.download_button(
                "Download comparison summary CSV",
                data=summary_csv.encode("utf-8"),
                file_name=f"atlas_compare_summary_{selected_var}_{label_a}_vs_{label_b}.csv",
                mime="text/csv",
                use_container_width=True,
            )

        render_info_banner(
            generate_compare_insight(
                format_variable_label(data_array, selected_var),
                format_variable_units(data_array) or selected_var,
                label_a,
                label_b,
                float(change["delta"]),
            )
        )

    except Exception as exc:
        st.warning(f"Compare view hit a recoverable issue: {exc}")
        st.info("Try using the bundled demo dataset if the uploaded file is missing expected time or map dimensions.")


if __name__ == "__main__":
    main()
