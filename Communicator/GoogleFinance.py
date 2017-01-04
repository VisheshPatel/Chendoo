'''
Created on Dec 25, 2016
@author: Vishal Chovatiya
@note: 
    - Current Price URL = http://finance.google.com/finance/info?q=SBI
    - Historical Candle Data URL = https://www.google.com/finance/getprices?q=SBIN&i=60&p=1d&f=d,o,h,l,c,v
    - One Day Data URL interval=250000
    - Google single day data is not accurate(as it not match with zerodha)
    
'''

from Communicator import URL


class GOOGLEdata:
    " Extract Data From Google Finance Server "

    def __init__(self):
        pass

    def get_quote(self, *symbols):
        " Gives You Current Day Candle(i.e High, Low, Open, Close, + Current)"
        current_state_url = 'http://finance.google.com/finance/info?q=' + \
            ','.join([arg for arg in symbols])
        url = URL.URLprocessor(current_state_url)
        return url.response

    def get_historical_candle_data(self, symbol, day=15, interval=250000):
        " One day data URL has interval value 250000"

        historiacal_candle_url = 'https://www.google.com/finance/getprices?q=' + \
            symbol + '&i=' + str(interval) + '&p=' + \
            str(day) + 'd&f=d,o,h,l,c,v'
        url = URL.URLprocessor(historiacal_candle_url)

        return url.response
