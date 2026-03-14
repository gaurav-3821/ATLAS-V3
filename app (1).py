from __future__ import annotations

from pathlib import Path

import streamlit as st

from utils.data_loader import get_active_dataset
from utils.style import apply_atlas_theme, render_feature_card, render_info_banner


st.set_page_config(
    page_title="ATLAS",
    page_icon=":material/public:",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main() -> None:
    apply_atlas_theme()
    dataset, source_label = get_active_dataset()
    logo_path = Path(__file__).resolve().parent / "assets" / "atlas_logo.svg"

    logo_col, hero_col = st.columns((0.16, 0.84))
    with logo_col:
        if logo_path.exists():
            st.image(str(logo_path), use_container_width=True)

    with hero_col:
        st.markdown(
            """
            <section class="atlas-hero">
                <div class="atlas-kicker">Hack It Out - Technex'26</div>
                <h1>ATLAS</h1>
                <p class="atlas-tagline">Turning Raw Climate Data into Compelling Visual Stories</p>
                <p class="atlas-subtitle">
                    Explore decades of climate change through maps, comparisons, guided narratives,
                    and a globe view built for judges, researchers, educators, and anyone with a browser.
                </p>
            </section>
            """,
            unsafe_allow_html=True,
        )

    render_info_banner(
        f"Live source: {source_label}. A synthetic NetCDF dataset is generated automatically on first launch if needed."
    )

    cta_col, stats_col = st.columns((1.1, 1.0))
    with cta_col:
        st.markdown("### What ATLAS does")
        st.write(
            "ATLAS turns raw NetCDF climate files into an editorial-style experience. "
            "Use Explore for the main story, Compare for measurable change, Story Mode for the pitch, "
            "and 3D Globe for the final memorable reveal."
        )
        st.page_link("pages/1_Explore.py", label="Open Explore", icon=":material/travel_explore:")
        st.page_link("pages/2_Compare.py", label="Open Compare", icon=":material/compare_arrows:")
        st.page_link("pages/Trends.py", label="Open Trends", icon=":material/show_chart:")
        st.page_link("pages/3_Story_Mode.py", label="Open Story Mode", icon=":material/menu_book:")
        st.page_link("pages/4_3D_Globe.py", label="Open 3D Globe", icon=":material/public:")
        st.page_link("pages/5_About.py", label="Open About", icon=":material/info:")

    with stats_col:
        st.markdown("### Why it wins")
        st.markdown(
            """
            <div class="atlas-card-grid">
                <div class="atlas-stat-card">
                    <span class="atlas-stat-label">Years of Data</span>
                    <span class="atlas-stat-value">1950 to 2023</span>
                </div>
                <div class="atlas-stat-card">
                    <span class="atlas-stat-label">Core Views</span>
                    <span class="atlas-stat-value">Explore, Compare, Trends, Story, Globe</span>
                </div>
                <div class="atlas-stat-card">
                    <span class="atlas-stat-label">Demo Reliability</span>
                    <span class="atlas-stat-value">Zero-internet fallback</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### Experience Highlights")
    feature_cols = st.columns(3)
    with feature_cols[0]:
        render_feature_card(
            "Explore",
            "Interactive heatmaps, local trend lines, anomaly markers, and insight cards.",
        )
    with feature_cols[1]:
        render_feature_card(
            "Compare",
            "Side-by-side period comparison plus a difference map that reveals where change happened.",
        )
    with feature_cols[2]:
        render_feature_card(
            "Story Mode",
            "A guided narrative through baseline climate, El Nino, Arctic amplification, and record heat.",
        )
    extra_col_a, extra_col_b = st.columns(2)
    with extra_col_a:
        render_feature_card(
            "Trends",
            "A dedicated long-term analysis page with moving averages, baseline anomalies, and trend-per-decade metrics.",
        )
    with extra_col_b:
        render_feature_card(
            "3D Globe",
            "An orbital perspective with a latitude profile and pitch guidance for the final demo moment.",
        )

    st.markdown("### Built for Team 404")
    team_left, team_right = st.columns((1.2, 1.0))
    with team_left:
        st.write(
            "The app is the pitch. Instead of switching to slides, your team can walk judges through the climate story directly inside ATLAS."
        )
        st.write(
            "The current demo dataset includes multiple variables and realistic signals such as seasonality, long-term warming, Arctic amplification, ENSO spikes, and a 2023 heat peak."
        )
    with team_right:
        st.markdown(
            """
            <div class="atlas-panel">
                <h4>Team 404</h4>
                <p>Gaurav Tayde - Backend & Architecture</p>
                <p>Aditya Kumar - Visualization & Frontend</p>
                <p>Gaurav Yadav - Features & Data Engineering</p>
                <p>Prem Prakash Singh - Story, Testing & Pitch</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### Suggested 2-Minute Demo Route")
    route_cols = st.columns(4)
    route_items = [
        ("1. Home", "Set the hook: ATLAS makes climate data explorable without code."),
        ("2. Explore", "Show the warming map, local trend line, and annual timelapse."),
        ("3. Story Mode", "Walk judges through the four-scene climate narrative."),
        ("4. Globe", "Finish with the globe for the memorable closing visual."),
    ]
    for col, (title, body) in zip(route_cols, route_items):
        with col:
            render_feature_card(title, body)

    with st.expander("Dataset Snapshot", expanded=False):
        st.write(dict(dataset.sizes))
        st.write("Variables", list(dataset.data_vars))
        st.write("Attributes", dict(dataset.attrs))


if __name__ == "__main__":
    main()
