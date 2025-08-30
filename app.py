import os
import streamlit as st
import streamlit.components.v1 as components

COMP_PATH = os.path.join(
    os.path.dirname(__file__),
    "components", "outcome_row", "frontend"
)

outcome_row = components.declare_component("outcome_row", path=COMP_PATH)

st.title("🦅 Eagles Season Simulator — Component Test")

index_html = os.path.join(COMP_PATH, "index.html")
bundle_js  = os.path.join(COMP_PATH, "build", "index.js")
st.caption(f"Component path: {COMP_PATH}")
st.caption(f"Has index.html? {'✅' if os.path.exists(index_html) else '❌'} — {index_html}")
st.caption(f"Has build/index.js? {'✅' if os.path.exists(bundle_js) else '❌'} — {bundle_js}")

st.divider()
st.subheader("Week Rows (test)")

res = outcome_row(
    week=1,
    label="Week 1 vs. Cowboys",
    defaultProb=71,
    valueProb=71,
    valueResult="TBD",
    locked=False,
    key="row-test"
)

st.write("Component returned:", res)