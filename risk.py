import statistics
import datetime
import calendar
import performance

#----------------------------------------------------------------------------------------------------------------------------------------------------
def standardDeviation(prices,dates):
    returns = performance.monthlyReturns(prices=prices,dates=dates)
    deviations = 0
    mymean = statistics.mean(returns)
    for value in returns:
        deviations+=(value-mymean)**2
    sd = (deviations/(len(returns)-1))**(0.5)
    # sd = statistics.stdev(returns)
    return sd


def myStandardDeviation(returns,myMean,numberOfPeriods):
    numerators = []
    for value in returns:
        numerators.append((value-myMean)**2)
    sd = (sum(numerators)/(numberOfPeriods))**(0.5)
    return sd


def gainStandardDeviation(prices,dates):
    returns = performance.monthlyReturns(prices=prices,dates=dates)
    gains = []
    for value in returns:
        if value > 0:
            gains.append(value)
    try:
        sd = statistics.stdev(gains)
    except:
        sd = None
    return sd


def lossStandardDeviation(prices,dates):
    returns = performance.monthlyReturns(prices=prices,dates=dates)
    losses = []
    for value in returns:
        if value < 0:
            losses.append(value)
    try:
        sd = statistics.stdev(losses)
    except:
        sd = None
    return sd


def downsideDeviation(prices,dates,minimumAcceptableReturn):
    returns = performance.monthlyReturns(prices=prices,dates=dates)
    values = []
    for value in returns:
        if value < minimumAcceptableReturn:
            values.append(value)
    try:
        sd = myStandardDeviation(values,minimumAcceptableReturn,len(returns))
    except:
        sd = None
    return sd


def semiDeviation(prices,dates):
    returns = performance.monthlyReturns(prices=prices, dates=dates)
    average_return = statistics.mean(returns)
    below_average = []

    for value in returns:
        if value < average_return:
            below_average.append(value)
    
    numerator = 0
    for value in below_average:
        numerator+=(value - average_return)**2

    try:
        sd = (numerator/(len(below_average) - 1))**(0.5)
    except ZeroDivisionError:
        sd = None
    return sd


def sharpeRatio(prices,dates,riskFreeReturn):
    returns = performance.monthlyReturns(prices=prices,dates=dates)
    myMean = statistics.mean(returns)
    sd = statistics.stdev(returns)

    try:
        sr = (myMean - riskFreeReturn)/sd
    except:
        sr = None
    return sr


def sortinoRatio(prices,dates,minimumAcceptableReturn):
    downside_deviation = downsideDeviation(prices,dates,minimumAcceptableReturn)
    compound_period_return = performance.compoundAverageReturn(prices=prices,dates=dates)
    try:
        sortino_ratio = (compound_period_return - minimumAcceptableReturn)/downside_deviation
    except:
        return None
    return sortino_ratio


def skewness(prices,dates):
    returns = performance.monthlyReturns(prices=prices,dates=dates)
    numberOfPeriods = len(returns)

    try:
        standard_deviation = statistics.stdev(returns)
        average_return = statistics.mean(returns)
    except:
        return None
    
    if numberOfPeriods < 3 or standard_deviation == 0:
        return None
    
    numerator = 0
    for value in returns:
        numerator+=(value-average_return)
    
    left = numberOfPeriods/((numberOfPeriods-1)*(numberOfPeriods-2))
    right = (numerator/standard_deviation)**3

    sk = left*right
    return sk


def calmarRatio(prices,dates,year=None):
    if year == None:year = int(dates[-1][6:])
    p1 = performance.getPricesYear(prices,dates,year-2)['prices']
    d1 = performance.getPricesYear(prices,dates,year-2)['dates']

    p2 = performance.getPricesYear(prices,dates,year-1)['prices']
    d2 = performance.getPricesYear(prices,dates,year-1)['dates']

    p3 = performance.getPricesYear(prices,dates,year)['prices']
    d3 = performance.getPricesYear(prices,dates,year)['dates']

    myprices = p1 + p2 + p3
    mydates = d1 + d2 + d3
    caror = performance.compoundAnnualizedROR(prices=myprices,dates=mydates)
    max_drawdown = maxDrawdown(prices=prices)
    try:
        calmar = caror/abs(max_drawdown)
    except ZeroDivisionError:
        calmar = None

    return calmar


