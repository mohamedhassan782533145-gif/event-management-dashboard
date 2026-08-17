import random
from datetime import datetime, timedelta

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ------------------------------------------------------------------------------------------------------------------

st.set_page_config(
    page_title="Event Management Dashboard",
    page_icon="📊",
    layout="wide"
)


# -----------------------------------------------------------------------------------------------------------------

st.markdown("""
<style>

.stApp {
    background-color: #050914;
}

.block-container {
    max-width: 1500px;
    padding-top: 20px;
    padding-bottom: 30px;
}

.dashboard-title {
    font-size: 34px;
    font-weight: 800;
    margin-bottom: 0;
}

.dashboard-subtitle {
    color: #9aa8bb;
    font-size: 15px;
    margin-bottom: 20px;
}

.kpi-card {
    background: linear-gradient(
        145deg,
        #0d1728,
        #09111f
    );

    border: 1px solid #223450;

    border-radius: 14px;

    padding: 15px;

    min-height: 105px;
}

.kpi-label {
    color: #94a5bb;
    font-size: 13px;
}

.kpi-value {
    font-size: 24px;
    font-weight: 800;

    margin-top: 7px;
}

.section-title {
    font-size: 20px;
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------------------------------------------
@st.cache_data
def create_data():

    random.seed(42)

    cities = [
        "Cairo",
        "Alexandria",
        "Giza",
        "Luxor",
        "Aswan",
        "Mansoura"
    ]

    event_types = [
        "Conference",
        "Workshop",
        "Wedding",
        "Exhibition",
        "Festival",
        "Corporate"
    ]

    organizers = [
        "Nile Events",
        "Skyline Group",
        "Prime Events",
        "Vision Hub",
        "Elite Planners",
        "Creative Minds"
    ]

    venues = [
        "Grand Hall",
        "Nile Ballroom",
        "Sky Center",
        "Expo Arena",
        "Royal Garden",
        "Downtown Hub"
    ]

    start_date = datetime(2025, 1, 1)

    rows = []

    for event_id in range(1, 385):

        event_date = (
            start_date
            + timedelta(days=random.randint(0, 364))
        )

        city = random.choice(cities)

        event_type = random.choice(event_types)

        organizer = random.choice(organizers)

        venue = random.choice(venues)

        capacity = random.randint(
            120,
            900
        )

        attendance = random.randint(
            max(50, int(capacity * 0.45)),
            capacity
        )

        ticket_price = random.randint(
            20,
            180
        )

        revenue = (
            attendance * ticket_price
            + random.randint(500, 12000)
        )

        costs = int(
            revenue
            * random.uniform(
                0.38,
                0.72
            )
        )

        profit = (
            revenue
            - costs
        )

        rows.append({

            "Event ID": event_id,

            "Date": event_date,

            "Event": f"Event {event_id:03d}",

            "City": city,

            "Event Type": event_type,

            "Organizer": organizer,

            "Venue": venue,

            "Capacity": capacity,

            "Attendance": attendance,

            "Ticket Price": ticket_price,

            "Revenue": revenue,

            "Costs": costs,

            "Profit": profit
        })

    df = pd.DataFrame(rows)

    df["Attendance Rate"] = (
        df["Attendance"]
        / df["Capacity"]
        * 100
    ).round(1)

    df["Profit Margin"] = (
        df["Profit"]
        / df["Revenue"]
        * 100
    ).round(1)

    df["Month"] = (
        df["Date"]
        .dt
        .to_period("M")
        .astype(str)
    )

    return df


df = create_data()


# ------------------------------------------------------------------------------------------------------------------

st.markdown(
    '<div class="dashboard-title">'
    '📊 EVENT MANAGEMENT DASHBOARD'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'Smart insights • Better events • Bigger impact'
    '</div>',
    unsafe_allow_html=True
)


# -------------------------------------------------------------------------------------------------------------------

with st.sidebar:

    st.header("🔎 Quick Filters")

    selected_city = st.multiselect(
        "City",
        sorted(df["City"].unique())
    )

    selected_type = st.multiselect(
        "Event Type",
        sorted(df["Event Type"].unique())
    )

    selected_organizer = st.multiselect(
        "Organizer",
        sorted(df["Organizer"].unique())
    )

    min_date = df["Date"].min().date()

    max_date = df["Date"].max().date()

    selected_dates = st.date_input(
        "Date Range",
        value=(min_date, max_date)
    )


#-------------------------------------------------------------------------------------------------------------------

filtered_df = df.copy()


if selected_city:

    filtered_df = filtered_df[
        filtered_df["City"].isin(
            selected_city
        )
    ]


if selected_type:

    filtered_df = filtered_df[
        filtered_df["Event Type"].isin(
            selected_type
        )
    ]


if selected_organizer:

    filtered_df = filtered_df[
        filtered_df["Organizer"].isin(
            selected_organizer
        )
    ]


if (
    isinstance(selected_dates, tuple)
    and len(selected_dates) == 2
):

    filtered_df = filtered_df[
        filtered_df["Date"].dt.date.between(
            selected_dates[0],
            selected_dates[1]
        )
    ]


#-------------------------------------------------------------------------------------------------------------------
total_events = len(filtered_df)

total_attendees = int(
    filtered_df["Attendance"].sum()
)

total_revenue = float(
    filtered_df["Revenue"].sum()
)

total_costs = float(
    filtered_df["Costs"].sum()
)

net_profit = float(
    filtered_df["Profit"].sum()
)

average_attendance = (

    filtered_df["Attendance"].mean()

    if total_events > 0

    else 0
)

profit_margin = (

    net_profit
    / total_revenue
    * 100

    if total_revenue > 0

    else 0
)

average_event_revenue = (

    total_revenue
    / total_events

    if total_events > 0

    else 0
)


# --------------------------------------------------------------------------------------------------------------------

kpis = [

    (
        "TOTAL EVENTS",
        f"{total_events:,}"
    ),

    (
        "TOTAL ATTENDEES",
        f"{total_attendees:,}"
    ),

    (
        "TOTAL REVENUE",
        f"${total_revenue:,.0f}"
    ),

    (
        "TOTAL COSTS",
        f"${total_costs:,.0f}"
    ),

    (
        "NET PROFIT",
        f"${net_profit:,.0f}"
    ),

    (
        "AVG ATTENDEES / EVENT",
        f"{average_attendance:,.0f}"
    ),

    (
        "PROFIT MARGIN",
        f"{profit_margin:.1f}%"
    ),

    (
        "AVG REVENUE / EVENT",
        f"${average_event_revenue:,.0f}"
    )
]


kpi_columns = st.columns(8)


for column, (label, value) in zip(
    kpi_columns,
    kpis
):

    column.markdown(
        f"""
        <div class="kpi-card">

            <div class="kpi-label">
                {label}
            </div>

            <div class="kpi-value">
                {value}
            </div>

        </div>
        """,

        unsafe_allow_html=True
    )


st.write("")


# ----------------------------------------------------------------------------------------------------------------

left_column, right_column = st.columns(2)


with left_column:

    st.subheader(
        "📊 Attendance by Event Type"
    )

    chart_data = (

        filtered_df

        .groupby(
            "Event Type",
            as_index=False
        )

        ["Attendance"]

        .sum()

        .sort_values(
            "Attendance",
            ascending=False
        )
    )

    figure = px.bar(
        chart_data,

        x="Event Type",

        y="Attendance",

        text_auto=".2s"
    )

    figure.update_layout(
        height=330,

        margin=dict(
            l=10,
            r=10,
            t=20,
            b=10
        )
    )

    st.plotly_chart(
        figure,
        use_container_width=True
    )


# -----------------------------------------------------------------------------------------------------------------

with right_column:

    st.subheader(
        "📈 Revenue Trend"
    )

    chart_data = (

        filtered_df

        .groupby(
            "Month",
            as_index=False
        )

        ["Revenue"]

        .sum()
    )

    figure = px.line(
        chart_data,

        x="Month",

        y="Revenue",

        markers=True
    )

    figure.update_layout(
        height=330,

        margin=dict(
            l=10,
            r=10,
            t=20,
            b=10
        )
    )

    st.plotly_chart(
        figure,
        use_container_width=True
    )


# ----------------------------------------------------------------------------------------------------------------

left_column, right_column = st.columns(2)


with left_column:

    st.subheader(
        "💰 Profitability by Event Type"
    )

    chart_data = (

        filtered_df

        .groupby(
            "Event Type",
            as_index=False
        )

        [["Revenue", "Costs", "Profit"]]

        .sum()
    )

    figure = px.bar(
        chart_data,

        x="Event Type",

        y=[
            "Revenue",
            "Costs",
            "Profit"
        ],

        barmode="group"
    )

    figure.update_layout(
        height=330,

        margin=dict(
            l=10,
            r=10,
            t=20,
            b=10
        )
    )

    st.plotly_chart(
        figure,
        use_container_width=True
    )


# -------------------------------------------------------------------------------------------------------------------

    st.subheader(
        "🏙️ Revenue by City"
    )

    chart_data = (

        filtered_df

        .groupby(
            "City",
            as_index=False
        )

        ["Revenue"]

        .sum()

        .sort_values(
            "Revenue",
            ascending=False
        )
    )

    figure = px.bar(
        chart_data,

        x="City",

        y="Revenue",

        text_auto=".2s"
    )

    figure.update_layout(
        height=330,

        margin=dict(
            l=10,
            r=10,
            t=20,
            b=10
        )
    )

    st.plotly_chart(
        figure,
        use_container_width=True
    )


#--------------------------------------------------------------------------------------------------------------------

left_column, right_column = st.columns(2)


with left_column:

    st.subheader(
        "🥧 Revenue Share by Organizer"
    )

    chart_data = (

        filtered_df

        .groupby(
            "Organizer",
            as_index=False
        )

        ["Revenue"]

        .sum()
    )

    figure = px.pie(
        chart_data,

        names="Organizer",

        values="Revenue",

        hole=0.48
    )

    figure.update_layout(
        height=330,

        margin=dict(
            l=10,
            r=10,
            t=20,
            b=10
        )
    )

    st.plotly_chart(
        figure,
        use_container_width=True
    )


# ---------------------------------------------------------------------------------------------------------------

with right_column:

    st.subheader(
        "💵 Revenue vs Costs"
    )

    chart_data = (

        filtered_df

        .groupby(
            "Month",
            as_index=False
        )

        [["Revenue", "Costs"]]

        .sum()
    )

    figure = go.Figure()


    figure.add_trace(
        go.Scatter(
            x=chart_data["Month"],

            y=chart_data["Revenue"],

            mode="lines+markers",

            name="Revenue"
        )
    )


    figure.add_trace(
        go.Scatter(
            x=chart_data["Month"],

            y=chart_data["Costs"],

            mode="lines+markers",

            name="Costs"
        )
    )


    figure.update_layout(

        height=330,

        margin=dict(
            l=10,
            r=10,
            t=20,
            b=10
        )
    )

    st.plotly_chart(
        figure,
        use_container_width=True
    )


# -----------------------------------------------------------------------------------------------

st.subheader(
    "🏆 TOP PERFORMING EVENTS"
)


top_events = (

    filtered_df

    .sort_values(
        "Profit",
        ascending=False
    )

    .head(10)

    [
        [
            "Event",
            "Date",
            "City",
            "Event Type",
            "Attendance",
            "Revenue",
            "Costs",
            "Profit",
            "Profit Margin"
        ]
    ]

    .copy()
)


top_events["Date"] = (

    top_events["Date"]

    .dt

    .strftime("%Y-%m-%d")
)


top_events["Revenue"] = (

    top_events["Revenue"]

    .map(
        lambda value:
        f"${value:,.0f}"
    )
)


top_events["Costs"] = (

    top_events["Costs"]

    .map(
        lambda value:
        f"${value:,.0f}"
    )
)


top_events["Profit"] = (

    top_events["Profit"]

    .map(
        lambda value:
        f"${value:,.0f}"
    )
)


top_events["Profit Margin"] = (

    top_events["Profit Margin"]

    .map(
        lambda value:
        f"{value:.1f}%"
    )
)


st.dataframe(
    top_events,

    use_container_width=True,

    hide_index=True
)


# ============================================================
# FOOTER
# ============================================================

st.caption(
    f"Showing {len(filtered_df):,} "
    f"of {len(df):,} total events"
)