import streamlit as st

# Import the simulation API and the live core data from simulator.py
from simulator import run_simulation, eagles_results as CORE_RESULTS, weight as CORE_WEIGHT, picks_dict

st.set_page_config(page_title="Eagles Season Simulator", layout="wide")
st.title("🦅 Eagles Season Simulator")

NUM_WEEKS = len(CORE_RESULTS)

# Session state for UI values (results & probabilities in 0–100 range)
if "ui_results" not in st.session_state:
    st.session_state.ui_results = [
        ("TBD" if r == "A" else r) for r in CORE_RESULTS
    ]
if "ui_probs" not in st.session_state:
    # CORE_WEIGHT is a dict {week_index: probability as 0–1}
    st.session_state.ui_probs = [round(CORE_WEIGHT[i] * 100) for i in range(NUM_WEEKS)]

st.subheader("📅 Game Outcomes & Odds")

# Build the inputs for each week
for i in range(NUM_WEEKS):
    locked_actual = CORE_RESULTS[i] in ("W", "L")  # lock when season result is known

    # If locked by actual result, force the UI values accordingly
    if locked_actual:
        st.session_state.ui_results[i] = CORE_RESULTS[i]
        st.session_state.ui_probs[i] = 100 if CORE_RESULTS[i] == "W" else 0

    # One row per week
    c1, c2 = st.columns([4, 1])

    with c1:
        st.session_state.ui_results[i] = st.selectbox(
            f"Week {i+1}",
            options=["TBD", "W", "L"],
            index=["TBD", "W", "L"].index(st.session_state.ui_results[i]),
            key=f"result_{i}",
            disabled=locked_actual,
        )

    with c2:
        # If the user selects W/L, force probability to 100/0 and disable the input
        sel = st.session_state.ui_results[i]
        if sel == "W":
            st.session_state.ui_probs[i] = 100
        elif sel == "L":
            st.session_state.ui_probs[i] = 0

        st.number_input(
            label=" ",
            min_value=0,
            max_value=100,
            step=1,
            value=int(st.session_state.ui_probs[i]),
            key=f"prob_{i}",
            disabled=locked_actual or sel in ("W", "L"),
            help="Eagles % chance to win this game",
        )

# Prepare inputs for the simulator
ui_results_final = [
    ("A" if r == "TBD" else r) for r in st.session_state.ui_results
]
ui_weight_final = {i: st.session_state.ui_probs[i] / 100 for i in range(NUM_WEEKS)}

# Run button
run = st.button("Run Simulation")

if run:
    try:
        out = run_simulation(ui_results_final, ui_weight_final)
        st.markdown("---")
        st.header("📊 Weighted Win Chances")

        # Display as two columns: competitor name and percentages
        names = list(picks_dict.keys())
        weighted = out["weighted"]
        straight = out["straight"]
        rows = []
        for name, w, s in zip(names, weighted, straight):
            rows.append({"Competitor": name, "Weighted %": w, "Straight %": s})
        st.dataframe(rows, hide_index=True, use_container_width=True)
    except Exception as e:
        st.error(f"Simulation error: {e}")

st.caption("Tip: Weeks with a finalized result in simulator.py are locked in this UI.")