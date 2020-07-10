from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.utils import iswrapper # just for decorator
from ibapi.contract import Contract
from ibapi.common import BarData
from utils import error_handle

import datetime

class TestApp(EWrapper, EClient):
    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)

    @iswrapper
    def nextValidId(self, orderId:int):
        #4 first message received is this one
        # print("setting nextValidOrderId: %d", orderId)
        self.nextValidOrderId = orderId
        #5 start requests here
        self.start()

    @iswrapper
    def historicalData(self, reqId:int, bar: BarData):
        #7 data is received for every bar
        print("HistoricalData. ReqId:", reqId, "Date:", bar.date, "Open:", bar.high,
              "High:", bar.open, "Low:", bar.low, "Close:", bar.close, "Volume:", bar.volume,
              "TradeCount:", bar.barCount, "WeightAvgPrice:", bar.average)

    def historicalDataEnd(self, reqId: int, start: str, end: str):
        #8 data is finished
        print("HistoricalDataEnd. ReqId:", reqId, "from", start, "to", end)
        #9 this is the logical end of your program
        self.disconnect()

    @iswrapper
    def error(self, reqId, errorCode, errorString):
        if error_handle(errorCode):
            self.done = True

    def start(self):
        queryTime = (datetime.datetime.today() - datetime.timedelta(days=3)).strftime("%Y%m%d %H:%M:%S")

        contract = Contract()
        contract.secType = "CASH"
        contract.symbol = "USD"
        contract.currency = "JPY"
        contract.exchange = "IDEALPRO"

        # contract = Contract()
        # contract.symbol = "FB"
        # contract.secType = "STK"
        # contract.currency = "USD"
        # contract.exchange = "SMART"
        # contract.primaryExchange = 'NASDAQ'

        #6 request data, using fx data because its free on demo
        self.reqHistoricalData(1004, contract, queryTime,
                              "1 D", "1 day", "MIDPOINT", 1, 1, False, [])

def main():
    app = TestApp()
    app.connect("127.0.0.1", 7497, clientId=100) #2 connect to TWS/IBG
    app.run() #3 start message thread

if __name__ == "__main__":
    main()