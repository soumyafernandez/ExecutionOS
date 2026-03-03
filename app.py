import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Execution OS", layout="wide")

DATA_PATH = "data/logs.csv"

# Ensure data folder exists
os.makedirs("data", exist_ok=True)

# Create file if not exists
if not os.path.exists(DATA_PATH):
    df = pd.DataFrame(columns=[
        "date", "planned_tasks", "completed_tasks",
        "deep_work_hours", "distraction_hours", "energy_level"
    ])
    df.to_csv(DATA_PATH, index=False)

# Sidebar
st.sidebar.title("Execution OS")
page = st.sidebar.radio("Navigate", ["Dashboard", "Daily Log"])

st.title("🔥 Execution OS")

# ===========================
# DASHBOARD
# ===========================
if page == "Dashboard":
    st.header("Dashboard")
    df = pd.read_csv(DATA_PATH)
    st.write("Total Entries:", len(df))
    st.dataframe(df)

# ===========================
# DAILY LOG
# ===========================
elif page == "Daily Log":
    st.header("Daily Log Entry")

    with st.form("log_form"):
        planned = st.number_input("Planned Tasks", min_value=0)
        completed = st.number_input("Completed Tasks", min_value=0)
        deep_work = st.number_input("Deep Work Hours", min_value=0.0)
        distraction = st.number_input("Distraction Hours", min_value=0.0)
        energy = st.slider("Energy Level", 1, 10)

        submitted = st.form_submit_button("Save Entry")

        if submitted:
            new_entry = {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "planned_tasks": planned,
                "completed_tasks": completed,
                "deep_work_hours": deep_work,
                "distraction_hours": distraction,
                "energy_level": energy
            }

            df = pd.read_csv(DATA_PATH)
            df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
            df.to_csv(DATA_PATH, index=False)

            st.success("Entry Saved Successfully ✅")