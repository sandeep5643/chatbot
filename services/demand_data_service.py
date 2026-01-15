# Mock NVIDIA demand data engine

def get_nvidia_demand_data(region="global"):
    """
    Simulates NVIDIA GPU demand data
    """
    return {
        "product": "NVIDIA H100",
        "region": region,
        "current_demand_index": 135,
        "last_month_index": 120,
        "growth_rate_percent": 12.5,
        "primary_driver": "AI / LLM training workloads"
    }
