from . import schemas

def calc_logistics(volume: float, coeff: float) -> float:
    """Calculate logistics cost based on volume and coefficient."""
    if volume >= 1:
        rounded_volume = round(volume + 0.49)
        base = 0.46 * coeff
        additional = (rounded_volume - 1) * (0.14 * coeff)
        return base + additional
    elif volume > 0.8:
        return 0.32 * coeff
    elif volume > 0.6:
        return 0.30 * coeff
    elif volume > 0.4:
        return 0.29 * coeff
    elif volume > 0.2:
        return 0.26 * coeff
    elif volume >= 0.001:
        return 0.23 * coeff
    return 0

def perform_calculation(calc: schemas.CalculationCreate) -> dict:
    """Perform the unit economics calculation."""
    # Calculate volume in liters
    volume_liters = (calc.length * calc.width * calc.height) / 1000
    
    # Calculate logistics costs
    logistics_cost = calc_logistics(volume_liters, calc.logistics_coefficient)
    total_logistics_cost = (logistics_cost + (1 - calc.buyout_percent / 100) * calc.return_cost) / (calc.buyout_percent / 100)
    
    # Calculate base cost
    base_cost = calc.purchase_price + total_logistics_cost + calc.storage_cost
    
    # Calculate percentages
    total_percent = (calc.commission_wb_percent + calc.acquiring_percent + calc.tax_percent + calc.ads_percent) / 100
    
    # Calculate client price
    if 1 - total_percent <= 0:
        raise ValueError("Total percentage is greater than or equal to 100%")
    
    client_price = (base_cost + calc.desired_profit) / (1 - total_percent)
    
    # Calculate costs
    ads_cost = client_price * calc.ads_percent / 100
    commission_wb_cost = client_price * calc.commission_wb_percent / 100
    acquiring_cost = client_price * calc.acquiring_percent / 100
    tax_cost = client_price * calc.tax_percent / 100
    
    # Calculate final results
    final_cost = base_cost + commission_wb_cost + acquiring_cost + tax_cost + ads_cost
    profit_per_unit = client_price - final_cost
    margin_percent = (profit_per_unit / client_price) * 100
    
    return {
        "volume_liters": volume_liters,
        "logistics_cost": logistics_cost,
        "total_logistics_cost": total_logistics_cost,
        "client_price": client_price,
        "ads_cost": ads_cost,
        "commission_wb_cost": commission_wb_cost,
        "acquiring_cost": acquiring_cost,
        "tax_cost": tax_cost,
        "storage_cost_result": calc.storage_cost,
        "final_cost": final_cost,
        "profit_per_unit": profit_per_unit,
        "margin_percent": margin_percent
    }