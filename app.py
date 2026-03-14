def inject_glass_ui() -> None:
    st.markdown(
        """
        <style>
        :root {
            --atlas-ink: #10243d;
            --atlas-muted: #4c617a;
            --glass-fill: linear-gradient(135deg, rgba(255,255,255,0.30), rgba(255,255,255,0.10));
            --glass-stroke: rgba(255,255,255,0.42);
            --glass-shadow: 0 24px 60px rgba(15, 42, 84, 0.14);
        }

        .stApp {
            background:
                radial-gradient(circle at 12% 12%, rgba(125, 211, 252, 0.28), transparent 30%),
                radial-gradient(circle at 88% 18%, rgba(147, 197, 253, 0.24), transparent 28%),
                linear-gradient(140deg, #eef5ff 0%, #dde8fb 45%, #f4f8ff 100%);
            color: var(--atlas-ink);
        }

        .main .block-container {
            max-width: 1180px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        [data-testid="stSidebar"] > div:first-child {
            background: linear-gradient(180deg, rgba(255,255,255,0.28), rgba(255,255,255,0.14));
            border-right: 1px solid rgba(255,255,255,0.42);
            backdrop-filter: blur(22px) saturate(180%);
            -webkit-backdrop-filter: blur(22px) saturate(180%);
        }

        .atlas-hero,
        .atlas-panel,
        .atlas-stat-card,
        .atlas-feature-card,
        [data-testid="stExpander"],
        [data-testid="stAlert"],
        div[data-testid="stPageLink"] {
            background: var(--glass-fill);
            border: 1px solid var(--glass-stroke);
            box-shadow: var(--glass-shadow), inset 0 1px 0 rgba(255,255,255,0.35);
            backdrop-filter: blur(24px) saturate(180%);
            -webkit-backdrop-filter: blur(24px) saturate(180%);
            border-radius: 24px;
            transition:
                transform 240ms cubic-bezier(.16,1,.3,1),
                box-shadow 240ms cubic-bezier(.16,1,.3,1),
                border-color 240ms ease,
                background 240ms ease;
            animation: atlasFadeUp 720ms cubic-bezier(.16,1,.3,1) both;
        }

        .atlas-hero {
            padding: 2rem 2.2rem;
            position: relative;
            overflow: hidden;
        }

        .atlas-hero::after {
            content: "";
            position: absolute;
            inset: auto -10% -35% auto;
            width: 16rem;
            height: 16rem;
            background: radial-gradient(circle, rgba(255,255,255,0.45), rgba(255,255,255,0));
            filter: blur(12px);
            pointer-events: none;
        }

        .atlas-kicker {
            font-size: 0.82rem;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            color: #48617e;
            margin-bottom: 0.35rem;
        }

        .atlas-hero h1 {
            font-family: "Aptos Display", "Segoe UI Variable", sans-serif;
            font-size: clamp(3rem, 8vw, 5.2rem);
            line-height: 0.95;
            letter-spacing: -0.04em;
            margin: 0;
            color: #0f1f36;
        }

        .atlas-tagline {
            font-size: 1.15rem;
            color: #28405d;
            margin-top: 0.9rem;
        }

        .atlas-subtitle {
            color: var(--atlas-muted);
            max-width: 52rem;
            line-height: 1.7;
            margin-bottom: 0;
        }

        .atlas-card-grid {
            display: grid;
            gap: 1rem;
        }

        .atlas-stat-card,
        .atlas-feature-card,
        .atlas-panel {
            padding: 1.1rem 1.15rem;
        }

        .atlas-stat-label {
            display: block;
            font-size: 0.82rem;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            color: #4a627e;
            margin-bottom: 0.45rem;
        }

        .atlas-stat-value {
            display: block;
            font-size: 1.15rem;
            font-weight: 600;
            color: #10243d;
        }

        .atlas-panel h4,
        .atlas-feature-card h4 {
            font-family: "Aptos Display", "Segoe UI Variable", sans-serif;
            letter-spacing: -0.02em;
        }

        .atlas-hero:hover,
        .atlas-panel:hover,
        .atlas-stat-card:hover,
        .atlas-feature-card:hover,
        [data-testid="stExpander"]:hover,
        div[data-testid="stPageLink"]:hover {
            transform: translateY(-4px);
            box-shadow: 0 28px 70px rgba(15, 42, 84, 0.18), inset 0 1px 0 rgba(255,255,255,0.46);
            border-color: rgba(255,255,255,0.60);
        }

        div[data-testid="stPageLink"] a {
            display: block;
            padding: 0.95rem 1rem;
            text-decoration: none;
            color: var(--atlas-ink);
        }

        p, label, .stMarkdown {
            color: var(--atlas-ink);
        }

        @keyframes atlasFadeUp {
            from {
                opacity: 0;
                transform: translateY(18px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @media (max-width: 900px) {
            .atlas-hero {
                padding: 1.5rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
