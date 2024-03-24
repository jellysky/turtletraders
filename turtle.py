# __author__ = 'koushik'

import pandas as pd
import numpy as np
import quandl as quandl
import sys
import datetime as datetime
import os as os
import pyexcelerate as pe

class const():
    @staticmethod
    def quandlKey():
        return 'oJQ8bM4ArnvxyLUSNjgf'
    @staticmethod
    def postCrisis():
        return datetime.datetime(2008, 1, 1)
    @staticmethod
    def percPos():
        return .01
    @staticmethod
    def initCap():
        return 10000
    @staticmethod
    def stopTolerance():
        return 1
    @staticmethod
    def contractSize():
        return 100  # 100 shares of SPY
    @staticmethod
    def maxUnits():
        return 5
    @staticmethod
    def txCost():
        return 0.01
    @staticmethod
    def shortCols():
        return ['2019', '2020', 'Sharpe Ratio', 'Turtle Return', 'Passive Return', 'Turtle - Passive']
    @staticmethod
    def longCols():
        return ['No:Trade', 'SumRet:Trade', 'MeanRet:Trade', 'SumVar:Trade', 'SumStdev:Trade', 'Sharpe:Trade','%Winners:Trade',
                'No:Longs', 'SumRet:Longs', 'MeanRet:Longs', 'SumVar:Longs', 'SumStdev:Longs', 'Sharpe:Longs','%Winners:Longs',
                'No:Shorts', 'SumRet:Shorts', 'MeanRet:Shorts', 'SumVar:Shorts', 'SumStdev:Shorts', 'Sharpe:Shorts','%Winners:Shorts',
                'No:Pre2008', 'SumRetRet:Pre2008', 'MeanRet:Pre2008', 'SumVar:Pre2008', 'SumStdev:Pre2008','Sharpe:Pre2008', '%Winners:Pre2008',
                'No:Post2008', 'SumRetRet:Post2008', 'MeanRet:Post2008', 'SumVar:Post2008', 'SumStdev:Post2008','Sharpe:Post2008', '%Winners:Post2008',
                'No:PrevTradeWinner', 'SumRetRet:PrevTradeWinner', 'MeanRet:PrevTradeWinner', 'SumVar:PrevTradeWinner','SumStdev:PrevTradeWinner', 'Sharpe:PrevTradeWinner', '%Winners:PrevTradeWinner',
                'No:PrevTradeLoser', 'SumRetRet:PrevTradeLoser', 'MeanRet:PrevTradeLoser', 'SumVar:PrevTradeLoser','SumStdev:PrevTradeLoser', 'Sharpe:PrevTradeLoser', '%Winners:PrevTradeLoser',
                'No:Txs', 'No:Stops', 'Passive Return']
    @staticmethod
    def backtestCols():
        return ['Trade', 'Unit', 'Date', 'LastPrice', 'CurrentPrice', 'EntryPrice', 'ExitPrice', 'StopPrice', 'StopInd','N', 'Direction',
                'StartPos', 'PNL', 'TxCost', 'EndPos','Return', 'RisktoEq%', 'PrevTradeLoser','PostCrisis','S1orS2']
    @staticmethod
    def longMetrics():
        return 7
    @staticmethod
    def xlsTabsSN():
        return ['Metrics','PNL','Price']
    @staticmethod
    def xlsTabsPort():
        return ['Short', 'Long']

def get_csv_data(path, column):
    # path to tickers for all stocks in index

    dtOut = pd.read_csv(path)[column]
    # print('Finished getting data for index: %s, column: %s...' %(path,column))
    return dtOut

def get_singlename_quandl_data(ticker, startDate, endDate):
    # ticker = 'YAHOO/INDEX_GSPC'
    # startDate = dt.datetime(1950, 1, 1)
    # endDate = dt.datetime(2016, 6, 22)

    dtPrice = quandl.get(ticker, start_date=startDate, end_date=endDate)
    dtPrice.columns = dtPrice.columns.str.strip()
    dtPrice = dtPrice.iloc[dtPrice['Volume'] > 0]
    # print('\nFinished getting data for %s...'%ticker)

    return dtPrice

