import streamlit as st
import pandas as pd
import plotly.express as px

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Intern Dashboard", layout="wide")

# ================= DARK THEME =================
st.markdown("""
<style>
body {
    background-color: #0E1117;
    color: white;
}
.kpi-card {
    background: #1C1F26;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.5);
}
.section {
    background: #1C1F26;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# ================= LOAD DATA =================
data = pd.read_csv(r"C:\Users\ELCOT\OneDrive\Desktop\streamlit\Intern_Performance_Data.csv")

# ================= PREPROCESS =================
data["Hire_Date"] = pd.to_datetime(data["Hire_Date"])
data["Year"] = data["Hire_Date"].dt.year

# ================= FILTERS =================
st.sidebar.title("🔍 Filters")

dept = st.sidebar.selectbox("Department", ["All"] + list(data["Department"].unique()))
gender = st.sidebar.selectbox("Gender", ["All"] + list(data["Gender"].unique()))

filtered = data.copy()

if dept != "All":
    filtered = filtered[filtered["Department"] == dept]

if gender != "All":
    filtered = filtered[filtered["Gender"] == gender]

# ================= DOWNLOAD BUTTON =================

csv = filtered.to_csv(index=False).encode('utf-8')

st.sidebar.download_button(
    label="📥 Download Filtered Data",
    data=csv,
    file_name="intern_performance_filtered.csv",
    mime="text/csv"
)

# ================= TITLE =================
st.title("📊 Intern Performance Dashboard")

# ================= KPIs =================
total = filtered.shape[0]
avg_perf = filtered["Performance_Score"].mean()
avg_sat = filtered["Intern_Satisfaction_Score"].mean()
attrition = (filtered["Resigned"].sum() / total) * 100 if total > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("👤 Total Interns", total)
col2.metric("📈 Avg Performance", round(avg_perf,2))
col3.metric("😊 Satisfaction", round(avg_sat,2))
col4.metric("⚠️ Attrition %", round(attrition,2))

st.markdown("---")

# ================= CHARTS =================
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Department Performance")
    fig1 = px.bar(filtered.groupby("Department")["Performance_Score"].mean().reset_index(),
                  x="Department", y="Performance_Score", color="Performance_Score")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.subheader("🥧 Attrition Distribution")

    fig2 = px.pie(
        filtered,
        names="Resigned",
        color="Resigned",
        color_discrete_map={
            True: "red",     # 🔴 Resigned = RED
            False: "green"   # 🟢 Not resigned = GREEN
        }
    )

    fig2.update_layout(template="plotly_dark")

    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ================= SECOND ROW =================
col3, col4 = st.columns(2)

# 🔹 Work Hours vs Performance (INTERACTIVE FIXED)
# 🔹 Work Hours vs Performance (Clean - No Legend)
with col3:
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.subheader("📍 Work Hours vs Performance")

    fig3 = px.scatter(
        filtered,
        x="Work_Hours_Per_Week",
        y="Performance_Score",
        color="Performance_Score",   # ✅ color by performance instead
        size="Performance_Score",
        hover_data=["Employee_ID"],
        color_continuous_scale="viridis"
    )

    fig3.update_layout(
        template="plotly_dark",
        title_x=0.25,
        showlegend=False   # ❌ removes department list
    )

    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
with col4:
    st.subheader("📈 Hiring Trend")
    trend = filtered.groupby("Year").size().reset_index(name="Hires")
    fig4 = px.line(trend, x="Year", y="Hires", markers=True)
    fig4.update_traces(fill='tozeroy')
    st.plotly_chart(fig4, use_container_width=True)

# ================= AI INSIGHTS =================
st.markdown("---")
st.subheader("🤖 AI Insights Summary")

insight1 = f"Average performance score is {avg_perf:.2f}"
insight2 = f"Attrition rate is {attrition:.2f}%"
insight3 = f"Top department performance: {filtered.groupby('Department')['Performance_Score'].mean().idxmax()}"

st.write("•", insight1)
st.write("•", insight2)
st.write("•", insight3)

# ================= LEADERBOARD =================
st.markdown("---")
st.subheader("🏆 Top Intern Leaderboard")

top_interns = filtered.sort_values(by="Performance_Score", ascending=False).head(10)

st.dataframe(top_interns[["Employee_ID", "Department", "Performance_Score"]])

# ================= FOOTER =================
st.markdown("---")
st.markdown("🚀 Final Professional Dashboard with AI Insights")