'''
Created on Dec 31, 2016
@author: Vishal Chovatiya
@note:    Candle Data
    - date
    - time
    - close
    - high
    - open
    - low
    - color
    - timeFrame - 1 min, 3 min, 5 min, 10 min, 15 min, 1 hour, 1 day
    
'''

GREEN = 'G'
RED = 'R'


class Interval(object):
    MIN = 1 * 60    # 60 second
    THREE_MIN = 3 * MIN
    FIVE_MIN = 5 * MIN
    TEN_MIN = 10 * MIN
    TEN_MIN = 10 * MIN
    FIFTEEN_MIN = 10 * MIN
    ONE_HOUR = 60 * MIN
    DAY = 250000
    NOT_SPECIFIED = 0


class Candle(object):

    def __init__(self, date="", time="", closeP=0.0, highP=0.0, lowP=0.0, openP=0.0, volume=0, timeFrame=Interval.NOT_SPECIFIED):
        self.date = date
        self.time = time
        self.timeFrame = timeFrame
        self.closeP = closeP
        self.highP = highP
        self.lowP = lowP
        self.openP = openP
        self.volume = volume

        self.color = GREEN if closeP - openP > 0.0 else RED
        self.precentageChange = 0.0

    def __repr__(self):
        return "date:{:>11}   time:{:>9}   open:{:06.2f}   high:{:06.2f}   low:{:06.2f}   close:{:06.2f}   volume:{:10d}   color:{:>2}".format(self.date, self.time, self.openP, self.highP, self.lowP, self.closeP, self.volume, self.color)
