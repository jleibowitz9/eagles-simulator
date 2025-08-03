import streamlit as st
from simulator import run_simulation  # <- your existing algorithm logic

st.set_page_config(page_title="Eagles Season Simulator", layout="wide")
st.title("🦅 Eagles Season Simulator")

NUM_WEEKS = 17

st.markdown("### 🗓️ Game Outcomes")
eagles_results = []
cols = st.columns(NUM_WEEKS)
for i in range(NUM_WEEKS):
    result = cols[i].selectbox(
        f"Week {i+1}",
        ["", "W", "L"],
        index=0,
        key=f"result-{i}"
    )
    eagles_results.append(result if result else "A")  # Use 'A' as your "not yet played" flag

st.markdown("---")

st.markdown("### 📊 ESPN Win Probabilities")
weight = []
cols = st.columns(NUM_WEEKS)
for i in range(NUM_WEEKS):
    prob = cols[i].slider(
        f"Week {i+1}", 0.0, 1.0, 0.5, step=0.01,
        key=f"prob-{i}"
    )
    weight.append(prob)

st.markdown("---")

if st.button("Run Simulation"):
    st.write("🔄 Running...")
    results = run_simulation(eagles_results, weight)

    st.markdown("### ✅ Weighted Results")
    # Static list of participant names in same order as simulator
    names = ['amir', 'andy', 'buhduh', 'emer', 'hanan', 'jacob', 'jay', 'jen', 'marsha', 'nathan', 'pop', 'sarah']
    weighted_data = {name: [val] for name, val in zip(names, results["weighted"])}
    st.bar_chart(weighted_data)

    st.markdown("### 🧮 Straight Results")
    straight_data = {f"Player {i+1}": [val] for i, val in enumerate(results["straight"])}
    st.bar_chart(straight_data)