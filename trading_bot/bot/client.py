import time
import hmac
import hashlib
from urllib.parse import urlencode

try:
    import requests
except ImportError as exc:
    raise ImportError("requests library is required. Install with: pip install -r requirements.txt") from exc

import os
from dotenv import load_dotenv
import random

from .logging_config import configure_logger

logger = configure_logger()


class BinanceFuturesClient:
    def __init__(self, api_key: str, api_secret: str, mode: str = "mock", base_url: str = "https://testnet.binancefuture.com"):
        load_dotenv()
        self.api_key = api_key or os.getenv("BINANCE_API_KEY")
        self.api_secret = api_secret or os.getenv("BINANCE_API_SECRET")
        self.mode = mode
        self.base_url = base_url.rstrip("/")
        if self.mode == "real":
            if not self.api_key or not self.api_secret:
                raise ValueError("API key and secret required for real mode")
            self.session = requests.Session()
            self.session.headers.update({
                "X-MBX-APIKEY": self.api_key,
                "Content-Type": "application/x-www-form-urlencoded",
            })

    def _timestamp(self) -> int:
        return int(time.time() * 1000)

    def _sign(self, params: dict) -> str:
        query = urlencode(sorted(params.items()))
        return hmac.new(self.api_secret.encode("utf-8"), query.encode("utf-8"), hashlib.sha256).hexdigest()

    def _request(self, http_method: str, endpoint: str, params: dict):
        url = f"{self.base_url}{endpoint}"
        logger.debug("HTTP %s %s payload=%s", http_method, url, params)

        try:
            if http_method.upper() == "GET":
                resp = self.session.get(url, params=params, timeout=10)
            else:
                resp = self.session.post(url, data=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            logger.debug("HTTP response %s", data)
            return data
        except requests.HTTPError as e:
            try:
                err = resp.json()
            except Exception:
                err = resp.text
            logger.error("API HTTP error %s %s", e, err)
            raise
        except requests.RequestException as e:
            logger.error("Network error: %s", e)
            raise

    def create_order(self, symbol: str, side: str, order_type: str, quantity: float, price: float = None):
        if self.mode == "mock":
            avg_price = price if price else round(random.uniform(40000, 60000), 2)
            logger.info("MOCK MODE: Simulated %s %s order for %s qty@%.2f", order_type, side, symbol, avg_price)
            return {
                "orderId": random.randint(10000000, 99999999),
                "status": "FILLED",
                "executedQty": str(quantity),
                "avgPrice": str(avg_price),
                "symbol": symbol,
                "side": side,
                "type": order_type
            }

        # Real mode
        path = "/fapi/v1/order"
        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
            "timestamp": self._timestamp(),
            "recvWindow": 5000,
        }

        if order_type == "LIMIT":
            params.update({"price": price, "timeInForce": "GTC"})

        signature = self._sign(params)
        params["signature"] = signature

        return self._request("POST", path, params)
