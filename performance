import csv
import statistics
import datetime


# ----------------------------------------------------------------------------------------------------------------------------------------------------
def change(startPrice, currentPrice):
    currentPrice = float(currentPrice)
    startPrice = float(startPrice)
    return (((currentPrice) - startPrice) / startPrice) * 100


def dateToString(mydate):
    mydate = str(mydate).split(' ')
    mydate = mydate[0]
    mydate = mydate.split('-')
    mydate.reverse()
    mydate = '-'.join(mydate)
    return mydate


def stringToDate(mydate):
    mydate = mydate.split('-')
    mydate = datetime.date(int(mydate[2]), int(mydate[1]), int(mydate[0]))

    return mydate


def isLeapYear(year):
    if year % 400 == 0:
        return True
    elif year % 100 == 0:
        return False
    elif year % 4 == 0:
        return True


def getPricesYear(prices, dates, year):
    myprices = []
    mydates = []
    data = {}

    for i, date in enumerate(dates):
        if int(date[6:]) == year:
            myprices.append(prices[i])
            mydates.append(date)
    data['prices'] = myprices
    data['dates'] = mydates

    return data


def getPricesPeriod(prices, dates, startDate, endDate):
    startDate = dateToString(startDate)
    endDate = dateToString(endDate)

    data = {}

    start_index = dates.index(startDate)
    end_index = dates.index(endDate)
    myprices = prices[start_index:end_index + 1]
    mydates = dates[start_index:end_index + 1]

    data['prices'] = myprices
    data['dates'] = mydates

    return data


# END OF AUXILIARY FUNCTIONS
# ----------------------------------------------------------------------------------------------------------------------------------------------------
# Year to date for all the data provided
def newYearToDate(prices, dates):
    ytd = []
    for date in dates:
        try:
            if date == '01-01-' + date[6:]:
                ytd.append(0.0)
                continue
            startDate = dates.index('01-01-' + date[6:])
            startPrice = prices[startDate]
            endPrice = prices[dates.index(date)]

            ytd.append(change(startPrice, endPrice))
        except:
            ytd.append(None)

    return ytd


# Year to date for a particular year
def YearToDate(prices, dates, year):
    years = []
    try:
        startDate = '01-01-' + str(year)
        startPrice = prices[dates.index(startDate)]
    except:
        return [None]

    ytd = []

    try:
        endDate = '31-12-' + str(year)
        for price in prices[dates.index(startDate):dates.index(endDate) + 1]:
            ytd.append(change(startPrice, price))
    except:
        for price in prices[dates.index(startDate):]:
            ytd.append(change(startPrice, price))

    return ytd


# ----------------------------------------------------------------------------------------------------------------------------------------------------
# Annualized return for a particular year
def annualizedReturnYear(prices, dates, year):
    ytd = YearToDate(prices, dates, year)
    annualized = []
    try:
        for i in range(len(ytd)):
            try:
                solution = (ytd[i] * 365) / i
                annualized.append(str((solution)))
            except ZeroDivisionError:
                annualized.append(None)
        return annualized
    except:
        return None


def annualizedReturn(prices, dates):
    ytd = newYearToDate(prices, dates)
    currentYear = dates[0][6:]
    days = 0
    annualized = []

    for i in range(len(ytd)):
        if ytd[i] == None:
            annualized.append(None)

        elif dates[i][6:] == currentYear:
            try:
                value = (ytd[i] * 365) / days
            except ZeroDivisionError:
                value = 0
            days += 1
            annualized.append(value)

        else:
            currentYear = dates[i][6:]
            days = 0
            try:
                value = (ytd[i] * 365) / days
            except ZeroDivisionError:
                value = 0
            days += 1
            annualized.append(value)
    return annualized


def monthlyReturns(prices, dates):
    days = []
    returns = []
    currentMonth = dates[0][3:5]
    for date in dates:
        if date[3:5] == currentMonth:
            days.append(prices[dates.index(date)])
        else:
            try:
                returns.append(change(days[0], days[-1]))
            except:
                print(f'{days[0]} and {days[-1]}')
                returns.append(None)
            days = []
            currentMonth = date[3:5]
            days.append(prices[dates.index(date)])

    returns.append(change(days[0], days[-1]))
    return returns


