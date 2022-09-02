import MetaTrader5 as mt5
import time
import ta
import pandas as pd
import pickle
from LR import LR


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

strategy = 'LR'

#carregando modelo
with open('logistic_regression.pkl', 'rb') as f:
    modelo = pickle.load(f)


while(True):

    #solicitando dados dos candles
    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_D1, 0, 35)
    # a partir dos dados recebidos criamos o DataFrame
    df = pd.DataFrame(rates)

    sinal = LR(modelo,df)

    if sinal:
        sell()

    else:
        buy()

    time.sleep(2)