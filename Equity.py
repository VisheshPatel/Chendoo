'''
Created on Dec 25, 2016
@author: Vishal Chovatiya
'''
import datetime
import time
import threading
from Communicator import GoogleFinance
from Indicator import Candle


class Share:
    " Data For Particular Script "
    symbol = None               # Company Symbol Name
    currentPrice = None         # Current Price Updated Every Second
    GOOGLEdata = GoogleFinance.GOOGLEdata()  # Communicator Mediator
    prevNthDayCandles = []      # List of Candle
    prevNthPeriodCandles = []
    prevDayCls = 0.0

    def __init__(self, symbol, candlePeriod=60):
        " Initialize symbol, previous 30 day data, previous day close"
        self.symbol = symbol
        self.prevNthDayCandles = self.get_previous_Nth_day_candle(day=30)

        try:
            # In case there is empty list
            self.prevDayCls = self.prevNthDayCandles[-1].closeP
        except:
            print "Unable to update previous day close price"

        try:
            # update candle list on every 1 minute
            t1 = threading.Thread(
                target=self.update_candle_list_thread, args=(candlePeriod,))
            t1.start()
        except:
            print "Unable to start candle thread"

    def get_prev_day_close(self):
        return self.prevDayCls

    def get_prev_Nth_preriod_candle(self):
        return self.prevNthPeriodCandles

    def get_current_price(self):
        dataStr = None

        while dataStr == None:    # Fetch Data Anyhow
            dataStr = self.GOOGLEdata.get_quote(self.symbol)
            if dataStr == None:
                print "Unable to get current price "

        start = dataStr[dataStr.find("\"l\""):]
        value = start[:start.find(",")]
        start = value.split(":")[1]
        price = start[start.find("\"") + 1:]
        price = price[:price.find("\"")]

        return float(price)

    def get_updated_candle(self, day=1, interval=Candle.Interval.MIN):
        " Default data set is of 1 day & 1 minute candle "

        histData = self.GOOGLEdata.get_historical_candle_data(
            self.symbol, day, interval)
        if histData == None:
            print "Unable to updated Nth day candles"

        histData = histData.split("\n")

        while histData != []:
            line = histData.pop()   # Extract from last
            splitLine = line.split(",")
            # print splitLine
            if len(splitLine) == 6:
                candle = Candle.Candle(
                    date=time.strftime("%d-%m-%Y", time.gmtime()),
                    time=time.strftime("%H:%M:%S", time.gmtime()),
                    closeP=float(splitLine[1]),
                    highP=float(splitLine[2]),
                    lowP=float(splitLine[3]),
                    openP=float(splitLine[4]),
                    volume=int(splitLine[5]),
                    timeFrame=interval)

                return candle

        return None

    def get_previous_Nth_day_candle(self, day=0):
        " Get the candle of specified date"
        if day == 0:
            print "returning already filled list"
            return self.prevNthDayCandles

        candleList = []

        histData = self.GOOGLEdata.get_historical_candle_data(
            self.symbol, day)
        if histData == None:
            print "Unable to updated Nth day candles"

        histData = histData.split("\n")

        for line in histData:
            splitLine = line.split(",")
            if len(splitLine) == 6 and "COLUMNS" not in line:
                dateTime = datetime.datetime.fromtimestamp(
                    int(str(splitLine[0][1:]))).strftime('%d-%m-%Y %H:%M:%S')

                dayCandle = Candle.Candle(
                    date=dateTime.split(" ")[0],
                    time=dateTime.split(" ")[1],
                    closeP=float(splitLine[1]),
                    highP=float(splitLine[2]),
                    lowP=float(splitLine[3]),
                    openP=float(splitLine[4]),
                    volume=int(splitLine[5]))

                candleList.append(dayCandle)

        return candleList

    def update_candle_list_thread(self, timeInterval):
        " Thread function to update candle list every time interval"

        while True:
            print "updating ", self.symbol, " candle list"
            candle = self.get_updated_candle(interval=Candle.Interval.MIN)

            self.prevNthPeriodCandles.append(candle)
            time.sleep(timeInterval - 0.01)
