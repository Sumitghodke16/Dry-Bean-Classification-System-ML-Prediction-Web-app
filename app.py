import streamlit as st
import numpy as np
import joblib
import base64


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Dry Bean Classification",
    page_icon="🫘",
    layout="wide"
)


# ==========================================
# BACKGROUND IMAGE FUNCTION
# ==========================================

def get_base64(file):
    with open(file, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


img = get_base64("bean_background.png")   # <-- Change filename if needed


# ==========================================
# LOAD MODEL FILES
# ==========================================

model = joblib.load("svm_model.pkl")
scaler = joblib.load("scaler.pkl")
power_transformer = joblib.load("power_transformer.pkl")
label_encoder = joblib.load("label_encoder.pkl")


# ==========================================
# BEAN INFORMATION
# ==========================================

bean_info = {

    "BARBUNYA":
    "Large kidney-shaped bean variety.",

    "BOMBAY":
    "Very large bean variety with high area and perimeter values.",

    "CALI":
    "Medium to large bean variety.",

    "DERMASON":
    "Small commercial bean variety with compact structure.",

    "HOROZ":
    "Elongated bean variety.",

    "SEKER":
    "Small rounded bean variety.",

    "SIRA":
    "Long and narrow bean variety."
}


# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown(
f"""
<style>

.stApp {{

background-image:
linear-gradient(
rgba(255,255,255,0.85),
rgba(255,255,255,0.85)
),
url("data:image/jpg;base64,{img}");

background-size: cover;
background-position: center;
background-attachment: fixed;

}}

/* Sidebar */

section[data-testid="stSidebar"] {{

background-color:#1B4332;

}}

section[data-testid="stSidebar"] * {{

color:white;

}}

/* Title */

.title {{

text-align:center;
font-size:60px;
font-weight:bold;
color:#1B4332;

}}

.subtitle {{

text-align:center;
font-size:22px;
color:#2D6A4F;

}}

/* Inputs */

[data-testid="stNumberInput"] {{

background-color:rgba(255,255,255,0.92);
padding:10px;
border-radius:12px;
border:1px solid #DAD7CD;

}}

/* Button */

.stButton>button {{

width:100%;
height:60px;

background:#2D6A4F;
color:white;

font-size:20px;
font-weight:bold;

border:none;
border-radius:12px;

}}

.stButton>button:hover {{

background:#1B4332;

}}

/* Result Card */

.result-box {{

background:rgba(216,243,220,0.95);

border:2px solid #2D6A4F;

padding:35px;

border-radius:20px;

text-align:center;

}}

.result-text {{

font-size:42px;
font-weight:bold;
color:#1B4332;

}}

</style>
""",
unsafe_allow_html=True
)


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("📊 Project Information")

st.sidebar.markdown("""

### Model Details

- Algorithm: SVM
- Test Accuracy: 92.36%
- F1 Score: 92.36%
- Classes: 7
- Dataset Size: 13,611

### Bean Classes

- BARBUNYA
- BOMBAY
- CALI
- DERMASON
- HOROZ
- SEKER
- SIRA

### Developer

Sumit Naresh Ghodke

""")


# ==========================================
# HEADER
# ==========================================

st.markdown(
"""
<div style='padding:25px;'>

<h1 class='title'>
🫘 Dry Bean Classification System
</h1>

<p class='subtitle'>
Predict Dry Bean Type Using Machine Learning (SVM)
</p>

</div>
""",
unsafe_allow_html=True
)

st.markdown("---")


# ==========================================
# INPUTS
# ==========================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    area = st.number_input("Area", value=53048.0)

    perimeter = st.number_input("Perimeter", value=855.0)

    major_axis = st.number_input("MajorAxisLength", value=320.0)

    minor_axis = st.number_input("MinorAxisLength", value=202.0)

with col2:

    aspect_ratio = st.number_input("AspectRatio", value=1.58)

    eccentricity = st.number_input("Eccentricity", value=0.75)

    convex_area = st.number_input("ConvexArea", value=53768.0)

    equiv_diameter = st.number_input("EquivDiameter", value=253.0)

with col3:

    extent = st.number_input("Extent", value=0.75)

    solidity = st.number_input("Solidity", value=0.98)

    roundness = st.number_input("Roundness", value=0.87)

    compactness = st.number_input("Compactness", value=0.80)

with col4:

    shape1 = st.number_input("ShapeFactor1", value=0.0065)

    shape2 = st.number_input("ShapeFactor2", value=0.0017)

    shape3 = st.number_input("ShapeFactor3", value=0.64)

    shape4 = st.number_input("ShapeFactor4", value=0.995)


# ==========================================
# PREDICTION
# ==========================================

# ==========================================
# PREDICTION
# ==========================================

if st.button("🔍 Predict Bean Class"):

    features = np.array([[

        area,
        perimeter,
        major_axis,
        minor_axis,

        aspect_ratio,
        eccentricity,
        convex_area,
        equiv_diameter,

        extent,
        solidity,
        roundness,
        compactness,

        shape1,
        shape2,
        shape3,
        shape4

    ]], dtype=float)

    # ==================================
    # SAME PREPROCESSING AS TRAINING
    # ==================================

    # Log Transformation

    features[0,0] = np.log1p(features[0,0])     # Area
    features[0,1] = np.log1p(features[0,1])     # Perimeter
    features[0,2] = np.log1p(features[0,2])     # MajorAxisLength
    features[0,3] = np.log1p(features[0,3])     # MinorAxisLength
    features[0,6] = np.log1p(features[0,6])     # ConvexArea
    features[0,7] = np.log1p(features[0,7])     # EquivDiameter

    # Yeo-Johnson Transformation

    yeo_cols = features[:, [5, 9, 15]]

    yeo_cols = power_transformer.transform(yeo_cols)

    features[:, [5, 9, 15]] = yeo_cols

    # Standard Scaling

    features_scaled = scaler.transform(features)

    # Prediction

    prediction = model.predict(features_scaled)

    bean_name = label_encoder.inverse_transform(prediction)

    # ==================================
    # DEBUG SECTION
    # ==================================

    st.write("Encoded Prediction:", prediction[0])

    st.write("Predicted Class:", bean_name[0])

    # ==================================
    # RESULT CARD
    # ==================================

    st.markdown(
        f"""
        <div class="result-box">

        <div class="result-text">

        🫘 Predicted Bean Type

        <br><br>

        {bean_name[0]}

        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.info(
        bean_info.get(
            bean_name[0],
            "Information not available."
        )
    )