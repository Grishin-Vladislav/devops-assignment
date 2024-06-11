import requests

from src.config import COIN_MARKET_TOKEN


# Needs proper handling of api errors, now it's up for users to check status code
def return_coin_info_or_status_code(coin_symbol: str) -> dict:
    """
    requests is synchronous for development speed
    """
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/map"
    params = {"symbol": coin_symbol}
    headers = {"Accepts": "application/json", "X-CMC_PRO_API_KEY": COIN_MARKET_TOKEN}

    response = requests.get(url, params=params, headers=headers)
    if response.status_code != 200:
        return {"error": response.status_code}

    data = response.json()
    return data["data"][0]


def check_coin_price_or_status_code(coin_id: int | str) -> dict:
    url = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest"
    params = {"id": coin_id}
    headers = {"Accepts": "application/json", "X-CMC_PRO_API_KEY": COIN_MARKET_TOKEN}

    response = requests.get(url, params=params, headers=headers)
    if response.status_code != 200:
        return {"error": response.status_code}

    data = response.json()
    return {"price": data["data"][coin_id]["quote"]["USD"]["price"]}
