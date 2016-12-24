'''
Created on Dec 25, 2016
@author: Vishal Chovatiya
'''
from Communicator import URL


class NSEdata:
    " Extract Data From NSE Server "
    # Not Used Now
    get_quote_url = 'http://nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?'
    advances_declines_url = 'http://www.nseindia.com/common/json/indicesAdvanceDeclines.json'

    # In Use
    stocks_csv_url = 'http://www.nseindia.com/content/equities/EQUITY_L.csv'
    top_gainer_url = 'http://www.nseindia.com/live_market/dynaContent/live_analysis/gainers/niftyGainers1.json'
    top_loser_url = 'http://www.nseindia.com/live_market/dynaContent/live_analysis/losers/niftyLosers1.json'
    index_url = "http://www.nseindia.com/homepage/Indices1.json"

    NSE_stock_list = None

    def __init__(self):
        " Initialize NSE Listed Comapny Entries"
        self.NSE_stock_list = self.get_stock_list()

    def get_stock_list(self):
        " Get Stock List Traded On NSE"
        url = URL.URLprocessor(self.stocks_csv_url)
        return url.response

    def get_top_gainer(self):
        " Today's Top Gainer "
        url = URL.URLprocessor(self.top_gainer_url)
        return url.response

    def get_top_loser(self):
        " Today's Top Looser "
        url = URL.URLprocessor(self.top_loser_url)
        return url.response

    def get_indices(self):
        " Get Data Of Index "
        url = URL.URLprocessor(self.index_url)
        return url.response

    def is_valid_stock(self, symbol):
        " Check For Valid NSE Entry"
        if symbol:
            if symbol.upper() in self.NSE_stock_list:
                return True
            else:
                return False

    # TODO
    def is_market_open(self):
        pass
