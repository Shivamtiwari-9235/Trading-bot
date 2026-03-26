import re


def validate_symbol(symbol: str) -> str:
    if not symbol or not isinstance(symbol, str):
        raise ValueError("symbol is required and must be a string")
    symbol = symbol.strip().upper()
    if not re.match(r"^[A-Z0-9]+$", symbol):
        raise ValueError("symbol must consist of letters and numbers only")
    return symbol


def validate_side(side: str) -> str:
    if not side or not isinstance(side, str):
        raise ValueError("side is required")
    side = side.strip().upper()
    if side not in {"BUY", "SELL"}:
        raise ValueError("side must be BUY or SELL")
    return side


def validate_order_type(order_type: str) -> str:
    if not order_type or not isinstance(order_type, str):
        raise ValueError("order type is required")
    order_type = order_type.strip().upper()
    if order_type not in {"MARKET", "LIMIT"}:
        raise ValueError("order_type must be MARKET or LIMIT")
    return order_type


def validate_quantity(quantity: str) -> float:
    try:
        q = float(quantity)
    except Exception as exc:
        raise ValueError("quantity must be numeric") from exc
    if q <= 0:
        raise ValueError("quantity must be greater than zero")
    return q


def validate_price(price: str) -> float:
    try:
        p = float(price)
    except Exception as exc:
        raise ValueError("price must be numeric") from exc
    if p <= 0:
        raise ValueError("price must be greater than zero")
    return p
