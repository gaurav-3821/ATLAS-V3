from __future__ import annotations

import streamlit as st

from utils.style import apply_atlas_theme, render_feature_card, render_info_banner, render_metric_card


st.set_page_config(page_title="ATLAS | About", page_icon=":material/info:", layout="wide")


def main() -> None:
    apply_atlas_theme()
    st.title("About ATLAS")
    render_info_banner("Built for Hack It Out - Technex'26 at IIT (BHU) Varanasi by Team 404.")

    metric_cols = st.columns(4)
    with metric_cols[0]:
        render_metric_card("Data Window", "1950-2023", "74 years of monthly climate history")
    with metric_cols[1]:
        render_metric_card("Variables", "4", "Temperature, precipitation, pressure, wind")
    with metric_cols[2]:
        render_metric_card("Views", "6", "Home, Explore, Compare, Trends, Story, Globe")
    with metric_cols[3]:
        render_metric_card("Demo Mode", "Offline", "Synthetic fallback keeps the app presentation-safe")

    left, right = st.columns((1.05, 0.95))
    with left:
        st.subheader("Dataset")
        st.write(
            "ATLAS is designed around ERA5-style monthly climate data from the Copernicus Climate Data Store. "
            "The bundled demo dataset mirrors a global gridded NetCDF workflow with temperature, precipitation, "
            "and sea level pressure."
        )
        st.subheader("Methodology")
        st.write(
            "Heatmaps are drawn from gridded spatial slices, local trends are computed with linear regression, "
            "and anomalies are detected with z-scores on the selected time series."
        )
        st.write(
            "Comparison Mode computes period means and subtracts them to show spatial change. Story Mode packages "
            "those same analytics into a guided narrative."
        )
        st.subheader("Why this matters")
        st.write(
            "Most climate data is technically public but practically inaccessible. ATLAS shortens the path from "
            "raw NetCDF files to a visual explanation that researchers, educators, policymakers, and the public can use."
        )

    with right:
        render_feature_card("Gaurav Tayde", "Lead Developer and backend architecture, data engine, caching, deployment.")
        render_feature_card("Aditya Kumar", "Visualization and frontend design, chart polish, globe, and interaction styling.")
        render_feature_card("Gaurav Yadav", "Comparison engine, anomaly detection, insights, and summary cards.")
        render_feature_card("Prem Prakash Singh", "Story Mode content, testing, documentation, and pitch design.")

    st.subheader("Hackathon Context")
    st.write(
        "ATLAS addresses the challenge of making NetCDF climate data accessible in a browser for researchers, educators, "
        "policymakers, and the general public. The goal is not just to show data, but to explain it."
    )
    st.markdown("- [ERA5 Reanalysis](https://cds.climate.copernicus.eu)")
    st.markdown("- [NASA Worldview](https://worldview.earthdata.nasa.gov)")
    st.markdown("- [Climate Reanalyzer](https://climatereanalyzer.org)")


if __name__ == "__main__":
    main()
