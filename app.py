import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
import os
from datetime import datetime

# =========================================================
# 1. PAGE CONFIGURATION & LOCAL STORAGE PATHS
# =========================================================
st.set_page_config(
    page_title="Emily Park | Wellness Analytics",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

PROFILE_FILE = "user_profile.json"
PREFS_FILE = "user_prefs.json"

# =========================================================
# 2. LOCAL STORAGE MANAGEMENT (PROFILE & PREFERENCES)
# =========================================================
DEFAULT_PROFILE = {
    "full_name": "Emily Park",
    "age": 21,
    "height_cm": 168.0,
    "weight_kg": 58.0,
    "blood_group": "A+"
}

DEFAULT_PREFS = {
    "theme": "Sage Green & White (Default)"
}

def load_profile():
    if os.path.exists(PROFILE_FILE):
        try:
            with open(PROFILE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return DEFAULT_PROFILE.copy()
    return DEFAULT_PROFILE.copy()

def save_profile(profile_data):
    with open(PROFILE_FILE, "w") as f:
        json.dump(profile_data, f, indent=4)

def load_prefs():
    if os.path.exists(PREFS_FILE):
        try:
            with open(PREFS_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return DEFAULT_PREFS.copy()
    return DEFAULT_PREFS.copy()

def save_prefs(prefs_data):
    with open(PREFS_FILE, "w") as f:
        json.dump(prefs_data, f, indent=4)

# Initialize Session State
if "profile" not in st.session_state:
    st.session_state["profile"] = load_profile()

if "prefs" not in st.session_state:
    st.session_state["prefs"] = load_prefs()

# Calculate BMI helper
def calculate_bmi(weight, height_cm):
    if height_cm and height_cm > 0 and weight and weight > 0:
        height_m = height_cm / 100.0
        bmi = weight / (height_m ** 2)
        if bmi < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi < 24.9:
            category = "Normal Weight"
        elif 25 <= bmi < 29.9:
            category = "Overweight"
        else:
            category = "Obesity"
        return round(bmi, 1), category
    return None, "N/A"

# =========================================================
# 3. COLOR THEME SYSTEM & CUSTOM CSS
# =========================================================
THEMES = {
    "Sage Green & White (Default)": {
        "bg": "#F4F8F6",
        "card": "#FFFFFF",
        "primary": "#064E3B",
        "emerald": "#21866D",
        "mint": "#83D6B8",
        "teal": "#83C9C8",
        "light_mint": "#DDF2EA",
        "text": "#173D35",
        "secondary_text": "#647873",
        "border": "#E4ECE8"
    },
    "Ocean Teal": {
        "bg": "#F0F7F7",
        "card": "#FFFFFF",
        "primary": "#0A4D5C",
        "emerald": "#137A8F",
        "mint": "#76C7D2",
        "teal": "#5BB5C4",
        "light_mint": "#E0F2F4",
        "text": "#0F3842",
        "secondary_text": "#517B85",
        "border": "#D5E7EA"
    },
    "Lavender & White": {
        "bg": "#F7F5FB",
        "card": "#FFFFFF",
        "primary": "#3C2A56",
        "emerald": "#6B4C9A",
        "mint": "#B8A2DB",
        "teal": "#9F86C0",
        "light_mint": "#ECE6F7",
        "text": "#2A1D3D",
        "secondary_text": "#685B7E",
        "border": "#E5DEFA"
    },
    "Dark Forest Green": {
        "bg": "#0D1F19",
        "card": "#142B23",
        "primary": "#52B788",
        "emerald": "#74C69D",
        "mint": "#95D5B2",
        "teal": "#B7E4C7",
        "light_mint": "#1E3D32",
        "text": "#E8F5E9",
        "secondary_text": "#A3B899",
        "border": "#24473B"
    }
}

active_theme_name = st.session_state["prefs"].get("theme", "Sage Green & White (Default)")
if active_theme_name not in THEMES:
    active_theme_name = "Sage Green & White (Default)"
T = THEMES[active_theme_name]

CUSTOM_CSS = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Inter', 'DM Sans', sans-serif;
    }}
    
    .stApp {{
        background-color: {T["bg"]};
        color: {T["text"]};
    }}
    
    /* Header Card */
    .header-card {{
        background-color: {T["card"]};
        border: 1px solid {T["border"]};
        border-radius: 16px;
        padding: 22px 28px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
    }}
    .header-title {{
        font-size: 26px;
        font-weight: 700;
        color: {T["primary"]};
        margin: 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }}
    .header-subtitle {{
        font-size: 14px;
        color: {T["secondary_text"]};
        margin-top: 4px;
    }}
    .header-date-badge {{
        background-color: {T["light_mint"]};
        color: {T["primary"]};
        font-weight: 600;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 13px;
        display: inline-block;
    }}
    
    /* KPI Card */
    .kpi-card-v2 {{
        background-color: {T["card"]};
        border: 1px solid {T["border"]};
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.02);
        transition: transform 0.2s ease;
    }}
    .kpi-card-v2:hover {{
        transform: translateY(-2px);
    }}
    .kpi-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    .kpi-label {{
        font-size: 13px;
        font-weight: 600;
        color: {T["secondary_text"]};
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    .kpi-icon-box {{
        width: 38px;
        height: 38px;
        border-radius: 10px;
        background-color: {T["light_mint"]};
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
    }}
    .kpi-val {{
        font-size: 28px;
        font-weight: 700;
        color: {T["primary"]};
        margin-top: 10px;
    }}
    .kpi-footer {{
        font-size: 12px;
        color: {T["emerald"]};
        margin-top: 4px;
        font-weight: 500;
    }}
    
    /* Section Title */
    .section-title {{
        font-size: 18px;
        font-weight: 700;
        color: {T["primary"]};
        margin-top: 15px;
        margin-bottom: 16px;
        border-left: 4px solid {T["emerald"]};
        padding-left: 10px;
    }}
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {{
        background-color: {T["card"]};
        border-right: 1px solid {T["border"]};
    }}
    
    /* General Container Card */
    .content-card {{
        background-color: {T["card"]};
        border: 1px solid {T["border"]};
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.02);
    }}

    /* Disclaimer box */
    .disclaimer-text {{
        font-size: 11px;
        color: {T["secondary_text"]};
        font-style: italic;
        margin-top: 6px;
    }}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# =========================================================
# 4. DATA LOADER & DATA CLEANING
# =========================================================
@st.cache_data
def load_dataset(source):
    try:
        df = pd.read_csv(source)
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y', errors='coerce')
            df = df.sort_values('date').reset_index(drop=True)
        return df
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return None

# =========================================================
# 5. SIDEBAR & PROFILE HANDLING
# =========================================================
st.sidebar.markdown(f"<h2 style='color:{T['primary']}; font-weight:700; font-size:22px; margin-bottom:0;'>🌿 Wellness Analytics</h2>", unsafe_allow_html=True)
st.sidebar.markdown(f"<p style='color:{T['secondary_text']}; font-size:12px;'>Emily Park Analytics Platform</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# Collapsible Personal Health Profile
with st.sidebar.expander("👤 Personal Health Profile", expanded=False):
    prof = st.session_state["profile"]
    bmi_val, bmi_cat = calculate_bmi(prof.get("weight_kg"), prof.get("height_cm"))
    
    if "edit_profile_mode" not in st.session_state:
        st.session_state["edit_profile_mode"] = False
        
    if not st.session_state["edit_profile_mode"]:
        st.markdown(f"**Full Name:** {prof.get('full_name')}")
        st.markdown(f"**Age:** {prof.get('age')} years")
        st.markdown(f"**Height:** {prof.get('height_cm')} cm")
        st.markdown(f"**Weight:** {prof.get('weight_kg')} kg")
        st.markdown(f"**Blood Group:** {prof.get('blood_group')}")
        if bmi_val:
            st.markdown(f"**BMI:** `{bmi_val}` ({bmi_cat})")
        else:
            st.markdown("**BMI:** N/A")
            
        st.markdown('<p class="disclaimer-text">* Note: BMI is informational only, not a medical diagnosis.</p>', unsafe_allow_html=True)
        
        if st.button("✏️ Edit Profile", use_container_width=True):
            st.session_state["edit_profile_mode"] = True
            st.rerun()
    else:
        with st.form("edit_profile_form"):
            new_name = st.text_input("Full Name", value=prof.get("full_name", ""))
            new_age = st.number_input("Age", min_value=1, max_value=120, value=int(prof.get("age", 21)))
            new_height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=float(prof.get("height_cm", 168.0)))
            new_weight = st.number_input("Weight (kg)", min_value=20.0, max_value=300.0, value=float(prof.get("weight_kg", 58.0)))
            new_bg = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"], index=["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"].index(prof.get("blood_group", "A+")))
            
            save_clicked = st.form_submit_button("💾 Save Profile", use_container_width=True)
            if save_clicked:
                updated_p = {
                    "full_name": new_name,
                    "age": new_age,
                    "height_cm": new_height,
                    "weight_kg": new_weight,
                    "blood_group": new_bg
                }
                st.session_state["profile"] = updated_p
                save_profile(updated_p)
                st.session_state["edit_profile_mode"] = False
                st.success("Profile saved successfully!")
                st.rerun()

st.sidebar.markdown("---")

# Dataset File Handler
default_csv = "PJ2_Emily_Park_wellness_2025.csv"
uploaded_file = st.sidebar.file_uploader("📂 Upload Dataset CSV", type=["csv"])

if uploaded_file is not None:
    df_raw = load_dataset(uploaded_file)
elif os.path.exists(default_csv):
    df_raw = load_dataset(default_csv)
else:
    df_raw = None

# Navigation Menu
nav_selection = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Overview",
        "🏃 Physical Activity",
        "🌙 Sleep Analysis",
        "❤️ Heart Health",
        "🧠 Mental Wellness",
        "💧 Lifestyle",
        "⚙️ Settings"
    ]
)