# Monthly returns for a specific year
def monthlyReturnsYear(prices, dates, year):
    days = []
    returns = []
    currentMonth = dates[0][3:5]
    for date in dates:
        if not (int(date[6:]) == year): continue
        if date[3:5] == currentMonth:
            days.append(prices[dates.index(date)])
        else:
            try:
                returns.append(change(days[0], days[-1]))
            except:
                pass
            days = []
            currentMonth = date[3:5]
            days.append(prices[dates.index(date)])
    try:
        returns.append(change(days[0], days[-1]))
    except:
        return None
    return returns


def monthlyReturnsFromInception(prices, dates):
    # print(f"prices:{prices}\ndates:{dates}")
    index_value = 0
    startPrice = prices[index_value]
    days = []
    returns = []
    currentMonth = dates[0][3:5]
    for date in dates:
        if date[3:5] == currentMonth:
            days.append(prices[dates.index(date)])
        else:
            try:
                returns.append(change(startPrice=startPrice, currentPrice=days[-1]))
            except:
                returns.append(None)
            days = []
            currentMonth = date[3:5]
            days.append(prices[dates.index(date)])

    returns.append(change(startPrice=startPrice, currentPrice=days[-1]))
    return returns

def monthsFromInception(prices, dates):
    months = []
    for date in dates:
        if date[3:] not in months:
            months.append(date[3:])
    return months


# Returns for numberOfMonths before a given date
def periodicReturns(prices, dates, day, month, year, numberOfMonths):
    currentDate = datetime.date(year, month, day)
    currentDate = dateToString(currentDate)
    if month - numberOfMonths < 1:
        year -= 1
        new_month = (month - numberOfMonths + 12)
    else:
        new_month = month - numberOfMonths

    new_day = day
    if new_month == 2 and day > 29: new_day = 29
    while True:
        try:
            if new_day < 1: return None
            mydate = datetime.date(year, new_month, new_day)
            mydate = dateToString(mydate)
            startPrice = prices[dates.index(mydate)]
            break
        except:
            new_day -= 1

    endPrice = prices[dates.index(currentDate)]
    # print(f"start:{startPrice} and end:{endPrice}")
    # print(f"start:{mydate} and end:{currentDate}")

    return change(startPrice=startPrice, currentPrice=endPrice)


# def periodicReturns(prices,dates,day,month,year,numberOfMonths):
#     currentDate = datetime.date(year,month,day)
#     currentDate = dateToString(currentDate)
#     if month - numberOfMonths < 1:
#         year-=1
#         new_month = (month - numberOfMonths + 12)
#     else:
#         new_month = month - numberOfMonths

#     if new_month == 2 and day > 29: day = 29
#     try:
#         mydate = datetime.date(year,new_month,day)
#         mydate = dateToString(mydate)
#         startPrice = prices[dates.index(mydate)]
#     except:
#         try:
#             mydate = datetime.date(year,new_month, day-1)
#             mydate = dateToString(mydate)
#             startPrice = prices[dates.index(mydate)]
#         except:
#             return None
#     try:
#         endPrice = prices[dates.index(currentDate)]
#     except:
#         return None
#     return change(startPrice=startPrice,currentPrice=endPrice)
# ----------------------------------------------------------------------------------------------------------------------------------------------------
def oneMonthReturn(prices, dates, day, month, year):
    return periodicReturns(prices=prices, dates=dates, day=day, month=month, year=year, numberOfMonths=1)


def twoMonthReturn(prices, dates, day, month, year):
    return periodicReturns(prices=prices, dates=dates, day=day, month=month, year=year, numberOfMonths=2)


def threeMonthReturn(prices, dates, day, month, year):
    return periodicReturns(prices=prices, dates=dates, day=day, month=month, year=year, numberOfMonths=3)


def sixMonthReturn(prices, dates, day, month, year):
    return periodicReturns(prices=prices, dates=dates, day=day, month=month, year=year, numberOfMonths=6)


def oneYearReturn(prices, dates, day, month, year):
    return periodicReturns(prices=prices, dates=dates, day=day, month=month, year=year, numberOfMonths=12)


# ----------------------------------------------------------------------------------------------------------------------------------------------------
# Average return for a particular year
def averageReturnYear(prices, dates, year):
    returns = monthlyReturnsYear(prices=prices, dates=dates, year=year)
    try:
        average = statistics.mean(returns)
    except:
        average = None

    return average


