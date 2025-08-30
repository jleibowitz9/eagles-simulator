# app.py — plain Streamlit simulator (no custom component)

import math
import streamlit as st
import simulator as sim  # your simulator.py

st.set_page_config(page_title="Eagles Season Simulator", page_icon="🦅", layout="centered")
st.title("🦅 Eagles Season Simulator")

# --- Labels/opponents for UI --------------------------------------------------
OPP = [
    "Week 1 vs. Cowboys",
    "Week 2 @ Chiefs",
    "Week 3 vs. Rams",
    "Week 4 @ Buccaneers",
    "Week 5 vs. Broncos",
    "Week 6 @ Giants",
    "Week 7 @ Vikings",
    "Week 8 vs. Giants",
    "Week 10 @ Packers",
    "Week 11 vs. Lions",
    "Week 12 @ Cowboys",
    "Week 13 vs. Bears",
    "Week 14 vs. Chargers",
    "Week 15 @ Raiders",
    "Week 16 vs. Commanders",
    "Week 17 @ Bills",
    "Week 18 vs. Commanders",
]
NUM_WEEKS = len(sim.eagles_results)

# Defaults from simulator.py
DEFAULT_RESULTS = sim.eagles_results[:]                       # list of 'A','W','L'
DEFAULT_PROBS   = {i: int(round(sim.weight.get(i, 0.5) * 100)) for i in range(NUM_WEEKS)}

# --- Session state init -------------------------------------------------------
def _init_state():
    for i in range(NUM_WEEKS):
        # Map backend 'A'->'TBD' for UI
        if f"res_{i}" not in st.session_state:
            st.session_state[f"res_{i}"] = "TBD" if DEFAULT_RESULTS[i] == "A" else DEFAULT_RESULTS[i]
        if f"prob_{i}" not in st.session_state:
            st.session_state[f"prob_{i}"] = DEFAULT_PROBS[i]
        if f"user_overrode_{i}" not in st.session_state:
            st.session_state[f"user_overrode_{i}"] = False

_init_state()

st.subheader("📅 Game Outcomes & Odds")

# --- Per-week controls --------------------------------------------------------
for i in range(NUM_WEEKS):
    label = OPP[i] if i < len(OPP) else f"Week {i+1}"
    backend = DEFAULT_RESULTS[i]                     # 'A' or 'W'/'L' from simulator.py
    locked = backend in {"W", "L"}                   # lock if game decided in backend

    # Layout: selector | percent | tiny reset
    c_sel, c_pct, c_reset = st.columns([5, 1.6, 0.7])

    # Decide whether the percent input is editable
    if locked:
        # Force frontend to reflect backend truth
        ui_res = backend
        ui_prob = 100 if backend == "W" else 0
        st.session_state[f"res_{i}"]  = ui_res
        st.session_state[f"prob_{i}"] = ui_prob
        c_sel.selectbox(label, options=["W", "L"], index=0 if ui_res == "W" else 1, disabled=True, key=f"sel_locked_{i}")
        c_pct.number_input("", min_value=0, max_value=100, value=ui_prob, step=1, disabled=True, key=f"pct_locked_{i}")
        c_reset.write("")  # spacer
        continue

    # Not locked — user can choose TBD/W/L
    current = st.session_state[f"res_{i}"]
    current_idx = {"TBD": 0, "W": 1, "L": 2}[current]
    choice = c_sel.selectbox(label, ["TBD", "W", "L"], index=current_idx, key=f"sel_{i}")

    # If W/L chosen, force prob to 100/0 and disable input
    if choice == "W":
        st.session_state[f"res_{i}"] = "W"
        st.session_state[f"prob_{i}"] = 100
        c_pct.number_input("", min_value=0, max_value=100, value=100, step=1, disabled=True, key=f"pct_{i}")
        c_reset.write("")  # no reset needed
        st.session_state[f"user_overrode_{i}"] = False

    elif choice == "L":
        st.session_state[f"res_{i}"] = "L"
        st.session_state[f"prob_{i}"] = 0
        c_pct.number_input("", min_value=0, max_value=100, value=0, step=1, disabled=True, key=f"pct_{i}")
        c_reset.write("")
        st.session_state[f"user_overrode_{i}"] = False

    else:
        # TBD — user may edit probability (defaults to ESPN %)
        st.session_state[f"res_{i}"] = "TBD"
        val = c_pct.number_input("", min_value=0, max_value=100,
                                 value=st.session_state[f"prob_{i}"], step=1, key=f"pct_{i}")
        # Track override vs default
        st.session_state[f"user_overrode_{i}"] = (val != DEFAULT_PROBS[i])

        # Show tiny reset button only if overridden
        if st.session_state[f"user_overrode_{i}"]:
            if c_reset.button("↺", key=f"reset_{i}", help="Reset to default (ESPN)"):
                st.session_state[f"prob_{i}"] = DEFAULT_PROBS[i]
                st.session_state[f"user_overrode_{i}"] = False
                st.rerun()
        else:
            c_reset.write("")

st.divider()

# --- Run simulation -----------------------------------------------------------
def build_inputs():
    # Convert UI state back to simulator’s expectations:
    # 'TBD' -> 'A', 'W' -> 'W', 'L' -> 'L'
    res_list = []
    for i in range(NUM_WEEKS):
        r = st.session_state[f"res_{i}"]
        res_list.append("A" if r == "TBD" else r)
    # Weights 0..1 from percent
    w = {i: st.session_state[f"prob_{i}"] / 100.0 for i in range(NUM_WEEKS)}
    return res_list, w

left, right = st.columns([1, 3])
with left:
    run = st.button("Run Simulation", type="primary")
with right:
    st.caption("Uses current selections. Weeks decided in the backend are locked.")

if run:
    eagles_results_input, weight_input = build_inputs()
    out = sim.run_simulation(eagles_results_input, weight_input)

    st.subheader("📊 Weighted Win Chances")
    names = list(sim.picks_dict.keys())
    weighted = out["weighted"]
    straight = out["straight"]

    # Sort by weighted percent desc
    rows = sorted(zip(names, weighted, straight), key=lambda x: x[1], reverse=True)
    for name, w_pct, s_pct in rows:
        st.write(f"**{name}** — Weighted: **{w_pct:.1f}%**, Straight: {s_pct:.1f}%")