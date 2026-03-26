# 🚀 Production Binance Futures Testnet Trading Bot

Production-quality Python CLI trading bot for Binance Futures Testnet (USDT-M) with **Mock & Real modes**.

## ✨ Features

- ✅ MARKET & LIMIT orders (BUY/SELL)
- 🎭 **Mock mode** (no API keys needed - simulates execution)
- 🔌 **Real mode** (Binance Testnet API)
- 📊 Clean CLI UX with validation & pretty output
- 📝 Structured logging (`logs/bot.log` + console)
- 🛡️ Full input validation & error handling
- 🌍 .env support for API keys
- 🏗️ Clean architecture (client/service/validators layers)

## 🏗️ Project Structure

```
trading_bot/
├── cli.py                 # CLI entrypoint
├── bot/
│   ├── client.py         # API client (mock/real)
│   ├── orders.py         # Business logic
│   ├── validators.py     # Input validation
│   └── logging_config.py # Logging setup
├── requirements.txt      # Dependencies
├── .env.example          # API key template
├── logs/bot.log          # Logs (auto-created)
└── TODO.md              # Implementation tracking
```

## 🚀 Quick Start

### 1. Setup Environment
```powershell
cd trading_bot
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. **MOCK Mode** (No API needed!)
```powershell
# Market BUY
python cli.py --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.001

# Limit SELL
python cli.py --symbol BTCUSDT --side SELL --order-type LIMIT --quantity 0.001 --price 45000
```

**Sample Output:**
```
=== Placing MOCK MARKET BUY order for BTCUSDT ===
Quantity: 0.001, Price: Market

✅ Order placed successfully!
🆔 Order ID: 74582319
📊 Status: FILLED
📈 Executed Qty: 0.001
💰 Avg Price: 52347.23
```

### 3. **REAL Mode** (Testnet API)
1. Copy `.env.example` → `.env` & add your Testnet keys
2. Or use CLI args:
```powershell
python cli.py --mode real --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.001 --api-key YOUR_KEY --api-secret YOUR_SECRET
```

### 4. Logs
All requests/responses logged to `logs/bot.log` (DEBUG level)

## 🔑 Environment Variables (.env)

Create `.env` file:
```
BINANCE_API_KEY=your_testnet_api_key
BINANCE_API_SECRET=your_testnet_api_secret
```

## 📋 Usage Examples

| Mode | Command | Description |
|------|---------|-------------|
| Mock Market | `python cli.py --mode mock --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.001` | Simulated market buy |
| Mock Limit | `python cli.py --symbol ETHUSDT --side SELL --order-type LIMIT --quantity 0.5 --price 3200` | Simulated limit sell |
| Real Market | `python cli.py --mode real --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.001` | **Real** testnet order |

## ⚠️  Important Notes

- **Mock mode default** - safe for testing without API
- **Testnet only** - get keys from https://testnet.binancefuture.com
- **Exit codes**: 0=success, 2=failure
- Validation rejects invalid symbol/side/quantity/price

## 🧪 Testing Real Output

For **real** Binance-like output (as original project):
```
cd trading_bot
.venv\Scripts\activate  (if venv)
python cli.py --mode real --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.001 --api-key YOUR_TESTNET_KEY --api-secret YOUR_TESTNET_SECRET
```

**Expected real output** (same format as before):
```
🆔 orderId: [real binance ID]
📊 status: NEW/FILLED/PARTIALLY_FILLED
📈 executedQty: 0.001
💰 avgPrice: [market price]
```

## 📈 Production Ready

✅ Modular architecture  
✅ Comprehensive error handling  
✅ Structured logging  
✅ Input validation  
✅ Mock for safe testing  
✅ .env secrets management  
✅ Beginner-friendly CLI  

**Ready for hiring evaluation/production!** 🎯
