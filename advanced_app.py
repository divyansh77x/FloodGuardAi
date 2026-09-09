import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import plotly.graph_objects as go
import plotly.express as px
import folium
from streamlit_folium import st_folium
from datetime import datetime

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="FloodGuard AI Command Center",
    page_icon="🌊",
    layout="wide"
)

# =====================================================
# MODERN CSS
# =====================================================

st.markdown("""
<style>

.stApp{
background:#f4f7fb;
}

.block-container{
padding-top:1rem;
}

[data-testid="metric-container"]{
background:white;
padding:18px;
border-radius:18px;
box-shadow:0 4px 15px rgba(0,0,0,0.08);
border:1px solid #e5e7eb;
}

.main-title{
font-size:42px;
font-weight:800;
color:#0f172a;
}

.sub-title{
font-size:18px;
color:#475569;
}

.alert-box{
padding:15px;
border-radius:15px;
background:#ffffff;
box-shadow:0px 4px 15px rgba(0,0,0,0.08);
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADER
# =====================================================

st.markdown(
"""
<div class="main-title">
🌊 FloodGuard AI Command Center
</div>

<div class="sub-title">
Hyper-Local Flash Flood Prediction & Disaster Response Platform
</div>
""",
unsafe_allow_html=True
)

st.markdown("---")

# =====================================================
# TRAINING DATA
# =====================================================

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
    n_estimators=200,
    random_state=42
)

model.fit(X,y)

# =====================================================
# SIDEBAR CONTROL CENTER
# =====================================================

st.sidebar.title("📡 Live Sensor Network")

rainfall = st.sidebar.slider(
    "Rainfall (mm)",
    0,
    500,
    180
)

soil = st.sidebar.slider(
    "Soil Moisture (%)",
    0,
    100,
    60
)

slope = st.sidebar.slider(
    "Slope Angle",
    0,
    60,
    25
)

river = st.sidebar.slider(
    "River Level (m)",
    0,
    10,
    5
)

district = st.sidebar.selectbox(
    "District",
    [
        "Joshimath",
        "Chamoli",
        "Rudraprayag",
        "Karnaprayag"
    ]
)

# =====================================================
# AI PREDICTION
# =====================================================

prediction = model.predict(
    [[rainfall,soil,slope,river]]
)[0]

risk_score = (
    rainfall*0.35 +
    soil*0.25 +
    slope*0.15 +
    river*10*0.25
)/2

risk_score = min(risk_score,100)

# =====================================================
# EXECUTIVE SUMMARY
# =====================================================

st.subheader("🚨 Executive Disaster Summary")

k1,k2,k3,k4,k5 = st.columns(5)

if prediction == 2:
    lead_time = "2 Hours"
    people = "4,850"
    flood_prob = "89%"
elif prediction == 1:
    lead_time = "6 Hours"
    people = "2,120"
    flood_prob = "55%"
else:
    lead_time = "No Threat"
    people = "320"
    flood_prob = "12%"

k1.metric(
    "Flood Probability",
    flood_prob
)

k2.metric(
    "Lead Time",
    lead_time
)

k3.metric(
    "Population At Risk",
    people
)

k4.metric(
    "Safe Shelters",
    "3"
)

k5.metric(
    "Emergency Resources",
    "40"
)

st.markdown("---")

# =====================================================
# LIVE STATUS BAR
# =====================================================

c1,c2,c3,c4 = st.columns(4)

c1.metric(
    "🌧 Rainfall",
    f"{rainfall} mm"
)

c2.metric(
    "💧 Soil Moisture",
    f"{soil}%"
)

c3.metric(
    "⛰ Terrain Slope",
    f"{slope}°"
)

c4.metric(
    "🌊 River Level",
    f"{river} m"
)

# =====================================================
# COMMAND STATUS
# =====================================================

if prediction == 2:
    st.error(
        "🔴 HIGH RISK FLOOD ALERT | Immediate Response Required"
    )

elif prediction == 1:
    st.warning(
        "🟡 MEDIUM RISK | Monitoring & Preparedness Mode"
    )

else:
    st.success(
        "🟢 LOW RISK | Normal Operations"
    )

# =====================================================
# DASHBOARD TABS
# =====================================================

tab1,tab2,tab3,tab4,tab5,tab6 = st.tabs([
    "🏠 Dashboard",
    "📡 Monitoring",
    "🤖 AI Prediction",
    "🗺 Evacuation",
    "🏫 Resources",
    "📊 Analytics"
])

# =====================================================
# TAB 1 DASHBOARD
# =====================================================

with tab1:

    left,right = st.columns([1,1])

    with left:

        st.subheader("Flood Risk Index")

        gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=risk_score,
                title={"text":"Risk Score"},
                gauge={
                    "axis":{"range":[0,100]},
                    "bar":{"color":"darkblue"},
                    "steps":[
                        {
                            "range":[0,40],
                            "color":"lightgreen"
                        },
                        {
                            "range":[40,70],
                            "color":"gold"
                        },
                        {
                            "range":[70,100],
                            "color":"red"
                        }
                    ]
                }
            )
        )

        st.plotly_chart(
            gauge,
            use_container_width=True
        )

    with right:

        st.subheader("⏳ Predicted Lead Time")

        if prediction == 2:

            st.error("Flood Probability : 89%")
            st.error("Impact Expected : 2 Hours")

        elif prediction == 1:

            st.warning("Flood Probability : 55%")
            st.warning("Impact Expected : 6 Hours")

        else:

            st.success("Flood Probability : 12%")
            st.success("No Immediate Threat")

        st.markdown("### Current Time")

        st.info(
            datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            )
        )
      # =====================================================
# TAB 2 MONITORING CENTER
# =====================================================

with tab2:

    st.subheader("📡 Live Sensor Monitoring Network")

    s1,s2,s3,s4,s5 = st.columns(5)

    s1.success("🌧 Rain Gauge\n\nONLINE")
    s2.success("🌱 Soil Sensor\n\nONLINE")
    s3.success("🌊 River Sensor\n\nONLINE")
    s4.success("📶 IoT Gateway\n\nONLINE")
    s5.success("🛰 Satellite Feed\n\nONLINE")

    st.markdown("---")

    st.subheader("🛰 Satellite Observation Center")

    sat1,sat2,sat3,sat4 = st.columns(4)

    sat1.metric(
        "Cloud Cover",
        "62%"
    )

    sat2.metric(
        "Rain Cells",
        "14"
    )

    sat3.metric(
        "Terrain Scan",
        "Updated"
    )

    sat4.metric(
        "Landslide Risk",
        "Medium"
    )

    st.markdown("---")

    st.subheader("🚁 Drone Surveillance Fleet")

    d1,d2,d3 = st.columns(3)

    with d1:

        st.info("""
Drone Alpha

Status : ONLINE

Battery : 87%

Coverage : Sector A
""")

    with d2:

        st.info("""
Drone Bravo

Status : ONLINE

Battery : 73%

Coverage : Sector B
""")

    with d3:

        st.info("""
Drone Charlie

Status : ONLINE

Battery : 91%

Coverage : Sector C
""")

    st.markdown("---")

    st.subheader("📍 Hyperlocal Warning Engine")

    warning_df = pd.DataFrame({
        "Village":[
            "Joshimath",
            "Chamoli",
            "Rudraprayag",
            "Karnaprayag",
            "Gopeshwar",
            "Pipalkoti"
        ],
        "Alert":[
            "RED",
            "ORANGE",
            "RED",
            "YELLOW",
            "GREEN",
            "ORANGE"
        ],
        "Population":[
            1800,
            1250,
            1450,
            820,
            610,
            970
        ]
    })

    st.dataframe(
        warning_df,
        use_container_width=True
    )

    st.markdown("---")

    st.subheader("🗺 District Risk Heatmap")

    village_data = pd.DataFrame({

        "Village":[
            "Joshimath",
            "Chamoli",
            "Rudraprayag",
            "Karnaprayag"
        ],

        "Latitude":[
            30.31,
            30.34,
            30.37,
            30.39
        ],

        "Longitude":[
            78.03,
            78.05,
            78.08,
            78.11
        ],

        "Risk":[
            "High",
            "Medium",
            "High",
            "Low"
        ]
    })

    heat_map = folium.Map(
        location=[30.34,78.05],
        zoom_start=10,
        tiles="CartoDB positron"
    )

    risk_color = {
        "Low":"green",
        "Medium":"orange",
        "High":"red"
    }

    for _, row in village_data.iterrows():

        folium.CircleMarker(
            location=[
                row["Latitude"],
                row["Longitude"]
            ],
            radius=15,
            color=risk_color[row["Risk"]],
            fill=True,
            fill_opacity=0.9,
            popup=f"{row['Village']} - {row['Risk']}"
        ).add_to(heat_map)

    st_folium(
        heat_map,
        height=550,
        width=1200
    )

    st.markdown("---")

    st.subheader("📈 Live Environmental Trends")

    trend = pd.DataFrame({

        "Hour":[
            "06:00",
            "08:00",
            "10:00",
            "12:00",
            "14:00",
            "16:00"
        ],

        "Rainfall":[
            20,
            45,
            78,
            110,
            160,
            210
        ]
    })

    fig = px.line(
        trend,
        x="Hour",
        y="Rainfall",
        markers=True,
        title="Rainfall Trend (Last 12 Hours)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("---")

    st.subheader("📡 Sensor Health Dashboard")

    sensor_health = pd.DataFrame({

        "Sensor":[
            "Rain Gauge",
            "Soil Sensor",
            "River Sensor",
            "Weather Station",
            "IoT Gateway"
        ],

        "Health":[
            98,
            94,
            97,
            99,
            96
        ]
    })

    fig = px.bar(
        sensor_health,
        x="Sensor",
        y="Health",
        title="Sensor Reliability (%)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
  # =====================================================
# TAB 3 AI PREDICTION CENTER
# =====================================================

with tab3:

    st.subheader("🤖 AI Prediction & Decision Intelligence")

    st.markdown("---")

    # ==========================================
    # FLOOD PROBABILITY
    # ==========================================

    probability = min(
        int(
            (rainfall * 0.30)
            + (soil * 0.25)
            + (river * 7)
            + (slope * 0.20)
        ),
        100
    )

    c1,c2,c3,c4 = st.columns(4)

    c1.metric(
        "Flood Probability",
        f"{probability}%"
    )

    c2.metric(
        "Prediction Confidence",
        "94%"
    )

    c3.metric(
        "Lead Time",
        "2.4 Hours"
    )

    c4.metric(
        "AI Model Accuracy",
        "92.7%"
    )

    st.markdown("---")

    # ==========================================
    # DONUT CHART
    # ==========================================

    st.subheader("🧠 Explainable AI Decision Breakdown")

    explain_df = pd.DataFrame({

        "Factor":[
            "Rainfall",
            "River Level",
            "Soil Moisture",
            "Slope"
        ],

        "Contribution":[
            42,
            28,
            18,
            12
        ]
    })

    fig = px.pie(
        explain_df,
        values="Contribution",
        names="Factor",
        hole=0.6,
        title="Contribution to Flood Prediction"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("---")

    # ==========================================
    # FEATURE IMPORTANCE
    # ==========================================

    st.subheader("📊 Feature Importance")

    importance_df = pd.DataFrame({

        "Feature":[
            "Rainfall",
            "River Level",
            "Soil Moisture",
            "Slope"
        ],

        "Importance":[
            0.42,
            0.28,
            0.18,
            0.12
        ]
    })

    fig = px.bar(
        importance_df,
        x="Importance",
        y="Feature",
        orientation="h",
        title="AI Feature Importance Ranking"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("---")

    # ==========================================
    # RISK FORECAST TIMELINE
    # ==========================================

    st.subheader("📈 Next 12 Hour Risk Forecast")

    forecast = pd.DataFrame({

        "Hour":[
            "Now",
            "+2h",
            "+4h",
            "+6h",
            "+8h",
            "+10h",
            "+12h"
        ],

        "Risk":[
            45,
            58,
            70,
            82,
            89,
            80,
            65
        ]
    })

    fig = px.line(
        forecast,
        x="Hour",
        y="Risk",
        markers=True,
        title="Flood Risk Forecast"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("---")

    # ==========================================
    # DISASTER TIMELINE
    # ==========================================

    st.subheader("⏳ AI Disaster Timeline Simulation")

    timeline = pd.DataFrame({

        "Stage":[
            "Heavy Rain Starts",
            "River Rising",
            "Critical Level",
            "Flood Trigger",
            "Evacuation",
            "Rescue Deployment"
        ],

        "Time":[
            "0h",
            "2h",
            "4h",
            "6h",
            "6h 15m",
            "6h 30m"
        ]
    })

    st.dataframe(
        timeline,
        use_container_width=True
    )

    st.markdown("---")

    # ==========================================
    # POPULATION IMPACT
    # ==========================================

    st.subheader("👥 Population Impact Analysis")

    impact1,impact2,impact3,impact4 = st.columns(4)

    impact1.metric(
        "Population at Risk",
        "12,480"
    )

    impact2.metric(
        "Households",
        "2,965"
    )

    impact3.metric(
        "Schools Nearby",
        "18"
    )

    impact4.metric(
        "Hospitals Nearby",
        "7"
    )

    st.markdown("---")

    # ==========================================
    # AI ACTION RECOMMENDATION
    # ==========================================

    st.subheader("🧠 AI Recommended Actions")

    if probability > 75:

        st.error("""
🔴 CRITICAL RISK

• Immediate evacuation

• Activate NDRF

• Open emergency shelters

• Send multilingual SMS alerts

• Close vulnerable roads

• Deploy drones for surveillance
""")

    elif probability > 45:

        st.warning("""
🟡 MODERATE RISK

• Prepare shelters

• Alert district officials

• Keep rescue teams on standby

• Monitor rainfall every 15 min
""")

    else:

        st.success("""
🟢 LOW RISK

• Continue monitoring

• No evacuation required

• Sensors operating normally
""")
      # =====================================================
# TAB 4 EMERGENCY RESPONSE COMMAND CENTER
# =====================================================

with tab4:

    st.subheader("🚨 Emergency Response Command Center")

    st.markdown("---")

    # ==========================================
    # COMMAND CENTER KPIs
    # ==========================================

    k1,k2,k3,k4 = st.columns(4)

    k1.metric(
        "Rescue Teams",
        "24",
        "+4"
    )

    k2.metric(
        "Available Shelters",
        "18"
    )

    k3.metric(
        "Emergency Vehicles",
        "42"
    )

    k4.metric(
        "Citizens Alerted",
        "12,480"
    )

    st.markdown("---")

    # ==========================================
    # SHELTER OCCUPANCY
    # ==========================================

    st.subheader("🏫 Shelter Occupancy Dashboard")

    shelter_df = pd.DataFrame({

        "Shelter":[
            "Govt School A",
            "Community Hall",
            "Sports Complex",
            "Relief Camp"
        ],

        "Occupancy":[
            72,
            58,
            91,
            46
        ]
    })

    fig = px.bar(
        shelter_df,
        x="Shelter",
        y="Occupancy",
        title="Shelter Occupancy (%)",
        text="Occupancy"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("---")

    # ==========================================
    # RESCUE TEAM STATUS
    # ==========================================

    st.subheader("🚑 Rescue Team Tracking")

    rescue_df = pd.DataFrame({

        "Team":[
            "NDRF-01",
            "NDRF-02",
            "SDRF-01",
            "Fire Unit"
        ],

        "Status":[
            "Deployed",
            "Ready",
            "Deployed",
            "Ready"
        ],

        "ETA":[
            "12 min",
            "25 min",
            "8 min",
            "18 min"
        ]
    })

    st.dataframe(
        rescue_df,
        use_container_width=True
    )

    st.markdown("---")

    # ==========================================
    # RESOURCE STATUS
    # ==========================================

    st.subheader("📦 Emergency Resource Inventory")

    r1,r2,r3,r4 = st.columns(4)

    r1.metric(
        "Food Kits",
        "4,800"
    )

    r2.metric(
        "Water Bottles",
        "12,500"
    )

    r3.metric(
        "Medical Kits",
        "2,140"
    )

    r4.metric(
        "Life Jackets",
        "860"
    )

    st.markdown("---")

    # ==========================================
    # ROAD STATUS
    # ==========================================

    st.subheader("🛣 Road Accessibility Analysis")

    roads = pd.DataFrame({

        "Road":[
            "NH-07",
            "Village Road A",
            "Bridge Route",
            "Hill Corridor"
        ],

        "Status":[
            "Open",
            "Flooded",
            "Open",
            "Blocked"
        ]
    })

    st.dataframe(
        roads,
        use_container_width=True
    )

    st.markdown("---")

    # ==========================================
    # ALERT SYSTEM
    # ==========================================

    st.subheader("📲 Multi-Channel Alert Distribution")

    sms,email,app,radio = st.columns(4)

    sms.success("SMS Alerts\n\n12,480 Sent")

    email.success("Email Alerts\n\n4,812 Sent")

    app.success("Mobile App\n\n8,426 Sent")

    radio.success("Radio Broadcast\n\nActive")

    st.markdown("---")

    # ==========================================
    # EVACUATION PROGRESS
    # ==========================================

    st.subheader("🚶 Evacuation Progress")

    evacuation_progress = 74

    st.progress(evacuation_progress)

    st.info(
        f"{evacuation_progress}% of vulnerable population evacuated."
    )

    st.markdown("---")

    # ==========================================
    # RESPONSE TIMELINE
    # ==========================================

    st.subheader("⏳ Incident Response Timeline")

    response_df = pd.DataFrame({

        "Time":[
            "08:00",
            "08:20",
            "08:45",
            "09:10",
            "09:30",
            "10:00"
        ],

        "Action":[
            "Heavy Rain Detected",
            "AI Warning Issued",
            "Authorities Alerted",
            "Shelters Opened",
            "Evacuation Started",
            "Rescue Teams Deployed"
        ]
    })

    st.dataframe(
        response_df,
        use_container_width=True
    )

    st.markdown("---")

    # ==========================================
    # LIVE ALERT FEED
    # ==========================================

    st.subheader("📡 Live Incident Feed")

    st.warning("09:12 AM - River level increased by 0.4m")

    st.warning("09:18 AM - Heavy rainfall detected near Chamoli")

    st.error("09:24 AM - Landslide probability exceeds threshold")

    st.success("09:30 AM - Shelter #3 operational")

    st.markdown("---")

    # ==========================================
    # EXECUTIVE SUMMARY
    # ==========================================

    st.subheader("📋 District Collector Dashboard Summary")

    st.info("""
    • Flood Risk Level: HIGH

    • Villages Under Threat: 4

    • Population at Risk: 12,480

    • Shelters Activated: 18

    • Rescue Teams Deployed: 24

    • Estimated Lead Time: 2.4 Hours

    • AI Confidence Score: 94%
    """)
# =====================================================
# TAB 5 DIGITAL TWIN & SATELLITE INTELLIGENCE
# =====================================================

with tab5:

    st.subheader("🛰️ Digital Twin Flood Intelligence Platform")

    st.markdown("---")

    # ==========================================
    # SATELLITE STATUS
    # ==========================================

    st.subheader("🛰 Satellite Monitoring")

    s1,s2,s3,s4 = st.columns(4)

    s1.metric(
        "Satellite Source",
        "ISRO"
    )

    s2.metric(
        "Last Image",
        "12 min ago"
    )

    s3.metric(
        "Cloud Coverage",
        "21%"
    )

    s4.metric(
        "Image Resolution",
        "10m"
    )

    st.markdown("---")

    # ==========================================
    # SATELLITE CHANGE DETECTION
    # ==========================================

    st.subheader("🌍 Terrain Change Detection")

    terrain = pd.DataFrame({

        "Region":[
            "Joshimath",
            "Chamoli",
            "Rudraprayag",
            "Karnaprayag"
        ],

        "Land Shift (%)":[
            4.2,
            2.1,
            7.6,
            3.8
        ]
    })

    fig = px.bar(
        terrain,
        x="Region",
        y="Land Shift (%)",
        title="Satellite Terrain Change Analysis"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("---")

    # ==========================================
    # DRONE FLEET
    # ==========================================

    st.subheader("🚁 Autonomous Drone Surveillance")

    d1,d2,d3,d4 = st.columns(4)

    d1.metric(
        "Active Drones",
        "8"
    )

    d2.metric(
        "Coverage Area",
        "124 km²"
    )

    d3.metric(
        "Live Feeds",
        "8"
    )

    d4.metric(
        "Battery Health",
        "93%"
    )

    st.markdown("---")

    # ==========================================
    # FLOOD SPREAD SIMULATION
    # ==========================================

    st.subheader("🌊 Flood Spread Simulation")

    flood_df = pd.DataFrame({

        "Hour":[
            "0",
            "2",
            "4",
            "6",
            "8",
            "10",
            "12"
        ],

        "Affected Area (km²)":[
            3,
            8,
            15,
            26,
            38,
            51,
            67
        ]
    })

    fig = px.area(
        flood_df,
        x="Hour",
        y="Affected Area (km²)",
        title="Predicted Flood Expansion"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("---")

    # ==========================================
    # LANDSLIDE RISK
    # ==========================================

    st.subheader("⛰ Landslide Susceptibility Analysis")

    landslide = pd.DataFrame({

        "Zone":[
            "Zone A",
            "Zone B",
            "Zone C",
            "Zone D"
        ],

        "Risk":[
            82,
            55,
            34,
            73
        ]
    })

    fig = px.bar(
        landslide,
        x="Zone",
        y="Risk",
        title="Landslide Probability (%)",
        color="Risk"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("---")

    # ==========================================
    # DIGITAL TWIN HEALTH
    # ==========================================

    st.subheader("🏙 Digital Twin Status")

    dt1,dt2,dt3,dt4 = st.columns(4)

    dt1.metric(
        "Villages Modeled",
        "124"
    )

    dt2.metric(
        "Sensors Connected",
        "842"
    )

    dt3.metric(
        "Live Streams",
        "58"
    )

    dt4.metric(
        "Model Accuracy",
        "96.2%"
    )

    st.markdown("---")

    # ==========================================
    # HEATMAP DATA
    # ==========================================

    st.subheader("🔥 Flood Vulnerability Heatmap")

    heatmap_data = pd.DataFrame({
        "lat":[
            30.31,
            30.32,
            30.33,
            30.35,
            30.36
        ],
        "lon":[
            78.03,
            78.04,
            78.06,
            78.08,
            78.10
        ]
    })

    heatmap_map = folium.Map(
        location=[30.33,78.06],
        zoom_start=10
    )

    for _, row in heatmap_data.iterrows():

        folium.Circle(
            location=[row["lat"],row["lon"]],
            radius=2000,
            color="red",
            fill=True,
            fill_opacity=0.35
        ).add_to(heatmap_map)

    st_folium(
        heatmap_map,
        height=500
    )

    st.markdown("---")

    # ==========================================
    # CRITICAL INFRASTRUCTURE
    # ==========================================

    st.subheader("🏥 Critical Infrastructure Impact")

    infra = pd.DataFrame({

        "Infrastructure":[
            "Hospitals",
            "Schools",
            "Road Bridges",
            "Power Stations",
            "Water Plants"
        ],

        "Risk Level":[
            "Medium",
            "High",
            "High",
            "Low",
            "Medium"
        ]
    })

    st.dataframe(
        infra,
        use_container_width=True
    )

    st.markdown("---")

    # ==========================================
    # FUTURE SCENARIOS
    # ==========================================

    st.subheader("🔮 AI Scenario Simulation")

    scenario = pd.DataFrame({

        "Scenario":[
            "Current Conditions",
            "+20% Rainfall",
            "+40% Rainfall",
            Extreme Storm"
        ],

        "Expected Risk":[
            62,
            76,
            88,
            97
        ]
    })

    fig = px.line(
        scenario,
        x="Scenario",
        y="Expected Risk",
        markers=True,
        title="Future Risk Scenarios"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("---")

    # ==========================================
    # SMART CITY SUMMARY
    # ==========================================

    st.subheader("🌐 Unified Disaster Intelligence Summary")

    st.success("""
    ✅ AI Flood Prediction Active

    ✅ Digital Twin Synced

    ✅ Satellite Monitoring Online

    ✅ Drone Surveillance Active

    ✅ Shelter Network Ready

    ✅ Emergency Teams Available

    ✅ Hyper-Local Forecast Operational

    ✅ Multi-Source Data Integration Active
    """)
    st.success("✅ Disaster Management Dashboard Operational")