def get_sp500_quandl_vols():

    stockNames = get_csv_data('Components/SP500.csv', 'ticker')
    dtVols = np.zeros(shape=(stockNames.shape[0], 2))

    for i, s in enumerate(stockNames):
        ticker = 'OPT/' + s
        dtVols[i,] = quandl.get(ticker, rows=1)[['m4atmiv', '252dclsHV']]
        print('\nFinished getting data for %s, %d...' % (s, i))

    return pd.DataFrame(data=dtVols, columns=['4mATMIvol', '1yHV'], index=stockNames)

def get_singlename_ib_data(ticker):

    print(ticker)
    dtPrice = pd.read_csv('Historical Data/' + ticker + '_IB20161031.csv')
    dtPrice.columns = dtPrice.columns.str.strip()
    dtPrice.index = pd.to_datetime(dtPrice['Date'])

    return dtPrice

def get_singlename_yahoo_data(ticker):

    dtPrice = pd.read_csv(filepath_or_buffer='Nifty50/' + ticker + ' 11.10.2020.csv',index_col='Date')
    dtPrice.index = pd.to_datetime(dtPrice.index,infer_datetime_format=True)
    dtPrice['Symbol'] = ticker

    return dtPrice

def get_stocknames(mypath):

    stockNames = []

    for f in os.listdir(mypath):
        #print(f)
        if os.path.isfile(os.path.join(mypath, f)) and f[-3:] == 'csv':
            stockNames.append(f[:f.index('_')])

    return np.array(stockNames)

def print_singlename_outputs(dts):

    wb = pe.Workbook()
    list_dts = dts
    ticker = dts[1]['Symbol'].iloc[0]
    for i, dt in enumerate(list_dts):
        # list_dts[i].to_csv(const.xlsTabs()[i] + '.csv', index=True)
        # print(i)

        data = [dt.columns.tolist(), ] + dt.values.tolist()
        indx = [''] + dt.index.tolist()
        data = [[index] + row for index, row in zip(indx, data)]
        wb.new_sheet(const.xlsTabsSN()[i], data=data)
        wb.save(ticker + '.xlsx', )

def print_portfolio_outputs(dts):

    wb = pe.Workbook()
    list_dts = dts
    for i, dt in enumerate(list_dts):
        # list_dts[i].to_csv(const.xlsTabs()[i] + '.csv', index=True)
        # print(i)

        data = [dt.columns.tolist(), ] + dt.values.tolist()
        indx = [''] + dt.index.tolist()
        data = [[index] + row for index, row in zip(indx, data)]
        wb.new_sheet(const.xlsTabsPort()[i], data=data)
        wb.save('Outputs.xlsx', )





def compute_ATR(dtPrice, mavg):
    # mavg=20
    dtN = np.zeros(shape=(dtPrice.shape[0], 6), dtype=float)

    # N1: Today's high less low, should always be +
    dtN[:, 0] = dtPrice['High'] - dtPrice['Low']
    # N2: Yesterday's close to today's high
    dtN[1:, 1] = np.absolute(dtPrice['Close'].iloc[0:-1].values - dtPrice['High'].iloc[1:].values)

    # N3: Yesterday's close to today's low
    dtN[1:, 2] = np.absolute(dtPrice['Close'].iloc[0:-1].values - dtPrice['Low'].iloc[1:].values)

    dtN[:, 3] = np.amax(dtN[:, 0:3], axis=1)

    dtN = pd.DataFrame(data=dtN, index=dtPrice.index, columns=['TR1', 'TR2', 'TR3', 'TRmax', 'N1', 'N2'])
    dtN['N1'] = dtN['TRmax'].rolling(center=False, window=mavg).mean()

    dtN['N2'] = np.nan
    for i in range(mavg, dtN.shape[0]):
        dtN.at[dtN.index[i],'N2'] = ((mavg - 1) * dtN['N1'].iloc[i - 1] + dtN['TRmax'].iloc[i]) / mavg
    # replacement of for loop - dtN.at[dtN.index[mavg:dtN.shape[0]], 'N2'] = ((mavg - 1) * dtN['N1'].iloc[mavg-1:dtN.shape[0]-1] + dtN['TRmax'].iloc[mavg:dtN.shape[0]]) / mavg


    # print('Finished computing N for Mavg = %d...'%mavg)

    return pd.concat([dtPrice, dtN], axis=1)