def sterlingRatio(prices,dates,year=None):
    if year == None:year = int(dates[-1][6:])
    num_years = 3
    d1 = maxDrawdownYear(prices=prices,dates=dates,year=year)
    d2 = maxDrawdownYear(prices=prices,dates=dates,year=year-1)
    d3 = maxDrawdownYear(prices=prices,dates=dates,year=year-2)

    if d3 == None:
        d3 = 0
        num_years-=1
        p3 = []
        date3 = []
    else:
        p3 = performance.getPricesYear(prices,dates,year-2)['prices']
        date3 = performance.getPricesYear(prices,dates,year-2)['dates']
    
    if d2 == None:
        d2 = 0
        num_years-=1
        p2 = []
        date2 = []
    else:
        p2 = performance.getPricesYear(prices,dates,year-1)['prices']
        date2 = performance.getPricesYear(prices,dates,year-1)['dates']
    
    if d1 == None:
        return None
    else:
        p1 = performance.getPricesYear(prices,dates,year)['prices']
        date1 = performance.getPricesYear(prices,dates,year)['dates']

    average_drawdown = (d1+d2+d3)/num_years
    myprices = p3 + p2 + p1
    mydates = date3 + date2 + date1

    caror = performance.compoundAnnualizedROR(prices=myprices,dates=mydates)
    sterling_ratio = caror/abs(average_drawdown-10)
    return sterling_ratio

def gainToLossRatio(prices,dates):
    avg_gain = performance.averageGain(prices=prices,dates=dates)
    avg_loss = performance.averageLoss(prices=prices,dates=dates)

    try:
        g2l = abs(avg_gain/avg_loss)
    except ZeroDivisionError:
        return None
    return g2l


def profitToLossRatio(prices,dates):
    returns = performance.monthlyReturns(prices=prices,dates=dates)
    profit = 0
    loss = 0
    gain_to_loss = gainToLossRatio(prices,dates)
    for value in returns:
        if value > 0:
            profit+=1
        elif value < 0:
            loss+=1
    
    profit_percent = 100*(profit/len(returns))
    loss_percent = 100*(loss/len(returns))

    try:
        profit_to_loss = (profit_percent/loss_percent)*gain_to_loss
    except ZeroDivisionError:
        return None
    return profit_to_loss

def kurtosis(prices,dates):
    returns = performance.monthlyReturns(prices,dates)
    sd = standardDeviation(prices,dates)

    N = len(returns)

    if len(returns) < 4 or sd == 0:
        return None
    average_return = performance.averageReturn(prices,dates)
    
    return_minus_mean = 0
    for value in returns:
        return_minus_mean+=(value - average_return)
    left = ( (N*(N+1)) / ((N-1)*(N-2)*(N-3)) ) * ((return_minus_mean/sd)**4)
    right = (3*((N-1)**2))/((N-2)*(N-3))
    kurtosis_value = left - right
    return kurtosis_value
#----------------------------------------------------------------------------------------------------------------------------------------------------
def standardDeviationYear(prices,dates,year):
    myprices = performance.getPricesYear(prices=prices,dates=dates,year=year)['prices']
    mydates = performance.getPricesYear(prices=prices,dates=dates,year=year)['dates']
    sd = standardDeviation(prices=myprices,dates=mydates)
    return sd


def gainStandardDeviationYear(prices,dates,year):
    myprices = performance.getPricesYear(prices=prices,dates=dates,year=year)['prices']
    mydates = performance.getPricesYear(prices=prices,dates=dates,year=year)['dates']
    gsd = gainStandardDeviation(myprices,mydates)
    return gsd


def lossStandardDeviationYear(prices,dates,year):
    myprices = performance.getPricesYear(prices=prices,dates=dates,year=year)['prices']
    mydates = performance.getPricesYear(prices=prices,dates=dates,year=year)['dates']
    lsd = lossStandardDeviation(myprices,mydates)
    return lsd


def downsideDeviationYear(prices,dates,minimumAcceptableReturn,year):
    myprices = performance.getPricesYear(prices=prices,dates=dates,year=year)['prices']
    mydates = performance.getPricesYear(prices=prices,dates=dates,year=year)['dates']
    dd = downsideDeviation(prices=myprices,dates=mydates, minimumAcceptableReturn=minimumAcceptableReturn)
    return dd


