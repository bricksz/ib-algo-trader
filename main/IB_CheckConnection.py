""" Do not use yet
"""

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.utils import iswrapper # just for decorator
from ibapi.common import *
from ibapi.contract import *
from utils import error_handle


class TestApp(EWrapper, EClient):
    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)

    @iswrapper
    def nextValidId(self, orderId:int):
        # print("setting nextValidOrderId: %d", orderId)
        self.nextValidOrderId = orderId
        self.connectAck()


    @iswrapper
    def error(self, reqId:TickerId, errorCode:int, errorString:str):
        print("Error. Id: " , reqId, " Code: " , errorCode , " Msg: " , errorString)
        # if error_handle(errorCode):
        #     self.done = True

    @iswrapper
    def connectAck(self):
        pass

def main():
    app = TestApp()
    app.connect("127.0.0.1", 7497, clientId=100) #2 connect to TWS/IBG
    print(app.isConnected())
    # app.run() #3 start message thread
    app.disconnect()


if __name__ == "__main__":
    main()