def compute_breakouts(dt):
    mavgs = [20, 10, 55, 20]
    dtMavg = np.zeros(shape=(dt.shape[0], len(mavgs)))

    for i, m in enumerate(mavgs):
        maxIndx = np.where(dt['Close'].rolling(center=False, window=m).max() == dt['Close'])
        minIndx = np.where(dt['Close'].rolling(center=False, window=m).min() == dt['Close'])
        dtMavg[maxIndx, i] = 1
        dtMavg[minIndx, i] = -1
        # print('\nCompleted computation of rolling maxes and mins for m = %d...'%m)

    dtMavg[dt.shape[0] - 1, 0] = 0
    dtMavg[dt.shape[0] - 1, 2] = 0
    dtMavg = pd.DataFrame(data=dtMavg, index=dt.index, columns=['MavgB1', 'MavgS1', 'MavgB2', 'MavgS2'])
    return pd.concat([dt, dtMavg], axis=1)

def calculate_trade_pnl(dtRow, entryThresholds):
    # calculates trade PNL for one trade, must track PNL for both PrevTradeLoser and PrevTradeWinner or else you don't know
    # if last trade was a winner or loser

    for i in range(0, dtRow.shape[0]):
        # print(i)
        # sets unit
        if (len(np.where(dtRow['EntryPrice'].iloc[i] * dtRow['Direction'].iloc[i] >= entryThresholds * dtRow['Direction'].iloc[i])[0]) == 0):
            dtRow.at[dtRow.index[i],'Unit'] = dtRow['Unit'].iloc[i - 1]
        else:
            dtRow.at[dtRow.index[i],'Unit'] = max(np.where(dtRow['EntryPrice'].iloc[i] * dtRow['Direction'].iloc[i] >= entryThresholds * dtRow['Direction'].iloc[i])[0].max() + 1, dtRow['Unit'].iloc[i - 1])
            # print('\nMax unit is: %d' %dtRow['Unit'].iloc[i])
        dtRow.at[dtRow.index[i],'StopPrice'] = dtRow['EntryPrice'].iloc[i] - const.stopTolerance() * dtRow['Direction'].iloc[i] * dtRow['N'].iloc[i]
        # tx costs incurred and entry price is a member of entryThresholds when unit changes (pyramiding)
        if (i > 0):
            if (dtRow['Unit'].iloc[i] - dtRow['Unit'].iloc[i - 1] > 0):
                dtRow.at[dtRow.index[i],'TxCost'] = dtRow['TxCost'].iloc[0]  # txCost is initialized in backtest_data
                dtRow.at[dtRow.index[i],'EntryPrice'] = entryThresholds[dtRow['Unit'].iloc[i].astype(int) - 1]
            # current StartPos is last EndPos
            dtRow.at[dtRow.index[i],'StartPos'] = dtRow['EndPos'].iloc[i - 1] + (dtRow['Unit'].iloc[i] - dtRow['Unit'].iloc[i - 1]) * dtRow['StartPos'].iloc[0]
        # if there is a stop, compute stops using EOD prices and see if it works
        if (dtRow['Direction'].iloc[i] * dtRow['StopPrice'].iloc[i] >= dtRow['Direction'].iloc[i] * dtRow['CurrentPrice'].iloc[i]) and (dtRow['StopInd'].iloc[i] == 1):
            dtRow.at[dtRow.index[i + 1:dtRow.shape[0]],'StopInd'] = 0
            dtRow.at[dtRow.index[i],'ExitPrice'] = dtRow['CurrentPrice'].iloc[i]