def semiDeviationYear(prices,dates,year):
    myprices = performance.getPricesYear(prices=prices,dates=dates,year=year)['prices']
    mydates = performance.getPricesYear(prices=prices,dates=dates,year=year)['dates']
    sd = semiDeviation(myprices,mydates)
    return sd


def sharpeRatioYear(prices,dates,riskFreeReturn,year):
    myprices = performance.getPricesYear(prices=prices,dates=dates,year=year)['prices']
    mydates = performance.getPricesYear(prices=prices,dates=dates,year=year)['dates']
    ratio = sharpeRatio(prices=myprices,mydates=dates,riskFreeReturn=riskFreeReturn)
    return ratio


def sortinoRatioYear(prices,dates,minimumAcceptableReturn,year):
    myprices = performance.getPricesYear(prices=prices,dates=dates,year=year)['prices']
    mydates = performance.getPricesYear(prices=prices,dates=dates,year=year)['dates']
    ratio = sortinoRatio(prices=myprices,dates=mydates,minimumAcceptableReturn=minimumAcceptableReturn)
    return ratio


def skewnessYear(prices,dates,year):
    myprices = performance.getPricesYear(prices=prices,dates=dates,year=year)['prices']
    mydates = performance.getPricesYear(prices=prices,dates=dates,year=year)['dates']
    sk = skewness(prices=myprices,dates=mydates)
    return sk


def gainToLossRatioYear(prices,dates,year):
    myprices = performance.getPricesYear(prices=prices,dates=dates,year=year)['prices']
    mydates = performance.getPricesYear(prices=prices,dates=dates,year=year)['dates']
    ratio = gainToLossRatio(prices=myprices,dates=mydates)
    return ratio


def profitToLossRatioYear(prices,dates,year):
    myprices = performance.getPricesYear(prices=prices,dates=dates,year=year)['prices']
    mydates = performance.getPricesYear(prices=prices,dates=dates,year=year)['dates']
    ratio = profitToLossRatio(prices=myprices,dates=mydates)
    return ratio


def drawdownYear(prices,dates,year):
    myprices = performance.getPricesYear(prices=prices,dates=dates,year=year)['prices']
    mydates = performance.getPricesYear(prices=prices,dates=dates,year=year)['dates']
    dd = drawdown(myprices)
    return dd


def losingStreakYear(prices,dates,year):
    myprices = performance.getPricesYear(prices=prices,dates=dates,year=year)['prices']
    mydates = performance.getPricesYear(prices=prices,dates=dates,year=year)['dates']
    streak = losingStreak(prices=myprices,dates=mydates)
    return streak

def kurtosisYear(prices,dates,year):
    myprices = performance.getPricesYear(prices=prices,dates=dates,year=year)['prices']
    mydates = performance.getPricesYear(prices=prices,dates=dates,year=year)['dates']
    kurtosis_value = kurtosis(prices=myprices,dates=mydates)
    return kurtosis_value
#----------------------------------------------------------------------------------------------------------------------------------------------------
def standardDeviationPeriod(prices,dates,startDate=None,endDate=None):
    try:
        if startDate != None:
            startDate = performance.dateToString(startDate)
        else:
            startDate = dates[0]
        
        if endDate != None:
            endDate = performance.dateToString(endDate)
        else:
            endDate = dates[-1]

        myprices = prices[dates.index(startDate):dates.index(endDate)+1]
        mydates = dates[dates.index(startDate):dates.index(endDate)+1]
        return standardDeviation(prices=myprices,dates=mydates)
    except:
        return None

def gainStandardDeviationPeriod(prices,dates,startDate=None,endDate=None):
    try:
        if startDate != None:
            startDate = performance.dateToString(startDate)
        else:
            startDate = dates[0]
        
        if endDate != None:
            endDate = performance.dateToString(endDate)
        else:
            endDate = dates[-1]

        myprices = prices[dates.index(startDate):dates.index(endDate)+1]
        mydates = dates[dates.index(startDate):dates.index(endDate)+1]

        return gainStandardDeviation(prices=myprices,dates=mydates)
    except:
        return None

