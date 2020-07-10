from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.utils import iswrapper # just for decorator
from ibapi.common import *
from ibapi.contract import *
from ibapi.order import Order
from ibapi.order_state import OrderState
import logging
from utils import error_handle

class TestApp(EWrapper, EClient):
    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)
        self.pending_order = False

    def open_orders(self):
        return self.pending_order

    @iswrapper
    def nextValidId(self, orderId:int):
        # print("setting nextValidOrderId: %d", orderId)

        # API starts below
        self.reqAllOpenOrders()

    @iswrapper
    def error(self, reqId:TickerId, errorCode:int, errorString:str):
        # print("Error. Id: " , reqId, " Code: " , errorCode , " Msg: " , errorString)
        if error_handle(errorCode):
            self.done = True

    @iswrapper
    def openOrder(self, order_id, contract, order, state):
        ''' Called in response to the submitted order '''
        print('Pending order! --- Do not Buy/Sell!')
        print(f"Contract symbol: {contract.symbol}, Status: {state.status}")

    @iswrapper
    def orderStatus(self, order_id, status, filled, remaining,
                    avgFillPrice, permId, parentId, lastFillPrice,
                    clientId, whyHeld, mktCapPrice):
        ''' Check the status of the submitted order '''
        super().orderStatus(order_id, status, filled, remaining,
                            avgFillPrice, permId, parentId, lastFillPrice,
                            clientId, whyHeld, mktCapPrice)

        # print("OrderStatus. Id:", order_id, "Status:", status, "Filled:", filled,
        #       "Remaining:", remaining, "AvgFillPrice:", avgFillPrice,
        #       "PermId:", permId, "ParentId:", parentId, "LastFillPrice:",
        #       lastFillPrice, "ClientId:", clientId, "WhyHeld:",
        #       whyHeld, "MktCapPrice:", mktCapPrice)

        self.pending_order = True
        print(f"Amount Filled: {filled}, Amount Remaining: {remaining}")
        print(f"Average fill price: {avgFillPrice}")

    @iswrapper
    def position(self, account, contract, pos, avgCost):
        ''' Read information about open positions '''
        print('Position in {}: {}'.format(contract.symbol, pos))

    @iswrapper
    def accountSummary(self, req_id, account, tag, value, currency):
        ''' Read information about the account '''
        print('Account {}: {} = {}'.format(account, tag, value))

    @iswrapper
    def openOrderEnd(self):
        super().openOrderEnd()

        # API ends and disconnects program
        self.done = True


def main():
    app = TestApp()
    app.connect("127.0.0.1", 7497, clientId=100)
    app.run()
    return app.open_orders()

if __name__ == "__main__":
    main()