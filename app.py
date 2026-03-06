import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
from datetime import datetime

def calculate_execution_score(row):
    planned = row["planned_tasks"]
    completed = row["completed_tasks"]
    deep_work = row["deep_work_hours"]
    distraction = row["distraction_hours"]
    energy = row["energy_level"]

    # Avoid division by zero
    completion = completed / planned if planned > 0 else 0
    total_time = deep_work + distraction
    focus = deep_work / total_time if total_time > 0 else 0
    energy_factor = energy / 10

    score = (
        completion * 0.5 +
        focus * 0.3 +
        energy_factor * 0.2
    ) * 100

    return round(score, 2)

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

    if len(df) == 0:
        st.info("No data yet. Start logging your days.")
    else:
        df["execution_score"] = df.apply(calculate_execution_score, axis=1)

        latest_score = df.iloc[-1]["execution_score"]

        st.metric("🔥 Today's Execution Score", f"{latest_score}/100")
        
        weekly_avg = df["execution_score"].tail(7).mean()
        st.metric("📊 Weekly Average Score", round(weekly_avg,2))
        
        # Streak counter 
        streak = 0
        for score in reversed(df["execution_score"]):
            if score >= 70:
                streak += 1
            else:
                break

        st.metric("🔥 High Performance Streak", streak)
        
        # Best day
        best_day = df.loc[df["execution_score"].idxmax()]

        st.write("🏆 Best Day:", best_day["date"])
        st.write("Best Score:", best_day["execution_score"])
        
        # Insight message 
        if latest_score >= 80:
            st.success("Excellent execution today 🚀")

        elif latest_score >= 60:
            st.info("Solid progress. Push a bit harder tomorrow.")

        else:
            st.warning("Execution was weak today. Reduce distractions.")
        
        st.subheader("All Entries")
        st.dataframe(df)

        # Deep work vs distraction
        st.subheader("Deep Work vs Distraction")

        fig, ax = plt.subplots()
        ax.plot(df["deep_work_hours"], label="Deep Work")
        ax.plot(df["distraction_hours"], label="Distraction")
        ax.legend()
        st.pyplot(fig)

        # Task completion
        st.subheader("Task Completion Trend")

        fig2, ax2 = plt.subplots()
        ax2.plot(df["planned_tasks"], label="Planned Tasks")
        ax2.plot(df["completed_tasks"], label="Completed Tasks")
        ax2.legend()
        st.pyplot(fig2)

        # Score over time
        st.subheader("Execution Score Over Time")

        df["date"] = pd.to_datetime(df["date"])

        fig3, ax3 = plt.subplots()
        ax3.plot(df["date"], df["execution_score"])
        st.pyplot(fig3)

        st.subheader("Score Trend")
        st.line_chart(df["execution_score"])

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
            