def lossStandardDeviationPeriod(prices,dates,startDate=None,endDate=None):
    try:
        if startDate != None:
            startDate = performance.dateToString(startDate)
        else:
            startDate = dates[0]
        
        if endDate != None:
            endDate = performance.dateToString(endDate)
        else:
            endDate = dates[-1]

        myprices = prices[dates.index(startDate):dates.index(endDate)+1]
        mydates = dates[dates.index(startDate):dates.index(endDate)+1]

        return lossStandardDeviation(prices=myprices,dates=mydates)
    except:
        return None

def downsideDeviationPeriod(prices,dates,minimumAcceptableReturn,startDate=None,endDate=None):
    try:
        if startDate != None:
            startDate = performance.dateToString(startDate)
        else:
            startDate = dates[0]
        
        if endDate != None:
            endDate = performance.dateToString(endDate)
        else:
            endDate = dates[-1]

        myprices = prices[dates.index(startDate):dates.index(endDate)+1]
        mydates = dates[dates.index(startDate):dates.index(endDate)+1]

        return downsideDeviation(prices=myprices,dates=mydates,minimumAcceptableReturn=minimumAcceptableReturn)
    except:
        return None

def semiDeviationPeriod(prices,dates,startDate=None,endDate=None):
    try:
        if startDate != None:
            startDate = performance.dateToString(startDate)
        else:
            startDate = dates[0]
        
        if endDate != None:
            endDate = performance.dateToString(endDate)
        else:
            endDate = dates[-1]

        myprices = prices[dates.index(startDate):dates.index(endDate)+1]
        mydates = dates[dates.index(startDate):dates.index(endDate)+1]

        return semiDeviation(prices=myprices,dates=mydates)
    except:
        return None

def sharpeRatioPeriod(prices,dates,riskFreeReturn,startDate=None,endDate=None):
    try:
        if startDate != None:
            startDate = performance.dateToString(startDate)
        else:
            startDate = dates[0]
        
        if endDate != None:
            endDate = performance.dateToString(endDate)
        else:
            endDate = dates[-1]

        myprices = prices[dates.index(startDate):dates.index(endDate)+1]
        mydates = dates[dates.index(startDate):dates.index(endDate)+1]

        return sharpeRatio(prices=myprices,dates=mydates,riskFreeReturn=riskFreeReturn)
    except:
        return None

def sortinoRatioPeriod(prices,dates,minimumAcceptableReturn,startDate=None,endDate=None):
    try:
        if startDate != None:
            startDate = performance.dateToString(startDate)
        else:
            startDate = dates[0]
        
        if endDate != None:
            endDate = performance.dateToString(endDate)
        else:
            endDate = dates[-1]

        myprices = prices[dates.index(startDate):dates.index(endDate)+1]
        mydates = dates[dates.index(startDate):dates.index(endDate)+1]

        return sortinoRatio(prices=myprices,dates=mydates,minimumAcceptableReturn=minimumAcceptableReturn)
    except:
        return None

def skewnessPeriod(prices,dates,startDate=None, endDate=None):
    try:
        if startDate != None:
            startDate = performance.dateToString(startDate)
        else:
            startDate = dates[0]
        
        if endDate != None:
            endDate = performance.dateToString(endDate)
        else:
            endDate = dates[-1]

        myprices = prices[dates.index(startDate):dates.index(endDate)+1]
        mydates = dates[dates.index(startDate):dates.index(endDate)+1]

        return skewness(prices=myprices,dates=mydates)
    except:
        return None


def calmarRatioPeriod(prices,dates,startDate=None,endDate=None):
    try:
        if startDate != None:
            startDate = performance.dateToString(startDate)
        else:
            startDate = dates[0]
        
        if endDate != None:
            endDate = performance.dateToString(endDate)
        else:
            endDate = dates[-1]

        myprices = prices[dates.index(startDate):dates.index(endDate)+1]
        mydates = dates[dates.index(startDate):dates.index(endDate)+1]

        return calmarRatio(prices=myprices,dates=mydates)
    except:
        return None

def sterlingRatioPeriod(prices,dates,startDate=None,endDate=None):
    try:
        if startDate != None:
            startDate = performance.dateToString(startDate)
        else:
            startDate = dates[0]
        
        if endDate != None:
            endDate = performance.dateToString(endDate)
        else:
            endDate = dates[-1]

        myprices = prices[dates.index(startDate):dates.index(endDate)+1]
        mydates = dates[dates.index(startDate):dates.index(endDate)+1]

        return sterlingRatio(prices=myprices,dates=mydates)
    except:
        return None

