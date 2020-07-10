import time
import datetime

def error_handle(errorCode: int):
    """ Error Codes

        Force exit if contain these error code
            1100 - Connectivity between IB and Trader Workstation has been lost.
            502 - No connection to TWS, either sleep for 60 or force quit
            321 - forgot
            354 - forgot
    """
    exit_codes = [502, 321, 354]
    if errorCode in exit_codes:
        print(f"error code: {errorCode}, force quitting...")
        return True
    return False

def error_loop(callback, data):
    for i in range(50):
        if not data:
            time.sleep(0.1)
        else:
            break

def check_trading_hours():
    start_hour = datetime.time(6,0,0)
    end_hour = datetime.time(18,0,0)
    current_time = datetime.datetime.now().time()

    if (current_time > start_hour) and (current_time < end_hour):
        return True
    print("Outside of trading hours.")
    return False