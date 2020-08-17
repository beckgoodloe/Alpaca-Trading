API_KEY = "PK3ANTVU884DPMPA4M64"
SECRET_KEY = "Ks9d1t4bQV4HZtPLx5Op49JUAltP4mPo5nv1nEgt"

BASE_URL_ACCOUNT = "https://paper-api.alpaca.markets"
BASE_URL_MARKET = "https://data.alpaca.markets/v1"
ACCOUNT_URL = "{}/v2/account".format(BASE_URL_ACCOUNT)
ORDERS_URL = "{}/v2/orders".format(BASE_URL_ACCOUNT)
POSITIONS_URL = "{}/v2/positions".format(BASE_URL_ACCOUNT)
LAST_TRADE_URL = "{}/bars".format(BASE_URL_MARKET)
MINUTE_BAR = "{}/v1/bars/minute".format(BASE_URL_ACCOUNT)
QUOTE_URL = "{}/last_quote/stocks/".format(BASE_URL_MARKET)
HEADERS = {'APCA-API-KEY-ID': API_KEY,
           'APCA-API-SECRET-KEY': SECRET_KEY}

STOCKS = ['AMD', 'JPM', 'MXIM', 'SIRI', 'GENE', 'NIO',
          'MRNA', 'AAL', 'SQQQ', 'MBRX', 'F', 'NCLH', 'GE']
# STOCKS = ['NIO']
RISK = 500  # Dollar value of each investment approximately
SELL_MARGIN = .02
