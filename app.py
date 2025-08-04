from simulator import run_simulation
import streamlit as st

st.set_page_config(page_title="Eagles Season Simulator", layout="wide")
st.title("🦅 Eagles Season Simulator")

NUM_WEEKS = 17

st.markdown("### 📅 Game Outcomes")
eagles_results = []
cols = st.columns(NUM_WEEKS)
for i in range(NUM_WEEKS):
    result = cols[i].selectbox(
        f"Week {i+1}",
        ["", "W", "L"],
        index=0,
        key=f"result-{i}"
    )
    eagles_results.append(result if result else "A")

# Default win probabilities (you can allow users to customize this too)
weight = {
    0:  .500, 1:  .626, 2:  .487, 3:  .610, 4:  .671, 5:  .641,
    6:  .499, 7:  .685, 8:  .597, 9:  .584, 10: .587, 11: .413,
    12: .851, 13: .610, 14: .577, 15: .768, 16: .834
}

if st.button("Run Simulation"):
    with st.spinner("Simulating..."):
        results = run_simulation(eagles_results, weight)
        st.success("Simulation complete!")
        st.markdown("### 🧮 Weighted Probabilities")
        st.write(results["weighted"])
        st.markdown("### 📊 Straight Probabilities")
        st.write(results["straight"])