import binanceAPI as BN_config

from binance.client import Client
from datetime import datetime
import pandas as pd
import re

if BN_config.isConfigExisted():
    BN_config.updateKeyAndSecret()

client = Client(BN_config.API_KEY, BN_config.API_SECRET)

# currently Binance only support the following quote asset class
# BTC|BNB|ETH|TRX|XRP|USDT|BUSD|AUD|BRL|EUR|GBP|RUB|TRY|TUSD|USDC|BIDR|DAI|IDRT|PAX|UAH|NGN|VAI|BVND
# reference: https://www.binance.com/en/trade-rule
support_market_key_list = [ "USDT", "BTC", "ETH", "BNB",
                        "BUSD", "TUSD", "USDC","TRX", 
                        "XRP", "AUD", "BRL", "EUR",  
                        "GBP", "RUB", "TRY", "BIDR", 
                        "DAI", "IDRT", "PAX", "UAH", 
                        "NGN", "VAI", "BVND" ]

coinPair_dict = { } # all market pair
support_market_dict = {}
for market in support_market_key_list:
        support_market_dict[market] = { }

def updateClient():
    global client
    client = Client(BN_config.API_KEY, BN_config.API_SECRET)
    # when API set, API_KEY and API_SECRET is also setting.
    # so we update client settings
    
def getAccountBalances():
    info = client.get_account()
    return info["balances"]

def getBinanceKLines_DataFame(coinSymbol, keepTime):
    if keepTime == "All history":
        candles = client.get_historical_klines(symbol=coinSymbol, interval=Client.KLINE_INTERVAL_1WEEK, start_str="1 Jan, 2017")
    else:
        if keepTime == "1 Hour": # see candlestick chart in a past hour
            kline_interval = Client.KLINE_INTERVAL_1MINUTE
            amount = 60
        elif keepTime == "1 Day": # see candlestick chart in a past day
            kline_interval = Client.KLINE_INTERVAL_15MINUTE
            amount = 96
        elif keepTime == "1 Week": # see candlestick chart in a past week
            kline_interval = Client.KLINE_INTERVAL_1HOUR
            amount = 168
        elif keepTime == "1 Month": # see candlestick chart in a past month
            kline_interval = Client.KLINE_INTERVAL_4HOUR
            amount = 186
        elif keepTime == "1 Year": # see candlestick chart in a past year
            kline_interval = Client.KLINE_INTERVAL_1DAY
            amount = 365

        candles = client.get_klines(symbol=coinSymbol, interval=kline_interval, limit=amount)
        
    candles_dataFrame = pd.DataFrame(candles)

    candles_dataFrame_date = candles_dataFrame[0]

    final_dates = []
    for d in candles_dataFrame_date:
        date = datetime.fromtimestamp(int(d/1000)) # from UNIX time to YYYY-MM-DD hh:mm:ss
        final_dates.append(date)

    candles_dataFrame.pop(0)
    candles_dataFrame.pop(11)

    dataFrame_last_dates = pd.DataFrame(final_dates)
    dataFrame_last_dates.columns = ["date"]

    final_dataFrame = candles_dataFrame.join(dataFrame_last_dates)
    final_dataFrame.set_index("date", inplace=True)
    final_dataFrame.columns = ["open", "high", "low", "close", "volume", "close_time", "asset_volume", "trade_number", "taker_buy_base", "taker_buy_quote"]

    for item in final_dataFrame:
        if not item == "trade_number":
            final_dataFrame[item] = final_dataFrame[item].astype(float)

    return final_dataFrame

def getPrice(symbol):
    prices = client.get_all_tickers()
    for p in prices:
        if symbol == p["symbol"]:
            result = p["price"].rstrip('0').rstrip('.')
            # using string.rstrip(xxxx)
            # remove all xxxx characters in the most right of string
            # (removing any trailing zeros)

            return result

def getSymbolsPair(coinSymbol):
    for market in support_market_key_list:
        regex = "^(\w+)({})$".format(market)
        symbols = re.search(regex, coinSymbol)
        if symbols:
            part1 = symbols.group(1)
            part2 = symbols.group(2)
            return f"{part1} / {part2}"  

def getAllCoinPair():
    global coinPair_dict
    tickers = client.get_all_tickers()

    for tick in tickers:
        for market in support_market_key_list:
            regex = "^(\w+)({})$".format(market)
            if re.search(regex, tick["symbol"]):
                symPair = getSymbolsPair(tick["symbol"])
                support_market_dict[market][symPair] = tick["symbol"]

    # merge dictionary
    for market in support_market_dict.keys():
        coinPair_dict.update(support_market_dict[market])

    return coinPair_dict

def getMarket(marketName):
    if not marketName == "ALL":
        return support_market_dict[marketName]
    
    return coinPair_dict
