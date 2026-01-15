import streamlit as st
import random
import os

# ==============================================================================
# PAGE CONFIG
# ==============================================================================
st.set_page_config(
    page_title="AI Stylist | Eco Hi-Tech Edition",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# ECO HI-TECH STYLE (EMERALD / GOLD / SUNSET PINK / DEEP BLUE)
# ==============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ==============================
   BASE
============================== */
.stApp {
    background:
        radial-gradient(circle at top right, rgba(26,255,163,0.12), transparent 40%),
        radial-gradient(circle at bottom left, rgba(255,209,102,0.08), transparent 45%),
        #050B1A;
    color: #E6F1FF;
}

/* ==============================
   SIDEBAR
============================== */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #050B1A 0%, #08132E 100%);
    border-right: 1px solid rgba(26,255,163,0.35);
    box-shadow: 4px 0 22px rgba(26,255,163,0.18);
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] label {
    color: #1AFFA3;
    text-shadow: 0 0 6px rgba(26,255,163,0.6);
}

/* ==============================
   HEADERS
============================== */
h1, h2 {
    color: #1AFFA3;
    text-shadow:
        0 0 6px rgba(26,255,163,0.7),
        0 0 14px rgba(183,255,42,0.35);
}

/* ==============================
   BUTTON
============================== */
div.stButton > button {
    background: linear-gradient(
        135deg,
        #1AFFA3,
        #FFD166
    );
    color: #050B1A;
    border: none;
    border-radius: 14px;
    padding: 0.7rem 1.4rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    box-shadow:
        0 0 14px rgba(26,255,163,0.6),
        0 0 28px rgba(255,209,102,0.45);
    transition: all 0.25s ease;
    width: 100%;
}

div.stButton > button:hover {
    background: linear-gradient(
        135deg,
        #B7FF2A,
        #FF6F91
    );
    color: #08132E;
    transform: translateY(-2px) scale(1.02);
    box-shadow:
        0 0 18px rgba(183,255,42,0.8),
        0 0 36px rgba(255,111,145,0.6);
}

/* ==============================
   SLIDER
============================== */
div[data-baseweb="slider"] > div {
    background-color: #08132E;
}

div[data-baseweb="slider"] span {
    color: #FFD166;
}

/* ==============================
   IMAGE CARD
============================== */
img {
    border-radius: 18px;
    border: 1px solid rgba(26,255,163,0.4);
    box-shadow:
        0 0 16px rgba(26,255,163,0.35),
        0 0 32px rgba(255,209,102,0.2);
}

/* ==============================
   EXPANDER
============================== */
details {
    background: linear-gradient(
        180deg,
        rgba(8,19,46,0.95),
        rgba(5,11,26,0.98)
    );
    border: 1px solid rgba(255,111,145,0.35);
    border-radius: 14px;
    padding: 0.6rem;
    box-shadow: 0 0 14px rgba(255,111,145,0.3);
}

summary {
    color: #FF6F91;
    font-weight: 600;
}

/* ==============================
   INFO BOX
============================== */
div[data-testid="stInfo"] {
    background: rgba(26,255,163,0.1);
    border: 1px solid #1AFFA3;
    color: #1AFFA3;
    box-shadow: 0 0 14px rgba(26,255,163,0.45);
}
</style>
""", unsafe_allow_html=True)

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

        for style, s_score in style_scores.items():
            for color, c_score in color_scores.items():
                total_weight = s_score + c_score
                if total_weight < min_weight:
                    continue

                path = os.path.join(base_dir, gender_dir, style, color)
                if os.path.exists(path):
                    for file in os.listdir(path):
                        if file.lower().endswith((".png", ".jpg", ".jpeg")):
                            candidates.append({
                                "path": os.path.join(path, file),
                                "style": style,
                                "color": color,
                                "weight": total_weight
                            })

        if not candidates:
            return []

        selected = []
        pool = candidates.copy()

        while pool and len(selected) < max_images:
            weights = [c["weight"] for c in pool]
            choice = random.choices(pool, weights=weights, k=1)[0]
            selected.append(choice)
            pool.remove(choice)

        return selected

# ==============================================================================
# SIDEBAR
# ==============================================================================
def sidebar_controls():
    with st.sidebar:
        st.header("⚙️ Preferences")

        gender = st.selectbox("Gender", ["male", "female"])

        st.divider()
        st.subheader("🌿 Style Ratings (0–10)")
        style_scores = {
            style: st.slider(style, 0, 10, 5)
            for style in StyleConfig.GENRES
        }

        st.divider()
        st.subheader("🎨 Color Ratings (0–10)")
        color_scores = {
            color: st.slider(color, 0, 10, 5)
            for color in StyleConfig.COLORS
        }

        st.divider()
        generate = st.button("✨ Generate Eco-Tech Outfit")

    return gender, style_scores, color_scores, generate

# ==============================================================================
# MAIN
# ==============================================================================
def main():
    st.title("AI Personal Stylist")
    st.caption("Eco Hi-Tech Edition · Clean Future Aesthetics · Weight ≥ 12")

    gender, style_scores, color_scores, generate = sidebar_controls()

    if "images" not in st.session_state:
        st.session_state["images"] = []

    if generate:
        st.session_state["images"] = ImageRecommender.recommend(
            gender=gender,
            style_scores=style_scores,
            color_scores=color_scores,
            max_images=3,
            min_weight=12
        )

    if st.session_state["images"]:
        cols = st.columns(3)

        for col, img in zip(cols, st.session_state["images"]):
            with col:
                st.image(img["path"], use_container_width=True)
                st.markdown(f"### {img['style']}")
                st.caption(f"Color: {img['color']} | Total Weight: {img['weight']}")

                with st.expander("Why this eco-tech outfit was selected", expanded=True):
                    st.markdown(f"""
- 🌍 Sustainable & future-oriented aesthetic
- Total eco-weight: **{img['weight']}**
- Threshold passed (**≥12**)
- Higher weight → stronger recommendation
- Clean & non-duplicated selection
""")
    else:
        st.info("👈 Adjust preferences and generate eco-tech fits")

# ==============================================================================
# RUN
# ==============================================================================
if __name__ == "__main__":
    main()