#dtRow['StopPrice'].iloc[i]
            dtRow.at[dtRow.index[i],'TxCost'] = dtRow['TxCost'].iloc[0]  # txCost is initialized in backtest_data
        # calculate PNL by row
        dtRow.at[dtRow.index[i],'PNL'] = (dtRow['ExitPrice'].iloc[i] / dtRow['EntryPrice'].iloc[i] - 1) * dtRow['Direction'].iloc[i] * dtRow['StartPos'].iloc[i] * dtRow['StopInd'].iloc[i]
        # if there is no stop before the end
        if (i == dtRow.shape[0] - 1) and (dtRow['StopInd'].iloc[i] == 1):
            dtRow.at[dtRow.index[i],'TxCost'] = dtRow['TxCost'].iloc[0]  # txCost is initialized in backtest_data
        dtRow.at[dtRow.index[i],'EndPos'] = dtRow['StartPos'].iloc[i] + dtRow['PNL'].iloc[i] - dtRow['TxCost'].iloc[i]
    dtRow['Return'] = dtRow['PNL'] / dtRow['StartPos']
    dtRow['RisktoEq%'] = dtRow['StartPos'] / (dtRow['StartPos'] + const.initCap())

    # print('\nCalculating PNL for entry: %s and exit: %s'%(dtRow['Date'].iloc[0].strftime('%Y-%m-%d'),
    #                                                     dtRow['Date'].iloc[i].strftime('%Y-%m-%d')))
    return dtRow[dtRow['StopInd'] == 1]

def calculate_unit_backtest(dt):
    # runs through PNL for all trades for one singlename
    #dt = dtPrice
    prevTradeLoser = 1
    dtPNL = pd.DataFrame(data=np.zeros(shape=(0, len(const.backtestCols()))), columns=const.backtestCols())
    entryIndxB1 = np.where(dt['MavgB1'] != 0)
    # entryIndxB2 = np.where(dt['MavgB2'] != 0)
    trade = 0
    endDate = dt.index[0]

    while trade < len(entryIndxB1[0]):

        entry = entryIndxB1[0][trade]
        unitPos = const.percPos() * const.initCap() / (dt['N2'].iloc[entry] * const.contractSize())
        entryString = 'MavgB1'
        exitString = 'MavgS1'

        if (prevTradeLoser == False):  # if previous trade is a winner then evaluate the next S1 entry
            # find the set of entries using the S2 series
            entryS2 = np.where(np.logical_and(dt['MavgS2'] != 0, dt['MavgS2'].index > dt.index[entry]))[0]
            # if the next entry is in S1 series then prevTradeLoser stays as is, if not then make prevTradeLoser True
            if (np.append(entryS2, entry).min() != entry):
                prevTradeLoser = True
                entry = np.append(entryS2, entry).min()
                entryString = 'MavgB2'
                exitString = 'MavgS2'

        exit = np.where(np.logical_and(dt[exitString] == -1 * dt[entryString].iloc[entry],
                                       dt[exitString].index > dt[entryString].index[entry]))[0]
        exit = np.append(exit, dt.shape[0] - 1).min()

        # print('\ntrade: %d, entry: %d, exit: %d, entryString: %s, exitString: %s' %(trade,entry,exit,entryString,exitString))
        # initialize dtRow and set entire column
        dtRow = pd.DataFrame(data=np.zeros(shape=(exit - entry, len(const.backtestCols()))), columns=const.backtestCols())

        dtRow['Trade'] = trade # tradeCounter
        dtRow['Date'] = dt.index[entry + 1:exit + 1]
        dtRow['LastPrice'] = dt['Close'].iloc[entry:exit].values
        dtRow['CurrentPrice'] = dt['Close'].iloc[entry + 1:exit + 1].values
        dtRow['EntryPrice'] = dt['Close'].iloc[entry:exit].values
        dtRow['ExitPrice'] = dt['Close'].iloc[entry + 1:exit + 1].values
        dtRow['N'] = dt['N2'].iloc[entry:exit].values
        dtRow['Direction'] = dt[entryString].iloc[entry]
        dtRow['StopInd'] = 1
        dtRow['PrevTradeLoser'] = prevTradeLoser
        if (dt.index[entry + 1] > const.postCrisis()):
            dtRow['PostCrisis'] = 1

        # initializing first value of column
        dtRow.at[0,'EntryPrice'] = dt['Close'].iloc[entry]
        dtRow.at[0,'StartPos'] = unitPos
        dtRow.at[0,'TxCost'] = const.txCost() * unitPos

        entryThresholds = np.arange(0, const.maxUnits()) * 0.5 * dtRow['N'].iloc[0] * dt[entryString].iloc[entry] + dt['Close'].iloc[entry]
        dtRow = calculate_trade_pnl(dtRow, entryThresholds)

        if (dtRow['PNL'].sum() > 0):
            prevTradeLoser = False
        else:
            prevTradeLoser = True

        if (entryString=='MavgB2'):
            dtRow['S1orS2'] = 2
        else:
            dtRow['S1orS2'] = 1

        # dtRow.to_csv('row.csv')
        dtPNL = pd.concat([dtPNL, dtRow], axis=0)
        endDate = dtPNL['Date'].iloc[dtPNL.shape[0] - 1]
        trade = np.where(dt.index[entryIndxB1[0]] > endDate)[0]
        trade = np.append(trade, len(entryIndxB1[0])).min()

    dtPNL.index = range(0, dtPNL.shape[0])
    #dtPNL.to_csv('PNL.csv')
    return dtPNL

