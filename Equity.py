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
    prevNDayCandles = []      # List of N Candle
    prevNPeriodCandles = []     # List of N period candle
    prevDayCls = 0.0
    averageFluctuationOfDay = 0.0
    pip = 0.0                   # Average one day fluctuation / 100

    def __init__(self, symbol, candlePeriod=60):
        " Initialize symbol, previous 30 day data, previous day close"
        self.symbol = symbol
        self.prevNDayCandles = self.get_previous_Nth_day_candle(day=30)
        self.averageFluctuationOfDay = self.get_average_fluctuation_of_N_day(
            N=30)
        self.pip = self.averageFluctuationOfDay / 100

        try:
            # In case there is empty list
            self.prevDayCls = self.prevNDayCandles[-1].closeP
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

    def get_prev_N_period_candle(self):
        return self.prevNPeriodCandles

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
            return self.prevNDayCandles

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
            print "updating ", self.symbol, " candle list every minute"
            candle = self.get_updated_candle(interval=Candle.Interval.MIN)

            self.prevNPeriodCandles.append(candle)
            time.sleep(timeInterval - 0.01)

    def get_average_fluctuation_of_N_day(self, N=30):
        " Average of 30 day max movement "
        sumOfNDayFluctuation = 0.0

        for i, candle in enumerate(self.prevNDayCandles):
            sumOfNDayFluctuation += abs(candle.highP - candle.lowP)
            if i == N - 1:
                break

        oneDayFluctuation = sumOfNDayFluctuation / N

        return oneDayFluctuation

    def get_pip(self):
        return self.pip
