from ibapi import wrapper
from ibapi.client import EClient
from ibapi.utils import iswrapper #just for decorator
from ibapi.common import *
from ibapi.contract import *
from ibapi.ticktype import *

from IB_OrderType import OrderType
from utils import error_handle

class TestApp(wrapper.EWrapper, EClient):
    def __init__(self):
        wrapper.EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)

    def set_order(self, contract, order):
        self.contract = contract
        self.order = order

    @iswrapper
    def nextValidId(self, orderId:int):
        # print("setting nextValidOrderId: %d", orderId)
        self.nextValidOrderId = orderId
        # API starts below
        self.reqMarketDataType(4)
        self.reqMktData(1000, self.contract, "", False, False, [])
        self.placeOrder(self.nextValidOrderId, self.contract, self.order)

    @iswrapper
    def error(self, reqId:TickerId, errorCode:int, errorString:str):
        if error_handle(errorCode):
            self.done = True

    @iswrapper
    def tickPrice(self, reqId: TickerId , tickType: TickType, price: float,
                  attrib:TickAttrib):
        # print("Tick Price. Ticker Id:", reqId, "tickType:", tickType, "Price:", price)
        # API ends and disconnects program because loop finishes
        self.done = True


def main(contract, order):
    app = TestApp()
    app.set_order(contract, order)
    app.connect("127.0.0.1", 7497, clientId=100)
    app.run()

if __name__ == "__main__":
    ticker = "GLD"

    contract = Contract()
    contract.symbol = ticker
    contract.secType = "STK"
    contract.currency = "USD"
    contract.exchange = "SMART"
    contract.primaryExchange = 'NASDAQ'

    market_order = OrderType(type='market', order="BUY", quantity="100").get_order()
    main(contract, market_order)
    print(f"Buying (or Covering) 100 Shares of {ticker}.")