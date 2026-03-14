from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go


def create_heatmap(
    map_slice,
    axes: dict[str, str | None],
    title: str,
    colorscale: str,
    colorbar_title: str,
) -> go.Figure:
    lat_axis = axes["lat"]
    lon_axis = axes["lon"]
    fig = go.Figure(
        data=[
            go.Heatmap(
                z=map_slice.values,
                x=map_slice[lon_axis].values,
                y=map_slice[lat_axis].values,
                colorscale=colorscale,
                colorbar=dict(title=colorbar_title),
                hovertemplate="Lon %{x:.1f}<br>Lat %{y:.1f}<br>Value %{z:.2f}<extra></extra>",
            )
        ]
    )
    fig.update_layout(
        title=title,
        margin=dict(l=10, r=10, t=55, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.55)",
        xaxis_title="Longitude",
        yaxis_title="Latitude",
    )
    return fig


def create_spatial_map(
    map_slice,
    axes: dict[str, str | None],
    title: str,
    colorscale: str,
    colorbar_title: str,
    projection: str,
) -> go.Figure:
    lat_axis = axes["lat"]
    lon_axis = axes["lon"]
    lon_values = np.asarray(map_slice[lon_axis].values)
    lon_values = np.where(lon_values > 180.0, lon_values - 360.0, lon_values)
    lat_values = np.asarray(map_slice[lat_axis].values)
    lon_mesh, lat_mesh = np.meshgrid(lon_values, lat_values)

    projection_map = {
        "Equirectangular": "equirectangular",
        "Robinson": "robinson",
        "Orthographic": "orthographic",
    }
    fig = go.Figure(
        go.Scattergeo(
            lon=lon_mesh.ravel(),
            lat=lat_mesh.ravel(),
            mode="markers",
            marker=dict(
                size=7,
                color=map_slice.values.ravel(),
                colorscale=colorscale,
                colorbar=dict(title=colorbar_title),
                opacity=0.9,
            ),
            hovertemplate="Lat %{lat:.1f}<br>Lon %{lon:.1f}<br>Value %{marker.color:.2f}<extra></extra>",
        )
    )
    fig.update_geos(
        projection_type=projection_map.get(projection, "equirectangular"),
        showland=True,
        landcolor="#EFE7DA",
        showocean=True,
        oceancolor="#DDE7EF",
        coastlinecolor="#B3B0AA",
        bgcolor="rgba(0,0,0,0)",
    )
    fig.update_layout(
        title=title,
        margin=dict(l=10, r=10, t=55, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def create_time_series(
    series_df: pd.DataFrame,
    value_column: str,
    trend_df: pd.DataFrame,
    anomaly_mask,
    title: str,
    y_label: str,
) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=series_df["time"],
            y=series_df[value_column],
            mode="lines+markers",
            name="Observed",
            line=dict(color="#D4654A", width=2.5),
            marker=dict(size=5),
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
    if anomaly_mask is not None and np.any(anomaly_mask):
        anomaly_df = series_df.loc[anomaly_mask]
        fig.add_trace(
            go.Scatter(
                x=anomaly_df["time"],
                y=anomaly_df[value_column],
                mode="markers",
                name="Anomalies",
                marker=dict(color="#8F2D2D", size=9, symbol="diamond"),
            )
        )

    fig.update_layout(
        title=title,
        margin=dict(l=10, r=10, t=55, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.55)",
        xaxis_title="Time",
        yaxis_title=y_label,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0.0),
    )
    return fig


def create_globe(
    map_slice,
    axes: dict[str, str | None],
    title: str,
    colorscale: str,
    colorbar_title: str,
    marker_size: int = 5,
) -> go.Figure:
    lat_axis = axes["lat"]
    lon_axis = axes["lon"]
    lon_values = np.asarray(map_slice[lon_axis].values)
    lat_values = np.asarray(map_slice[lat_axis].values)
    lon_mesh, lat_mesh = np.meshgrid(lon_values, lat_values)

    fig = go.Figure(
        go.Scattergeo(
            lon=lon_mesh.ravel(),
            lat=lat_mesh.ravel(),
            mode="markers",
            marker=dict(
                size=marker_size,
                color=map_slice.values.ravel(),
                colorscale=colorscale,
                colorbar=dict(title=colorbar_title),
                opacity=0.85,
            ),
            hovertemplate="Lon %{lon:.1f}<br>Lat %{lat:.1f}<br>Value %{marker.color:.2f}<extra></extra>",
        )
    )
    fig.update_geos(
        projection_type="orthographic",
        showland=True,
        landcolor="#EFE7DA",
        showcountries=False,
        showocean=True,
        oceancolor="#DDE7EF",
        bgcolor="rgba(0,0,0,0)",
    )
    fig.update_layout(
        title=title,
        margin=dict(l=10, r=10, t=55, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def create_latitude_profile(
    map_slice,
    axes: dict[str, str | None],
    title: str,
    x_label: str,
) -> go.Figure:
    lat_axis = axes["lat"]
    lon_axis = axes["lon"]
    profile = map_slice.mean(dim=lon_axis)

    fig = go.Figure(
        data=[
            go.Scatter(
                x=profile.values,
                y=profile[lat_axis].values,
                mode="lines",
                line=dict(color="#2C5F2D", width=3),
                fill="tozerox",
                fillcolor="rgba(44,95,45,0.12)",
                hovertemplate=f"{x_label} %{{x:.2f}}<br>Lat %{{y:.1f}}<extra></extra>",
            )
        ]
    )
    fig.update_layout(
        title=title,
        margin=dict(l=10, r=10, t=50, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.55)",
        xaxis_title=x_label,
        yaxis_title="Latitude",
        showlegend=False,
    )
    return fig


def create_animated_heatmap(
    annual_data,
    axes: dict[str, str | None],
    title: str,
    colorscale: str,
    colorbar_title: str,
) -> go.Figure:
    lat_axis = axes["lat"]
    lon_axis = axes["lon"]
    years = annual_data["year"].values.tolist()
    first = annual_data.isel(year=0)

    fig = go.Figure(
        data=[
            go.Heatmap(
                z=first.values,
                x=first[lon_axis].values,
                y=first[lat_axis].values,
                colorscale=colorscale,
                colorbar=dict(title=colorbar_title),
                hovertemplate="Lon %{x:.1f}<br>Lat %{y:.1f}<br>Value %{z:.2f}<extra></extra>",
            )
        ],
        frames=[
            go.Frame(
                data=[
                    go.Heatmap(
                        z=annual_data.sel(year=year).values,
                        x=annual_data[lon_axis].values,
                        y=annual_data[lat_axis].values,
                        colorscale=colorscale,
                    )
                ],
                name=str(year),
            )
            for year in years
        ],
    )
    fig.update_layout(
        title=title,
        margin=dict(l=10, r=10, t=55, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.55)",
        xaxis_title="Longitude",
        yaxis_title="Latitude",
        updatemenus=[
            {
                "type": "buttons",
                "showactive": False,
                "x": 1.0,
                "y": 1.15,
                "buttons": [
                    {
                        "label": "Play",
                        "method": "animate",
                        "args": [None, {"frame": {"duration": 220, "redraw": True}, "fromcurrent": True}],
                    }
                ],
            }
        ],
        sliders=[
            {
                "active": 0,
                "currentvalue": {"prefix": "Year: "},
                "steps": [
                    {
                        "label": str(year),
                        "method": "animate",
                        "args": [[str(year)], {"mode": "immediate", "frame": {"duration": 0, "redraw": True}}],
                    }
                    for year in years
                ],
            }
        ],
    )
    return fig
