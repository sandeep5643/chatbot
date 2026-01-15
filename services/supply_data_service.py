def get_nvidia_supply_status(region="global"):
    """
    Simulates NVIDIA GPU supply data
    """
    return {
        "product": "NVIDIA H100",
        "region": region,
        "available_units": 4200,
        "monthly_production_capacity": 5000,
        "backlog_units": 1800,
        "risk_level": "HIGH"
    }
