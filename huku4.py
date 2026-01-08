import streamlit as st
import random
from PIL import Image, ImageDraw

st.set_page_config(page_title="Outfit Recommendation", layout="wide")

# -----------------------------
# 未来チック + 白文字 カスタムCSS
# -----------------------------
st.markdown("""
<style>

body {
    background-color: #0a0f1f;
    color: #e0eaff;
    font-family: 'Segoe UI', sans-serif;
}

/* タイトル */
h1, h2, h3 {
    color: #7ab8ff !important;
    text-shadow: 0 0 12px #3a7bd5;
}

/* カードデザイン */
.card {
    background: rgba(20, 30, 60, 0.6);
    border: 1px solid rgba(80, 150, 255, 0.4);
    border-radius: 14px;
    padding: 20px;
    box-shadow: 0 0 20px rgba(80, 150, 255, 0.2);
    backdrop-filter: blur(8px);
    margin-bottom: 25px;
}

/* スライダーのバー */
.stSlider > div > div > div {
    background: linear-gradient(90deg, #3a7bd5, #00d4ff) !important;
    height: 6px;
    border-radius: 4px;
}

/* サイドバー背景 */
[data-testid="stSidebar"] {
    background: rgba(10, 20, 40, 0.8);
    backdrop-filter: blur(6px);
    border-right: 1px solid rgba(80, 150, 255, 0.3);
}

/* ▼▼ 文字色を白にする設定 ▼▼ */

/* サイドバー内の文字 */
[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

/* スライダーのラベル */
.stSlider label {
    color: #ffffff !important;
}

/* 入力系コンポーネントのラベル */
.stSelectbox label, .stMultiSelect label, .stTextInput label {
    color: #ffffff !important;
}

/* セレクトボックス内部の文字 */
div[data-baseweb="select"] * {
    color: #ffffff !important;
}

/* ▲▲ ここまで追加 ▲▲ */

</style>
""", unsafe_allow_html=True)

st.title("👗 Futuristic Outfit Recommendation System")

# -----------------------------
# Sidebar Input
# -----------------------------
st.sidebar.header("🎛 Style Preferences")

GENRES = ["Streetwear", "Casual", "Minimal", "Techwear", "Vintage", "Formal"]
COLORS = ["Black", "White", "Gray", "Navy", "Brown", "Beige", "Green", "Red"]

COLOR_RGB = {
    "Black": (30, 30, 30),
    "White": (240, 240, 240),
    "Gray": (160, 160, 160),
    "Navy": (40, 60, 100),
    "Brown": (120, 80, 50),
    "Beige": (210, 200, 170),
    "Green": (60, 120, 80),
    "Red": (160, 50, 50)
}

st.sidebar.subheader("1️⃣ Style Preference (0–5)")
genre_scores = {g: st.sidebar.slider(g, 0, 5, 0) for g in GENRES}

st.sidebar.subheader("2️⃣ Color Preference (0–5)")
color_scores = {c: st.sidebar.slider(c, 0, 5, 0) for c in COLORS}

# -----------------------------
# Score Completion
# -----------------------------
def complete_scores(scores: dict):
    avg = sum(scores.values()) / len(scores)
    return {k: (v if v > 0 else round(avg, 2)) for k, v in scores.items()}

genre_scores = complete_scores(genre_scores)
color_scores = complete_scores(color_scores)

top_genres = sorted(genre_scores, key=genre_scores.get, reverse=True)[:3]
top_colors = sorted(color_scores, key=color_scores.get, reverse=True)[:3]

