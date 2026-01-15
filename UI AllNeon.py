import streamlit as st
import random
import os

# ==============================================================================
# PAGE CONFIG
# ==============================================================================
st.set_page_config(
    page_title="AI Stylist | Multi Theme Edition",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# THEME DEFINITIONS
# ==============================================================================
THEMES = {
    "Cyberpunk": """
    background: radial-gradient(circle at top, #05070A 0%, #02030A 70%);
    main: #00F6FF;
    sub: #FF2A9D;
    accent: #39FF14;
    base: #02030A;
    """,

    "Bio Neon": """
    background: radial-gradient(circle, rgba(57,255,20,0.15), transparent 60%), #020A05;
    main: #39FF14;
    sub: #FF4FD8;
    accent: #20FFC6;
    base: #020A05;
    """,

    "Eco Hi-Tech": """
    background: radial-gradient(circle, rgba(46,204,113,0.15), transparent 60%), #02130A;
    main: #2ECC71;
    sub: #FFD700;
    accent: #FF6F91;
    base: #02130A;
    """,

    "Hologram": """
    background: linear-gradient(120deg,
        rgba(0,191,255,0.15),
        rgba(255,105,180,0.15),
        rgba(138,43,226,0.15)
    ), #05060A;
    main: #6ECFFF;
    sub: #FF8DEB;
    accent: #CFAAFF;
    base: #05060A;
    """,

    "Electric Sunset": """
    background: radial-gradient(circle at bottom, rgba(255,94,77,0.2), transparent 60%), #160015;
    main: #FF5E9C;
    sub: #FF8C00;
    accent: #FFD54F;
    base: #160015;
    """,

    "Shinto": """
    background: radial-gradient(circle, rgba(255,215,0,0.1), transparent 60%), #000814;
    main: #FFFFFF;
    sub: #FF4500;
    accent: #00BFFF;
    base: #000814;
    """,

    "Wafu Neon Sakura": """
    background: radial-gradient(circle, rgba(255,105,180,0.15), transparent 60%), #0A0F1F;
    main: #FF69B4;
    sub: #00BFFF;
    accent: #FFD700;
    base: #0A0F1F;
    """
}

# ==============================================================================
# THEME APPLY
# ==============================================================================
def apply_theme(theme_css):
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Orbitron', sans-serif;
    }}

    .stApp {{
        {theme_css}
        color: #F8FAFF;
    }}

    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, var(--base), #000);
        border-right: 1px solid rgba(255,255,255,0.15);
    }}

    h1, h2 {{
        color: var(--main);
        text-shadow: 0 0 12px var(--main);
    }}

    div.stButton > button {{
        background: linear-gradient(135deg, var(--main), var(--sub));
        color: #000;
        border-radius: 14px;
        box-shadow: 0 0 18px var(--accent);
        width: 100%;
    }}

    img {{
        border-radius: 16px;
        box-shadow: 0 0 24px var(--main);
    }}
    </style>
    """.replace("var(--main)", extract(theme_css, "main"))
       .replace("var(--sub)", extract(theme_css, "sub"))
       .replace("var(--accent)", extract(theme_css, "accent"))
       .replace("var(--base)", extract(theme_css, "base")),
    unsafe_allow_html=True)

def extract(css, key):
    for line in css.splitlines():
        if key in line:
            return line.split(":")[1].replace(";", "").strip()
    return "#FFF"

# ==============================================================================
# DATA
# ==============================================================================
class StyleConfig:
    GENRES = ["streetwear", "casual", "minimal", "vintage", "kireime"]
    COLORS = ["black", "white", "gray", "navy", "brown", "beige", "green", "red"]

# ==============================================================================
# IMAGE RECOMMENDER
# ==============================================================================
class ImageRecommender:
    @staticmethod
    def recommend(gender, style_scores, color_scores, max_images=3, min_weight=12):
        base_dir = "ai_images"
        gender_dir = "male" if gender == "male" else "female"
        candidates = []

        for s, sv in style_scores.items():
            for c, cv in color_scores.items():
                if sv + cv < min_weight:
                    continue
                path = os.path.join(base_dir, gender_dir, s, c)
                if os.path.exists(path):
                    for f in os.listdir(path):
                        if f.lower().endswith((".jpg", ".png")):
                            candidates.append({
                                "path": os.path.join(path, f),
                                "style": s,
                                "color": c,
                                "weight": sv + cv
                            })

        return random.sample(candidates, min(len(candidates), max_images)) if candidates else []

# ==============================================================================
# SIDEBAR
# ==============================================================================
with st.sidebar:
    st.header("🎛 Theme")
    theme = st.selectbox("UI Theme", list(THEMES.keys()))
    apply_theme(THEMES[theme])

    st.divider()
    gender = st.selectbox("Gender", ["male", "female"])

    st.subheader("🎨 Style")
    style_scores = {s: st.slider(s, 0, 10, 5) for s in StyleConfig.GENRES}

    st.subheader("🌈 Color")
    color_scores = {c: st.slider(c, 0, 10, 5) for c in StyleConfig.COLORS}

    generate = st.button("✨ Recommend")

# ==============================================================================
# MAIN
# ==============================================================================
st.title("AI Personal Stylist")
st.caption("Multi-Theme Edition · Switchable UI · Weight ≥ 12")

if generate:
    st.session_state["images"] = ImageRecommender.recommend(
        gender, style_scores, color_scores
    )

if "images" in st.session_state and st.session_state["images"]:
    cols = st.columns(3)
    for col, img in zip(cols, st.session_state["images"]):
        with col:
            st.image(img["path"], use_container_width=True)
            st.markdown(f"### {img['style']}")
            st.caption(f"{img['color']} · weight {img['weight']}")
else:
    st.info("👈 Select theme & preferences, then recommend")
