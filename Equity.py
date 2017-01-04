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
    prevNDayCandles = []        # List of N Candle
    prevNPeriodCandles = []     # List of N period candle
    prevDayCls = 0.0
    averageFluctuationOfDay = 0.0
    pip = 0.0                   # Average one day fluctuation / 100
    
    buyPrice = None
    sellPrice = None
    stopLoss = None
    qauntity = None
    

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

        # update candle list on every 1 minute
        self.update_candle_list_thread(
            timeIntervalToUpdateList=60, candleInterval=Candle.Interval.MIN)
        
      
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

    def update_candle_list_thread(self, timeIntervalToUpdateList, candleInterval):
        " Thread function to update candle list every time interval"
        candle = self.get_updated_candle(interval=candleInterval)
        if candle != None:
            print "updating", self.symbol, "candle list"    
        
        # Check for duplicate candle
        if self.prevNPeriodCandles != []:
            lastCandle = self.prevNPeriodCandles[len(self.prevNPeriodCandles)-1]
            if candle != lastCandle:    
                candle.no = lastCandle.no + 1
                self.prevNPeriodCandles.append(candle)
        else:
            candle.no = 0
            self.prevNPeriodCandles.append(candle)        

        # Schedule for next candle
        threading.Timer(
            timeIntervalToUpdateList - 0.01, self.update_candle_list_thread, [timeIntervalToUpdateList, candleInterval]).start()

    def buy_and_sell(self, buyPrice=None, sellPrice=None, qauntity = 1, stopLoss=None, isSquareOff=False):
        isStartStopLossHandler = False        
        # First buy
        if self.buyPrice == None and buyPrice != None and isSquareOff == False:
            self.buyPrice = buyPrice
            self.stopLoss = stopLoss
            self.qauntity = qauntity
            isStartStopLossHandler = True
        # First sell    
        elif self.sellPrice == None and sellPrice != None and isSquareOff == False :    
            self.sellPrice = sellPrice
            self.stopLoss = stopLoss
            self.qauntity = qauntity
            isStartStopLossHandler = True
        # Square off already bought/sold
        else:
            # Sell, already bought
            if self.buyPrice != None :
                self.sellPrice = sellPrice
            # Buy, already sold
            else:
                self.buyPrice = buyPrice
            isStartStopLossHandler = False
            
            # get profit/loss entry
            "".center(150,"-")
            print "Buy =",self.buyPrice," Sell =", self.sellPrice," Quantity =", self.qauntity," P&L = ",self.sellPrice-self.buyPrice
            "".center(150,"-")
            # NULL all data
            self.buyPrice=self.sellPrice=self.stopLoss=self.qauntity=None
            
        self.stop_loss_handler_thread( isStartStopLossHandler, timeInterval=5)
            
    def stop_loss_handler_thread(self, timeInterval=5, isStartStopLossHandler=True):
        " Thread function to watch stop loss hit every time interval"
        if isStartStopLossHandler == False:
            return

        currPrice = self.get_current_price()
        
        if (currPrice+self.pip) >= self.stopLoss and self.stopLoss >= (currPrice-self.pip) :
            # Square Off
            self.buy_and_sell(isSquareOff=True)
        else:
            threading.Timer(
                timeInterval - 0.01, self.stop_loss_handler_thread, [timeInterval, isStartStopLossHandler]).start()

    def get_average_fluctuation_of_N_day(self, N=30):
        " Average of 30 day max movement "
        sumOfNDayFluctuation = 0.0

        for i, candle in enumerate(self.prevNDayCandles):
            sumOfNDayFluctuation += candle.maxFluctuation
            if i == N - 1:
                break

        oneDayFluctuation = sumOfNDayFluctuation / N

        return oneDayFluctuation

    def get_pip(self):
        return self.pip

    # TODO repair sequence problem
    def get_updated_N_HeikinAshi_candle(self, N=4):
        '''
            - We consider only last(recent) N candles
        '''
        noOfCandles = len(self.prevNPeriodCandle)
        
        if noOfCandles < N:
            print "There is no enough candle you requested"
            return []
        
        print "noOfCandles\t=", noOfCandles
        prevNHeinkinAshiCandles = []
        prevNPeriodCandles = self.prevNPeriodCandles[noOfCandles-N : ]
        
        if len(prevNPeriodCandles) == N:
            print "=========================================get requested candles"
        
        normalPrevCandle = prevNPeriodCandles[0]
        
        for normalCurrCandle in prevNPeriodCandles:
            
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

            #print "Normal Candle\t=", normalCurrCandle
            #print "Heikin Ashi\t=", heikinAshiCandle
            prevNHeinkinAshiCandles.append(heikinAshiCandle)
            
            normalPrevCandle = normalCurrCandle
            
        return prevNHeinkinAshiCandles