def averageGainYear(prices, dates, year):
    returns = monthlyReturnsYear(prices=prices, dates=dates, year=year)
    gains = []
    for value in returns:
        if value > 0: gains.append(value)
    try:
        average = statistics.mean(gains)
    except:
        average = 0
    return average


def averageLossYear(prices, dates, year):
    returns = monthlyReturnsYear(prices=prices, dates=dates, year=year)
    losses = []
    for value in returns:
        if value < 0: losses.append(value)
    try:
        average = statistics.mean(losses)
    except:
        average = 0
    return average


# ----------------------------------------------------------------------------------------------------------------------------------------------------
def averageReturnPeriod(prices, dates, startDate, endDate):
    startDate = dateToString(startDate)
    endDate = dateToString(endDate)

    months = monthsFromInception(prices, dates)
    days = []
    returns = []

    mr = monthlyReturns(prices, dates)
    mr = mr[months.index(startDate[3:]):months.index(endDate[3:]) + 1]
    avgReturn = statistics.mean(mr)
    return avgReturn


def averageGainPeriod(prices, dates, startDate, endDate):
    startDate = dateToString(startDate)
    endDate = dateToString(endDate)

    months = monthsFromInception(prices, dates)
    gains = []

    mr = monthlyReturns(prices, dates)

    print(f'\n{mr}')
    mr = mr[months.index(startDate[3:]):months.index(endDate[3:]) + 1]
    print(f'\n{mr}')

    for value in mr:
        if value > 0:
            gains.append(value)
    try:
        avgGain = statistics.mean(gains)
    except:
        avgGain = None
    return avgGain


def averageLossPeriod(prices, dates, startDate, endDate):
    startDate = dateToString(startDate)
    endDate = dateToString(endDate)

    months = monthsFromInception(prices, dates)
    days = []
    losses = []

    mr = monthlyReturns(prices, dates)
    mr = mr[months.index(startDate[3:]):months.index(endDate[3:]) + 1]

    for value in mr:
        if value < 0:
            losses.append(value)
    try:
        avgLoss = statistics.mean(losses)
    except:
        avgLoss = None
    return avgLoss


# ----------------------------------------------------------------------------------------------------------------------------------------------------

def averageReturn(prices, dates):
    returns = monthlyReturns(prices=prices, dates=dates)
    try:
        average = statistics.mean(returns)
    except:
        average = None
    return average


def averageGain(prices, dates):
    returns = monthlyReturns(prices=prices, dates=dates)
    gains = []
    for value in returns:
        if value > 0: gains.append(value)
    try:
        average = statistics.mean(gains)
    except:
        average = 0
    return average


def averageLoss(prices, dates):
    returns = monthlyReturns(prices=prices, dates=dates)
    losses = []
    for value in returns:
        if value < 0: losses.append(value)
    try:
        average = statistics.mean(losses)
    except:
        average = 0
    return average


def compoundAverageReturn(prices, dates):
    vami = VAMI(prices, dates)
    compoundMonthlyROR = ((vami[-1] / 1000)) ** (1 / len(vami)) - 1

    return compoundMonthlyROR * 100


def compoundAnnualizedROR(prices, dates):
    monthly = compoundAverageReturn(prices, dates)
    annualized = ((1 + (monthly / 100)) ** (12)) - 1

    return annualized * 100


def compoundAverageReturnYear(prices, dates, year):
    vami = VAMIYear(prices, dates, year)
    try:
        compoundMonthlyROR = ((vami[-1] / 1000)) ** (1 / len(vami)) - 1
    except:
        return None
    return compoundMonthlyROR * 100


def compoundAverageReturnPeriod(prices, dates, startDate=None, numberOfMonths=None):
    vami = VAMIPeriod(prices=prices, dates=dates, startDate=startDate, numberOfMonths=numberOfMonths)
    if numberOfMonths > len(vami): return None
    compoundMonthlyROR = ((vami[-1] / 1000)) ** (1 / len(vami)) - 1

    return compoundMonthlyROR * 100


'''
def compoundAnnualizedROR(prices,dates,year):
    monthlyROR = compoundAverageReturnYear(prices,dates,year)
    caror = ((1+monthlyROR)**(1/12)) - 1
    return caror
'''