# -----------------------------
# Outfit Templates
# -----------------------------
OUTFIT_LIBRARY = {
    "Streetwear": {
        "inner": ["Graphic Tee", "Long Sleeve Tee"],
        "outer": ["Hoodie", "Zip Hoodie"],
        "bottom": ["Wide Pants", "Cargo Pants"]
    },
    "Casual": {
        "inner": ["Plain T-Shirt", "Knit"],
        "outer": ["Cardigan", "Light Jacket"],
        "bottom": ["Denim", "Chinos"]
    },
    "Minimal": {
        "inner": ["Plain Tee"],
        "outer": ["Tailored Jacket"],
        "bottom": ["Slim Slacks"]
    },
    "Techwear": {
        "inner": ["Functional Tee"],
        "outer": ["Shell Jacket"],
        "bottom": ["Tech Pants"]
    },
    "Vintage": {
        "inner": ["Retro Tee"],
        "outer": ["Denim Jacket"],
        "bottom": ["Straight Jeans"]
    },
    "Formal": {
        "inner": ["Dress Shirt"],
        "outer": ["Blazer"],
        "bottom": ["Slacks"]
    }
}

def generate_outfit(genre, color):
    parts = OUTFIT_LIBRARY[genre]
    return {
        "Genre": genre,
        "Color Theme": color,
        "Inner": f"{color} {random.choice(parts['inner'])}",
        "Outer": f"{color} {random.choice(parts['outer'])}",
        "Bottom": f"{color} {random.choice(parts['bottom'])}"
    }

# -----------------------------
# Image Generator
# -----------------------------
def generate_image(outfit):
    base_color = COLOR_RGB[outfit["Color Theme"]]
    img = Image.new("RGB", (260, 440), (245, 245, 245))
    d = ImageDraw.Draw(img)

    skin = (220, 200, 180)
    shadow = tuple(max(0, c - 30) for c in base_color)
    inner_color = tuple(min(255, c + 35) for c in base_color)
    bottom_color = tuple(max(0, c - 50) for c in base_color)

    d.ellipse([105, 20, 155, 70], fill=skin, outline="black")
    d.rectangle([120, 70, 140, 95], fill=skin)
    d.rectangle([50, 120, 80, 260], fill=shadow)
    d.rectangle([180, 120, 210, 260], fill=shadow)

    d.polygon([(70, 100), (190, 100), (210, 270), (50, 270)], fill=base_color, outline="black")
    d.rectangle([95, 120, 165, 250], fill=inner_color, outline="black")

    d.polygon([(115, 120), (145, 120), (130, 150)], fill=(240, 240, 240))

    if "Hoodie" in outfit["Outer"]:
        d.arc([85, 75, 175, 145], start=0, end=180, fill="black", width=4)

    if "Graphic Tee" in outfit["Inner"]:
        d.rectangle([115, 170, 145, 200], fill=(255, 255, 255))

    d.rectangle([95, 270, 125, 400], fill=bottom_color, outline="black")
    d.rectangle([135, 270, 165, 400], fill=bottom_color, outline="black")

    d.rectangle([90, 400, 130, 420], fill=(40, 40, 40))
    d.rectangle([130, 400, 170, 420], fill=(40, 40, 40))

    return img

# -----------------------------
# Output Section
# -----------------------------
st.markdown('<h2>👕 Recommended Outfits</h2>', unsafe_allow_html=True)

used_colors = []

for i, genre in enumerate(top_genres):
    color = random.choice(top_colors)
    if color in used_colors and len(top_colors) > 1:
        color = random.choice([c for c in top_colors if c not in used_colors])
    used_colors.append(color)

    outfit = generate_outfit(genre, color)
    img = generate_image(outfit)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.image(img, caption=f"Outfit {i+1}")

    with col2:
        st.subheader(f"Outfit {i+1} Details")
        st.write(f"**Genre:** {outfit['Genre']}")
        st.write(f"**Color Theme:** {outfit['Color Theme']}")
        st.write(f"👕 Inner: {outfit['Inner']}")
        st.write(f"🧥 Outer: {outfit['Outer']}")
        st.write(f"👖 Bottom: {outfit['Bottom']}")

    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Final Scores
# -----------------------------
st.markdown('<h2>📊 Final Recommendation Scores</h2>', unsafe_allow_html=True)

st.subheader("Genre Scores")
st.json(genre_scores)

st.subheader("Color Scores")
st.json(color_scores)