def calculate_singlename_backtest(s, startDate, endDate, switch):

    #s = 'ADANIPORTS.NS',startDate = datetime.datetime(2019, 1, 1),endDate = datetime.datetime(2020, 11, 10),switch = 'Yahoo'
    if (switch == 'IB'):
        dtPrice = get_singlename_ib_data(s.strip('\u200b'))
    elif (switch == 'Quandl'):
        dtPrice = get_singlename_quandl_data(s.strip('\u200b'), startDate, endDate)
    elif (switch == 'Yahoo'):
        dtPrice = get_singlename_yahoo_data(s.strip('\u200b'))
    #print('\nCalculating pnl for %s...' % s)

    dtPrice = compute_ATR(dtPrice, 20) # compute the ATR
    dtPrice = compute_breakouts(dtPrice) # compute breakouts
    dtPNL = calculate_unit_backtest(dtPrice) # compute breakouts

    dtPNL = dtPrice.merge(dtPNL, how='outer', right_on='Date', left_index=True) # merge breakouts with prices
    dtPNL.index = dtPrice.index
    dtMetrics = calculate_singlename_short_outputs(dtPNL) # calculate returns: by year, active or passive strategy, sharpe ratio

    return dtMetrics,dtPNL,dtPrice


def calculate_singlename_short_outputs(dtPNL):
    # calculates returns per year for one singlename
    dtOut = pd.DataFrame(data=np.zeros(shape=(1, len(const.shortCols()))), columns=const.shortCols(),index=[dtPNL['Symbol'].iloc[0]])

    prevIndx = np.where(dtPNL['PrevTradeLoser'] == 1)
    dtPNL['Year'] = pd.DatetimeIndex(dtPNL['Date']).year
    ticker = dtPNL['Symbol'].iloc[0]

    dtOut.at[ticker,['2019','2020']] = dtPNL.iloc[prevIndx].groupby(['Year'])['Return'].sum().values
    dtOut.at[ticker, 'Sharpe Ratio'] = dtPNL.iloc[prevIndx].groupby(['Trade'])['Return'].sum().mean() / dtPNL.iloc[prevIndx].groupby(['Trade'])['Return'].sum().std()
    dtOut.at[ticker,'Turtle Return'] = dtPNL['Return'].iloc[prevIndx].sum()
    dtOut.at[ticker,'Passive Return'] = dtPNL['Close'].iloc[-1] / dtPNL['Open'].iloc[0] - 1
    dtOut.at[ticker,'Turtle - Passive'] = dtOut['Turtle Return'] - dtOut['Passive Return']

    return dtOut

