from simulator import run_simulation
from simulator import eagles_results as CORE_RESULTS
import streamlit as st

st.markdown(
    """
    <style>
    div.block-container {
      max-width: 400px;
      margin: auto;
      padding: 1rem;
    }
    /* Lighten dropdown menu panels */
    .baseweb-popover-content, 
    div[data-baseweb="select"] ul {
      background-color: #25282c !important;
    }
    /* Force dropdown panel background */
    div[role="listbox"] {
        background-color: #25282c !important;
    }
    /* Force dropdown options background and hover */
    div[role="option"] {
        background-color: #25282c !important;
    }
    div[role="option"]:hover {
        background-color: #2f3237 !important;
    }
    /* Force columns to stay side-by-side, even on narrow screens */
    .stColumns {
        display: flex !important;
        flex-wrap: nowrap !important;
        overflow-x: auto !important;
    }
    /* Ensure each column keeps its width */
    .stColumns > div {
        flex: 0 0 auto !important;
        width: auto !important;
    }
    /* Decrease horizontal gap between dropdown and input */
    div[data-testid="column"] {
        gap: 0.5rem !important;
    }

    /* Increase vertical spacing between each week row */
    div[data-testid="column"] + div[data-testid="column"] {
        margin-top: 1.5rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.set_page_config(page_title="Eagles Season Simulator", layout="wide")
st.title("🦅 Eagles Season Simulator")


NUM_WEEKS = 17

# List of participants matching the order in simulator.py
PARTICIPANTS = [
    'amir', 'andy', 'buhduh', 'emer', 'hanan',
    'jacob', 'jay', 'jen', 'marsha', 'nathan',
    'pop', 'sarah'
]

# List of opponents for each week
OPPONENTS = [
    "vs. Cowboys", "@ Chiefs", "vs. Rams", "@ Buccaneers", "vs. Broncos",
    "@ Giants", "@ Vikings", "vs. Giants", "@ Packers", "vs. Lions",
    "@ Cowboys", "vs. Bears", "@ Chargers", "vs. Raiders", "@ Commanders",
    "@ Bills", "vs. Commanders"
]

st.markdown("### 📅 Game Outcomes & Odds")

eagles_results = []
odds = []
for i in range(NUM_WEEKS):
    col1, col2 = st.columns([3, 1])
    with col1:
        # Backend “actual” result for this week
        actual = CORE_RESULTS[i]
        locked = actual in ("W", "L")
        # Determine initial dropdown value
        default = actual if locked else "?"
        result = st.selectbox(
            f"Week {i+1} {OPPONENTS[i]}",
            ["?", "W", "L"],
            index=["?", "W", "L"].index(default),
            key=f"result-{i}",
            disabled=locked
        )
    with col2:
        # Frontend lock when user picks a result
        frontend_locked = (result != "?")
        if locked or frontend_locked:
            # Either backend or user locked: show 100% for W, 0% for L
            display_val = 100.0 if result == "W" else 0.0
            st.number_input(
                "",
                min_value=0.0,
                max_value=100.0,
                value=display_val,
                disabled=True,
                key=f"locked-prob-{i}"
            )
        else:
            # Editable when undecided by both backend and user
            prob = st.number_input(
                "",
                min_value=0.0,
                max_value=100.0,
                value=50.0,
                key=f"prob-{i}"
            )

    eagles_results.append(actual if locked else (result if result != "?" else "A"))
    if locked or result != "?":
        odds.append(display_val / 100)
    else:
        odds.append(prob / 100)

if st.button("Run Simulation"):
    with st.spinner("Simulating..."):
        weight_dict = {i: odds[i] for i in range(NUM_WEEKS)}
        results = run_simulation(eagles_results, weight_dict)
        st.success("Simulation complete!")
        st.markdown("### 🧮 Weighted Probabilities")
        # Map results back to participant names
        weighted_dict = {PARTICIPANTS[i]: results["weighted"][i] for i in range(len(PARTICIPANTS))}
        straight_dict = {PARTICIPANTS[i]: results["straight"][i] for i in range(len(PARTICIPANTS))}
        st.write(weighted_dict)
        st.markdown("### 📊 Straight Probabilities")
        st.write(straight_dict)