// Minimal TS/React component using Streamlit's JS bridge
import React, { useEffect, useState } from "react";
import { Streamlit, withStreamlitConnection } from "streamlit-component-lib";

// Types we expect from Python
type Props = {
  args: {
    week: number;
    label: string;              // "vs. Cowboys"
    defaultProb: number;        // integer 0..100
    valueProb: number;          // integer 0..100 (current)
    valueResult: "TBD"|"W"|"L"; // current selection
    locked: boolean;            // backend or frontend lock
  };
};

function OutcomeRow({ args }: Props) {
  const {
    label, defaultProb, valueProb, valueResult, locked,
  } = args;

  const [result, setResult] = useState<"TBD"|"W"|"L">(valueResult);
  const [prob, setProb] = useState<number>(valueProb);
  const [showReset, setShowReset] = useState<boolean>(valueProb !== defaultProb);

  // Lock if backend W/L or user picked W/L
  const frontendLocked = result !== "TBD";
  const isLocked = locked || frontendLocked;

  useEffect(() => {
    // On any change, send value back to Python
    Streamlit.setComponentValue({ result, prob });
  }, [result, prob]);

  useEffect(() => {
    setShowReset(!isLocked && prob !== defaultProb);
  }, [isLocked, prob, defaultProb]);

  const onReset = () => setProb(defaultProb);

  return (
    <div style={{
      display: "grid",
      gridTemplateColumns: "1fr auto auto",
      gap: "8px",
      alignItems: "center",
      width: "100%",
    }}>
      {/* Label + dropdown */}
      <div>
        <div style={{ fontSize: 14, opacity: 0.9, marginBottom: 6 }}>{label}</div>
        <select
          value={result}
          onChange={(e) => setResult(e.target.value as "TBD"|"W"|"L")}
          disabled={locked}
          style={{
            width: "100%",
            padding: "10px 12px",
            borderRadius: 8,
            background: "#2b2e33",
            color: "#fafafa",
            border: "1px solid rgba(255,255,255,0.08)"
          }}
        >
          <option value="TBD">TBD</option>
          <option value="W">W</option>
          <option value="L">L</option>
        </select>
      </div>

      {/* Percent input */}
      <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
        <input
          type="number"
          min={0}
          max={100}
          step={1}
          value={isLocked ? (result === "W" ? 100 : 0) : prob}
          onChange={(e) => setProb(Math.max(0, Math.min(100, parseInt(e.target.value || "0", 10))))}
          disabled={isLocked}
          style={{
            width: 72,
            padding: "10px 12px",
            borderRadius: 8,
            background: "#2b2e33",
            color: "#fafafa",
            textAlign: "right",
            border: "1px solid rgba(255,255,255,0.08)"
          }}
        />
        <span style={{ width: 16, textAlign: "center", opacity: 0.8 }}>%</span>
      </div>

      {/* Reset */}
      <div style={{ textAlign: "center" }}>
        {showReset ? (
          <button
            onClick={onReset}
            title={`Reset to default (${defaultProb}%)`}
            style={{
              padding: "8px 10px",
              borderRadius: 10,
              background: "transparent",
              color: "#fafafa",
              border: "1px solid rgba(255,255,255,0.15)",
              cursor: "pointer"
            }}
          >
            ↺
          </button>
        ) : null}
      </div>
    </div>
  );
}

export default withStreamlitConnection(OutcomeRow);