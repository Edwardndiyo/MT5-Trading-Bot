import MetaTrader5 as mt5

# Connect to MetaTrader 5
if not mt5.initialize():
    print("MT5 connection failed")
    mt5.shutdown()
else:
    print("Connected to MT5")

# Shutdown MT5 connection
mt5.shutdown()
