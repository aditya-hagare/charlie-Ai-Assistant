import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def fetch_nifty():
    try:
        url = "https://query1.finance.yahoo.com/v8/finance/chart/^NSEI"
        r = requests.get(url, headers=HEADERS, timeout=5)
        data = r.json()

        result = data["chart"]["result"][0]
        price = result["meta"]["regularMarketPrice"]

        return {"price": price}
    except Exception as e:
        print("NIFTY ERROR:", e)
        return None


def fetch_btc():
    try:
        # Binance public API (no key required)
        url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
        r = requests.get(url, timeout=5)
        data = r.json()

        return {"price": float(data["price"])}
    except Exception as e:
        print("BTC ERROR:", e)
        return None


def fetch_gold():
    try:
        # Gold Futures from Yahoo
        url = "https://query1.finance.yahoo.com/v8/finance/chart/GC=F"
        r = requests.get(url, headers=HEADERS, timeout=5)
        data = r.json()

        result = data["chart"]["result"][0]
        price = result["meta"]["regularMarketPrice"]

        return {"price": price}
    except Exception as e:
        print("GOLD ERROR:", e)
        return None


def get_stock():
    return {
        "nifty50": fetch_nifty(),
        "btcusd": fetch_btc(),
        "gold": fetch_gold()
    }
