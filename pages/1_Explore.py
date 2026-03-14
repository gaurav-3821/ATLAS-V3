from __future__ import annotations

import pandas as pd
import streamlit as st

from utils.chart_factory import create_animated_heatmap, create_heatmap, create_spatial_map, create_time_series
from utils.data_loader import (
    REGION_BOUNDS,
    annual_mean_series,
    clear_uploaded_file,
    detect_axes,
    format_variable_label,
    format_variable_units,
    get_active_dataset,
    get_dataset_choice,
    get_dataset_choices,
    get_time_values,
    nearest_point_series,
    prepare_map_slice,
    register_dataset_choice,
    register_uploaded_file,
    subset_region,
    to_display_array,
    variable_label_map,
    variable_options,
)
from utils.insights_generator import generate_explore_insight
from utils.stats_engine import build_trend_series, compute_linear_trend, detect_anomalies, summarize_values
from utils.style import apply_atlas_theme, render_info_banner, render_metric_card


st.set_page_config(page_title="ATLAS | Explore", page_icon=":material/travel_explore:", layout="wide")

COLOR_MAPS = {
    "Temperature Anomaly": "RdBu_r",
    "Absolute Temperature": "YlOrRd",
    "Precipitation": "YlGnBu",
    "Pressure": "Viridis",
    "Wind": "Tealgrn",
}


def resolve_colorscale(variable_name: str, anomaly_mode: bool, choice: str) -> str:
    if anomaly_mode:
        return "RdBu_r"
    if variable_name == "precipitation":
        return "YlGnBu"
    if variable_name == "wind_speed":
        return "Tealgrn"
    if variable_name == "sea_level_pressure":
        return "Viridis"
    return COLOR_MAPS.get(choice, "YlOrRd")


