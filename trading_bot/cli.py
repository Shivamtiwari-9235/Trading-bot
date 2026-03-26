import argparse
import os
import sys

from bot.client import BinanceFuturesClient
from bot.orders import OrderService
from bot.logging_config import configure_logger
from bot.validators import validate_symbol, validate_side, validate_order_type, validate_quantity, validate_price


def main():
    parser = argparse.ArgumentParser(description="Production Binance Futures Testnet Trading Bot CLI (Mock/Real modes)")
    parser.add_argument("--symbol", required=True, help="Trading pair e.g. BTCUSDT")
    parser.add_argument("--side", required=True, choices=["BUY", "SELL"], help="Order side")
    parser.add_argument("--order-type", required=True, choices=["MARKET", "LIMIT"], help="Order type")
    parser.add_argument("--quantity", required=True, help="Order quantity (e.g. 0.001)")
    parser.add_argument("--price", required=False, help="Order price (required for LIMIT)")
    parser.add_argument("--mode", default="mock", choices=["mock", "real"], help="Execution mode (default: mock)")
    parser.add_argument("--base-url", default="https://testnet.binancefuture.com", help="API base URL")
    parser.add_argument("--api-key", help="Override BINANCE_API_KEY from .env")
    parser.add_argument("--api-secret", help="Override BINANCE_API_SECRET from .env")
    parser.add_argument("--log-file", default="logs/bot.log", help="Log file (default: logs/bot.log)")

    args = parser.parse_args()

    logger = configure_logger(args.log_file)

    print(f"=== Placing {args.mode.upper()} {args.order_type} {args.side} order for {args.symbol} ===")
    print(f"Quantity: {args.quantity}, Price: {args.price or 'Market'}")
    logger.info("CLI order request: %s", vars(args))

    client = BinanceFuturesClient(api_key=args.api_key, api_secret=args.api_secret, mode=args.mode, base_url=args.base_url)
    service = OrderService(client)

    try:
        response = service.place_order(symbol=args.symbol, side=args.side, order_type=args.order_type, quantity=args.quantity, price=args.price)
        logger.info("Order response: %s", response)

        print("\n✅ Order placed successfully!")
        print(f"🆔 Order ID: {response.get('orderId')}")
        print(f"📊 Status: {response.get('status')}")
        print(f"📈 Executed Qty: {response.get('executedQty')}")
        print(f"💰 Avg Price: {response.get('avgPrice', 'N/A')}")

    except Exception as error:
        logger.error("Order placement failed: %s", error)
        print("Order placement failed:", error)
        sys.exit(2)


if __name__ == "__main__":
    main()
