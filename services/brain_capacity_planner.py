# services/brain_capacity_planner.py

import json
import os
from datetime import datetime

BRAIN_MEMORY_FILE = "data/brain_memory.json"

# -----------------------------
# Load Brain Memory
# -----------------------------
def load_brain_memory():
    if not os.path.exists(BRAIN_MEMORY_FILE):
        return {
            "past_predictions": [],
            "confidence_score": 0.6   # initial confidence
        }

    with open(BRAIN_MEMORY_FILE, "r") as f:
        return json.load(f)

# -----------------------------
# Save Brain Memory
# -----------------------------
def save_brain_memory(memory):
    os.makedirs("data", exist_ok=True)
    with open(BRAIN_MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

# -----------------------------
# Capacity Planning Brain
# -----------------------------
def capacity_planning_brain(input_data):
    demand = input_data.get("demand_index", 0)
    capacity = input_data.get("supply_capacity", 0)
    backlog = input_data.get("backlog", 0)
    signal = input_data.get("live_market_signal", "Unknown")

    # ------------------------
    # Default safe output
    # ------------------------
    decision = "Hold capacity"
    reason = "Insufficient signals to justify expansion"
    risk = "Low"
    confidence = 0.5

    # ------------------------
    # Core Brain Logic
    # ------------------------
    if demand >= 7 and backlog >= 2000:
        decision = "Expand capacity"
        reason = "High demand index with significant backlog"
        risk = "Medium"
        confidence = 0.75

    if "Rising" in signal:
        decision = "Expand aggressively"
        reason = "Positive market momentum and demand pressure"
        risk = "Medium-High"
        confidence = 0.82

    if "Softening" in signal:
        decision = "Delay expansion"
        reason = "Market demand signals weakening"
        risk = "High"
        confidence = 0.4

    # ------------------------
    return {
        "decision": decision,
        "reason": reason,
        "risk_flag": risk,
        "confidence": confidence
    }
