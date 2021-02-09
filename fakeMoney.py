


def resetBalance():
    balance = str(10000)
    f = open('balance.txt', 'w')
    f.write(balance)
    return balance

def getBalance():
    f = open('balance.txt', 'r')
    balance = f.read()

    return balance


def buyBalance(amount):
    currentBalance = float(getBalance()) - amount - 1           #-1 beause of courtage
    f = open('balance.txt', 'w')
    f.write(str(currentBalance))

    return currentBalance

def sellBalance(amount):
    currentBalance = float(getBalance()) + amount - 1           #-1 beause of courtage
    f = open('balance.txt', 'w')
    f.write(str(currentBalance))

    return currentBalance
