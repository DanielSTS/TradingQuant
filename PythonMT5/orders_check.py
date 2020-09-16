import MetaTrader5 as mt5

# exibimos dados sobre o pacote MetaTrader5
print("MetaTrader5 package author: ", mt5.__author__)
print("MetaTrader5 package version: ", mt5.__version__)

# estabelecemos a conexão ao terminal MetaTrader 5
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# obtemos a moeda da conta
account_currency = mt5.account_info().currency
print("Account currency:", account_currency)

# preparamos a estrutura da solicitação
symbol = "USDJPY"
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

# preparamos a solicitação
point = mt5.symbol_info(symbol).point
request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volume": 1.0,
    "type": mt5.ORDER_TYPE_BUY,
    "price": mt5.symbol_info_tick(symbol).ask,
    "sl": mt5.symbol_info_tick(symbol).ask - 100 * point,
    "tp": mt5.symbol_info_tick(symbol).ask + 100 * point,
    "deviation": 10,
    "magic": 234000,
    "comment": "python script",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_RETURN,
}

# verificamos e exibimos o resultado como está
result = mt5.order_check(request)
print(result)
# solicitamos o resultado na forma de um dicionário e exibimos elemento por elemento
result_dict = result._asdict()
for field in result_dict.keys():
    print("   {}={}".format(field, result_dict[field]))
    # se esta for uma estrutura de uma solicitação de negociação, também a exibiremos elemento a elemento
    if field == "request":
        traderequest_dict = result_dict[field]._asdict()
        for tradereq_filed in traderequest_dict:
            print("       traderequest: {}={}".format(tradereq_filed, traderequest_dict[tradereq_filed]))

# concluímos a conexão ao terminal MetaTrader 5
mt5.shutdown()