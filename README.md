# Event Management Dashboard — Python

A professional, interactive Event Management Dashboard built with Python, Pandas, Plotly, and Streamlit.

## Features

- KPI cards for events, attendees, revenue, costs, profit, attendance, and margin
- Interactive filters for City, Event Type, Organizer, and Date Range
- Attendance analysis by event type
- Revenue trend over time
- Revenue, cost, and profit comparison
- Revenue comparison by city
- Revenue share by organizer
- Top-performing events table

## Project Structure

```text
event_management_dashboard_python/
├── data/
│   └── events.csv
├── dashboard/
│   └── app.py
├── src/
│   ├── data_cleaning.py
│   └── metrics.py
├── .streamlit/
│   └── config.toml
├── requirements.txt
└── README.md
```

## Run the Project

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Install packages:

```bash
pip install -r requirements.txt
```

Run dashboard:

```bash
streamlit run dashboard/app.py
```

Then open the local Streamlit address shown in the terminal.

## Next Upgrade Ideas

1. Connect a real database.
2. Add monthly/yearly comparison.
3. Add event ROI.
4. Add customer segmentation.
5. Add export buttons for CSV/Excel.
6. Add authentication and deployment.
