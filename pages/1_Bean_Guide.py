import streamlit as st
import pandas as pd
import base64

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Bean Guide",
    page_icon="📚",
    layout="wide"
)

# ==========================================
# BACKGROUND IMAGE
# ==========================================

def get_base64(file):
    with open(file, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

img = get_base64("bean_background.png")

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
    url("data:image/png;base64,{img}");

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

/* Main Card */

.guide-card {{

    background:rgba(255,255,255,0.92);

    padding:30px;

    border-radius:20px;

    box-shadow:0px 4px 15px rgba(0,0,0,0.15);

    margin-bottom:20px;
}}

.title {{

    text-align:center;

    font-size:55px;

    font-weight:bold;

    color:#1B4332;
}}

.subtitle {{

    text-align:center;

    font-size:20px;

    color:#2D6A4F;
}}

.bean-card {{

    background:rgba(255,255,255,0.92);

    padding:15px;

    border-radius:12px;

    margin-bottom:10px;

    border-left:5px solid #2D6A4F;
}}

</style>
""",
unsafe_allow_html=True
)

# ==========================================
# HEADER
# ==========================================

st.markdown(
"""
<div class="guide-card">

<h1 class="title">
📚 Dry Bean Measurement Guide
</h1>

<p class="subtitle">

Use this guide to understand typical measurements
for each bean variety.

</p>

<p class="subtitle">

Copy values from the table and test them in the
Prediction page.

</p>

</div>
""",
unsafe_allow_html=True
)

# ==========================================
# REFERENCE TABLE
# ==========================================

bean_reference = pd.read_csv("bean_reference.csv")

st.markdown(
"""
<div class="guide-card">
<h2 style='color:#1B4332;'>
📊 Average Measurements by Bean Class
</h2>
</div>
""",
unsafe_allow_html=True
)

st.dataframe(
    bean_reference,
    use_container_width=True
)

st.success(
"""
Tip:

Copy a complete row from this table and enter the values
in the Prediction page to test how the model classifies
that bean variety.
"""
)

st.divider()

# ==========================================
# BEAN INFORMATION
# ==========================================

st.markdown(
"""
<div class="guide-card">
<h2 style='color:#1B4332;'>
🫘 Bean Class Overview
</h2>
</div>
""",
unsafe_allow_html=True
)

bean_info = {

    "BARBUNYA":
    "Large kidney-shaped bean variety.",

    "BOMBAY":
    "Very large bean variety.",

    "CALI":
    "Medium to large bean variety.",

    "DERMASON":
    "Small compact bean variety.",

    "HOROZ":
    "Long elongated bean variety.",

    "SEKER":
    "Small rounded bean variety.",

    "SIRA":
    "Long narrow bean variety."
}

for bean, desc in bean_info.items():

    st.markdown(
        f"""
        <div class="bean-card">

        <h3>🫘 {bean}</h3>

        <p>{desc}</p>

        </div>
        """,
        unsafe_allow_html=True
    )