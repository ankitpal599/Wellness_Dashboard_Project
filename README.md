[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://wellnessdashboardproject-7spdbvdwlyy9eptultg3dc.streamlit.app)
Live Interactive Demo: [Click Here to View Dashboard](https://wellnessdashboardproject-7spdbvdwlyy9eptultg3dc.streamlit.app)

# Personal Wellness Dashboard
A modern, interactive, and data-driven personal wellness analytics platform built using Python and Streamlit. This application processes wearable fitness telemetry data to provide holistic insights into daily physical activity, sleep quality, cardiovascular health, mental stress, and hydration patterns.

# 1. Project Introduction
In today's fast-paced world, tracking personal health metrics has become essential for maintaining long-term biological well-being and physical fitness. Wearable devices collect vast amounts of telemetry data, but raw numbers are often difficult to interpret without proper visual aggregation.

The "Personal Wellness Dashboard" bridges this gap by transforming raw daily health logs into intuitive, interactive visual analytics. Designed with an executive bio-harmonious interface, the application empowers users to monitor their personal physical performance, biological recovery, sleep efficiency, and stress levels through unified data visualizations.

# 2. Project Objectives
* Holistic Analytics: Build a central dashboard unifying activity, sleep, cardiovascular health, hydration, and stress metrics into a single interface.
* Interactive Visualization: Provide dynamic, responsive Plotly visual analytics allowing users to inspect trends, filter date ranges, and analyze patterns.
* Local Data Persistence: Allow users to update and persist personal health profiles (height, weight, blood group, age) locally using JSON file storage with automatic BMI calculation.
* Data Transparency & Inspection: Implement a dedicated Data Analysis module for descriptive statistics, correlation heatmaps, data completeness checks, and CSV data exports.
* Custom User Experience: Support dynamic UI theme customization (Sage Green, Ocean Teal, Lavender, Dark Forest Green) tailored for health-tech application standards.

# 4. Technologies Used
* Core Programming Language: Python 3.9+
* Web Framework: Streamlit (UI rendering, layout containers, sidebar controls, session state management)
* Data Manipulation & Analysis: Pandas, NumPy
* Data Visualization: Plotly Express, Plotly Graph Objects (Interactive, responsive charts)
* Local Storage & Persistence: JSON (`user_profile.json`, `user_prefs.json`)

# 5. Dataset Description

The application processes daily health telemetry logs stored in `PJ2_Emily_Park_wellness_2025.csv` (365 records representing daily logs for the year 2025 across 19 features):

| Column Name | Data Type | Description |
| `date` | String (`DD-MM-YYYY`) | Date of entry |
| `day_of_week` | String | Day of the week |
| `steps` | Float | Total daily step count |
| `distance_km` | Float | Distance covered in kilometers |
| `calories_burned` | Float | Total energy expenditure in kilocalories (kcal) |
| `exercise_minutes` | Integer | Active exercise duration in minutes |
| `exercise_type` | String | Category of workout (Weight Training, Walking, Dancing, Running, Yoga) |
| `avg_heart_rate_bpm` | Integer | Average daily heart rate in beats per minute |
| `resting_heart_rate_bpm` | Integer | Resting heart rate upon waking up (BPM) |
| `hrv_ms` | Float | Heart Rate Variability in milliseconds (HRV) |
| `sleep_hours` | Float | Total duration of sleep in hours |
| `deep_sleep_pct` | Float | Percentage of total sleep spent in deep sleep |
| `bedtime` | String | Time going to bed (`HH:MM`) |
| `wake_time` | String | Time waking up (`HH:MM`) |
| `sleep_score` | Float | Sleep quality rating index (0–100 scale) |
| `stress_score` | Float | Estimated physiological stress score (1.0–10.0 scale) |
| `water_liters` | Float | Daily fluid intake in liters |
| `weight_kg` | Float | Body weight logged in kilograms |
| `mood_1to5` | Integer | Self-reported mood rating (1 to 5 scale) |

# 6. Dashboard Modules & Features
# 1. Header & Dynamic Navigation
* Dynamic Header Banner: Automatically updates to reflect the active date range bounds (`Jan 01, 2025 – Dec 31, 2025`) and current filtered log counts.
* Collapsible Sidebar: Navigation menu, custom CSV dataset uploader, date range filtering slider, and collapsible Personal Health Profile.

# 2. Personal Health Profile Management
* Displays user details: Full Name (*Emily Park*), Age, Height (cm), Weight (kg), and Blood Group.
* Automatically computes Body Mass Index (BMI) and provides weight category classifications.
* Persistent editing via an interactive form that updates `user_profile.json`.

# 3. Overview Module
* KPI Cards: Top 4 executive metric cards for Average Daily Steps, Average Calories Burned, Average Sleep Duration, and Average Heart Rate.
* Integrated Charts: Daily Steps Line Chart, 7-Day Rolling Sleep Score vs. HRV Recovery Trajectory, Exercise Category Bar Chart, and Stress vs. Water Intake Trends.

# 4. Physical Activity Module
* Smooth line chart for steps progression with 10k target markers.
* Distance vs. Calories Burned scatter plot with color-coded exercise duration.
* Daily distance covered histogram and Exercise Type distribution Donut Chart.

# 5. Sleep Analysis Module
* Dual-line trend chart comparing Sleep Hours against Deep Sleep %.
* Histogram distribution of Sleep Quality Scores.
* Average sleep KPI cards.

# 6. Heart Health Module
* Combined line chart for Average Heart Rate vs. Resting Heart Rate.
* Filled area chart for Heart Rate Variability (`hrv_ms`) trends.

# 7. Mental Wellness Module
* Donut chart illustrating daily self-reported Mood distribution (1 to 5 scale).
* Daily Stress Score line chart.
* Mood vs. Stress scatter plot colored by Sleep Quality Score.

# 8. Lifestyle Module
* Bar chart tracking daily fluid intake against a 3.0 Liters target line.
* Interactive Plotly gauge chart displaying average hydration progress.
* Weight progression line chart.

# 9. System Settings & Customization
* Theme Switcher: Live switching across 4 color palettes (*Sage Green & White*, *Ocean Teal*, *Lavender & White*, *Dark Forest Green*).
* Reset & Restore Controls: One-click confirmation buttons to reset themes, health profile data, preferences, or date filters.

# 7. Project Folder Structure
Wellness_Dashboard/
│
├── app.py
│   # Main Streamlit application script
│
├── PJ2_Emily_Park_wellness_2025.csv
│   # Primary health telemetry dataset
│
├── requirements.txt
│   # Python dependencies file
│
├── README.md
│   # Project documentation
│
├── user_profile.json
│   # Local storage for user profile data (auto-generated)
│
├── user_prefs.json
│   # Local storage for UI preferences (auto-generated)
│
├── prompt_logs/
│   # Development and AI prompt logs
│
└── outputs/
    # Saved visual charts and generated reports

# 8. Expected Output
* When successfully launched, the application displays:
* An executive green header displaying user welcome greetings and dynamic dataset date ranges.
* A sidebar featuring a collapsible health profile manager, dataset uploader, date filter controls, and navigation tabs.
* High-contrast KPI cards showcasing calculated metric averages.
* Interactive, hoverable Plotly charts across all 6 specialized wellness modules.
* Instant visual theme updating when changed from the Settings module.

# 9. Future Scope
* Machine Learning Predictive Analytics: Integrate predictive models to forecast future sleep quality or recommend rest days based on HRV recovery trends.
* Real-time API Integration: Connect to commercial smartwatch APIs (e.g., Apple HealthKit, Fitbit API, Garmin Connect) for real-time live data syncing.
* Multi-User Authentication: Implement secure login functionality with database integration (e.g., SQLite or PostgreSQL) to manage multiple user profiles.
* Automated PDF Health Report Generation: Allow users to export weekly or monthly summarized health PDF reports directly from the dashboard.
  
# Note:
# Install dependencies
pip install -r requirements.txt
# Run Streamlit dashboard
streamlit run app.py
