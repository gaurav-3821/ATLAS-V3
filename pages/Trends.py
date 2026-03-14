from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from utils.data_loader import (
    clear_uploaded_file,
    detect_axes,
    format_variable_label,
    format_variable_units,
    get_active_dataset,
    get_dataset_choice,
    get_dataset_choices,
    get_time_values,
    nearest_point_series,
    register_dataset_choice,
    register_uploaded_file,
    to_display_array,
    variable_label_map,
    variable_options,
)
from utils.stats_engine import build_trend_series, compute_linear_trend, detect_anomalies
from utils.style import apply_atlas_theme, render_info_banner, render_metric_card, render_story_panel


st.set_page_config(page_title="ATLAS | Trends", page_icon=":material/show_chart:", layout="wide")


def create_trends_figure(
    series_df: pd.DataFrame,
    trend_df: pd.DataFrame,
    moving_df: pd.DataFrame,
    value_column: str,
    anomaly_mask,
    title: str,
    y_label: str,
) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=series_df["time"],
            y=series_df[value_column],
            mode="lines",
            name="Observed",
            line=dict(color="#D4654A", width=2),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=trend_df["time"],
            y=trend_df["trend"],
            mode="lines",
            name="Trend",
            line=dict(color="#2C5F2D", width=2, dash="dash"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=moving_df["time"],
            y=moving_df["moving_average"],
            mode="lines",
            name="Moving average",
            line=dict(color="#1A73E8", width=2.5),
        )
    )
    if anomaly_mask is not None and np.any(anomaly_mask):
        anomaly_df = series_df.loc[anomaly_mask]
        fig.add_trace(
            go.Scatter(
                x=anomaly_df["time"],
                y=anomaly_df[value_column],
                mode="markers",
                name="Anomalies",
                marker=dict(color="#8F2D2D", size=8, symbol="diamond"),
            )
        )
    fig.update_layout(
        title=title,
        margin=dict(l=10, r=10, t=50, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.55)",
        xaxis_title="Time",
        yaxis_title=y_label,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0.0),
    )
    return fig


def main() -> None:
    apply_atlas_theme()
    st.title("Climate Trends")

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
        with st.spinner("Loading trend analysis workspace..."):
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

        lat_values = data_array[axes["lat"]].values
        lon_values = data_array[axes["lon"]].values
        selected_lat = st.sidebar.number_input("Latitude", value=float(lat_values[len(lat_values) // 2]), min_value=float(lat_values.min()), max_value=float(lat_values.max()), step=2.5)
        selected_lon = st.sidebar.number_input("Longitude", value=float(lon_values[len(lon_values) // 2]), min_value=float(lon_values.min()), max_value=float(lon_values.max()), step=2.5)
        moving_window = st.sidebar.slider("Moving average window (months)", min_value=6, max_value=120, value=24, step=6)
        baseline = st.sidebar.select_slider("Baseline period", options=sorted(pd.DatetimeIndex(time_values).year.unique().tolist()), value=(1961, 1990))
        anomaly_mode = st.sidebar.toggle("Show anomalies vs local mean", value=False)

        with st.spinner("Computing trends and anomalies..."):
            series = nearest_point_series(data_array, axes, selected_lat, selected_lon, anomaly_mode)
            series_df = series.to_dataframe(name=selected_var).reset_index().rename(columns={axes["time"]: "time"})
            series_df["moving_average"] = series_df[selected_var].rolling(window=moving_window, min_periods=max(3, moving_window // 3)).mean()
            trend = compute_linear_trend(series, axes["time"])
            trend_df = build_trend_series(series, axes["time"], trend)
            anomalies = detect_anomalies(series)

        nearest_lat = float(series.coords[axes["lat"]].item())
        nearest_lon = float(series.coords[axes["lon"]].item())
        baseline_mask = (series_df["time"].dt.year >= baseline[0]) & (series_df["time"].dt.year <= baseline[1])
        baseline_mean = float(series_df.loc[baseline_mask, selected_var].mean())
        latest_value = float(series_df[selected_var].iloc[-1])
        anomaly_from_baseline = latest_value - baseline_mean
        peak_idx = series_df[selected_var].idxmax()
        peak_time = pd.Timestamp(series_df.loc[peak_idx, "time"]).strftime("%Y-%m")
        units_label = format_variable_units(data_array) or selected_var

        metric_cols = st.columns(4)
        with metric_cols[0]:
            render_metric_card("Trend / decade", f"{float(trend['slope_per_year']) * 10:+.2f}", units_label)
        with metric_cols[1]:
            render_metric_card("Latest vs baseline", f"{anomaly_from_baseline:+.2f}", f"{baseline[0]}-{baseline[1]}")
        with metric_cols[2]:
            render_metric_card("Anomalies", str(int(anomalies['count'])), "Values beyond ±2 standard deviations")
        with metric_cols[3]:
            render_metric_card("Peak month", peak_time, f"{series_df.loc[peak_idx, selected_var]:.2f} {units_label}")

        chart_col, side_col = st.columns((1.35, 0.85))
        with chart_col:
            st.plotly_chart(
                create_trends_figure(
                    series_df=series_df,
                    trend_df=trend_df,
                    moving_df=series_df[["time", "moving_average"]],
                    value_column=selected_var,
                    anomaly_mask=anomalies["mask"],
                    title=f"{format_variable_label(data_array, selected_var)} at ({nearest_lat:.1f}, {nearest_lon:.1f})",
                    y_label=f"{format_variable_label(data_array, selected_var)} ({units_label})",
                ),
                use_container_width=True,
            )

        with side_col:
            render_story_panel(
                "Trend interpretation",
                f"The selected point shows a {str(trend['label']).lower()} trend of {float(trend['slope_per_year']):+.3f} {units_label}/year.",
            )
            render_info_banner(
                f"Nearest grid cell: ({nearest_lat:.1f}, {nearest_lon:.1f}). Latest value is {latest_value:.2f} {units_label}, "
                f"which is {anomaly_from_baseline:+.2f} {units_label} relative to the {baseline[0]}-{baseline[1]} baseline."
            )
            st.download_button(
                "Download trend series CSV",
                data=series_df.to_csv(index=False).encode("utf-8"),
                file_name=f"atlas_trends_{selected_var}_{nearest_lat:.1f}_{nearest_lon:.1f}.csv",
                mime="text/csv",
                use_container_width=True,
            )

    except Exception as exc:
        st.warning(f"Trends view hit a recoverable issue: {exc}")
        st.info("ATLAS keeps the page alive so the demo stays safe. Switch to the demo dataset if an uploaded file is incomplete.")


if __name__ == "__main__":
    main()
