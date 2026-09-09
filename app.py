import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="FloodGuard AI",
    page_icon="🌊",
    layout="wide"
)

# ----------------------------
# CUSTOM CSS
# ----------------------------
st.markdown("""
<style>
.main {
    background-color:#f5f7fa;
}
h1,h2,h3{
    color:#003366;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# SAMPLE TRAINING DATA
# ----------------------------
data = pd.DataFrame({
    "rainfall":[50,100,150,200,250,300,350,400,450],
    "soil":[20,35,50,65,75,85,90,95,98],
    "slope":[10,15,20,25,30,35,40,45,50],
    "river":[1,2,3,4,5,6,7,8,9],
    "risk":[0,0,1,1,1,2,2,2,2]
})

X = data[["rainfall","soil","slope","river"]]
y = data["risk"]

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X,y)

# ----------------------------
# HEADER
# ----------------------------
st.title("🌊 FloodGuard AI")
st.subheader("Hyper-Local Flash Flood Prediction System")

st.markdown("---")

# ----------------------------
# SIDEBAR
# ----------------------------
st.sidebar.header("Input Parameters")

rainfall = st.sidebar.slider(
    "Rainfall (mm)",
    0,500,180
)

soil = st.sidebar.slider(
    "Soil Moisture (%)",
    0,100,60
)

slope = st.sidebar.slider(
    "Slope Angle",
    0,60,25
)

river = st.sidebar.slider(
    "River Level (m)",
    0,10,5
)

# ----------------------------
# RISK SCORE
# ----------------------------
risk_score = (
    rainfall*0.35 +
    soil*0.25 +
    slope*0.15 +
    river*10*0.25
)/2

prediction = model.predict(
    [[rainfall,soil,slope,river]]
)[0]

# ----------------------------
# METRICS
# ----------------------------
c1,c2,c3,c4 = st.columns(4)

c1.metric("Rainfall",f"{rainfall} mm")
c2.metric("Soil Moisture",f"{soil}%")
c3.metric("Slope",f"{slope}°")
c4.metric("River Level",f"{river} m")

st.markdown("---")

# ----------------------------
# RESULT
# ----------------------------
if prediction == 0:
    st.success("🟢 LOW FLOOD RISK")

elif prediction == 1:
    st.warning("🟡 MEDIUM FLOOD RISK")

else:
    st.error("🔴 HIGH FLOOD RISK")

st.subheader("Flood Risk Score")

st.progress(min(int(risk_score),100))
st.write(f"Risk Score: {round(risk_score,1)}/100")

# ----------------------------
# MAP DATA
# ----------------------------
st.subheader("Village Risk Monitoring")

locations = pd.DataFrame({
    "Village":[
        "Village A",
        "Village B",
        "Village C",
        "Village D"
    ],
    "Latitude":[30.31,30.34,30.37,30.39],
    "Longitude":[78.03,78.05,78.08,78.11],
    "Risk":[
        "Low",
        "Medium",
        "High",
        "Medium"
    ]
})

st.dataframe(locations)

st.map(
    pd.DataFrame({
        "lat":locations["Latitude"],
        "lon":locations["Longitude"]
    })
)

# ----------------------------
# ALERT SYSTEM
# ----------------------------
st.subheader("🚨 Early Warning Center")

if prediction == 2:

    st.error("""
    ALERT GENERATED

    • Notify District Authority

    • Send SMS Alerts

    • Activate Emergency Team

    • Start Evacuation Process
    """)

elif prediction == 1:

    st.warning("""
    WATCH MODE

    • Increased Monitoring

    • Alert Local Officials

    • Keep Rescue Teams Ready
    """)

else:

    st.success("""
    NORMAL CONDITIONS

    • Continue Monitoring
    """)

# ----------------------------
# EVACUATION PANEL
# ----------------------------
# ----------------------------
# EVACUATION MAP
# ----------------------------
import folium
from streamlit_folium import st_folium

st.subheader("🗺 Safe Evacuation Route")

village_lat = 30.3165
village_lon = 78.0322

shelter_lat = 30.3265
shelter_lon = 78.0422

m = folium.Map(
    location=[village_lat, village_lon],
    zoom_start=13
)

folium.Marker(
    [village_lat, village_lon],
    popup="Risk Zone",
    tooltip="Village"
).add_to(m)

folium.Marker(
    [shelter_lat, shelter_lon],
    popup="Government School Shelter",
    tooltip="Safe Shelter"
).add_to(m)

folium.PolyLine(
    [
        [village_lat, village_lon],
        [shelter_lat, shelter_lon]
    ],
    weight=5
).add_to(m)

st_folium(m, width=900, height=500)

if prediction == 2:
    st.error("🔴 Immediate evacuation recommended")
    st.write("Nearest Safe Shelter: Government School")
    st.write("Estimated Evacuation Time: 30 mins")

elif prediction == 1:
    st.warning("🟡 Keep evacuation route ready")

else:
    st.success("🟢 No evacuation required")

st.markdown("---")

st.info("""
AI Inputs Used

✓ Rainfall Data

✓ Soil Moisture

✓ River Level

✓ Terrain Slope

✓ Historical Disaster Data
""")

st.success("SIH Prototype Ready")
