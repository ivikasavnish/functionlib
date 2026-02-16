"""
Financial Functions

Financial calculations including interest, loans, investments, and present value.
"""

import math
from typing import List, Optional


def simple_interest(principal: float, rate: float, time: float) -> float:
    """
    Calculates simple interest: I = Prt
    
    Args:
        principal: Initial amount
        rate: Annual interest rate (decimal, e.g., 0.05 for 5%)
        time: Time in years
        
    Returns:
        Interest amount
        
    Example:
        >>> simple_interest(1000, 0.05, 2)
        100.0
    """
    return principal * rate * time


def compound_interest(principal: float, rate: float, time: float, n: int = 1) -> float:
    """
    Calculates compound interest: A = P(1 + r/n)^(nt)
    
    Args:
        principal: Initial amount
        rate: Annual interest rate (decimal)
        time: Time in years
        n: Compounding frequency per year (1=annually, 12=monthly, 365=daily)
        
    Returns:
        Final amount
        
    Example:
        >>> compound_interest(1000, 0.05, 2, 12)
        1104.94...
    """
    return principal * (1 + rate / n) ** (n * time)


def continuous_compound_interest(principal: float, rate: float, time: float) -> float:
    """
    Continuous compounding: A = Pe^(rt)
    
    Args:
        principal: Initial amount
        rate: Annual interest rate (decimal)
        time: Time in years
        
    Returns:
        Final amount
        
    Example:
        >>> continuous_compound_interest(1000, 0.05, 2)
        1105.17...
    """
    return principal * math.exp(rate * time)


def future_value(pv: float, rate: float, periods: int) -> float:
    """
    Future value: FV = PV(1 + r)^n
    
    Args:
        pv: Present value
        rate: Interest rate per period (decimal)
        periods: Number of periods
        
    Returns:
        Future value
        
    Example:
        >>> future_value(1000, 0.05, 10)
        1628.89...
    """
    return pv * (1 + rate) ** periods


def present_value(fv: float, rate: float, periods: int) -> float:
    """
    Present value: PV = FV / (1 + r)^n
    
    Args:
        fv: Future value
        rate: Interest rate per period (decimal)
        periods: Number of periods
        
    Returns:
        Present value
        
    Example:
        >>> present_value(1628.89, 0.05, 10)
        999.99...
    """
    return fv / (1 + rate) ** periods


def annuity_future_value(payment: float, rate: float, periods: int) -> float:
    """
    Future value of ordinary annuity: FV = PMT × [(1+r)^n - 1] / r
    
    Args:
        payment: Payment per period
        rate: Interest rate per period
        periods: Number of periods
        
    Returns:
        Future value
        
    Example:
        >>> annuity_future_value(100, 0.05, 10)
        1257.78...
    """
    if rate == 0:
        return payment * periods
    
    return payment * ((1 + rate) ** periods - 1) / rate


def annuity_present_value(payment: float, rate: float, periods: int) -> float:
    """
    Present value of ordinary annuity: PV = PMT × [1 - (1+r)^(-n)] / r
    
    Args:
        payment: Payment per period
        rate: Interest rate per period
        periods: Number of periods
        
    Returns:
        Present value
        
    Example:
        >>> annuity_present_value(100, 0.05, 10)
        772.17...
    """
    if rate == 0:
        return payment * periods
    
    return payment * (1 - (1 + rate) ** (-periods)) / rate


def loan_payment(principal: float, rate: float, periods: int) -> float:
    """
    Monthly loan payment: PMT = P × [r(1+r)^n] / [(1+r)^n - 1]
    
    Args:
        principal: Loan amount
        rate: Interest rate per period
        periods: Number of periods
        
    Returns:
        Payment per period
        
    Example:
        >>> loan_payment(10000, 0.05/12, 60)
        188.71...
    """
    if rate == 0:
        return principal / periods
    
    return principal * (rate * (1 + rate) ** periods) / ((1 + rate) ** periods - 1)