# ----------------------------------------------------------------------------------------------------------------------------------------------------
def dailyReturnsFromInception(prices):
    startPrice = prices[0]
    returns = []
    for endPrice in prices:
        returns.append(change(startPrice, endPrice))
    return returns


# Value Added Monthly Index from inception
def VAMI(prices, dates):
    returns = monthlyReturnsFromInception(prices, dates)
    values = []
    for value in returns:
        vami = (1 + (value / 100)) * 1000
        values.append(vami)

    return values


# Value Added Monthly Index for a given year
def VAMIYear(prices, dates, year):
    returns = monthlyReturnsYear(prices, dates, year)
    values = []
    for value in returns:
        vami = (1 + (value / 100)) * 1000
        values.append(vami)

    return values


# Value Added Monthly Index for a number of months after a given start date
def VAMIPeriod(prices, dates, startDate=None, numberOfMonths=None):
    if numberOfMonths == 0:
        return [1000]

    if startDate != None:
        my_prices = prices[dates.index(dateToString(startDate)):]
        my_dates = dates[dates.index(dateToString(startDate)):]

    else:
        my_prices = prices
        my_dates = dates

    returns = monthlyReturnsFromInception(my_prices, my_dates)
    if numberOfMonths == None:
        end_index = len(returns)
    else:
        end_index = numberOfMonths
        returns = returns[:end_index]

    values = []
    vami = 1000
    for value in returns:
        vami = (1 + (value / 100)) * 1000
        values.append(vami)

    return values


# ----------------------------------------------------------------------------------------------------------------------------------------------------
def showResults(prices, dates, filename):
    myDay = 19
    myMonth = 3
    myYear = 2021
    vami_months = 1
    numberOfMonths = 17

    startDate = datetime.date(2020, 1, 1)
    endDate = datetime.date(2021, 5, 31)

    print(f"====PERFORMANCE ANALYTICS FOR {filename}====")

    # writeToFile(prices=prices,dates=dates,ytd=newYearToDate(prices,dates),annualized=annualizedReturn(prices=prices,dates=dates),incepttion=dailyReturnsFromInception(prices))
    # print(f'\nYear to Date:\n{newYearToDate(prices,dates)}')
    # print(f'\nAnnualized:\n{annualizedReturn(prices,dates)}')
    print(f'\n3 month return: {threeMonthReturn(prices, dates, myDay, myMonth, myYear)}')
    print(f'\n6 month return: {sixMonthReturn(prices, dates, myDay, myMonth, myYear)}')
    print(f'\n1 year return: {oneYearReturn(prices, dates, myDay, myMonth, myYear)}')
    print(f'\nMonthly returns\n{monthlyReturns(prices, dates)}')
    print(f'\nAverage Return: {averageReturn(prices, dates)}')
    print(f'\nAverage Gain: {averageGain(prices, dates)}')
    print(f'\nAverage Loss: {averageLoss(prices, dates)}')
    print(f'\nCompound average return: {compoundAverageReturn(prices, dates)}')
    print(f'\nVAMI\n{VAMI(prices, dates)}')

    # print(f'\nMonthly returns\n{monthlyReturns(prices,dates)}')
    # print(f'\nMonthly returns\n{monthlyReturnsYear(prices,dates,myYear)}')
    # print(f'\nMonthly returns\n{monthlyReturnsFromInception(prices,dates)}')

    # print(f'\nYear to Date:\n{YearToDate(prices,dates,myYear)}')
    # print(f'\nAnnualized:\n{annualizedReturnYear(prices,myYear)}')
    # print(f'\nAverage Return: {averageReturnPeriod(prices,dates,startDate=startDate,endDate=endDate)}')
    # print(f'\nAverage Gain: {averageGainPeriod(prices,dates,startDate=startDate,endDate=endDate)}')
    # print(f'\nAverage Loss: {averageLossPeriod(prices,dates,startDate=startDate,endDate=endDate)}')
    # print(f'\nCompound average return: {compoundAverageReturnPeriod(prices,dates,startDate=startDate,numberOfMonths=numberOfMonths)}')
    # print(f'\nVAMI\n{VAMIPeriod(prices,dates,startDate=startDate,numberOfMonths=numberOfMonths)}')

    # print(f'\nVAMI\n{VAMIYear(prices,dates,myYear)}')
    # print(f'\nAverage Return: {averageReturnYear(prices,dates,myYear)}')