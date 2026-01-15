# services/demand_classifier.py

LIVE_MARKET_KEYWORDS = [
    "market price",
    "current price",
    "stock price",
    "share price",
    "nvidia stock",
    "nvda price",
    "today price",
    "trading price",
    "live price",
    "price today"
]

DEMAND_KEYWORDS = [
    "demand", "forecast", "requirement", "need", "order", "sales"
]

SUPPLY_KEYWORDS = [
    "supply", "inventory", "warehouse",
    "production", "manufacturing", "shipment"
]

NVIDIA_KEYWORDS = [
    "nvidia", "gpu", "rtx", "cuda", "dgx",
    "jetson", "ai", "datacenter", "nvda"
]

CAPACITY_KEYWORDS = [
    "capacity", "expand", "increase", "production",
    "safe", "scaling", "manufacturing"
]


def classify_user_demand(user_msg: str) -> str:
    text = user_msg.lower()

    # 1️⃣ LIVE MARKET
    if any(k in text for k in LIVE_MARKET_KEYWORDS):
        return "LIVE_MARKET_DATA"

    # 2️⃣ CAPACITY PLANNING (🔥 NVIDIA assumed)
    if any(k in text for k in CAPACITY_KEYWORDS):
        return "CAPACITY_PLANNING"

    # 3️⃣ Demand + Supply
    if any(k in text for k in DEMAND_KEYWORDS) and any(k in text for k in SUPPLY_KEYWORDS):
        return "DEMAND_SUPPLY_ANALYSIS"

    # 4️⃣ Demand only
    if any(k in text for k in DEMAND_KEYWORDS):
        return "DEMAND_SIGNAL"

    # 5️⃣ Supply only
    if any(k in text for k in SUPPLY_KEYWORDS):
        return "SUPPLY_STATUS"

    # 6️⃣ NVIDIA general
    if any(k in text for k in NVIDIA_KEYWORDS):
        return "NVIDIA_INFO"

    return "OUT_OF_SCOPE"