def gainToLossRatioPeriod(prices,dates,startDate=None,endDate=None):
    try:
        if startDate != None:
            startDate = performance.dateToString(startDate)
        else:
            startDate = dates[0]
        
        if endDate != None:
            endDate = performance.dateToString(endDate)
        else:
            endDate = dates[-1]

        myprices = prices[dates.index(startDate):dates.index(endDate)+1]
        mydates = dates[dates.index(startDate):dates.index(endDate)+1]

        return gainToLossRatio(prices=myprices,dates=mydates)
    except:
        return None

def profitToLossRatioPeriod(prices,dates,startDate=None,endDate=None):
    try:
        if startDate != None:
            startDate = performance.dateToString(startDate)
        else:
            startDate = dates[0]
        
        if endDate != None:
            endDate = performance.dateToString(endDate)
        else:
            endDate = dates[-1]

        myprices = prices[dates.index(startDate):dates.index(endDate)+1]
        mydates = dates[dates.index(startDate):dates.index(endDate)+1]

        return profitToLossRatio(prices=myprices,dates=mydates)
    except:
        return None

def kurtosisPeriod(prices,dates,startDate=None, endDate=None):
    try:
        if startDate != None:
            startDate = performance.dateToString(startDate)
        else:
            startDate = dates[0]
        
        if endDate != None:
            endDate = performance.dateToString(endDate)
        else:
            endDate = dates[-1]

        myprices = prices[dates.index(startDate):dates.index(endDate)+1]
        mydates = dates[dates.index(startDate):dates.index(endDate)+1]

        return kurtosis(prices=myprices,dates=mydates)
    except:
        return None


def losingStreakPeriod(prices,dates,startDate=None,endDate=None):
    try:
        if startDate != None:
            startDate = performance.dateToString(startDate)
        else:
            startDate = dates[0]
        
        if endDate != None:
            endDate = performance.dateToString(endDate)
        else:
            endDate = dates[-1]

        myprices = prices[dates.index(startDate):dates.index(endDate)+1]
        mydates = dates[dates.index(startDate):dates.index(endDate)+1]

        return losingStreak(prices=myprices,dates=mydates)
    except:
        return None

def drawdownPeriod(prices,dates,startDate=None,endDate=None):
    try:
        if startDate != None:
            startDate = performance.dateToString(startDate)
        else:
            startDate = dates[0]
        
        if endDate != None:
            endDate = performance.dateToString(endDate)
        else:
            endDate = dates[-1]

        myprices = prices[dates.index(startDate):dates.index(endDate)+1]
        mydates = dates[dates.index(startDate):dates.index(endDate)+1]

        return drawdown(prices=myprices)
    except:
        return None

def maxDrawdownPeriod(prices,dates,startDate=None,endDate=None):
    try:
        if startDate != None:
            startDate = performance.dateToString(startDate)
        else:
            startDate = dates[0]
        
        if endDate != None:
            endDate = performance.dateToString(endDate)
        else:
            endDate = dates[-1]

        myprices = prices[dates.index(startDate):dates.index(endDate)+1]
        mydates = dates[dates.index(startDate):dates.index(endDate)+1]

        return maxDrawdown(prices=myprices)
    except:
        return None



#----------------------------------------------------------------------------------------------------------------------------------------------------
""" 
def annualizedSharpeRatio(prices,dates,minimumAcceptableReturn,year):
    if len(performance.monthlyReturnsYear(prices,dates,year)) != 12:
        return None
    
    monthly_sharpe = sharpeRatioYear(prices,dates,minimumAcceptableReturn,year)
    annualized_sharpe_ratio = monthlySharpe/((12)**(0.5))
    
    return annualized_sharpe_ratio
def annualizedSortinoRatio(prices,dates,minimumAcceptableReturn,year):
     if len(performance.monthlyReturnsYear(prices,dates,year)) != 12:
        return None
    monthly_sortino = sortinoRatioYear(prices=prices,dates=dates,minimumAcceptableReturn=minimumAcceptableReturn,year=year)
    annualized_sortino_ratio = monthly_sortino/((12)**(0.5))
    return annualized_sortino_ratio
 """
