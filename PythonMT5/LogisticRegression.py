import time
import MetaTrader5 as mt5
import ta
import pandas as pd

import pickle

# exibimos dados sobre o pacote MetaTrader5
print("MetaTrader5 package author: ", mt5.__author__)
print("MetaTrader5 package version: ", mt5.__version__)

# estabelecemos a conexão ao MetaTrader 5
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# preparamos a estrutura de solicitação para compra
symbol = "EURUSD"
symbol_info = mt5.symbol_info(symbol)
if symbol_info is None:
    print(symbol, "not found, can not call order_check()")
    mt5.shutdown()
    quit()

# se o símbolo não estiver disponível no MarketWatch, adicionamo-lo
if not symbol_info.visible:
    print(symbol, "is not visible, trying to switch on")
    if not mt5.symbol_select(symbol, True):
        print("symbol_select({}}) failed, exit", symbol)
        mt5.shutdown()
        quit()





rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_D1, 0, 35)
# a partir dos dados recebidos criamos o DataFrame
df = pd.DataFrame(rates)
# convertemos o tempo em segundos no formato datetime
df['time'] = pd.to_datetime(df['time'], unit='s')

indicator_rsi2 = ta.momentum.RSIIndicator(close=df['close'], n=2, fillna=False)
indicator_rsi5 = ta.momentum.RSIIndicator(close=df['close'], n=5, fillna=False)
indicator_rsi14 = ta.momentum.RSIIndicator(close=df['close'], n=14, fillna=False)
indicator_rsi21 = ta.momentum.RSIIndicator(close=df['close'], n=21, fillna=False)
indicator_macd = ta.trend.MACD(close=df['close'], n_slow=26, n_fast=12, n_sign=9, fillna=False)
indicator_ema20 = ta.trend.EMAIndicator(close=df['close'], n=14, fillna=False)

df['return'] = df['close'].pct_change()
df['rsi2'] = indicator_rsi2.rsi()
df['rsi5'] = indicator_rsi5.rsi()
df['rsi14'] = indicator_rsi14.rsi()
df['rsi21'] = indicator_rsi21.rsi()
df['macd'] = indicator_macd.macd_signal()
df['ema20'] = indicator_ema20.ema_indicator()
df.dropna(inplace=True)

p = modelo.predict(df[['return','rsi2','rsi5','rsi14','rsi21','macd','ema20']])



max_atual = df['high'][34]
min_atual = df['low'][34]
max_ant = df['high'][33]
min_ant = df['low'][33]


if p[0] == 1:

    lot = 0.01
    point = mt5.symbol_info(symbol).point
    price = mt5.symbol_info_tick(symbol).ask
    deviation = 20
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        "sl": min_ant,
        "tp": price + (max_ant - min_ant),
        "deviation": deviation,
        "magic": 234000,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_DAY,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    # enviamos a solicitação de negociação
    result = mt5.order_send(request)
    # verificamos o resultado da execução
    print("1. order_send(): by {} {} lots at {} with deviation={} points".format(symbol, lot, price, deviation));
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("2. order_send failed, retcode={}".format(result.retcode))
        # solicitamos o resultado na forma de dicionário e exibimos elemento por elemento
        result_dict = result._asdict()
        for field in result_dict.keys():
            print("   {}={}".format(field, result_dict[field]))
            # se esta for uma estrutura de uma solicitação de negociação, também a exibiremos elemento a elemento
            if field == "request":
                traderequest_dict = result_dict[field]._asdict()
                for tradereq_filed in traderequest_dict:
                    print("       traderequest: {}={}".format(tradereq_filed, traderequest_dict[tradereq_filed]))

else:

    lot = 0.01
    point = mt5.symbol_info(symbol).point
    price = mt5.symbol_info_tick(symbol).bid
    deviation = 20
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_SELL,
        "price": price,
        "sl": max_ant,
        "tp": price - (max_ant - min_ant),
        "deviation": deviation,
        "magic": 234000,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_DAY,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    # enviamos a solicitação de negociação
    result = mt5.order_send(request)
    # verificamos o resultado da execução
    print("1. order_send(): by {} {} lots at {} with deviation={} points".format(symbol, lot, price, deviation));
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("2. order_send failed, retcode={}".format(result.retcode))
        # solicitamos o resultado na forma de dicionário e exibimos elemento por elemento
        result_dict = result._asdict()
        for field in result_dict.keys():
            print("   {}={}".format(field, result_dict[field]))
            # se esta for uma estrutura de uma solicitação de negociação, também a exibiremos elemento a elemento
            if field == "request":
                traderequest_dict = result_dict[field]._asdict()
                for tradereq_filed in traderequest_dict:
                    print("       traderequest: {}={}".format(tradereq_filed, traderequest_dict[tradereq_filed]))

mt5.shutdown()
