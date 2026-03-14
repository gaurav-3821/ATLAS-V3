from __future__ import annotations

import streamlit as st


ATLAS_CSS = """
<style>
    :root {
        --atlas-bg: #F5F0E8;
        --atlas-surface: #FAF7F2;
        --atlas-border: #C8C0B4;
        --atlas-text: #1A1A1A;
        --atlas-muted: #4A4A4A;
        --atlas-accent: #D4654A;
        --atlas-green: #2C5F2D;
        --atlas-shadow: 0 18px 40px rgba(26, 26, 26, 0.08);
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(212, 101, 74, 0.15), transparent 30%),
            linear-gradient(180deg, rgba(245, 240, 232, 1) 0%, rgba(250, 247, 242, 1) 100%);
    }

    .atlas-hero,
    .atlas-panel,
    .atlas-feature-card,
    .atlas-info-banner,
    .atlas-metric-card {
        background: rgba(255, 255, 255, 0.8);
        border: 1px solid var(--atlas-border);
        border-radius: 18px;
        box-shadow: var(--atlas-shadow);
    }

    .atlas-hero {
        padding: 2.75rem 2.25rem;
        margin-bottom: 1.5rem;
    }

    .atlas-kicker {
        color: var(--atlas-accent);
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
    }

    .atlas-hero h1 {
        margin: 0.4rem 0 0.1rem 0;
        font-size: 4rem;
        line-height: 1;
    }

    .atlas-tagline {
        font-size: 1.35rem;
        font-weight: 700;
        margin-bottom: 0.35rem;
    }

    .atlas-subtitle {
        color: var(--atlas-muted);
        max-width: 820px;
        font-size: 1.05rem;
        line-height: 1.6;
    }

    .atlas-feature-card,
    .atlas-panel,
    .atlas-info-banner {
        padding: 1.1rem 1rem;
        margin-bottom: 1rem;
    }

    .atlas-feature-card h4,
    .atlas-panel h4 {
        margin: 0 0 0.5rem 0;
    }

    .atlas-feature-card p,
    .atlas-panel p,
    .atlas-info-banner p {
        margin: 0;
        color: var(--atlas-muted);
        line-height: 1.5;
    }

    .atlas-card-grid {
        display: grid;
        grid-template-columns: 1fr;
        gap: 0.85rem;
    }

    .atlas-stat-card {
        background: rgba(255, 255, 255, 0.85);
        border: 1px solid var(--atlas-border);
        border-radius: 16px;
        padding: 1rem;
    }

    .atlas-stat-label {
        display: block;
        color: var(--atlas-muted);
        font-size: 0.85rem;
        margin-bottom: 0.25rem;
    }

    .atlas-stat-value {
        display: block;
        font-weight: 700;
        font-size: 1.1rem;
    }

    .atlas-metric-card {
        padding: 1rem;
        min-height: 120px;
    }

    .atlas-metric-label {
        color: var(--atlas-muted);
        font-size: 0.85rem;
        margin-bottom: 0.4rem;
    }

    .atlas-metric-value {
        font-size: 1.65rem;
        font-weight: 700;
        line-height: 1.2;
    }

    .atlas-metric-sub {
        margin-top: 0.35rem;
        color: var(--atlas-muted);
        font-size: 0.9rem;
    }

    .atlas-story-label {
        color: var(--atlas-accent);
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 700;
    }

    .atlas-stepper {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 0.7rem;
        margin: 0.25rem 0 1.25rem 0;
    }

    .atlas-step-chip {
        padding: 0.85rem 0.9rem;
        border-radius: 16px;
        border: 1px solid var(--atlas-border);
        background: rgba(255, 255, 255, 0.5);
    }

    .atlas-step-chip.active {
        background: rgba(212, 101, 74, 0.12);
        border-color: var(--atlas-accent);
    }

    .atlas-step-chip strong {
        display: block;
        margin-bottom: 0.2rem;
        font-size: 0.95rem;
    }

    .atlas-step-chip span {
        color: var(--atlas-muted);
        font-size: 0.82rem;
    }

    .atlas-story-panel {
        background: rgba(255, 255, 255, 0.84);
        border: 1px solid var(--atlas-border);
        border-left: 5px solid var(--atlas-accent);
        border-radius: 18px;
        box-shadow: var(--atlas-shadow);
        padding: 1.15rem 1rem;
        margin-bottom: 1rem;
    }

    .atlas-story-panel p {
        margin: 0;
        color: var(--atlas-muted);
        line-height: 1.6;
    }
</style>
"""


def apply_atlas_theme() -> None:
    st.markdown(ATLAS_CSS, unsafe_allow_html=True)


def render_feature_card(title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="atlas-feature-card">
            <h4>{title}</h4>
            <p>{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_info_banner(message: str) -> None:
    st.markdown(
        f"""
        <div class="atlas-info-banner">
            <p>{message}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metric_card(title: str, value: str, subtext: str) -> None:
    st.markdown(
        f"""
        <div class="atlas-metric-card">
            <div class="atlas-metric-label">{title}</div>
            <div class="atlas-metric-value">{value}</div>
            <div class="atlas-metric-sub">{subtext}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_story_panel(title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="atlas-story-panel">
            <h4>{title}</h4>
            <p>{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_story_stepper(steps: list[dict[str, str]], active_index: int) -> None:
    chips: list[str] = []
    for idx, step in enumerate(steps):
        active_class = "active" if idx == active_index else ""
        chips.append(
            f"""
            <div class="atlas-step-chip {active_class}">
                <strong>{idx + 1}. {step["slug"]}</strong>
                <span>{step["region"]}</span>
            </div>
            """
        )
    st.markdown(f"<div class='atlas-stepper'>{''.join(chips)}</div>", unsafe_allow_html=True)
