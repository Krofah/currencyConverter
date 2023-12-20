#!/usr/bin/env python3
import argparse
from decimal import Decimal, ROUND_HALF_UP
import requests
from typing import Any, Callable, Dict, Optional, Union

LATEST = "latest"

def get_major_currency_rates(base_currency: str, date: Optional[str] = None) -> Dict[str, float]:
    date = date or LATEST
    url = f"https://api.example.com/major-currencies/{date}?base={base_currency.upper()}"
    api_response = requests.get(url)
    rates_json: Dict[str, Dict[str, float]] = api_response.json()
    try:
        return rates_json["rates"]
    except KeyError:
        error_msg = rates_json.get("error") or "Unknown error"
        raise ValueError(error_msg)

def convert(
    amount: Union[int, str, float, Decimal],
    base_currency: str,
    target_currency: str,
    date: Optional[str] = None,
    decimal_precision: int = 2,
) -> Decimal:
    rates = get_major_currency_rates(base_currency, date)
    target_currency = target_currency.upper()
    try:
        converted_amount = Decimal(amount) * Decimal(str(rates[target_currency]))
        return converted_amount.quantize(Decimal(".1") ** decimal_precision, rounding=ROUND_HALF_UP)
    except KeyError:
        raise ValueError(f"No rate available for {target_currency}")
    except InvalidOperation:
        raise ValueError(f'Invalid amount value "{amount}"')

def factorial(n: int) -> int:
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

if __name__ == "__main__":
    # Example usage of the factorial function
    result = factorial(5)
    print(result)