def calculate_portfolio_short_outputs(startDate,endDate,switch):
    # calculates returns each year and total sharpe
    #startDate = datetime.datetime(2019, 1, 1), endDate = datetime.datetime(2020, 10, 11)
    stockNames = get_csv_data('Components/nifty50.csv', 'Symbol')
    dtStocks = pd.DataFrame(data=np.zeros(shape=(0,len(const.shortCols()))),columns=const.shortCols())

    for i, s in enumerate(stockNames):
    #i=2, s = stockNames.iloc[i]
        dtMetrics, dtPNL, dtPrice = calculate_singlename_backtest(s, startDate, endDate, switch)
        dtStocks = pd.concat([dtStocks,dtMetrics],axis=0)
        print('Calculated short outputs for %s, %d...' % (s, i))

        if (dtPNL['Symbol'].iloc[0] in ['TATAMOTORS.NS','WIPRO.NS','BAJFINANCE.NS','GRASIM.NS']):
            print_singlename_outputs([dtMetrics.fillna(0),dtPNL.fillna(0),dtPrice.fillna(0)])

    return dtStocks

def calculate_unit_long_outputs(dtPNL):
# Need to add prevIndx to screen out PrevTradeWinner trades
    dtOut = np.zeros(shape=(1, const.longMetrics()))
    #dtInput = dtPNL.groupby(['Trade'])['Return'].agg({'sum': np.sum, 'mean': np.mean, 'stdev': np.std, 'var': np.var}) # retired this code
    dtInput = dtPNL.groupby(['Trade'])['Return'].agg([np.sum, np.mean, np.std, np.var])


    dtOut[0, 0] = dtInput.shape[0]  # number
    dtOut[0, 1] = dtInput['sum'].sum()  # sum of returns
    dtOut[0, 2] = dtInput['mean'].mean()  # mean of returns
    dtOut[0, 3] = dtInput['var'].sum()  # sum of var of returns
    dtOut[0, 4] = np.sqrt(dtInput['var'].sum())  # std of returns
    if (np.sqrt(dtInput['var'].sum()) != 0):
        dtOut[0, 5] = dtInput['mean'].sum() / np.sqrt(dtInput['var'].sum())  # sharpe of returns
    else:
        dtOut[0, 5] = 0
    if (dtInput.shape[0] > 0):
        dtOut[0, 6] = dtInput[dtInput['sum'] > 0].shape[0] / dtInput.shape[0]  # % winners
    else:
        dtOut[0, 6] = 0

    return dtOut

def calculate_singlename_long_outputs(dtPNL):
    #startDate = datetime.datetime(2019, 1, 1)
    #endDate = datetime.datetime(2020, 11, 10)
    dtOut = np.zeros(shape=(1,len(const.longCols())))

    dtOut[0,0:const.longMetrics()] = calculate_unit_long_outputs(dtPNL)  # all trades
    dtOut[0,const.longMetrics():2 * const.longMetrics()] = calculate_unit_long_outputs(dtPNL[dtPNL['Direction'] == 1])  # longs
    dtOut[0,2 * const.longMetrics():3 * const.longMetrics()] = calculate_unit_long_outputs(dtPNL[dtPNL['Direction'] == -1])  # shorts
    dtOut[0,3 * const.longMetrics():4 * const.longMetrics()] = calculate_unit_long_outputs(dtPNL[dtPNL['PostCrisis'] == 0])  # precrisis
    dtOut[0,4 * const.longMetrics():5 * const.longMetrics()] = calculate_unit_long_outputs(dtPNL[dtPNL['PostCrisis'] == 1])  # postcrisis
    dtOut[0,5 * const.longMetrics():6 * const.longMetrics()] = calculate_unit_long_outputs(dtPNL[dtPNL['PrevTradeLoser'] == 0])  # prevtradewinner
    dtOut[0,6 * const.longMetrics():7 * const.longMetrics()] = calculate_unit_long_outputs(dtPNL[dtPNL['PrevTradeLoser'] == 1])  # prevtradeloser

    dtOut[0,7 * const.longMetrics()] = dtPNL[dtPNL['TxCost'] > 0].shape[0] # No of tx's
    dtOut[0,7 * const.longMetrics() + 1] = np.logical_and(dtPNL['StopInd'].iloc[1:dtPNL.shape[0]] == 0,dtPNL['StopInd'].iloc[0:dtPNL.shape[0] - 1] == 1).sum() / \
                                               dtPNL['Trade'].unique().shape[0] # No of stops
    dtOut[0,7 * const.longMetrics() + 2] = dtPNL['Close'].iloc[-1] / dtPNL['Close'].iloc[0] - 1 # Total passive return

    dtOut = pd.DataFrame(data=dtOut, columns=const.longCols(),index=[dtPNL['Symbol'].iloc[0]])

    return dtOut

