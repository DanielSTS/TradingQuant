import pandas as pd
import MetaTrader5 as mt5
import time

# estabelecemos a conexão ao MetaTrader 5
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

symbol = "EURUSD"
timeframe = 'M1'
lot = 0.01
periodoLongo = 40
periodoCurto = 20
sl = 100
tp = 100


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



def compra(l,sl,tp):
    point = mt5.symbol_info(symbol).point
    price = mt5.symbol_info_tick(symbol).ask
    deviation = 20
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": l,
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        "sl":  price - sl * point,
        "tp": price + tp * point ,
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


def venda(l,sl,tp):
    point = mt5.symbol_info(symbol).point
    price = mt5.symbol_info_tick(symbol).bid
    deviation = 20
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": l,
        "type": mt5.ORDER_TYPE_SELL,
        "price": price,
        "sl": price + sl * point,
        "tp": price - tp * point,
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

def checkMedia(c,l):

    if(c > l):
        return 1
    if(l > c):
        return -1



while(True):

    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, periodoLongo)
    rates_frame = pd.DataFrame(rates)

    mCurta = rates_frame['close'].rolling(periodoCurto).mean().iloc[-1]
    mLonga = rates_frame['close'].rolling(periodoLongo).mean().iloc[-1]


    if(not mt5.positions_get(symbol = symbol)):
        a = checkMedia(mCurta,mLonga)
        if(a == 1):
            compra(lot,sl,tp)
        if(a == -1):
            venda(lot,sl,tp)




    time.sleep(1)