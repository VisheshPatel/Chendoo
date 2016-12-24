'''
Created on Dec 25, 2016
@author: Vishal Chovatiya
'''
import Equity
import datetime
import time
import schedule
from Communicator import NSE
from Indicator import Candle

print "App Started"
symbol = "SBIN"
SBI = Equity.Share(symbol)

while True:
    print "".center(100, "*")
    for candle in SBI.prevNthPeriodCandles:
        print candle
    print "".center(100, "*")
    time.sleep(1)
