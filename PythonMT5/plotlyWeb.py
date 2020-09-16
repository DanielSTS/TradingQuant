from datetime import datetime
import MetaTrader5 as mt5
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio

# exibimos dados sobre o pacote MetaTrader5
print("MetaTrader5 package author: ", mt5.__author__)
print("MetaTrader5 package version: ", mt5.__version__)

# estabelecemos a conexão ao MetaTrader 5
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

symbol = "XAUUSD"

# solicitamos 2000 barras do symbol
rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_D1, 0, 2000)

# concluímos a conexão ao terminal MetaTrader 5
mt5.shutdown()

# a partir dos dados recebidos criamos o DataFrame
rates_frame = pd.DataFrame(rates)

# convertemos o tempo em segundos no formato datetime
rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')


#Observamos o gráfico a partir de um html gerado
fig = go.Figure(data=[go.Candlestick(x=rates_frame['time'],
                                     open=rates_frame['open'],
                                     high=rates_frame['high'],
                                     low=rates_frame['low'],
                                     close=rates_frame['close'])])

pio.write_html(fig, file=str(symbol)+'.html', auto_open=True)