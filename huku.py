import streamlit as st
import random
from PIL import Image, ImageDraw

st.set_page_config(layout="wide")
st.title("Outfit Visual Prototype (No AI Image)")
st.title("Content-Based Outfit Recommendation (Visual Prototype)")

# --------------------
# User Inputs
# --------------------
# ======================
# 1. Definitions
# ======================

gender = st.selectbox("Gender", ["Male", "Female"])
body_type = st.selectbox("Body Type", ["Slim", "Average", "Athletic", "Curvy", "Plus-size"])
pattern = st.selectbox("Pattern", ["Solid", "Striped", "Checked", "Graphic Print", "Minimal Logo"])
color = st.selectbox("Color", ["Black", "Navy", "Beige", "Green", "Red"])
GENRES = ["Streetwear", "Casual", "Minimal", "Techwear", "Vintage", "Formal"]
COLORS = ["Black", "White", "Gray", "Navy", "Beige", "Green", "Red"]
PATTERNS = ["Solid", "Striped", "Checked", "Graphic Print", "Minimal Logo"]

COLOR_MAP = {
COLOR_RGB = {
    "Black": (40, 40, 40),
    "White": (240, 240, 240),
    "Gray": (160, 160, 160),
    "Navy": (50, 70, 110),
    "Beige": (210, 200, 170),
    "Green": (70, 120, 90),
    "Red": (150, 60, 60)
}

# --------------------
# Silhouette Parameters
# --------------------
# ======================
# 2. User Input
# ======================

st.header("1️⃣ Basic Attributes")

gender = st.selectbox("Gender", ["Male", "Female"])
body_type = st.selectbox(
    "Body Type", ["Slim", "Average", "Athletic", "Curvy", "Plus-size"]
)

st.header("2️⃣ Rate Style Preference (0–5)")

genre_scores = {g: st.slider(g, 0, 5, 0) for g in GENRES}
color_scores = {c: st.slider(c, 0, 5, 0) for c in COLORS}
pattern_scores = {p: st.slider(p, 0, 5, 0) for p in PATTERNS}

# ======================
# 3. Score Completion
# ======================

def complete_scores(scores: dict):
    avg = sum(scores.values()) / len(scores)
    return {k: (v if v > 0 else round(avg, 2)) for k, v in scores.items()}

genre_scores = complete_scores(genre_scores)
color_scores = complete_scores(color_scores)
pattern_scores = complete_scores(pattern_scores)

# ======================
# 4. Top Selections
# ======================

top_genres = sorted(genre_scores, key=genre_scores.get, reverse=True)[:3]
top_colors = sorted(color_scores, key=color_scores.get, reverse=True)[:3]
top_patterns = sorted(pattern_scores, key=pattern_scores.get, reverse=True)[:2]

# ======================
# 5. Silhouette Parameters
# ======================

GENDER_PARAMS = {
    "Male": {"shoulder": 1.2, "hip": 0.9},
@@ -38,9 +77,9 @@
    "Plus-size": 1.3
}

# --------------------
# Pattern Drawing
# --------------------
# ======================
# 6. Pattern Drawing
# ======================

def draw_pattern(draw, box, pattern, color):
    x1, y1, x2, y2 = box
@@ -60,67 +99,82 @@ def draw_pattern(draw, box, pattern, color):

    elif pattern == "Graphic Print":
        draw.rectangle(box, fill=color)
        draw.rectangle((x1+25, y1+30, x2-25, y1+80), fill="white")
        draw.text((x1+40, y1+40), "GRAPHIC", fill="black")
        draw.rectangle((x1+30, y1+40, x2-30, y1+90), fill="white")
        draw.text((x1+45, y1+50), "GRAPHIC", fill="black")

    elif pattern == "Minimal Logo":
        draw.rectangle(box, fill=color)
        draw.ellipse((x1+50, y1+40, x1+65, y1+55), fill="white")

# --------------------
# Image Generator
# --------------------
# ======================
# 7. Image Generator
# ======================

def generate_image():
    img = Image.new("RGB", (300, 500), "white")
def generate_image(color_name, pattern):
    img = Image.new("RGB", (280, 480), "white")
    d = ImageDraw.Draw(img)

    base_width = 80
    base_hip = 70

    shoulder = base_width * GENDER_PARAMS[gender]["shoulder"] * BODY_PARAMS[body_type]
    hip = base_hip * GENDER_PARAMS[gender]["hip"] * BODY_PARAMS[body_type]
    color = COLOR_RGB[color_name]

    center = 150
    shoulder = 70 * GENDER_PARAMS[gender]["shoulder"] * BODY_PARAMS[body_type]
    hip = 60 * GENDER_PARAMS[gender]["hip"] * BODY_PARAMS[body_type]
    center = 140

    # Head
    d.ellipse((125, 20, 175, 70), fill=(220, 200, 180))
    d.ellipse((115, 20, 165, 70), fill=(220, 200, 180))

    # Torso (Top)
    torso_box = (
        center - shoulder,
        80,
        center + shoulder,
        220
    )

    draw_pattern(d, torso_box, pattern, COLOR_MAP[color])
    # Torso
    torso_box = (center - shoulder, 80, center + shoulder, 220)
    draw_pattern(d, torso_box, pattern, color)

    # Bottom
    bottom_box = (
        center - hip,
        220,
        center + hip,
        420
    )

    d.rectangle(bottom_box, fill=COLOR_MAP[color])
    d.rectangle((center - hip, 220, center + hip, 420), fill=color)

    return img

# --------------------
# Output
# --------------------
# ======================
# 8. Output 3 Outfits
# ======================

st.header("👕 Recommended Outfits")

used_colors = []

for i, genre in enumerate(top_genres):

    color = random.choice(top_colors)
    if color in used_colors and len(top_colors) > 1:
        color = random.choice([c for c in top_colors if c not in used_colors])
    used_colors.append(color)

    pattern = random.choice(top_patterns)

    img = generate_image(color, pattern)

    col1, col2 = st.columns([1, 1.4])

    with col1:
        st.image(img, caption=f"Outfit {i+1}")

    with col2:
        st.subheader(f"Outfit {i+1} Details")
        st.write(f"**Genre:** {genre}")
        st.write(f"**Gender:** {gender}")
        st.write(f"**Body Type:** {body_type}")
        st.write(f"**Color:** {color}")
        st.write(f"**Pattern:** {pattern}")

# ======================
# 9. Final Scores
# ======================

st.header("📊 Final Recommendation Scores")

st.header("Generated Outfit Image")
st.subheader("Genre")
st.json(genre_scores)

img = generate_image()
st.image(img)
st.subheader("Color")
st.json(color_scores)

st.subheader("Outfit Attributes")
st.write({
    "Gender": gender,
    "Body Type": body_type,
    "Pattern": pattern,
    "Color": color
})
st.subheader("Pattern")
st.json(pattern_scores)