# Date Filter (if data available)
if df_raw is not None and not df_raw.empty and 'date' in df_raw.columns:
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"<p style='font-size:13px; font-weight:600; color:{T['secondary_text']};'>📅 Date Range Filter</p>", unsafe_allow_html=True)
    min_d = df_raw['date'].min().date()
    max_d = df_raw['date'].max().date()
    
    date_range = st.sidebar.date_input(
        "Select Range:",
        value=[min_d, max_d],
        min_value=min_d,
        max_value=max_d
    )
    if isinstance(date_range, list) or isinstance(date_range, tuple):
        if len(date_range) == 2:
            start_d, end_d = date_range
            mask = (df_raw['date'].dt.date >= start_d) & (df_raw['date'].dt.date <= end_d)
            df = df_raw.loc[mask].copy()
        else:
            df = df_raw.copy()
    else:
        df = df_raw.copy()
else:
    df = df_raw.copy() if df_raw is not None else None

# =========================================================
# 6. HEADER RENDERER (DYNAMIC DATASET BOUNDS)
# =========================================================
current_user = st.session_state["profile"].get("full_name", "Emily Park")

# Safely extract dataset start date, end date, and record count dynamically
if df is not None and not df.empty and 'date' in df.columns:
    start_date_str = df['date'].min().strftime('%b %d, %Y')
    end_date_str = df['date'].max().strftime('%b %d, %Y')
    total_records = len(df)
    date_display = f"📅 {start_date_str} – {end_date_str} | {total_records} Logs"
