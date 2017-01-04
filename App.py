'''
Created on Dec 25, 2016
@author: Vishal Chovatiya
'''
import Equity
import datetime
import time
import sys
import threading
import schedule
from Communicator import NSE
from Indicator import Candle

now = datetime.datetime.now()
#MARKET_START_TIME = "9:15"
MARKET_START_TIME = "{}:{}".format(now.hour,now.minute+1)
print MARKET_START_TIME
VIRTUAL_MONEY = 5000


def startApp(schedulerMsg):
    print schedulerMsg
    SUNPHARMA = Equity.Share("SUNPHARMA")

    time.sleep(60*4)    # 4 Minute sleep to acquire 4 candles for heikinashi strategy

    greenCandleCnt = 0
    for candle in SUNPHARMA.get_updated_N_HeikinAshi_candle(N=4):
        if candle.color == Candle.GREEN:
            greenCandleCnt += 1
            pass
        
        

def stopApp(schedulerMsg):
    print schedulerMsg
    sys.exit(0)
    
schedule.every().day.at(MARKET_START_TIME).do( startApp, 'App Started')
schedule.every().day.at(MARKET_START_TIME).do( stopApp, 'App Stopped')

while True:    
    schedule.run_pending()
    time.sleep(60)


if __name__ == "__main__":
    pass