def mortgage_payment(principal: float, annual_rate: float, years: int) -> float:
    """
    Monthly mortgage payment
    
    Args:
        principal: Loan amount
        annual_rate: Annual interest rate (decimal)
        years: Loan term in years
        
    Returns:
        Monthly payment
        
    Example:
        >>> mortgage_payment(200000, 0.04, 30)
        954.83...
    """
    monthly_rate = annual_rate / 12
    periods = years * 12
    
    return loan_payment(principal, monthly_rate, periods)


def amortization_schedule(principal: float, rate: float, periods: int) -> List[dict]:
    """
    Generates loan amortization schedule
    
    Args:
        principal: Loan amount
        rate: Interest rate per period
        periods: Number of periods
        
    Returns:
        List of payment details
        
    Example:
        >>> schedule = amortization_schedule(10000, 0.05/12, 12)
        >>> len(schedule)
        12
    """
    payment = loan_payment(principal, rate, periods)
    balance = principal
    schedule = []
    
    for period in range(1, periods + 1):
        interest = balance * rate
        principal_paid = payment - interest
        balance -= principal_paid
        
        schedule.append({
            'period': period,
            'payment': round(payment, 2),
            'principal': round(principal_paid, 2),
            'interest': round(interest, 2),
            'balance': round(max(0, balance), 2)
        })
    
    return schedule


def roi(gain: float, cost: float) -> float:
    """
    Return on Investment: ROI = (Gain - Cost) / Cost
    
    Args:
        gain: Final value
        cost: Initial investment
        
    Returns:
        ROI as percentage
        
    Example:
        >>> roi(1500, 1000)
        50.0
    """
    if cost == 0:
        raise ValueError("Cost cannot be zero")
    
    return ((gain - cost) / cost) * 100


def cagr(beginning_value: float, ending_value: float, years: float) -> float:
    """
    Compound Annual Growth Rate
    
    Args:
        beginning_value: Starting value
        ending_value: Ending value
        years: Number of years
        
    Returns:
        CAGR as percentage
        
    Example:
        >>> cagr(1000, 2000, 5)
        14.86...
    """
    return ((ending_value / beginning_value) ** (1 / years) - 1) * 100


def rule_of_72(rate: float) -> float:
    """
    Rule of 72: estimates doubling time
    
    Args:
        rate: Annual return rate (percentage)
        
    Returns:
        Years to double
        
    Example:
        >>> rule_of_72(8)
        9.0
    """
    return 72 / rate


def break_even_point(fixed_costs: float, price_per_unit: float, variable_cost_per_unit: float) -> float:
    """
    Break-even point in units
    
    Args:
        fixed_costs: Total fixed costs
        price_per_unit: Selling price per unit
        variable_cost_per_unit: Variable cost per unit
        
    Returns:
        Break-even units
        
    Example:
        >>> break_even_point(10000, 50, 30)
        500.0
    """
    contribution_margin = price_per_unit - variable_cost_per_unit
    
    if contribution_margin <= 0:
        raise ValueError("Price must exceed variable cost")
    
    return fixed_costs / contribution_margin


def profit_margin(revenue: float, cost: float) -> float:
    """
    Profit margin percentage
    
    Args:
        revenue: Total revenue
        cost: Total cost
        
    Returns:
        Profit margin as percentage
        
    Example:
        >>> profit_margin(1000, 700)
        30.0
    """
    if revenue == 0:
        raise ValueError("Revenue cannot be zero")
    
    return ((revenue - cost) / revenue) * 100


def markup_percentage(cost: float, selling_price: float) -> float:
    """
    Markup percentage
    
    Args:
        cost: Cost price
        selling_price: Selling price
        
    Returns:
        Markup as percentage
        
    Example:
        >>> markup_percentage(100, 150)
        50.0
    """
    if cost == 0:
        raise ValueError("Cost cannot be zero")
    
    return ((selling_price - cost) / cost) * 100


def discount_price(original_price: float, discount_percent: float) -> float:
    """
    Price after discount
    
    Args:
        original_price: Original price
        discount_percent: Discount percentage
        
    Returns:
        Discounted price
        
    Example:
        >>> discount_price(100, 20)
        80.0
    """
    return original_price * (1 - discount_percent / 100)


