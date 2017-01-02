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
from Strategy import HeikinAshi

virtualMoney = 5000


def App():
    print "App Started"
    SBI = Equity.Share("SBIN")
    SBIHeikinAshi = HeikinAshi.HeikinAshi(SBI)

    greenCandleCnt = 0
    for candle in SBIHeikinAshi.get_updated_N_HeikinAshi_candle(N=4):
        if candle.color == Candle.GREEN:
            greenCandleCnt += 1
            pass

SBI = Equity.Share("SBIN")

print SBI.get_average_fluctuation_of_N_day()
print SBI.get_pip()
# for candle in SBI.get_previous_Nth_day_candle(day=5):
#    print candle

while True:
    print "".center(120, "*")
    # SBI.get_previous_Nth_day_candle(day=5)
    print "".center(120, "*")
    time.sleep(61)
