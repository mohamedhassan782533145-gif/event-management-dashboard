import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Event Management Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "events.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH, parse_dates=["event_date"])
    df["attendance_rate"] = (df["attendance"] / df["capacity"] * 100).round(1)
    df["profit_margin"] = (df["profit"] / df["revenue"] * 100).round(1)
    df["month"] = df["event_date"].dt.to_period("M").astype(str)
    return df

df = load_data()

# -------------------------
# Custom CSS
# -------------------------
st.markdown(
    """
    <style>
    .main {background: #050b16;}
    .block-container {padding-top: 1.2rem; padding-bottom: 1.5rem;}
    .dashboard-title {
        font-size: 2rem;
        font-weight: 800;
        margin-bottom: 0.1rem;
    }
    .dashboard-subtitle {
        color: #9ba9bd;
        margin-bottom: 1.0rem;
    }
    .kpi-card {
        border: 1px solid #20324a;
        border-radius: 12px;
        padding: 14px 16px;
        background: linear-gradient(145deg, #0b1524, #0a111c);
        min-height: 105px;
    }
    .kpi-label {color: #9ba9bd; font-size: 0.82rem;}
    .kpi-value {font-size: 1.55rem; font-weight: 800; margin-top: 4px;}
    .section-card {
        background: #0b1524;
        border: 1px solid #20324a;
        border-radius: 12px;
        padding: 12px;
    }
    div[data-testid="stMetric"] {
        background: #0b1524;
        border: 1px solid #20324a;
        border-radius: 12px;
        padding: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="dashboard-title">📊 EVENT MANAGEMENT DASHBOARD</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="dashboard-subtitle">Smart insights, better events, bigger impact</div>',
    unsafe_allow_html=True,
)

# -------------------------
# Filters
# -------------------------
with st.sidebar:
    st.header("🔎 Quick Filters")
    city_filter = st.multiselect("City", sorted(df["city"].unique()))
    type_filter = st.multiselect("Event Type", sorted(df["event_type"].unique()))
    organizer_filter = st.multiselect("Organizer", sorted(df["organizer"].unique()))
    date_range = st.date_input(
        "Date Range",
        value=(df["event_date"].min().date(), df["event_date"].max().date()),
    )

filtered = df.copy()

if city_filter:
    filtered = filtered[filtered["city"].isin(city_filter)]
if type_filter:
    filtered = filtered[filtered["event_type"].isin(type_filter)]
if organizer_filter:
    filtered = filtered[filtered["organizer"].isin(organizer_filter)]

if isinstance(date_range, tuple) and len(date_range) == 2:
    filtered = filtered[
        filtered["event_date"].dt.date.between(date_range[0], date_range[1])
    ]

# -------------------------
# KPI row
# -------------------------
total_events = len(filtered)
total_attendees = int(filtered["attendance"].sum())
total_revenue = filtered["revenue"].sum()
total_costs = filtered["costs"].sum()
net_profit = filtered["profit"].sum()
avg_attendance = filtered["attendance"].mean() if total_events else 0
profit_margin = (net_profit / total_revenue * 100) if total_revenue else 0
avg_event_revenue = (total_revenue / total_events) if total_events else 0

kpis = [
    ("TOTAL EVENTS", f"{total_events:,}"),
    ("TOTAL ATTENDEES", f"{total_attendees:,}"),
    ("TOTAL REVENUE", f"${total_revenue:,.0f}"),
    ("TOTAL COSTS", f"${total_costs:,.0f}"),
    ("NET PROFIT", f"${net_profit:,.0f}"),
    ("AVG ATTENDEES / EVENT", f"{avg_attendance:,.0f}"),
    ("PROFIT MARGIN", f"{profit_margin:.1f}%"),
    ("AVG REVENUE / EVENT", f"${avg_event_revenue:,.0f}"),
]

cols = st.columns(8)
for col, (label, value) in zip(cols, kpis):
    col.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")

# -------------------------
# Charts
# -------------------------
c1, c2 = st.columns(2)

with c1:
    st.subheader("📅 Attendance by Event Type")
    tmp = filtered.groupby("event_type", as_index=False).agg(
        attendance=("attendance", "sum"),
        events=("event_id", "count")
    )
    fig = px.bar(tmp, x="event_type", y="attendance", text_auto=".2s")
    fig.update_layout(margin=dict(l=10, r=10, t=20, b=10), height=330)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("💰 Revenue Trend")
    tmp = filtered.groupby("month", as_index=False)["revenue"].sum()
    fig = px.line(tmp, x="month", y="revenue", markers=True)
    fig.update_layout(margin=dict(l=10, r=10, t=20, b=10), height=330)
    st.plotly_chart(fig, use_container_width=True)

c3, c4 = st.columns(2)

with c3:
    st.subheader("📊 Profitability by Event Type")
    tmp = filtered.groupby("event_type", as_index=False).agg(
        revenue=("revenue", "sum"),
        costs=("costs", "sum"),
        profit=("profit", "sum"),
    )
    fig = px.bar(tmp, x="event_type", y=["revenue", "costs", "profit"], barmode="group")
    fig.update_layout(margin=dict(l=10, r=10, t=20, b=10), height=330)
    st.plotly_chart(fig, use_container_width=True)

with c4:
    st.subheader("🏙️ Revenue by City")
    tmp = filtered.groupby("city", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False)
    fig = px.bar(tmp, x="city", y="revenue", text_auto=".2s")
    fig.update_layout(margin=dict(l=10, r=10, t=20, b=10), height=330)
    st.plotly_chart(fig, use_container_width=True)

c5, c6 = st.columns(2)

with c5:
    st.subheader("🎯 Revenue Share by Organizer")
    tmp = filtered.groupby("organizer", as_index=False)["revenue"].sum()
    fig = px.pie(tmp, names="organizer", values="revenue", hole=0.48)
    fig.update_layout(margin=dict(l=10, r=10, t=20, b=10), height=330)
    st.plotly_chart(fig, use_container_width=True)

with c6:
    st.subheader("💵 Revenue vs Event Cost")
    tmp = filtered.groupby("month", as_index=False).agg(
        revenue=("revenue", "sum"),
        costs=("costs", "sum"),
    )
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=tmp["month"], y=tmp["revenue"], mode="lines+markers", name="Revenue"))
    fig.add_trace(go.Scatter(x=tmp["month"], y=tmp["costs"], mode="lines+markers", name="Costs"))
    fig.update_layout(margin=dict(l=10, r=10, t=20, b=10), height=330)
    st.plotly_chart(fig, use_container_width=True)

# -------------------------
# Top events table
# -------------------------
st.subheader("🏆 Top Performing Events")

top_events = (
    filtered.sort_values("profit", ascending=False)
    .head(10)[
        ["event_name", "event_date", "city", "event_type",
         "attendance", "revenue", "costs", "profit", "profit_margin"]
    ]
    .copy()
)

top_events["event_date"] = top_events["event_date"].dt.strftime("%Y-%m-%d")
top_events["revenue"] = top_events["revenue"].map(lambda x: f"${x:,.0f}")
top_events["costs"] = top_events["costs"].map(lambda x: f"${x:,.0f}")
top_events["profit"] = top_events["profit"].map(lambda x: f"${x:,.0f}")
top_events["profit_margin"] = top_events["profit_margin"].map(lambda x: f"{x:.1f}%")

st.dataframe(top_events, use_container_width=True, hide_index=True)

st.caption(
    "Data-driven decisions for successful event management • "
    f"Showing {len(filtered):,} of {len(df):,} events"
)
