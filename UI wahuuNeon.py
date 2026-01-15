import streamlit as st
import random
import os

# ==============================================================================
# PAGE CONFIG
# ==============================================================================
st.set_page_config(
    page_title="AI Stylist | Wafu Neon Sakura",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# WAFU NEON SAKURA STYLE
# ==============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Serif JP', serif;
}

/* ==============================
   BASE
============================== */
.stApp {
    background:
        radial-gradient(circle at top right, rgba(255,105,180,0.12), transparent 45%),
        radial-gradient(circle at bottom left, rgba(0,191,255,0.10), transparent 45%),
        linear-gradient(180deg, #0A0F1F 0%, #001122 100%);
    color: #F9FAFF;
}

/* ==============================
   SIDEBAR
============================== */
section[data-testid="stSidebar"] {
    background:
        linear-gradient(180deg, #001122 0%, #0A0F1F 100%);
    border-right: 1px solid rgba(255,105,180,0.45);
    box-shadow: 4px 0 28px rgba(255,105,180,0.35);
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] label {
    color: #FF69B4;
    text-shadow:
        0 0 6px rgba(255,105,180,0.7),
        0 0 14px rgba(0,191,255,0.4);
}

/* ==============================
   HEADERS
============================== */
h1, h2 {
    color: #FF69B4;
    text-shadow:
        0 0 8px rgba(255,105,180,0.8),
        0 0 18px rgba(255,105,180,0.5),
        0 0 28px rgba(0,191,255,0.3);
}

/* ==============================
   BUTTON
============================== */
div.stButton > button {
    background: linear-gradient(
        135deg,
        #FF69B4,
        #C71585,
        #FFD700
    );
    color: #0A0F1F;
    border: none;
    border-radius: 16px;
    padding: 0.75rem 1.5rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    box-shadow:
        0 0 16px rgba(255,105,180,0.8),
        0 0 32px rgba(255,215,0,0.6);
    transition: all 0.3s ease;
    width: 100%;
}

div.stButton > button:hover {
    transform: translateY(-2px) scale(1.03);
    box-shadow:
        0 0 22px rgba(255,105,180,1),
        0 0 44px rgba(255,215,0,0.8);
}

/* ==============================
   SLIDER
============================== */
div[data-baseweb="slider"] > div {
    background-color: #001122;
}

div[data-baseweb="slider"] span {
    color: #00BFFF;
}

/* ==============================
   IMAGE CARD
============================== */
img {
    border-radius: 18px;
    border: 1px solid rgba(255,105,180,0.45);
    box-shadow:
        0 0 20px rgba(255,105,180,0.4),
        0 0 40px rgba(0,191,255,0.25);
}

/* ==============================
   EXPANDER
============================== */
details {
    background:
        linear-gradient(
            180deg,
            rgba(10,15,31,0.96),
            rgba(0,17,34,0.98)
        );
    border: 1px solid rgba(0,191,255,0.45);
    border-radius: 16px;
    padding: 0.6rem;
    box-shadow: 0 0 16px rgba(0,191,255,0.35);
}

summary {
    color: #FFD700;
    font-weight: 600;
}

/* ==============================
   INFO BOX
============================== */
div[data-testid="stInfo"] {
    background: rgba(255,105,180,0.10);
    border: 1px solid #FF69B4;
    color: #FF69B4;
    box-shadow: 0 0 16px rgba(255,105,180,0.45);
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
        st.header("🌸 Preferences")

        gender = st.selectbox("Gender", ["male", "female"])

        st.divider()
        st.subheader("👘 Style Ratings (0–10)")
        style_scores = {
            style: st.slider(style, 0, 10, 5)
            for style in StyleConfig.GENRES
        }

        st.divider()
        st.subheader("🎐 Color Ratings (0–10)")
        color_scores = {
            color: st.slider(color, 0, 10, 5)
            for color in StyleConfig.COLORS
        }

        st.divider()
        generate = st.button("✨ Summon Sakura Outfit")

    return gender, style_scores, color_scores, generate

# ==============================================================================
# MAIN
# ==============================================================================
def main():
    st.title("AI Personal Stylist")
    st.caption("Wafu Neon Sakura · Tradition × Neon · Weight ≥ 12")

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

                with st.expander("Why this outfit bloomed", expanded=True):
                    st.markdown(f"""
- 🌸 Sakura neon harmony
- Style + Color weight = **{img['weight']}**
- Threshold passed (**≥12**)
- Balanced tradition & future
- No duplicate fate
""")
    else:
        st.info("👈 Adjust preferences and summon style")

# ==============================================================================
# RUN
# ==============================================================================
if __name__ == "__main__":
    main()
