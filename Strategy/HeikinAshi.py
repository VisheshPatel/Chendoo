'''
Created on Dec 31, 2016
@author: Vishal Chovatiya
@note: 
    - This is not pure Heikin Ashi chart type, This is strategy
    - we consider only last(recent) N candles
'''

from Equity import Share
import datetime
import time
from Indicator import Candle


class HeikinAshi(object):

    def __init__(self, Share):
        self.Share = Share

    def get_updated_N_HeikinAshi_candle(self, N=4):
        prevNHeinkinAshicandles = []
        prevNPeriodCandles = self.Share.get_prev_N_period_candle()
        noOfCandles = len(prevNPeriodCandles)
        print "noOfCandles\t=", noOfCandles
        i = 0

        if noOfCandles < N:
            print "There is no enough candle you requested"
            return

        while i < N:
            normalCurrCandle = prevNPeriodCandles[noOfCandles - i - 1]
            if noOfCandles - i - 2 < 0:
                normalPrevCandle = normalCurrCandle
            else:
                normalPrevCandle = prevNPeriodCandles[noOfCandles - i - 2]

            heikinAshiCandle = Candle.Candle(
                date=time.strftime("%d-%m-%Y", time.gmtime()),
                time=time.strftime("%H:%M:%S", time.gmtime()),
                closeP=(normalCurrCandle.openP + normalCurrCandle.highP +
                        normalCurrCandle.lowP + normalCurrCandle.closeP) / 4,
                highP=max(
                    normalCurrCandle.openP, normalCurrCandle.highP, normalCurrCandle.closeP),
                lowP=min(
                    normalCurrCandle.openP, normalCurrCandle.lowP, normalCurrCandle.closeP),
                openP=(normalPrevCandle.openP + normalPrevCandle.closeP) / 2,
                volume=normalCurrCandle.volume,
                timeFrame=normalCurrCandle.timeFrame)

            print "Normal Candle\t=", normalCurrCandle
            print "Heikin Ashi\t=", heikinAshiCandle
            i += 1
            prevNHeinkinAshicandles.insert(0, heikinAshiCandle)

        return prevNHeinkinAshicandles
