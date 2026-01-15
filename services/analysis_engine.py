from services.demand_data_service import get_nvidia_demand_data
from services.supply_data_service import get_nvidia_supply_status
from services.live_market_service import fetch_nvda_live_data
from services.brain_capacity_planner import capacity_planning_brain


# -----------------------------------
# 🧠 Market Signal Inference (Fallback Brain)
# -----------------------------------
def infer_market_signal(demand, backlog, gap):
    if demand >= 7 and backlog > 3000:
        return "Strong AI infrastructure demand"
    if gap > 2:
        return "Demand-led expansion signal"
    if demand >= 5:
        return "Stable growth environment"
    return "Uncertain demand outlook"

# -----------------------------------
# 📊 Demand vs Supply Analyzer
# -----------------------------------
def analyze_demand_vs_supply(region="global"):
    demand = get_nvidia_demand_data(region)
    supply = get_nvidia_supply_status(region)

    # Demand–Supply gap
    gap = demand["current_demand_index"] - (
        supply["monthly_production_capacity"] / 50
    )

    # Default signal
    market_signal = "Unknown"

    # -----------------------------------
    # 🔴 Try live market first
    # -----------------------------------
    try:
        live_market = fetch_nvda_live_data()

        if live_market["percent_change"] > 2:
            market_signal = "Rising demand momentum"
        elif live_market["percent_change"] < -2:
            market_signal = "Softening demand signal"
        else:
            market_signal = "Stable"

    except Exception as e:
        print("⚠️ Live market fetch failed:", e)

        # -----------------------------------
        # 🟡 Intelligent fallback (Brain Growing)
        # -----------------------------------
        market_signal = infer_market_signal(
            demand["current_demand_index"],
            supply["backlog_units"],
            gap
        )

    # -----------------------------------
    # 🧠 Brain Capacity Planning Decision
    # -----------------------------------
    brain_result = capacity_planning_brain({
        "demand_index": demand["current_demand_index"],
        "supply_capacity": supply["monthly_production_capacity"],
        "backlog": supply["backlog_units"],
        "live_market_signal": market_signal
    })

    # -----------------------------------
    return {
        "product": demand["product"],
        "region": region,
        "demand_index": demand["current_demand_index"],
        "supply_capacity": supply["monthly_production_capacity"],
        "backlog": supply["backlog_units"],
        "gap_score": gap,
        "risk": supply["risk_level"],
        "live_market_signal": market_signal,
        "brain_decision": brain_result
    }