def calculate_portfolio_long_outputs(startDate,endDate,switch):
    # startDate = datetime.datetime(2019, 1, 1)
    # endDate = datetime.datetime(2020, 11, 10)

    # stockNames = get_index_data('Components/sp500.csv', 'free_code')
    stockNames = pd.read_csv('Components/nifty50.csv')['Symbol']
    dtOut = pd.DataFrame(data=np.zeros(shape=(0, len(const.longCols()))),columns=const.longCols())

    for i, s in enumerate(stockNames):

        dtMetrics, dtPNL, dtPrice = calculate_singlename_backtest(s, startDate, endDate, switch)
        dtStock = calculate_singlename_long_outputs(dtPNL)
        # dtStock.to_csv('dtStock.csv')
        print('Calculated long outputs for %s, %d...' % (s,i))
        dtOut = pd.concat([dtOut,dtStock],axis=0)

    return dtOut

def generate_trades(startDate, endDate):
    #startDate = datetime.datetime(2016,1,1),endDate = datetime.datetime(2016,9,12)
    tradeNames = get_csv_data('Components/tradenames.csv', 'names')

    for s in tradeNames:
        # s=tradeNames[0]
        dtMetrics, dtPNL, dtPrice = calculate_singlename_backtest(s, startDate, endDate)
        print('\nFinished calculating %s PNL for %s...' % (dtPNL['Date'].iloc[-1].strftime('%Y-%m-%d'), s))

        if (dtPNL['Direction'].iloc[-1].is_integer() == True):
            print('Put on units: %.2f with change: %s of stock: %s on date: %s with stop: %.2f...'
# why 500?  Shouldnt it be unitPos??
                  % ((dtPNL['Direction'].iloc[-1] * 500 / dtPNL['N1'].iloc[-1]) / dtPNL['CurrentPrice'].iloc[-1],
                     str(dtPNL['Unit'].iloc[-1] - dtPNL['Unit'].iloc[-2]),s,dtPNL['Date'].iloc[-1].strftime('%Y-%m-%d'),dtPNL['StopPrice'].iloc[-1]))
            dtPNL.to_csv('Trades/' + s + ' ' + endDate.strftime('%Y-%m-%d') + '.csv')

        if (dtPNL['S1orS2'].iloc[-1] == 1):
            stopCol = 'MavgS1'
        else: #(dtOut['S1orS2'].iloc[-1] == 2):
            stopCol = 'MavgS2'

        if (dtPNL['Direction'].iloc[-1] * -1 == dtPNL[stopCol].iloc[-1]):
            print('Get out of trade on stock: %s on date: %s...' % (s, dtOut['Date'].iloc[-1].strftime('%Y-%m-%d')))
            # return dtOut


def main(argv = sys.argv):

#quandl.ApiConfig.api_key = const.quandlKey()
startDate = datetime.datetime(2019, 1, 1)
endDate = datetime.datetime(2020, 10, 11)
switch='Yahoo'
dtShort = calculate_portfolio_short_outputs(startDate,endDate,switch)
dtLong = calculate_portfolio_long_outputs(startDate,endDate,switch)

dtMetrics, dtPNL, dtPrice = calculate_singlename_backtest('TATAMOTORS.NS', startDate, endDate, switch)
short = calculate_singlename_long_outputs(dtPNL)
long = calculate_singlename_long_outputs(dtPNL)
print_portfolio_outputs([dtShort,dtLong])


generate_trades(datetime.datetime(2019,1,1),datetime.datetime.today())

dtOut,dtStocks,dtPrice = calculate_singlename_backtest('ADANIPORTS.NS',datetime.datetime(2019, 1, 1),datetime.datetime(2020, 11, 10),'Yahoo')

if __name__ == "__main__":
    sys.exit(main())
