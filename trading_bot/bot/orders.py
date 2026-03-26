from typing import Dict

from .client import BinanceFuturesClient
from .validators import validate_symbol, validate_side, validate_order_type, validate_quantity, validate_price


class OrderService:
    def __init__(self, client: BinanceFuturesClient):
        self.client = client

    def place_order(self, symbol: str, side: str, order_type: str, quantity: str, price: str = None) -> Dict:
        symbol = validate_symbol(symbol)
        side = validate_side(side)
        order_type = validate_order_type(order_type)
        quantity = validate_quantity(quantity)

        if order_type == "MARKET":
            return self.client.create_order(symbol=symbol, side=side, order_type=order_type, quantity=quantity)

        if order_type == "LIMIT":
            if price is None:
                raise ValueError("price is required for LIMIT order")
            price = validate_price(price)
            return self.client.create_order(symbol=symbol, side=side, order_type=order_type, quantity=quantity, price=price)

        raise ValueError("unknown order type")
