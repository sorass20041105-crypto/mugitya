import streamlit as st
import random
import os

# ==============================================================================
# PAGE CONFIG
# ==============================================================================
st.set_page_config(
    page_title="AI Stylist | Bio-Neon Edition",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# BIO-NEON STYLE (NEON GREEN / BIO PINK / TURQUOISE / DEEP GREEN BLACK)
# ==============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Rajdhani', sans-serif;
}

/* ==============================
   BASE
============================== */
.stApp {
    background:
        radial-gradient(circle at top left, rgba(139,92,246,0.08), transparent 40%),
        radial-gradient(circle at bottom right, rgba(46,242,194,0.12), transparent 45%),
        #020806;
    color: #D1FAE5;
}

/* ==============================
   SIDEBAR
============================== */
section[data-testid="stSidebar"] {
    background:
        linear-gradient(180deg, #020806 0%, #04110D 100%);
    border-right: 1px solid rgba(60,255,91,0.35);
    box-shadow: 4px 0 26px rgba(60,255,91,0.25);
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] label {
    color: #3CFF5B;
    text-shadow:
        0 0 6px rgba(60,255,91,0.7),
        0 0 14px rgba(60,255,91,0.4);
}

/* ==============================
   HEADERS
============================== */
h1, h2 {
    color: #3CFF5B;
    text-shadow:
        0 0 8px rgba(60,255,91,0.8),
        0 0 20px rgba(46,242,194,0.5);
}

/* ==============================
   BUTTON
============================== */
div.stButton > button {
    background: linear-gradient(
        135deg,
        #3CFF5B,
        #2EF2C2
    );
    color: #020806;
    border: none;
    border-radius: 18px;
    padding: 0.75rem 1.5rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    box-shadow:
        0 0 14px rgba(60,255,91,0.7),
        0 0 28px rgba(46,242,194,0.5);
    transition: all 0.3s ease;
    width: 100%;
}

div.stButton > button:hover {
    background: linear-gradient(
        135deg,
        #FF4FD8,
        #8B5CF6
    );
    color: #F0FDF4;
    transform: translateY(-2px) scale(1.03);
    box-shadow:
        0 0 18px rgba(255,79,216,0.8),
        0 0 36px rgba(139,92,246,0.6);
}

/* ==============================
   SLIDER
============================== */
div[data-baseweb="slider"] > div {
    background-color: #04110D;
}

div[data-baseweb="slider"] span {
    color: #2EF2C2;
}

/* ==============================
   IMAGE CARD
============================== */
img {
    border-radius: 22px;
    border: 1px solid rgba(46,242,194,0.45);
    box-shadow:
        0 0 20px rgba(60,255,91,0.35),
        0 0 40px rgba(255,79,216,0.25);
}

/* ==============================
   EXPANDER
============================== */
details {
    background:
        linear-gradient(
            180deg,
            rgba(4,17,13,0.9),
            rgba(2,8,6,0.95)
        );
    border: 1px solid rgba(255,79,216,0.4);
    border-radius: 16px;
    padding: 0.6rem;
    box-shadow: 0 0 16px rgba(255,79,216,0.35);
}

summary {
    color: #FF4FD8;
    font-weight: 600;
}

/* ==============================
   INFO BOX
============================== */
div[data-testid="stInfo"] {
    background: rgba(60,255,91,0.1);
    border: 1px solid #3CFF5B;
    color: #3CFF5B;
    box-shadow: 0 0 16px rgba(60,255,91,0.5);
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
        st.subheader("🧬 Style Ratings (0–10)")
        style_scores = {
            style: st.slider(style, 0, 10, 5)
            for style in StyleConfig.GENRES
        }

        st.divider()
        st.subheader("🌱 Color Ratings (0–10)")
        color_scores = {
            color: st.slider(color, 0, 10, 5)
            for color in StyleConfig.COLORS
        }

        st.divider()
        generate = st.button("✨ Generate Bio-Neon Fit")

    return gender, style_scores, color_scores, generate

# ==============================================================================
# MAIN
# ==============================================================================
def main():
    st.title("AI Personal Stylist")
    st.caption("Bio-Neon Edition · Organic Glow · Weight ≥ 12")

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

                with st.expander("Why this bio-neon outfit was selected", expanded=True):
                    st.markdown(f"""
- 🧬 Organic style + color synergy
- Total bio-weight: **{img['weight']}**
- Threshold passed (**≥12**)
- Higher weight → stronger recommendation
- No duplicate organisms detected
""")
    else:
        st.info("👈 Adjust bio-preferences and generate")

# ==============================================================================
# RUN
# ==============================================================================
if __name__ == "__main__":
    main()
