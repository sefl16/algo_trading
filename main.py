import avanza
import json
import time

import apiHelper
import fakeMoney
import strategy


def startBot():
    while True:
        strategy.attemptToMakeTrade()
        time.sleep(30)


startBot()
