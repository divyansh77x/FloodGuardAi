import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="FloodGuard AI",
    page_icon="🌊",
    layout="wide"
)

# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown("""
<style>
.main {
    background-color: #f8fafc;
}
.metric-card {
    background: white;
    padding: 10px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# TRAINING DATA
# -----------------------------
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

# -----------------------------
# HEADER
# -----------------------------
st.title("🌊 FloodGuard AI")
st.subheader("Hyper-Local Flash Flood Prediction System")

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.header("Live Sensor Inputs")

rainfall = st.sidebar.slider(
    "Rainfall (mm)", 0, 500, 180
)

soil = st.sidebar.slider(
    "Soil Moisture (%)", 0, 100, 60
)

slope = st.sidebar.slider(
    "Slope Angle (°)", 0, 60, 25
)

river = st.sidebar.slider(
    "River Level (m)", 0, 10, 5
)

# -----------------------------
# PREDICTION
# -----------------------------
risk_score = (
    rainfall*0.35 +
    soil*0.25 +
    slope*0.15 +
    river*10*0.25
)/2

prediction = model.predict(
    [[rainfall, soil, slope, river]]
)[0]

# -----------------------------
# KPI CARDS
# -----------------------------
c1,c2,c3,c4 = st.columns(4)

c1.metric("🌧 Rainfall", f"{rainfall} mm")
c2.metric("💧 Soil Moisture", f"{soil}%")
c3.metric("⛰ Slope", f"{slope}°")
c4.metric("🌊 River Level", f"{river} m")

st.markdown("---")

# -----------------------------
# FLOOD STATUS
# -----------------------------
if prediction == 0:
    st.success("🟢 LOW FLOOD RISK")

elif prediction == 1:
    st.warning("🟡 MEDIUM FLOOD RISK")

else:
    st.error("🔴 HIGH FLOOD RISK")

# -----------------------------
# GAUGE
# -----------------------------
st.subheader("Flood Risk Index")

fig = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=min(risk_score,100),
        title={"text":"Risk Score"},
        gauge={
            "axis":{"range":[0,100]},
            "bar":{"color":"darkblue"},
            "steps":[
                {"range":[0,40],"color":"lightgreen"},
                {"range":[40,70],"color":"gold"},
                {"range":[70,100],"color":"red"}
            ]
        }
    )
)

st.subheader("⏳ Predicted Lead Time")  if prediction == 2:     st.error("Flood Probability: 89%")     st.error("Estimated Impact Time: 2 Hours")  elif prediction == 1:     st.warning("Flood Probability: 55%")     st.warning("Estimated Impact Time: 6 Hours")  else:     st.success("Flood Probability: 12%")     st.success("No Immediate Threat")

# -----------------------------
# VILLAGE RISK MAP
# -----------------------------
st.subheader("📍 Village Risk Monitoring")

locations = pd.DataFrame({
    "Village":[
    "Joshimath",
    "Chamoli",
    "Rudraprayag",
    "Karnaprayag"
]
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

risk_colors = {
    "Low":"green",
    "Medium":"orange",
    "High":"red"
}

m = folium.Map(
    location=[30.34,78.05],
    zoom_start=11,
    tiles="CartoDB positron"
)

for _, row in locations.iterrows():

    folium.CircleMarker(
        location=[row["Latitude"], row["Longitude"]],
        radius=12,
        popup=f"{row['Village']} - {row['Risk']}",
        color=risk_colors[row["Risk"]],
        fill=True,
        fill_opacity=0.8
    ).add_to(m)

st_folium(m, height=500, width=1200)

# -----------------------------
# ALERT CENTER
# -----------------------------
st.subheader("🚨 Early Warning Center")

if prediction == 2:

    st.error("""
    HIGH ALERT

    • Notify District Authority
    • Send SMS Alerts
    • Activate Emergency Team
    • Begin Evacuation
    """)

elif prediction == 1:

    st.warning("""
    WATCH MODE

    • Increase Monitoring
    • Alert Local Officials
    • Prepare Rescue Teams
    """)

else:

    st.success("""
    NORMAL CONDITIONS

    • Continue Monitoring
    """)

# -----------------------------
# EVACUATION MAP
# -----------------------------
st.subheader("🗺 Evacuation Route")

village_lat = 30.3165
village_lon = 78.0322

shelter_lat = 30.3265
shelter_lon = 78.0422

route_map = folium.Map(
    location=[village_lat, village_lon],
    zoom_start=13
)

folium.Marker(
    [village_lat, village_lon],
    popup="Flood Risk Zone",
    tooltip="Village"
).add_to(route_map)

folium.Marker(
    [shelter_lat, shelter_lon],
    popup="Government Shelter",
    tooltip="Safe Shelter"
).add_to(route_map)

folium.PolyLine(
    [
        [village_lat, village_lon],
        [shelter_lat, shelter_lon]
    ],
    weight=6
).add_to(route_map)

st_folium(route_map, height=450)

# -----------------------------
# AI RECOMMENDATIONS
# -----------------------------
st.subheader("🤖 AI Recommendations")

if prediction == 2:

    st.error("""
    Immediate evacuation recommended.

    • Open shelters
    • Deploy rescue teams
    • Send emergency alerts
    • Monitor river level every 15 minutes
    """)

elif prediction == 1:

    st.warning("""
    Elevated flood conditions.

    • Prepare evacuation logistics
    • Keep rescue teams on standby
    • Monitor weather updates
    """)

else:

    st.success("""
    Conditions stable.

    • Continue monitoring
    • No evacuation required
    """)

st.markdown("---")

st.subheader("📡 Multi-Source Data Integration")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("""
    🌧 Rainfall Data

    Source:
    IMD Automatic Weather Station

    Location:
    Village Rain Gauge Station
    """)

with col2:
    st.info("""
    🌱 Soil Moisture

    Sensor:
    Capacitive Soil Moisture Sensor

    Location:
    Agricultural Fields
    """)

with col3:
    st.info("""
    🌊 River Water Level

    Sensor:
    Ultrasonic Water Level Sensor

    Location:
    River / Stream Bank
    """)

col4, col5, col6 = st.columns(3)

with col4:
    st.info("""
    ⛰ Terrain & Slope

    Source:
    ISRO Bhuvan DEM

    Technology:
    GIS Analysis
    """)

with col5:
    st.info("""
    📚 Historical Flood Data

    Source:
    NDMA + Central Water Commission

    Coverage:
    Past Flood Events
    """)

with col6:
    st.info("""
    🤖 AI Prediction Engine

    Model:
    Random Forest

    Output:
    Flood Risk Forecast
    """)

st.success("✅ SIH Prototype Ready")
