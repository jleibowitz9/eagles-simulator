from simulator import run_simulation
from simulator import eagles_results as CORE_RESULTS
from simulator import weight as DEFAULT_WEIGHT
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
    default_prob_pct = int(round(DEFAULT_WEIGHT.get(i, 0.5) * 100.0))

    prob_key = f"prob-{i}"
    reset_flag_key = f"prob-reset-{i}"
    # If a reset was requested in the previous interaction, apply it now before creating the widget
    if st.session_state.get(reset_flag_key):
        st.session_state[prob_key] = int(default_prob_pct)
        st.session_state[reset_flag_key] = False

    col1, col2 = st.columns([3, 1])
    with col1:
        # Backend “actual” result for this week
        actual = CORE_RESULTS[i]
        locked = actual in ("W", "L")
        # Determine initial dropdown value
        default = actual if locked else "Undecided"
        result = st.selectbox(
            f"Week {i+1} {OPPONENTS[i]}",
            ["Undecided", "W", "L"],
            index=["Undecided", "W", "L"].index(default),
            key=f"result-{i}",
            disabled=locked
        )
    with col2:
        # If backend has an actual result or the user picked W/L, lock field and set 100/0
        frontend_locked = (result != "Undecided")
        if locked or frontend_locked:
            display_val = 100.0 if result == "W" else 0.0
            sub1, sub2 = st.columns([4, 1], gap="small")
            with sub1:
                st.number_input(
                    "",
                    min_value=0,
                    max_value=100,
                    value=int(display_val),
                    step=1,
                    format="%d",
                    disabled=True,
                    key=f"locked-prob-{i}"
                )
            # Do not show reset button in locked state
            current_prob = display_val / 100.0
        else:
            # Editable when undecided by both backend and user
            sub1, sub2 = st.columns([4, 1], gap="small")
            with sub1:
                current_val = st.session_state.get(prob_key, default_prob_pct)
                st.number_input(
                    "",
                    min_value=0,
                    max_value=100,
                    value=int(current_val),
                    step=1,
                    format="%d",
                    key=prob_key
                )
            with sub2:
                # Only show reset if user has overridden the default value
                current_val = st.session_state.get(prob_key, default_prob_pct)
                if current_val != default_prob_pct:
                    # Small top padding to visually center-align the button with the input
                    st.markdown("<div style='padding-top:14px'></div>", unsafe_allow_html=True)
                    if st.button("↺", help=f"Reset to default ({default_prob_pct}%)", key=f"reset-{i}"):
                        st.session_state[reset_flag_key] = True
                        st.rerun()
            current_prob = st.session_state.get(prob_key, default_prob_pct) / 100.0

    eagles_results.append(actual if locked else (result if result != "Undecided" else "A"))
    odds.append(current_prob)

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