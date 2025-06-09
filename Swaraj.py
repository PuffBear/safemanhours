import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, time as dt_time
import time

# ----------------- Streamlit Config -----------------
st.set_page_config(page_title="Safety Dashboard", layout="wide")
st.markdown("""
<div style="background-color:#0f4c75;padding:10px;border-radius:10px">
    <h2 style="color:white;text-align:center;">Safety Dashboard – Daily Swaraj P3 </h2>
</div>
""", unsafe_allow_html=True)

# ----------------- Columns Setup -----------------
left, right = st.columns([1, 1.5])

# ----------------- LEFT COLUMN -----------------
with left:
    st.subheader("Live Safe Manhours Counter")

    # Input Fields
    manpower = st.number_input("Enter No. of Workers", min_value=1, value=400)
    shift_hours = 8.5
    total_shift_seconds = int(shift_hours * 60 * 60)  # 30600 seconds

    # Shift Timing
    shift_start = dt_time(8, 30)
    shift_end = dt_time(17, 0)
    now = datetime.now().time()

    # Time Passed Since Shift Start
    if shift_start <= now <= shift_end:
        seconds_passed = (
            datetime.combine(datetime.today(), now) -
            datetime.combine(datetime.today(), shift_start)
        ).total_seconds()

        # Safe manhours so far
        per_second_rate = manpower / total_shift_seconds
        live_manhours = int(seconds_passed * per_second_rate)

        # Live Counter with st.empty()
        placeholder = st.empty()
        for i in range(live_manhours, live_manhours + 1000):
            placeholder.metric("Total Safe Manhours", f"{i:,}")
            time.sleep(1)
    else:
        st.warning("Outside shift hours (8:30 AM - 5:00 PM)")
        st.metric("Total Safe Manhours", "0 hrs")

    # Shift Time Display
    st.markdown(" **Shift Time:** 8:30 AM to 5:00 PM")

    # Calendar Section
    st.subheader("Monthly Safety Calendar")
    st.caption("Green = Accident-Free Days")

    # Static calendar example (update dynamically later)
    calendar = [
        ["", "", "1", "2", "3", "4", "5"],
        ["6", "7", "8", "9", "10", "11", "12"],
        ["13", "14", "15", "16", "17", "18", "19"],
        ["20", "21", "22", "23", "24", "25", "26"],
        ["27", "28", "29", "30", "", "", ""],
    ]
    accident_free = {"1", "2", "3", "4", "5"}

    st.markdown("<div style='font-family:monospace'>", unsafe_allow_html=True)
    for week in calendar:
        row = ""
        for day in week:
            if day == "":
                row += "    "
            elif day in accident_free:
                row += f":green[{day: >2}] "
            else:
                row += f"{day: >2}  "
        st.markdown(row)
    st.markdown("</div>", unsafe_allow_html=True)

# ----------------- RIGHT COLUMN -----------------
with right:
    st.subheader("Safety Pyramid Overview")

    # Incident Data
    labels = ["Fatal", "Major Accident", "FAC/NRA", "Near Miss", "UA/UC"]
    values = [0, 0, 1, 21, 272]
    colors = ["#ff4d4d", "#ffa500", "#00cc66", "#00ccff", "#4d4dff"]

    # Funnel Chart
    fig = go.Funnel(
        y=labels[::-1],
        x=values[::-1],
        textinfo="value+percent previous",
        marker=dict(color=colors[::-1])
    )
    st.plotly_chart(fig, use_container_width=True)

    # Incident Breakdown
    st.subheader(" Incident Summary")
    st.markdown("""
    - 🟥 **Fatal**: 0  
    - 🟧 **Major Accident**: 0  
    - 🟩 **FAC/NRA**: 1  
    - 🟦 **Near Miss**: 21  
    - 🟪 **UA/UC**: 272  
    """)

    # Zero Incident Banner
    st.success("🎯 **Zero Incident Achieved!**")

from datetime import datetime, time as dt_time, timedelta
import pytz

st.subheader("Live Safe Manhours Counter")

# --- Constants ---
manpower = st.number_input("Enter No. of Workers", min_value=1, value=400)
shift_hours = 8.5
total_shift_seconds = int(shift_hours * 60 * 60)  # 30600 seconds

# --- Get current IST time ---
IST = pytz.timezone("Asia/Kolkata")
now_ist = datetime.now(IST).time()

shift_start = dt_time(8, 30)
shift_end = dt_time(17, 0)

if shift_start <= now_ist <= shift_end:
    # Calculate seconds passed since 8:30 AM IST
    today = datetime.now(IST).date()
    start_datetime = IST.localize(datetime.combine(today, shift_start))
    now_datetime = datetime.now(IST)
    seconds_passed = (now_datetime - start_datetime).total_seconds()

    # Safe manhours counter logic
    per_second_rate = manpower / total_shift_seconds
    live_manhours = int(seconds_passed * per_second_rate)

    ph = st.empty()
    for i in range(live_manhours, live_manhours + 1000):
        ph.metric("Total Safe Manhours", f"{i:,} hrs")
        time.sleep(1)
else:
    st.warning("Off-shift (Counter runs between 8:30 AM and 5:00 PM IST)")
    st.metric("Total Safe Manhours", "0 hrs")