def main() -> None:
    apply_atlas_theme()
    st.title("Explore Climate Change")

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
        with st.spinner("Loading climate dataset..."):
            dataset, label = get_active_dataset()
        render_info_banner(f"Loaded source: {label}")

        variables = variable_options(dataset)
        if not variables:
            st.warning("No plottable climate variables were found. Switching back to the demo dataset is recommended.")
            return

        with st.sidebar:
            labels = variable_label_map(dataset)
            selected_var = st.selectbox("Variable", variables, index=0, format_func=lambda var: labels.get(var, var))
            raw_array = dataset[selected_var]
            data_array = to_display_array(raw_array, selected_var)
            axes = detect_axes(data_array)
            time_values = get_time_values(data_array, axes)
            selected_time = st.select_slider(
                "Time step",
                options=list(time_values),
                value=time_values[-1],
                format_func=lambda ts: pd.Timestamp(ts).strftime("%Y-%m"),
            )
            region_name = st.selectbox("Region", list(REGION_BOUNDS.keys()), index=0)
            color_choice = st.selectbox("Colormap", list(COLOR_MAPS.keys()), index=1)
            projection = st.selectbox("Projection", ["Equirectangular", "Robinson", "Orthographic"], index=0)
            spatial_mode = st.radio("Spatial style", ["Geo Map", "Grid Heatmap"], index=0)
            anomaly_mode = st.toggle("Show anomaly mode", value=False)
            show_timelapse = st.toggle("Show annual timelapse", value=False)

        region_view = subset_region(data_array, axes, region_name)
        lat_axis = axes["lat"]
        lon_axis = axes["lon"]
        lat_values = region_view[lat_axis].values
        lon_values = region_view[lon_axis].values

        selected_lat = st.sidebar.slider(
            "Latitude",
            min_value=float(lat_values.min()),
            max_value=float(lat_values.max()),
            value=float(lat_values[len(lat_values) // 2]),
            step=2.5,
        )
        selected_lon = st.sidebar.slider(
            "Longitude",
            min_value=float(lon_values.min()),
            max_value=float(lon_values.max()),
            value=float(lon_values[len(lon_values) // 2]),
            step=2.5,
        )

        with st.spinner("Building spatial and temporal views..."):
            map_slice = prepare_map_slice(data_array, axes, pd.Timestamp(selected_time), region_name, anomaly_mode)
            series = nearest_point_series(data_array, axes, selected_lat, selected_lon, anomaly_mode)
            series_df = series.to_dataframe(name=selected_var).reset_index().rename(columns={axes["time"]: "time"})
            trend = compute_linear_trend(series, axes["time"])
            trend_df = build_trend_series(series, axes["time"], trend)
            anomalies = detect_anomalies(series)
            summary = summarize_values(map_slice)

        metric_cols = st.columns(4)
        with metric_cols[0]:
            render_metric_card("Mean", f"{summary['mean']:.2f}", format_variable_units(data_array) or "units")
        with metric_cols[1]:
            render_metric_card("Max", f"{summary['max']:.2f}", f"{format_variable_label(data_array, selected_var)} peak")
        with metric_cols[2]:
            render_metric_card("Min", f"{summary['min']:.2f}", "Current slice minimum")
        with metric_cols[3]:
            render_metric_card("Trend", f"{trend['arrow']} {trend['slope_per_year']:+.3f}", f"{int(anomalies['count'])} anomalies at point")

        map_col, series_col = st.columns((1.3, 1.0))
        colorscale = resolve_colorscale(selected_var, anomaly_mode, color_choice)

        with map_col:
            if spatial_mode == "Geo Map":
                st.plotly_chart(
                    create_spatial_map(
                        map_slice,
                        axes,
                        title=f"{format_variable_label(data_array, selected_var)} - {pd.Timestamp(selected_time).strftime('%B %Y')}",
                        colorscale=colorscale,
                        colorbar_title=format_variable_units(data_array) or selected_var,
                        projection=projection,
                    ),
                    use_container_width=True,
                )
            else:
                st.plotly_chart(
                    create_heatmap(
                        map_slice,
                        axes,
                        title=f"{format_variable_label(data_array, selected_var)} - {pd.Timestamp(selected_time).strftime('%B %Y')}",
                        colorscale=colorscale,
                        colorbar_title=format_variable_units(data_array) or selected_var,
                    ),
                    use_container_width=True,
                )

        with series_col:
            st.plotly_chart(
                create_time_series(
                    series_df=series_df,
                    value_column=selected_var,
                    trend_df=trend_df,
                    anomaly_mask=anomalies["mask"],
                    title=f"Local Trend near ({selected_lat:.1f}, {selected_lon:.1f})",
                    y_label=f"{format_variable_label(data_array, selected_var)} ({format_variable_units(data_array)})",
                ),
                use_container_width=True,
            )

            nearest_lat = float(series.coords[axes["lat"]].item())
            nearest_lon = float(series.coords[axes["lon"]].item())
            render_info_banner(
                generate_explore_insight(
                    format_variable_label(data_array, selected_var),
                    format_variable_units(data_array) or selected_var,
                    pd.Timestamp(selected_time),
                    str(trend["label"]),
                    float(trend["slope_per_year"]),
                    int(anomalies["count"]),
                    summary,
                    nearest_lat,
                    nearest_lon,
                )
            )
            st.caption(
                f"Nearest grid cell used for the time series: latitude {nearest_lat:.1f}, longitude {nearest_lon:.1f}."
            )

        export_col_a, export_col_b = st.columns(2)
        with export_col_a:
            slice_df = map_slice.to_dataframe(name=selected_var).reset_index()
            st.download_button(
                "Download current map slice CSV",
                data=slice_df.to_csv(index=False).encode("utf-8"),
                file_name=f"atlas_{selected_var}_{pd.Timestamp(selected_time).strftime('%Y_%m')}_map.csv",
                mime="text/csv",
                use_container_width=True,
            )
        with export_col_b:
            st.download_button(
                "Download local time series CSV",
                data=series_df.to_csv(index=False).encode("utf-8"),
                file_name=f"atlas_{selected_var}_{selected_lat:.1f}_{selected_lon:.1f}_series.csv",
                mime="text/csv",
                use_container_width=True,
            )

        if show_timelapse:
            annual_view = annual_mean_series(data_array, axes, region_name, anomaly_mode)
            st.plotly_chart(
                create_animated_heatmap(
                    annual_view,
                    axes,
                    title=f"Annual Timelapse - {format_variable_label(data_array, selected_var)}",
                    colorscale=colorscale,
                    colorbar_title=format_variable_units(data_array) or selected_var,
                ),
                use_container_width=True,
            )

    except Exception as exc:
        st.warning(f"Explore view hit a recoverable issue: {exc}")
        st.info("ATLAS keeps the page alive so the demo does not crash. Try switching back to the demo dataset.")


if __name__ == "__main__":
    main()