#----------------------------------------------------------------------------------------------------------------------------------------------------
def drawdown(prices):
    dd = []
    if len(prices) == 0:
        return None
    peak = float(prices[0])
    for price in prices:
        if float(price) > peak: 
            peak = float(price)
        value = 100*((peak - float(price)) / peak)
        dd.append(value)
    real_drawdown = []
    intermediate = []
    for i, down in enumerate(dd):
        if down != 0:
            intermediate.append(down)
        elif down == 0 and len(intermediate) > 0:
            value = max(intermediate)
            if value > 0:
                real_drawdown.append(value)
            intermediate = []
    try:
        value = max(intermediate)
        if value > 0:
            real_drawdown.append(value)
        intermediate = []
    except:
        pass
    return real_drawdown

def maxDrawdown(prices):
    if len(prices) == 0:
        return None
    mdd = 0
    peak = float(prices[0])
    for price in prices:
        if float(price) > peak: 
            peak = float(price)
        dd = (peak - float(price)) / peak
        if dd > mdd:
            mdd = dd
    return mdd*100

def maxDrawdownYear(prices,dates,year):
    myprices = performance.getPricesYear(prices=prices,dates=dates,year=year)['prices']
    mydates = performance.getPricesYear(prices=prices,dates=dates,year=year)['dates']
    mdd = maxDrawdown(myprices)
    return mdd

def losingStreak(prices,dates):
    days = []
    streak = 0
    data = {}
    loss = 1

    for i in range(1,len(prices)):
        if prices[i-1] > prices[i]:
            streak+=1
            days.append(dates[i])
        else:
            if streak > 1:
                data[loss] = [days[0],days[-1],streak]
                loss+=1
            streak=0
            days = []
    if len(data) == 0:
        return None
    return data


def graph(prices,dates,numberOfPoints=None):
    if numberOfPoints == None:
        numberOfPoints = -1
    myprices = prices[:numberOfPoints] 
    x_vals = dates[:numberOfPoints]
    import matplotlib.pyplot as plt

    thing = plt
    plt.plot(x_vals,myprices)
    plt.show()
#----------------------------------------------------------------------------------------------------------------------------------------------------

#TESTING


def showResults(prices,dates,filename,section=None,):
    mar = 10
    minimumAcceptableReturn = mar/12
    riskFreeReturn = 1
    myYear = 2020
    numberOfMonths = 25

    startDate = datetime.date(2020,1,1)
    endDate = datetime.date(2021,5,29)

    print(f"====RISK ANALYTICS FOR {filename}====")
    print(f"Minimum acceptable return: {minimumAcceptableReturn}")
#NON OVERLOAD
    if section == None:
        # print(f"\nMonthly Returns: {performance.monthlyReturns(prices=prices,dates=dates)}")
        print(f"\nStandard Deviation: {standardDeviation(prices=prices,dates=dates)}")
        print(f"\nGain Standard Deviation: {gainStandardDeviation(prices=prices,dates=dates)}")
        print(f"\nLoss Standard Deviation: {lossStandardDeviation(prices=prices,dates=dates)}")
        print(f"\nDownside Deviation: {downsideDeviation(prices=prices,dates=dates,minimumAcceptableReturn=minimumAcceptableReturn)}")
        print(f"\nSemi Deviation: {semiDeviation(prices=prices,dates=dates)}")
        print(f"\nSharpe Ratio: {sharpeRatio(prices=prices,dates=dates,minimumAcceptableReturn=minimumAcceptableReturn)}")
        print(f"\nSortino Ratio: {sortinoRatio(prices=prices,dates=dates,minimumAcceptableReturn=minimumAcceptableReturn)}")
        print(f"\nSkewness: {skewness(prices=prices,dates=dates)}")
        print(f"\nKurtosis: {kurtosis(prices=prices,dates=dates)}")
        print(f"\nCalmar Ratio: {calmarRatio(prices=prices,dates=dates)}")
        print(f"\nSterling Ratio: {sterlingRatio(prices=prices,dates=dates,year=myYear)}")
        print(f"\nGain to loss Ratio: {gainToLossRatio(prices=prices,dates=dates)}")
        #print(f"\nDrawdown\n{drawdown(prices=prices)}")
        print(f"\nLosing streak\n{losingStreak(prices=prices,dates=dates)}")
        print(f"\nProfit to Loss Ratio: {profitToLossRatio(prices=prices,dates=dates)}")
        print(f'\nMax Drawdown: {maxDrawdown(prices=prices)}')
    