else:
    date_display = "📅 No Data Selected"

st.markdown(
    f"""
    <div class="header-card">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
            <div>
                <div class="header-title">
                    <span>🌿 Emily Park Wellness Dashboard</span>
                </div>
                <div class="header-subtitle">
                    Welcome back, <b>{current_user}</b>! Your daily health, activity, and lifestyle telemetry insights.
                </div>
            </div>
            <div style="text-align: right;">
                <span class="header-date-badge">{date_display}</span>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

if df is None or df.empty:
    st.warning("⚠️ No valid dataset loaded. Please upload a dataset or ensure `PJ2_Emily_Park_wellness_2025.csv` is present.")
    st.stop()

# Helper for Plotly layout styling
def apply_chart_theme(fig, title=""):
    fig.update_layout(
        title=dict(text=title, font=dict(family="Inter, sans-serif", size=15, color=T["primary"])),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif", color=T["text"]),
        margin=dict(t=40, b=30, l=30, r=30),
        xaxis=dict(showgrid=True, gridcolor=T["border"], color=T["secondary_text"]),
        yaxis=dict(showgrid=True, gridcolor=T["border"], color=T["secondary_text"]),
        legend=dict(font=dict(color=T["text"]))
    )
    return fig

# =========================================================
# 7. PAGE MODULES
# =========================================================

# --- MODULE 1: OVERVIEW ---
if nav_selection == "🏠 Overview":
    st.markdown('<div class="section-title">Executive Wellness Overview</div>', unsafe_allow_html=True)
    
    k1, k2, k3, k4 = st.columns(4)
    
    with k1:
        v_steps = df['steps'].mean() if 'steps' in df.columns else None
        val_str = f"{v_steps:,.0f}" if pd.notnull(v_steps) else "N/A"
        st.markdown(
            f"""
            <div class="kpi-card-v2">
                <div class="kpi-header">
                    <span class="kpi-label">Avg Daily Steps</span>
                    <div class="kpi-icon-box">👟</div>
                </div>
                <div class="kpi-val">{val_str}</div>
                <div class="kpi-footer">Target: 10,000 steps/day</div>
            </div>
            """, unsafe_allow_html=True
        )

    with k2:
        v_cal = df['calories_burned'].mean() if 'calories_burned' in df.columns else None
        val_str = f"{v_cal:,.0f} kcal" if pd.notnull(v_cal) else "N/A"
        st.markdown(
            f"""
            <div class="kpi-card-v2">
                <div class="kpi-header">
                    <span class="kpi-label">Avg Calories</span>
                    <div class="kpi-icon-box">🔥</div>
                </div>
                <div class="kpi-val">{val_str}</div>
                <div class="kpi-footer">Daily Energy Output</div>
            </div>
            """, unsafe_allow_html=True
        )

    with k3:
        v_slp = df['sleep_hours'].mean() if 'sleep_hours' in df.columns else None
        val_str = f"{v_slp:.1f} hrs" if pd.notnull(v_slp) else "N/A"
        st.markdown(
            f"""
            <div class="kpi-card-v2">
                <div class="kpi-header">
                    <span class="kpi-label">Avg Sleep</span>
                    <div class="kpi-icon-box">🌙</div>
                </div>
                <div class="kpi-val">{val_str}</div>
                <div class="kpi-footer">Target: 7.0 - 9.0 hrs</div>
            </div>
            """, unsafe_allow_html=True
        )

    with k4:
        v_hr = df['avg_heart_rate_bpm'].mean() if 'avg_heart_rate_bpm' in df.columns else None
        val_str = f"{v_hr:.0f} bpm" if pd.notnull(v_hr) else "N/A"
        st.markdown(
            f"""
            <div class="kpi-card-v2">
                <div class="kpi-header">
                    <span class="kpi-label">Avg Heart Rate</span>
                    <div class="kpi-icon-box">❤️</div>
                </div>
                <div class="kpi-val">{val_str}</div>
                <div class="kpi-footer">Resting baseline: {df['resting_heart_rate_bpm'].mean():.0f} bpm</div>
            </div>
            """, unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        if 'date' in df.columns and 'steps' in df.columns:
            fig1 = px.line(df, x='date', y='steps', color_discrete_sequence=[T["emerald"]])
            apply_chart_theme(fig1, "Daily Steps Trajectory")
            st.plotly_chart(fig1, use_container_width=True)

    with col_b:
        if 'date' in df.columns and 'sleep_score' in df.columns and 'hrv_ms' in df.columns:
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=df['date'], y=df['sleep_score'].rolling(7).mean(), mode='lines', name='Sleep Score (7d)', line=dict(color=T["primary"], width=2)))
            fig2.add_trace(go.Scatter(x=df['date'], y=df['hrv_ms'].rolling(7).mean(), mode='lines', name='HRV ms (7d)', line=dict(color=T["teal"], width=2)))
            apply_chart_theme(fig2, "Sleep Quality vs. HRV Recovery Trend (7-Day Rolling)")
            st.plotly_chart(fig2, use_container_width=True)

# --- MODULE 2: PHYSICAL ACTIVITY ---
elif nav_selection == "🏃 Physical Activity":
    st.markdown('<div class="section-title">Physical Activity & Energy Expenditure</div>', unsafe_allow_html=True)
    
    r1_1, r1_2 = st.columns(2)
    with r1_1:
        if 'date' in df.columns and 'steps' in df.columns:
            fig = px.line(df, x='date', y='steps', color_discrete_sequence=[T["emerald"]])
            fig.update_traces(line=dict(shape='spline', width=2))
            apply_chart_theme(fig, "Daily Steps Trend (Smooth Line)")
            st.plotly_chart(fig, use_container_width=True)

    with r1_2:
        if 'date' in df.columns and 'calories_burned' in df.columns:
            fig = px.area(df, x='date', y='calories_burned', color_discrete_sequence=[T["mint"]])
            apply_chart_theme(fig, "Calories Burned (Area Chart)")
            st.plotly_chart(fig, use_container_width=True)

    r2_1, r2_2 = st.columns(2)
    with r2_1:
        if 'date' in df.columns and 'distance_km' in df.columns:
            fig = px.bar(df, x='date', y='distance_km', color_discrete_sequence=[T["teal"]])
            apply_chart_theme(fig, "Distance Covered in Km (Bar Chart)")
            st.plotly_chart(fig, use_container_width=True)

    with r2_2:
        if 'exercise_type' in df.columns:
            ex_counts = df['exercise_type'].value_counts(dropna=False).reset_index()
            ex_counts.columns = ['exercise_type', 'count']
            ex_counts['exercise_type'] = ex_counts['exercise_type'].fillna('Rest / Unlogged')
            fig = px.pie(ex_counts, values='count', names='exercise_type', hole=0.45,
                         color_discrete_sequence=[T["primary"], T["emerald"], T["mint"], T["teal"], T["light_mint"]])
            apply_chart_theme(fig, "Exercise Type Distribution (Donut Chart)")
            st.plotly_chart(fig, use_container_width=True)

# --- MODULE 3: SLEEP ANALYSIS ---
elif nav_selection == "🌙 Sleep Analysis":
    st.markdown('<div class="section-title">Sleep Architecture & Quality Analytics</div>', unsafe_allow_html=True)
    
    s1, s2, s3 = st.columns(3)
    with s1:
        if 'date' in df.columns and 'sleep_hours' in df.columns:
            fig = px.line(df, x='date', y='sleep_hours', color_discrete_sequence=[T["primary"]])
            apply_chart_theme(fig, "Sleep Duration (Line Chart)")
            st.plotly_chart(fig, use_container_width=True)

    with s2:
        if 'sleep_score' in df.columns:
            fig = px.histogram(df, x='sleep_score', nbins=20, color_discrete_sequence=[T["emerald"]])
            apply_chart_theme(fig, "Sleep Quality Distribution (Bar Chart)")
            st.plotly_chart(fig, use_container_width=True)

    with s3:
        if 'date' in df.columns and 'deep_sleep_pct' in df.columns:
            fig = px.area(df, x='date', y='deep_sleep_pct', color_discrete_sequence=[T["teal"]])
            apply_chart_theme(fig, "Deep Sleep % Trend (Area Chart)")
            st.plotly_chart(fig, use_container_width=True)

# --- MODULE 4: HEART HEALTH ---
elif nav_selection == "❤️ Heart Health":
    st.markdown('<div class="section-title">Cardiovascular & Recovery Biomarkers</div>', unsafe_allow_html=True)
    
    h1, h2, h3 = st.columns(3)
    with h1:
        if 'date' in df.columns and 'avg_heart_rate_bpm' in df.columns:
            fig = px.line(df, x='date', y='avg_heart_rate_bpm', color_discrete_sequence=["#E63946"])
            apply_chart_theme(fig, "Average Heart Rate (Line Chart)")
            st.plotly_chart(fig, use_container_width=True)

    with h2:
        if 'date' in df.columns and 'resting_heart_rate_bpm' in df.columns:
            fig = px.line(df, x='date', y='resting_heart_rate_bpm', color_discrete_sequence=[T["primary"]])
            apply_chart_theme(fig, "Resting Heart Rate (Line Chart)")
            st.plotly_chart(fig, use_container_width=True)

    with h3:
        if 'date' in df.columns and 'hrv_ms' in df.columns:
            fig = px.area(df, x='date', y='hrv_ms', color_discrete_sequence=[T["mint"]])
            apply_chart_theme(fig, "Heart Rate Variability HRV (Area Chart)")
            st.plotly_chart(fig, use_container_width=True)

# --- MODULE 5: MENTAL WELLNESS ---
elif nav_selection == "🧠 Mental Wellness":
    st.markdown('<div class="section-title">Mental Wellness & Stress Metrics</div>', unsafe_allow_html=True)
    
    m1, m2, m3 = st.columns(3)
    with m1:
        if 'mood_1to5' in df.columns:
            m_counts = df['mood_1to5'].value_counts().sort_index().reset_index()
            m_counts.columns = ['mood_score', 'count']
            fig = px.pie(m_counts, values='count', names='mood_score', hole=0.4,
                         color_discrete_sequence=[T["primary"], T["emerald"], T["mint"], T["teal"], T["light_mint"]])
            apply_chart_theme(fig, "Mood Score Distribution (Donut Chart)")
            st.plotly_chart(fig, use_container_width=True)

    with m2:
        if 'date' in df.columns and 'stress_score' in df.columns:
            fig = px.line(df, x='date', y='stress_score', color_discrete_sequence=["#D90429"])
            apply_chart_theme(fig, "Daily Stress Score Trend (Line Chart)")
            st.plotly_chart(fig, use_container_width=True)

    with m3:
        if 'stress_score' in df.columns and 'mood_1to5' in df.columns:
            fig = px.scatter(df, x='stress_score', y='mood_1to5', color='sleep_score' if 'sleep_score' in df.columns else None,
                             color_continuous_scale='Viridis')
            apply_chart_theme(fig, "Mood vs. Stress Level (Scatter Plot)")
            st.plotly_chart(fig, use_container_width=True)

# --- MODULE 6: LIFESTYLE ---
elif nav_selection == "💧 Lifestyle":
    st.markdown('<div class="section-title">Hydration & Weight Telemetry</div>', unsafe_allow_html=True)
    
    l1, l2, l3 = st.columns(3)
    with l1:
        if 'date' in df.columns and 'water_liters' in df.columns:
            fig = px.bar(df, x='date', y='water_liters', color_discrete_sequence=[T["teal"]])
            apply_chart_theme(fig, "Daily Water Intake in Liters (Bar Chart)")
            st.plotly_chart(fig, use_container_width=True)

    with l2:
        if 'water_liters' in df.columns:
            avg_w = df['water_liters'].mean()
            target_w = 3.0
            pct = min(100.0, (avg_w / target_w) * 100) if target_w else 0
            
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=avg_w,
                number={'suffix': " L", 'font': {'color': T["primary"]}},
                gauge={
                    'axis': {'range': [None, 4.0], 'tickcolor': T["secondary_text"]},
                    'bar': {'color': T["emerald"]},
                    'bgcolor': T["bg"],
                    'bordercolor': T["border"],
                    'steps': [
                        {'range': [0, 2.0], 'color': T["light_mint"]},
                        {'range': [2.0, 3.0], 'color': T["mint"]}
                    ]
                }
            ))
            apply_chart_theme(fig, "Hydration Goal Completion Gauge")
            st.plotly_chart(fig, use_container_width=True)

    with l3:
        if 'date' in df.columns and 'weight_kg' in df.columns:
            fig = px.line(df, x='date', y='weight_kg', color_discrete_sequence=[T["primary"]])
            apply_chart_theme(fig, "Weight Progression in Kg (Line Chart)")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Weight tracking data not available in current filtered range.")

# --- MODULE 7: SETTINGS ---
elif nav_selection == "⚙️ Settings":
    st.markdown('<div class="section-title">System Settings & Preferences</div>', unsafe_allow_html=True)
    
    st.markdown("### 🎨 Theme Customization")
    selected_theme = st.selectbox(
        "Choose Color Theme:",
        list(THEMES.keys()),
        index=list(THEMES.keys()).index(active_theme_name)
    )
    
    if selected_theme != active_theme_name:
        st.session_state["prefs"]["theme"] = selected_theme
        save_prefs(st.session_state["prefs"])
        st.success(f"Theme changed to {selected_theme}!")
        st.rerun()

    st.markdown("---")
    st.markdown("### 🔄 Reset & Restore Options")
    
    r_col1, r_col2, r_col3, r_col4 = st.columns(4)
    
    with r_col1:
        if st.button("Reset Theme to Default", use_container_width=True):
            st.session_state["prefs"]["theme"] = "Sage Green & White (Default)"
            save_prefs(st.session_state["prefs"])
            st.success("Theme reset to default!")
            st.rerun()
            
    with r_col2:
        if st.button("Reset Health Profile", use_container_width=True):
            st.session_state["reset_profile_confirm"] = True

    with r_col3:
        if st.button("Reset Preferences", use_container_width=True):
            st.session_state["prefs"] = DEFAULT_PREFS.copy()
            save_prefs(DEFAULT_PREFS)
            st.success("Preferences reset!")
            st.rerun()

    with r_col4:
        if st.button("Reset Filters", use_container_width=True):
            st.success("Filters reset!")
            st.rerun()

    if st.session_state.get("reset_profile_confirm", False):
        st.warning("⚠️ Are you sure you want to permanently reset your saved personal profile?")
        c_yes, c_no = st.columns(2)
        with c_yes:
            if st.button("Yes, Reset Profile", use_container_width=True):
                st.session_state["profile"] = DEFAULT_PROFILE.copy()
                save_profile(DEFAULT_PROFILE)
                st.session_state["reset_profile_confirm"] = False
                st.success("Profile restored to default!")
                st.rerun()
        with c_no:
            if st.button("Cancel", use_container_width=True):
                st.session_state["reset_profile_confirm"] = False
                st.rerun()