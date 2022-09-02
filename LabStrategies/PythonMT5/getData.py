from datetime import datetime
import MetaTrader5 as mt5

import pandas as pd
import pytz

# estabelecemos a conexão ao MetaTrader 5
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

symbols = ['EURUSD','GBPUSD','USDCHF','USDJPY','USDCAD']


for i in symbols:

    # definimos o fuso horário como UTC
    timezone = pytz.timezone("Etc/UTC")
    # criamos o objeto datatime no fuso horário UTC para que não seja aplicado o deslocamento do fuso horário local
    utc_from = datetime(2013, 1, 1, tzinfo=timezone)
    utc_to = datetime(2019, 12, 31, tzinfo=timezone)
    # obtemos as barras no intervalo 2013-2019
    rates = mt5.copy_rates_range(i, mt5.TIMEFRAME_H12, utc_from, utc_to)
    # a partir dos dados recebidos criamos o DataFrame
    rates_frame = pd.DataFrame(rates)
    # convertemos o tempo em segundos no formato datetime
    rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
    #renomeando colunas
    rates_frame.rename(columns={"time": "Date","open": "Open", "high": "High","low": "Low", "close": "Close" },inplace=True)
    variaveis = ["Date","Open","High","Low","Close"]
    # armazenamos em um arquivo .csv
    rates_frame[variaveis].to_csv(str(i)+ "H12"+".csv", header=True)



# concluímos a conexão ao terminal MetaTrader 5
mt5.shutdown()