def sales_tax(amount: float, tax_rate: float) -> float:
    """
    Calculates sales tax
    
    Args:
        amount: Pre-tax amount
        tax_rate: Tax rate as percentage
        
    Returns:
        Tax amount
        
    Example:
        >>> sales_tax(100, 8.5)
        8.5
    """
    return amount * (tax_rate / 100)


def tip_amount(bill: float, tip_percent: float) -> float:
    """
    Calculates tip amount
    
    Args:
        bill: Bill amount
        tip_percent: Tip percentage
        
    Returns:
        Tip amount
        
    Example:
        >>> tip_amount(50, 20)
        10.0
    """
    return bill * (tip_percent / 100)


def effective_annual_rate(nominal_rate: float, n: int) -> float:
    """
    Effective Annual Rate: EAR = (1 + r/n)^n - 1
    
    Args:
        nominal_rate: Nominal annual rate (decimal)
        n: Compounding periods per year
        
    Returns:
        Effective annual rate (percentage)
        
    Example:
        >>> effective_annual_rate(0.12, 12)
        12.68...
    """
    return ((1 + nominal_rate / n) ** n - 1) * 100


def bond_price(face_value: float, coupon_rate: float, yield_rate: float, years: int, frequency: int = 2) -> float:
    """
    Bond price calculation
    
    Args:
        face_value: Face/par value
        coupon_rate: Annual coupon rate (decimal)
        yield_rate: Required yield (decimal)
        years: Years to maturity
        frequency: Coupon payments per year (default 2 for semi-annual)
        
    Returns:
        Bond price
        
    Example:
        >>> bond_price(1000, 0.05, 0.04, 10)
        1081.10...
    """
    periods = years * frequency
    coupon = face_value * coupon_rate / frequency
    rate_per_period = yield_rate / frequency
    
    # Present value of coupons
    pv_coupons = annuity_present_value(coupon, rate_per_period, periods)
    
    # Present value of face value
    pv_face = present_value(face_value, rate_per_period, periods)
    
    return pv_coupons + pv_face


def net_present_value(rate: float, cash_flows: List[float]) -> float:
    """
    Net Present Value
    
    Args:
        rate: Discount rate (decimal)
        cash_flows: List of cash flows (first is initial investment, negative)
        
    Returns:
        NPV
        
    Example:
        >>> net_present_value(0.1, [-1000, 300, 300, 300, 300, 300])
        137.23...
    """
    npv = 0
    for t, cf in enumerate(cash_flows):
        npv += cf / (1 + rate) ** t
    
    return npv


def internal_rate_of_return(cash_flows: List[float], iterations: int = 100) -> Optional[float]:
    """
    Internal Rate of Return (approximation using Newton's method)
    
    Args:
        cash_flows: List of cash flows
        iterations: Maximum iterations
        
    Returns:
        IRR as decimal
        
    Example:
        >>> irr = internal_rate_of_return([-1000, 300, 300, 300, 300, 300])
        >>> 0.15 < irr < 0.16
        True
    """
    # Initial guess
    rate = 0.1
    
    for _ in range(iterations):
        npv = sum(cf / (1 + rate) ** t for t, cf in enumerate(cash_flows))
        
        # Derivative of NPV
        dnpv = sum(-t * cf / (1 + rate) ** (t + 1) for t, cf in enumerate(cash_flows))
        
        if abs(dnpv) < 1e-10:
            break
        
        new_rate = rate - npv / dnpv
        
        if abs(new_rate - rate) < 1e-6:
            return new_rate
        
        rate = new_rate
    
    return rate


# Export all functions
__all__ = [
    'simple_interest', 'compound_interest', 'continuous_compound_interest',
    'future_value', 'present_value',
    'annuity_future_value', 'annuity_present_value',
    'loan_payment', 'mortgage_payment', 'amortization_schedule',
    'roi', 'cagr', 'rule_of_72',
    'break_even_point', 'profit_margin', 'markup_percentage',
    'discount_price', 'sales_tax', 'tip_amount',
    'effective_annual_rate', 'bond_price',
    'net_present_value', 'internal_rate_of_return',
]
