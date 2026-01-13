import streamlit as st
import random
from PIL import Image, ImageDraw

# ==============================================================================
# CONFIG
# ==============================================================================
st.set_page_config(
    page_title="AI Stylist | Neon Edition",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# NEON UI STYLE (CYAN BOOSTED)
# ==============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
}

/* ===== Background ===== */
.stApp {
    background: radial-gradient(circle at top, #0f2027, #02121a 60%, #00060a 90%);
    color: #EAFBFF;
}

/* ===== Sidebar ===== */
section[data-testid="stSidebar"] {
    background: rgba(5, 15, 25, 0.95);
    border-right: 1px solid rgba(0, 255, 255, 0.35);
    box-shadow: 0 0 25px rgba(0, 255, 255, 0.15);
}

/* ===== Headings ===== */
h1, h2, h3 {
    color: #DFFFFF;
    text-shadow:
        0 0 12px rgba(0, 255, 255, 0.45),
        0 0 22px rgba(0, 180, 255, 0.35);
}

/* ===== Buttons ===== */
div.stButton > button {
    background: linear-gradient(135deg, #00F5FF, #4F9DFF);
    color: #020409;
    border-radius: 10px;
    padding: 0.7rem 1.2rem;
    font-weight: 600;
    border: none;
    width: 100%;
    box-shadow:
        0 0 18px rgba(0, 245, 255, 0.55),
        0 0 28px rgba(0, 180, 255, 0.35);
    transition: all 0.25s ease;
}

div.stButton > button:hover {
    transform: translateY(-2px) scale(1.03);
    box-shadow:
        0 0 25px rgba(0, 255, 255, 0.8),
        0 0 45px rgba(0, 180, 255, 0.7);
}

/* ===== Expanders ===== */
div[data-testid="stExpander"] {
    background: rgba(0, 10, 15, 0.45);
    border-radius: 10px;
    border: 1px solid rgba(0, 255, 255, 0.25);
    box-shadow: 0 0 15px rgba(0, 255, 255, 0.15);
}

/* ===== Labels / Text ===== */
label, .stSelectbox label, .stMultiSelect label {
    color: #CFFFFF !important;
    text-shadow: 0 0 6px rgba(0, 255, 255, 0.3);
}

/* ===== Info Box ===== */
.stAlert {
    background: rgba(0, 40, 50, 0.35) !important;
    border-left: 4px solid #00F5FF !important;
    color: #DFFFFF !important;
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# DATA
# ==============================================================================
class StyleConfig:
    GENRES = ["Streetwear", "Casual", "Minimal", "Techwear", "Vintage", "Formal"]
    COLORS = ["Black", "White", "Gray", "Navy", "Brown", "Beige", "Green", "Red"]

    COLOR_MAP = {
        "Black": (20, 20, 20),
        "White": (245, 245, 245),
        "Gray": (120, 120, 125),
        "Navy": (30, 45, 80),
        "Brown": (100, 70, 50),
        "Beige": (220, 210, 190),
        "Green": (55, 90, 60),
        "Red": (160, 40, 40)
    }

    OUTFIT_LIBRARY = {
        "Streetwear": {
            "inner": ["Oversized Tee", "Graphic Hoodie"],
            "outer": ["Bomber Jacket", "Puffer Vest"],
            "bottom": ["Cargo Pants", "Joggers"],
            "skirt": ["Pleated Mini", "Sport Skirt"],
            "shoe": ["Chunky Sneakers", "High Tops"]
        },
        "Casual": {
            "inner": ["Cotton Tee", "Soft Knit"],
            "outer": ["Denim Jacket", "Cardigan"],
            "bottom": ["Straight Jeans", "Chinos"],
            "skirt": ["A-Line Skirt", "Long Denim Skirt"],
            "shoe": ["Low Sneakers", "Loafers"]
        },
        "Minimal": {
            "inner": ["Mock Neck", "Crisp Shirt"],
            "outer": ["Trench Coat", "Wool Coat"],
            "bottom": ["Tapered Slacks", "Wide Trousers"],
            "skirt": ["Silk Skirt", "Pencil Skirt"],
            "shoe": ["Leather Boots", "Minimal Sneakers"]
        },
        "Techwear": {
            "inner": ["Compression Top", "Tech Tee"],
            "outer": ["Hardshell Parka", "Utility Vest"],
            "bottom": ["Tech Cargo", "Nylon Pants"],
            "skirt": ["Utility Skirt"],
            "shoe": ["Tactical Boots", "Running Shoes"]
        },
        "Vintage": {
            "inner": ["Ringer Tee", "Flannel Shirt"],
            "outer": ["Corduroy Jacket", "Varsity Jacket"],
            "bottom": ["Washed Jeans", "Corduroy Pants"],
            "skirt": ["Checkered Skirt", "Midi Skirt"],
            "shoe": ["Retro Trainers", "Leather Shoes"]
        },
        "Formal": {
            "inner": ["Dress Shirt", "Silk Blouse"],
            "outer": ["Tailored Blazer", "Long Coat"],
            "bottom": ["Dress Trousers", "Pressed Slacks"],
            "skirt": ["Formal Midi"],
            "shoe": ["Derby Shoes", "Heels"]
        }
    }

# ==============================================================================
# LOGIC
# ==============================================================================
class OutfitGenerator:
    @staticmethod
    def get_complementary_color(base_color, colors):
        pairs = {
            "Black": ["White", "Gray", "Beige", "Red"],
            "White": ["Black", "Navy", "Gray"],
            "Navy": ["White", "Beige"],
            "Brown": ["Beige", "White"],
            "Beige": ["Black", "Navy"],
            "Gray": ["Black", "White"],
            "Green": ["Beige", "Black"],
            "Red": ["Black", "White"]
        }
        return random.choice(pairs.get(base_color, colors))

    @staticmethod
    def create(genre, color, gender, use_outer, colors):
        lib = StyleConfig.OUTFIT_LIBRARY[genre]
        accent = OutfitGenerator.get_complementary_color(color, colors)
        is_skirt = gender == "Female" and random.random() < 0.6

        return {
            "genre": genre,
            "main_color": color,
            "accent_color": accent,
            "items": {
                "inner": random.choice(lib["inner"]),
                "outer": random.choice(lib["outer"]) if use_outer else None,
                "bottom": random.choice(lib["skirt"] if is_skirt else lib["bottom"]),
                "shoe": random.choice(lib["shoe"])
            },
            "meta": {
                "is_skirt": is_skirt,
                "has_outer": use_outer
            }
        }

# ==============================================================================
# AVATAR
# ==============================================================================
class AvatarRenderer:
    @staticmethod
    def render(outfit):
        W, H = 500, 900
        img = Image.new("RGB", (W, H), (2, 4, 9))
        d = ImageDraw.Draw(img)

        skin = (235, 215, 200)
        main = StyleConfig.COLOR_MAP[outfit["main_color"]]
        accent = StyleConfig.COLOR_MAP[outfit["accent_color"]]

        d.ellipse([200, 50, 300, 160], fill=skin)
        d.rectangle([235, 150, 265, 190], fill=skin)

        d.rectangle([180, 180, 320, 460], fill=accent)

        if outfit["meta"]["is_skirt"]:
            d.polygon([(180, 460), (320, 460), (360, 650), (140, 650)], fill=main)
            d.rectangle([210, 650, 240, 820], fill=skin)
            d.rectangle([260, 650, 290, 820], fill=skin)
        else:
            d.rectangle([180, 460, 320, 820], fill=main)

        if outfit["meta"]["has_outer"]:
            d.rectangle([140, 170, 210, 480], fill=main)
            d.rectangle([290, 170, 360, 480], fill=main)

        d.rectangle([190, 820, 240, 870], fill=(20, 20, 20))
        d.rectangle([260, 820, 310, 870], fill=(20, 20, 20))

        return img.resize((250, 450), Image.LANCZOS)

# ==============================================================================
# UI
# ==============================================================================
def sidebar():
    with st.sidebar:
        st.header("⚙️ Persona")

        gender = st.selectbox("Gender", ["Male", "Female"], index=1)
        use_outer = st.toggle("Include Outerwear", True)

        genres = st.multiselect(
            "Styles",
            StyleConfig.GENRES,
            default=["Casual", "Minimal"]
        )

        colors = st.multiselect(
            "Colors",
            StyleConfig.COLORS,
            default=["Black", "Beige", "Navy"]
        )

        if st.button("✨ Generate"):
            return gender, use_outer, genres, colors, True

    return None, None, None, None, False

# ==============================================================================
# MAIN
# ==============================================================================
def main():
    if "outfits" not in st.session_state:
        st.session_state.outfits = []

    st.title("AI Personal Stylist")
    st.caption("Neon-powered outfit generation")

    gender, use_outer, genres, colors, go = sidebar()

    if go:
        st.session_state.outfits = [
            OutfitGenerator.create(
                random.choice(genres),
                random.choice(colors),
                gender,
                use_outer,
                colors
            ) for _ in range(3)
        ]

    if st.session_state.outfits:
        cols = st.columns(3)
        for col, outfit in zip(cols, st.session_state.outfits):
            with col:
                st.image(AvatarRenderer.render(outfit), use_container_width=True)
                st.subheader(outfit["genre"])
                st.caption(f'{outfit["main_color"]} × {outfit["accent_color"]}')
                with st.expander("Details", expanded=True):
                    for k, v in outfit["items"].items():
                        st.write(f"**{k.capitalize()}**: {v}")

    else:
        st.info("👈 左の設定から Generate を押してください")

if __name__ == "__main__":
    main()
