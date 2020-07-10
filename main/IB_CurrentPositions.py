from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.utils import iswrapper # just for decorator
from ibapi.common import *
from ibapi.contract import *
from utils import error_handle

import pandas as pd

class TestApp(EWrapper, EClient):
    fname = 'fname.txt'

    def __init__(self):
        EClient.__init__(self, self)
        self.posns = []

    def get_current_position(self):
        return self.posns

    @iswrapper
    def nextValidId(self, orderId:int):
        # print("setting nextValidOrderId: %d", orderId)

        # API starts below
        self.reqPositions()

    @iswrapper
    def error(self, reqId:TickerId, errorCode:int, errorString:str):
        print("Error. Id: " , reqId, " Code: " , errorCode , " Msg: " , errorString)
        if error_handle(errorCode):
            self.done = True

    @iswrapper
    def position(self, account: str, contract: Contract, position: float, avgCost: float):
        self.posns.append((account, contract.symbol, position, avgCost))
        # print(contract.symbol, position)

    @iswrapper
    def positionEnd(self):
        # self.disconnect()
        self.done = True

        # write posns to file or delete file if no positions
        # if self.posns: #means not empty
        #     with open(self.fname, "w") as outfile:
        #         outfile.write('\n'.join(str(posn) for posn in self.posns))
        # else: # no posns so delete file
        #     os.remove(self.fname)

def main():
    app = TestApp()
    app.connect("127.0.0.1", 7497, clientId=100)
    app.run()
    return app.get_current_position()

if __name__ == "__main__":
    accountID = "DU2422130"
    ticker = "SPY"

    all_positions = main()
    df_positions = pd.DataFrame(all_positions,
                                columns=['account', 'symbol', 'position',
                                         'avgCost'])
    df_positions = df_positions[df_positions['account'].isin([accountID])]
    print(df_positions)