from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.utils import iswrapper # just for decorator
from ibapi.common import *
from ibapi.contract import *
from ibapi.ticktype import *
from utils import error_handle


class TestApp(EWrapper, EClient):
    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)
        self.current_price = 0

    def set_stock_symbol(self,stock):
        self.stock_symbol = stock

    def get_current_price(self):
        return self.current_price

    @iswrapper
    def nextValidId(self, orderId:int):
        print("setting nextValidOrderId: %d", orderId)
        self.nextValidOrderId = orderId

        # API starts below
        contract = Contract()
        contract.symbol = self.stock_symbol
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"
        contract.primaryExchange = 'NASDAQ'
        self.reqMarketDataType(4)   # when using live account, change this
        self.reqMktData(1004, contract, "", False, False, [])

    @iswrapper
    def error(self, reqId:TickerId, errorCode:int, errorString:str):
        if error_handle(errorCode):
            self.done = True

    @iswrapper
    def tickPrice(self, reqId: TickerId , tickType: TickType, price: float,
                  attrib:TickAttrib):
        print("Tick Price. Ticker Id:", reqId, "tickType:", tickType, "Price:", price)
        self.current_price = price
        # API ends and disconnects program because loop finishes
        self.done = True

def main(stock_symbol):
    app = TestApp()
    app.set_stock_symbol(stock_symbol)
    app.connect("127.0.0.1", 7497, clientId=100)
    app.run()
    return app.get_current_price()

if __name__ == "__main__":
    try:
        symbol = "SPY"
        main(symbol)
    except Exception as e:
        print('Missing ticker symbol, defaulting to "SPY"')
        main("SPY")