#OVERLOADS FOR A PARTICULAR YEAR
    if section=='year':
        # print(f"\nMonthly Returns: {performance.monthlyReturnsYear(prices=prices,dates=dates,year=myYear)}")
        print(f"\nStandard Deviation: {standardDeviationYear(prices=prices,dates=dates,year=myYear)}")
        print(f"\nGain Standard Deviation: {gainStandardDeviationYear(prices=prices,dates=dates,year=myYear)}")
        print(f"\nLoss Standard Deviation: {lossStandardDeviationYear(prices=prices,dates=dates,year=myYear)}")
        print(f"\nDownside Deviation: {downsideDeviationYear(prices=prices,dates=dates,minimumAcceptableReturn=minimumAcceptableReturn,year=myYear)}")
        print(f"\nSemi Deviation: {semiDeviationYear(prices=prices,dates=dates,year=myYear)}")
        print(f"\nSharpe Ratio: {sharpeRatio(prices=prices,dates=dates,minimumAcceptableReturn=minimumAcceptableReturn)}")
        print(f"\nSortino Ratio: {sortinoRatioYear(prices=prices,dates=dates,minimumAcceptableReturn=minimumAcceptableReturn,year=myYear)}")
        print(f"\nSkewness: {skewness(prices=prices,dates=dates)}")
        print(f"\nSterling Ratio: {sterlingRatio(prices=prices,dates=dates,year=myYear)}")
        print(f"\nGain to loss Ratio: {gainToLossRatioYear(prices=prices,dates=dates,year=myYear)}")
        print(f"\nDrawdown\n{drawdownYear(prices=prices,dates=dates,year=myYear)}")
        print(f"\nLosing streak\n{losingStreakYear(prices=prices,dates=dates,year=myYear)}")
        print(f"\nProfit to Loss Ratio: {profitToLossRatioYear(prices=prices,dates=dates,year=myYear)}")
        print(f'\nMax Drawdown: {maxDrawdownYear(prices=prices,dates=dates,year=myYear)}')

#OVERLOADS FOR A START AND END DATE
    if section=='period':
        print(f"\nStandard Deviation: {standardDeviationPeriod(prices=prices,dates=dates,startDate=startDate,endDate=endDate)}")
        print(f"\nGain Standard Deviation: {gainStandardDeviationPeriod(prices=prices,dates=dates,startDate=startDate,endDate=endDate)}")
        print(f"\nLoss Standard Deviation: {lossStandardDeviationPeriod(prices=prices,dates=dates,startDate=startDate,endDate=endDate)}")
        print(f"\nDownside Deviation: {downsideDeviationPeriod(prices=prices,dates=dates,minimumAcceptableReturn=minimumAcceptableReturn,startDate=startDate,endDate=endDate)}")
        print(f"\nSemi Deviation: {semiDeviationPeriod(prices=prices,dates=dates,startDate=startDate,endDate=endDate)}")
        print(f"\nSharpe Ratio: {sharpeRatioPeriod(prices=prices,dates=dates,minimumAcceptableReturn=minimumAcceptableReturn)}")
        print(f"\nSortino Ratio: {sortinoRatioPeriod(prices=prices,dates=dates,minimumAcceptableReturn=minimumAcceptableReturn,startDate=startDate,endDate=endDate)}")
        print(f"\nSkewness: {skewness(prices=prices,dates=dates)}")
        print(f"\nSterling Ratio: {sterlingRatioPeriod(prices=prices,dates=dates,startDate=startDate,endDate=endDate)}")
        print(f"\nGain to loss Ratio: {gainToLossRatioPeriod(prices=prices,dates=dates,startDate=startDate,endDate=endDate)}")
        print(f"\nDrawdown\n{drawdownPeriod(prices=prices,dates=dates,startDate=startDate,endDate=endDate)}")
        print(f"\nLosing streak\n{losingStreakPeriod(prices=prices,dates=dates,startDate=startDate,endDate=endDate)}")
        print(f"\nProfit to Loss Ratio: {profitToLossRatioPeriod(prices=prices,dates=dates,startDate=startDate,endDate=endDate)}")
        print(f'\nMax Drawdown: {maxDrawdownPeriod(prices=prices,dates=dates,startDate=startDate,endDate=endDate)}')
        # `graph(prices,dates,numberOfPoints=numberOfPoints)

