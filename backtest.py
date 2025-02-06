#  backtesting profitability of strategy

# improved test for efficiency

# import MetaTrader5 as mt5
# import pandas as pd
# import time
# import winsound  # For sound alerts
# import mplfinance as mpf
# from datetime import datetime, timedelta
# from tqdm import tqdm  # Progress bar library

# # Connect to MetaTrader 5
# if not mt5.initialize():
#     print("MT5 connection failed")
#     mt5.shutdown()
#     quit()

# print("Connected to MT5")

# # Define parameters
# symbol = "GBPJPY"
# timeframe_H1 = mt5.TIMEFRAME_H1
# timeframe_M15 = mt5.TIMEFRAME_M15
# num_bars = 500  # Number of candles to fetch (adjust as needed)
# lookback = 20  # Lookback window for support/resistance
# invalidate_threshold = 3  # Number of consecutive candles for invalidation
# take_profit = 30  # in pips
# stop_loss = 20  # in pips

# # Function to get historical data in smaller chunks
# def get_data_in_chunks(symbol, timeframe, start_time, end_time, chunk_size=100):
#     data = []
#     current_start_time = start_time

#     while current_start_time < end_time:
#         current_end_time = current_start_time + timedelta(minutes=chunk_size * 15)  # M15 candles
#         if current_end_time > end_time:
#             current_end_time = end_time
#         rates = mt5.copy_rates_range(symbol, timeframe, current_start_time, current_end_time)
#         if rates is None:
#             break
#         df = pd.DataFrame(rates)
#         df['time'] = pd.to_datetime(df['time'], unit='s')
#         df.set_index('time', inplace=True)
#         data.append(df)
#         current_start_time = current_end_time
#     return pd.concat(data, axis=0) if data else None

# # Function to identify support and resistance
# def find_support_resistance(df, lookback):
#     support_levels = []
#     resistance_levels = []

#     for i in range(lookback, len(df) - lookback):
#         if df['low'].iloc[i] == min(df['low'].iloc[i - lookback:i + lookback]):
#             support_levels.append((df.index[i], df['low'].iloc[i]))  # Store time and price
#         if df['high'].iloc[i] == max(df['high'].iloc[i - lookback:i + lookback]):
#             resistance_levels.append((df.index[i], df['high'].iloc[i]))  # Store time and price
    
#     if support_levels and resistance_levels:
#         return support_levels[-1], resistance_levels[-1]  # Return most recent support/resistance
#     else:
#         return None, None  # Return None if no levels found

# # Function to invalidate support/resistance if broken by consecutive candles
# def invalidate_zone(df, support, resistance, invalidate_threshold):
#     if support:
#         support_index = df.index.get_loc(support[0])  # Get the integer position of the timestamp
#         support_price = support[1]
#         consecutive_bearish = 0
#         for i in range(support_index, len(df)):
#             if df['close'].iloc[i] < support_price:
#                 consecutive_bearish += 1
#             else:
#                 consecutive_bearish = 0
#             if consecutive_bearish >= invalidate_threshold:
#                 return True
#     if resistance:
#         resistance_index = df.index.get_loc(resistance[0])  # Get the integer position of the timestamp
#         resistance_price = resistance[1]
#         consecutive_bullish = 0
#         for i in range(resistance_index, len(df)):
#             if df['close'].iloc[i] > resistance_price:
#                 consecutive_bullish += 1
#             else:
#                 consecutive_bullish = 0
#             if consecutive_bullish >= invalidate_threshold:
#                 return True
#     return False  # No invalidation

# # Function to check M15 confirmation
# def check_m15_confirmation(support, resistance, df_m15):
#     latest_price = df_m15['close'].iloc[-1]

#     # If price is at resistance, wait for a break of recent low
#     if latest_price >= resistance[1]:
#         recent_low = min(df_m15['low'].iloc[-10:])  # Get lowest point in last 10 candles
#         if latest_price < recent_low:  # Price broke recent low
#             return 'sell'

#     # If price is at support, wait for a break of recent high
#     elif latest_price <= support[1]:
#         recent_high = max(df_m15['high'].iloc[-10:])  # Get highest point in last 10 candles
#         if latest_price > recent_high:  # Price broke recent high
#             return 'buy'
    
#     return None  # No confirmation

# # Function to simulate the backtest
# def backtest(symbol, start_date, end_date):
#     confirmed_buys = 0
#     confirmed_sells = 0
#     buy_tps = 0
#     buy_sls = 0
#     sell_tps = 0
#     sell_sls = 0
    
#     # Fetch the data in chunks
#     df_h1 = get_data_in_chunks(symbol, timeframe_H1, start_date, end_date)
#     df_m15 = get_data_in_chunks(symbol, timeframe_M15, start_date, end_date)

#     if df_h1 is None or df_m15 is None:
#         print("Data retrieval failed.")
#         return
    
#     # Create progress bar
#     for i in tqdm(range(len(df_h1) - 1), desc="Processing H1 data", unit="bars"):
#         support_h1, resistance_h1 = find_support_resistance(df_h1, lookback)
#         support_m15, resistance_m15 = find_support_resistance(df_m15, lookback)

#         # Invalidate zones if necessary
#         if invalidate_zone(df_h1, support_h1, resistance_h1, invalidate_threshold):
#             support_h1, resistance_h1 = None, None
#         if invalidate_zone(df_m15, support_m15, resistance_m15, invalidate_threshold):
#             support_m15, resistance_m15 = None, None
        
#         # Check for confirmation
#         if support_h1 is not None and resistance_h1 is not None:
#             confirmation = check_m15_confirmation(support_h1, resistance_h1, df_m15)
#             if confirmation == 'buy' and df_h1['close'].iloc[i] <= support_h1[1]:
#                 confirmed_buys += 1
#                 tp_price = df_h1['close'].iloc[i] + take_profit * 0.0001
#                 sl_price = df_h1['close'].iloc[i] - stop_loss * 0.0001
#                 if df_h1['high'].iloc[i] >= tp_price:
#                     buy_tps += 1
#                 elif df_h1['low'].iloc[i] <= sl_price:
#                     buy_sls += 1
            
#             elif confirmation == 'sell' and df_h1['close'].iloc[i] >= resistance_h1[1]:
#                 confirmed_sells += 1
#                 tp_price = df_h1['close'].iloc[i] - take_profit * 0.0001
#                 sl_price = df_h1['close'].iloc[i] + stop_loss * 0.0001
#                 if df_h1['low'].iloc[i] <= tp_price:
#                     sell_tps += 1
#                 elif df_h1['high'].iloc[i] >= sl_price:
#                     sell_sls += 1

#     print(f"Confirmed Buy Opportunities: {confirmed_buys}")
#     print(f"Confirmed Sell Opportunities: {confirmed_sells}")
#     print(f"Buy Opportunities that hit TP: {buy_tps}")
#     print(f"Buy Opportunities that hit SL: {buy_sls}")
#     print(f"Sell Opportunities that hit TP: {sell_tps}")
#     print(f"Sell Opportunities that hit SL: {sell_sls}")

# # Backtest using the last 2 months of data
# end_date = datetime.now()
# start_date = end_date - timedelta(days=10)  # 2 months back

# backtest(symbol, start_date, end_date)







# inacuracy in logic, only checking h1 timeframe resulting in false output of data

# import MetaTrader5 as mt5
# import pandas as pd
# import time
# import winsound  # For sound alerts
# import mplfinance as mpf
# from datetime import datetime, timedelta
# from tqdm import tqdm  # Progress bar library

# # Connect to MetaTrader 5
# if not mt5.initialize():
#     print("MT5 connection failed")
#     mt5.shutdown()
#     quit()

# print("Connected to MT5")

# # Define parameters
# symbol = "GBPJPY"
# timeframe_H1 = mt5.TIMEFRAME_H1
# timeframe_M15 = mt5.TIMEFRAME_M15
# num_bars = 480  # Adjusted for 20 days of H1 data (20 days * 24 hours = 480 bars)
# lookback = 20  # Lookback window for support/resistance
# invalidate_threshold = 3  # Number of consecutive candles for invalidation
# take_profit = 30  # in pips
# stop_loss = 20  # in pips

# # Function to get historical data in smaller chunks
# def get_data_in_chunks(symbol, timeframe, start_time, end_time, chunk_size=100):
#     data = []
#     current_start_time = start_time

#     while current_start_time < end_time:
#         current_end_time = current_start_time + timedelta(minutes=chunk_size * 15)  # M15 candles
#         if current_end_time > end_time:
#             current_end_time = end_time
#         rates = mt5.copy_rates_range(symbol, timeframe, current_start_time, current_end_time)
#         if rates is None:
#             break
#         df = pd.DataFrame(rates)
#         df['time'] = pd.to_datetime(df['time'], unit='s')
#         df.set_index('time', inplace=True)
#         data.append(df)
#         current_start_time = current_end_time
#     return pd.concat(data, axis=0) if data else None

# # Function to identify support and resistance
# def find_support_resistance(df, lookback):
#     support_levels = []
#     resistance_levels = []

#     for i in range(lookback, len(df) - lookback):
#         if df['low'].iloc[i] == min(df['low'].iloc[i - lookback:i + lookback]):
#             support_levels.append((df.index[i], df['low'].iloc[i]))  # Store time and price
#         if df['high'].iloc[i] == max(df['high'].iloc[i - lookback:i + lookback]):
#             resistance_levels.append((df.index[i], df['high'].iloc[i]))  # Store time and price
    
#     if support_levels and resistance_levels:
#         return support_levels[-1], resistance_levels[-1]  # Return most recent support/resistance
#     else:
#         return None, None  # Return None if no levels found

# # Function to invalidate support/resistance if broken by consecutive candles
# def invalidate_zone(df, support, resistance, invalidate_threshold):
#     if support:
#         support_index = df.index.get_loc(support[0])  # Get the integer position of the timestamp
#         support_price = support[1]
#         consecutive_bearish = 0
#         for i in range(support_index, len(df)):
#             if df['close'].iloc[i] < support_price:
#                 consecutive_bearish += 1
#             else:
#                 consecutive_bearish = 0
#             if consecutive_bearish >= invalidate_threshold:
#                 return True
#     if resistance:
#         resistance_index = df.index.get_loc(resistance[0])  # Get the integer position of the timestamp
#         resistance_price = resistance[1]
#         consecutive_bullish = 0
#         for i in range(resistance_index, len(df)):
#             if df['close'].iloc[i] > resistance_price:
#                 consecutive_bullish += 1
#             else:
#                 consecutive_bullish = 0
#             if consecutive_bullish >= invalidate_threshold:
#                 return True
#     return False  # No invalidation

# # Function to check M15 confirmation
# def check_m15_confirmation(support, resistance, df_m15):
#     latest_price = df_m15['close'].iloc[-1]

#     # If price is at resistance, wait for a break of recent low
#     if latest_price >= resistance[1]:
#         recent_low = min(df_m15['low'].iloc[-10:])  # Get lowest point in last 10 candles
#         if latest_price < recent_low:  # Price broke recent low
#             return 'sell'

#     # If price is at support, wait for a break of recent high
#     elif latest_price <= support[1]:
#         recent_high = max(df_m15['high'].iloc[-10:])  # Get highest point in last 10 candles
#         if latest_price > recent_high:  # Price broke recent high
#             return 'buy'
    
#     return None  # No confirmation

# # Function to simulate the backtest
# def backtest(symbol, start_date, end_date):
#     confirmed_buys = 0
#     confirmed_sells = 0
#     buy_tps = 0
#     buy_sls = 0
#     sell_tps = 0
#     sell_sls = 0
    
#     # Fetch the data in chunks
#     df_h1 = get_data_in_chunks(symbol, timeframe_H1, start_date, end_date)
#     df_m15 = get_data_in_chunks(symbol, timeframe_M15, start_date, end_date)

#     if df_h1 is None or df_m15 is None:
#         print("Data retrieval failed.")
#         return
    
#     # Create progress bar
#     for i in tqdm(range(len(df_h1) - 1), desc="Processing H1 data", unit="bars"):
#         support_h1, resistance_h1 = find_support_resistance(df_h1, lookback)
#         support_m15, resistance_m15 = find_support_resistance(df_m15, lookback)

#         # Invalidate zones if necessary
#         if invalidate_zone(df_h1, support_h1, resistance_h1, invalidate_threshold):
#             support_h1, resistance_h1 = None, None
#         if invalidate_zone(df_m15, support_m15, resistance_m15, invalidate_threshold):
#             support_m15, resistance_m15 = None, None
        
#         # Check for confirmation
#         if support_h1 is not None and resistance_h1 is not None:
#             confirmation = check_m15_confirmation(support_h1, resistance_h1, df_m15)
#             if confirmation == 'buy' and df_h1['close'].iloc[i] <= support_h1[1]:
#                 confirmed_buys += 1
#                 tp_price = df_h1['close'].iloc[i] + take_profit * 0.0001
#                 sl_price = df_h1['close'].iloc[i] - stop_loss * 0.0001
#                 if df_h1['high'].iloc[i] >= tp_price:
#                     buy_tps += 1
#                 elif df_h1['low'].iloc[i] <= sl_price:
#                     buy_sls += 1
            
#             elif confirmation == 'sell' and df_h1['close'].iloc[i] >= resistance_h1[1]:
#                 confirmed_sells += 1
#                 tp_price = df_h1['close'].iloc[i] - take_profit * 0.0001
#                 sl_price = df_h1['close'].iloc[i] + stop_loss * 0.0001
#                 if df_h1['low'].iloc[i] <= tp_price:
#                     sell_tps += 1
#                 elif df_h1['high'].iloc[i] >= sl_price:
#                     sell_sls += 1

#     print(f"Confirmed Buy Opportunities: {confirmed_buys}")
#     print(f"Confirmed Sell Opportunities: {confirmed_sells}")
#     print(f"Buy Opportunities that hit TP: {buy_tps}")
#     print(f"Buy Opportunities that hit SL: {buy_sls}")
#     print(f"Sell Opportunities that hit TP: {sell_tps}")
#     print(f"Sell Opportunities that hit SL: {sell_sls}")

# # Backtest using the last 20 days of data
# end_date = datetime.now()
# start_date = end_date - timedelta(days=20)  # Adjusted to 20 days back

# backtest(symbol, start_date, end_date)





# corrected logic (hopefuly)

# import MetaTrader5 as mt5
# import pandas as pd
# import time
# import winsound  # For sound alerts
# import mplfinance as mpf
# from datetime import datetime, timedelta
# from tqdm import tqdm  # Progress bar library

# # Connect to MetaTrader 5
# if not mt5.initialize():
#     print("MT5 connection failed")
#     mt5.shutdown()
#     quit()

# print("Connected to MT5")

# # Define parameters
# symbol = "GBPJPY"
# timeframe_H1 = mt5.TIMEFRAME_H1
# timeframe_M15 = mt5.TIMEFRAME_M15
# num_bars = 500  # Number of candles to fetch (adjust as needed)
# lookback = 20  # Lookback window for support/resistance
# invalidate_threshold = 3  # Number of consecutive candles for invalidation
# take_profit = 30  # in pips
# stop_loss = 20  # in pips

# # Function to get historical data in smaller chunks
# def get_data_in_chunks(symbol, timeframe, start_time, end_time, chunk_size=100):
#     data = []
#     current_start_time = start_time

#     while current_start_time < end_time:
#         current_end_time = current_start_time + timedelta(minutes=chunk_size * 15)  # M15 candles
#         if current_end_time > end_time:
#             current_end_time = end_time
#         rates = mt5.copy_rates_range(symbol, timeframe, current_start_time, current_end_time)
#         if rates is None:
#             break
#         df = pd.DataFrame(rates)
#         df['time'] = pd.to_datetime(df['time'], unit='s')
#         df.set_index('time', inplace=True)
#         data.append(df)
#         current_start_time = current_end_time
#     return pd.concat(data, axis=0) if data else None

# # Function to identify support and resistance
# def find_support_resistance(df, lookback):
#     support_levels = []
#     resistance_levels = []

#     for i in range(lookback, len(df) - lookback):
#         if df['low'].iloc[i] == min(df['low'].iloc[i - lookback:i + lookback]):
#             support_levels.append((df.index[i], df['low'].iloc[i]))  # Store time and price
#         if df['high'].iloc[i] == max(df['high'].iloc[i - lookback:i + lookback]):
#             resistance_levels.append((df.index[i], df['high'].iloc[i]))  # Store time and price
    
#     if support_levels and resistance_levels:
#         return support_levels[-1], resistance_levels[-1]  # Return most recent support/resistance
#     else:
#         return None, None  # Return None if no levels found

# # Function to invalidate support/resistance if broken by consecutive candles
# def invalidate_zone(df, support, resistance, invalidate_threshold):
#     if support:
#         support_index = df.index.get_loc(support[0])  # Get the integer position of the timestamp
#         support_price = support[1]
#         consecutive_bearish = 0
#         for i in range(support_index, len(df)):
#             if df['close'].iloc[i] < support_price:
#                 consecutive_bearish += 1
#             else:
#                 consecutive_bearish = 0
#             if consecutive_bearish >= invalidate_threshold:
#                 return True
#     if resistance:
#         resistance_index = df.index.get_loc(resistance[0])  # Get the integer position of the timestamp
#         resistance_price = resistance[1]
#         consecutive_bullish = 0
#         for i in range(resistance_index, len(df)):
#             if df['close'].iloc[i] > resistance_price:
#                 consecutive_bullish += 1
#             else:
#                 consecutive_bullish = 0
#             if consecutive_bullish >= invalidate_threshold:
#                 return True
#     return False  # No invalidation

# # Function to check M15 confirmation
# def check_m15_confirmation(support, resistance, df_m15):
#     latest_price = df_m15['close'].iloc[-1]

#     # If price is at resistance, wait for a break of recent low
#     if latest_price >= resistance[1]:
#         recent_low = min(df_m15['low'].iloc[-10:])  # Get lowest point in last 10 candles
#         if latest_price < recent_low:  # Price broke recent low
#             return 'sell'

#     # If price is at support, wait for a break of recent high
#     elif latest_price <= support[1]:
#         recent_high = max(df_m15['high'].iloc[-10:])  # Get highest point in last 10 candles
#         if latest_price > recent_high:  # Price broke recent high
#             return 'buy'
    
#     return None  # No confirmation

# # Function to simulate the backtest
# def backtest(symbol, start_date, end_date):
#     confirmed_buys = 0
#     confirmed_sells = 0
#     buy_tps = 0
#     buy_sls = 0
#     sell_tps = 0
#     sell_sls = 0
    
#     # Fetch the data in chunks
#     df_h1 = get_data_in_chunks(symbol, timeframe_H1, start_date, end_date)
#     df_m15 = get_data_in_chunks(symbol, timeframe_M15, start_date, end_date)

#     if df_h1 is None or df_m15 is None:
#         print("Data retrieval failed.")
#         return
    
#     # Create progress bar
#     for i in tqdm(range(len(df_h1) - 1), desc="Processing data", unit="bars"):
#         # Find support and resistance for both timeframes
#         support_h1, resistance_h1 = find_support_resistance(df_h1, lookback)
#         support_m15, resistance_m15 = find_support_resistance(df_m15, lookback)

#         # Invalidate zones if necessary for both timeframes
#         if invalidate_zone(df_h1, support_h1, resistance_h1, invalidate_threshold):
#             support_h1, resistance_h1 = None, None
#         if invalidate_zone(df_m15, support_m15, resistance_m15, invalidate_threshold):
#             support_m15, resistance_m15 = None, None
        
#         # Check for confirmation using M15
#         if support_h1 and resistance_h1:
#             confirmation = check_m15_confirmation(support_h1, resistance_h1, df_m15)
            
#             if confirmation == 'buy' and df_h1['close'].iloc[i] <= support_h1[1]:
#                 confirmed_buys += 1
#                 tp_price = df_h1['close'].iloc[i] + take_profit * 0.0001
#                 sl_price = df_h1['close'].iloc[i] - stop_loss * 0.0001
#                 if df_h1['high'].iloc[i] >= tp_price:
#                     buy_tps += 1
#                 elif df_h1['low'].iloc[i] <= sl_price:
#                     buy_sls += 1
            
#             elif confirmation == 'sell' and df_h1['close'].iloc[i] >= resistance_h1[1]:
#                 confirmed_sells += 1
#                 tp_price = df_h1['close'].iloc[i] - take_profit * 0.0001
#                 sl_price = df_h1['close'].iloc[i] + stop_loss * 0.0001
#                 if df_h1['low'].iloc[i] <= tp_price:
#                     sell_tps += 1
#                 elif df_h1['high'].iloc[i] >= sl_price:
#                     sell_sls += 1

#     print(f"Confirmed Buy Opportunities: {confirmed_buys}")
#     print(f"Confirmed Sell Opportunities: {confirmed_sells}")
#     print(f"Buy Opportunities that hit TP: {buy_tps}")
#     print(f"Buy Opportunities that hit SL: {buy_sls}")
#     print(f"Sell Opportunities that hit TP: {sell_tps}")
#     print(f"Sell Opportunities that hit SL: {sell_sls}")

# # Backtest using the last 20 days of data
# end_date = datetime.now()
# start_date = end_date - timedelta(days=20)  # 20 days back

# backtest(symbol, start_date, end_date)



# Modified backtest script with debug prints

import MetaTrader5 as mt5
import pandas as pd
import time
import winsound  # For sound alerts
import mplfinance as mpf
from datetime import datetime, timedelta
from tqdm import tqdm  # Progress bar library

# Connect to MetaTrader 5
if not mt5.initialize():
    print("MT5 connection failed")
    mt5.shutdown()
    quit()

print("Connected to MT5")

# Define parameters
symbol = "GBPJPY"
timeframe_H1 = mt5.TIMEFRAME_H1
timeframe_M15 = mt5.TIMEFRAME_M15
num_bars = 500  # Number of candles to fetch (adjust as needed)
lookback = 20  # Lookback window for support/resistance
invalidate_threshold = 3  # Number of consecutive candles for invalidation
take_profit = 30  # in pips
stop_loss = 20  # in pips
atr_period = 14  # ATR period for stop loss and take profit

# Function to get historical data in smaller chunks
def get_data_in_chunks(symbol, timeframe, start_time, end_time, chunk_size=100):
    data = []
    current_start_time = start_time

    while current_start_time < end_time:
        current_end_time = current_start_time + timedelta(minutes=chunk_size * 15)  # M15 candles
        if current_end_time > end_time:
            current_end_time = end_time
        rates = mt5.copy_rates_range(symbol, timeframe, current_start_time, current_end_time)
        if rates is None:
            break
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df.set_index('time', inplace=True)
        data.append(df)
        current_start_time = current_end_time
    return pd.concat(data, axis=0) if data else None

# Function to calculate ATR manually using Pandas
def calculate_atr(df, period=14):
    df['H-L'] = df['high'] - df['low']
    df['H-PC'] = abs(df['high'] - df['close'].shift(1))
    df['L-PC'] = abs(df['low'] - df['close'].shift(1))
    
    df['TR'] = df[['H-L', 'H-PC', 'L-PC']].max(axis=1)
    df['ATR'] = df['TR'].rolling(window=period).mean()
    
    return df['ATR']

# Function to identify support and resistance
def find_support_resistance(df, lookback):
    support_levels = []
    resistance_levels = []

    for i in range(lookback, len(df) - lookback):
        if df['low'].iloc[i] == min(df['low'].iloc[i - lookback:i + lookback]):
            support_levels.append((df.index[i], df['low'].iloc[i]))  # Store time and price
        if df['high'].iloc[i] == max(df['high'].iloc[i - lookback:i + lookback]):
            resistance_levels.append((df.index[i], df['high'].iloc[i]))  # Store time and price
    
    if support_levels and resistance_levels:
        print(f"Latest Support Level: {support_levels[-1]}")  # Debug
        print(f"Latest Resistance Level: {resistance_levels[-1]}")  # Debug
        return support_levels[-1], resistance_levels[-1]  # Return most recent support/resistance
    else:
        return None, None  # Return None if no levels found

# Function to invalidate support/resistance if broken by consecutive candles
def invalidate_zone(df, support, resistance, invalidate_threshold):
    if support:
        support_index = df.index.get_loc(support[0])  # Get the integer position of the timestamp
        support_price = support[1]
        consecutive_bearish = 0
        for i in range(support_index, len(df)):
            if df['close'].iloc[i] < support_price:
                consecutive_bearish += 1
            else:
                consecutive_bearish = 0
            if consecutive_bearish >= invalidate_threshold:
                return True
    if resistance:
        resistance_index = df.index.get_loc(resistance[0])  # Get the integer position of the timestamp
        resistance_price = resistance[1]
        consecutive_bullish = 0
        for i in range(resistance_index, len(df)):
            if df['close'].iloc[i] > resistance_price:
                consecutive_bullish += 1
            else:
                consecutive_bullish = 0
            if consecutive_bullish >= invalidate_threshold:
                return True
    return False  # No invalidation

# Function to check M15 confirmation
def check_m15_confirmation(support, resistance, df_m15):
    latest_price = df_m15['close'].iloc[-1]
    print(f"Latest M15 Price: {latest_price}")  # Debug

    # If price is at resistance, wait for a break of recent low
    if latest_price >= resistance[1]:
        recent_low = min(df_m15['low'].iloc[-10:])  # Get lowest point in last 10 candles
        if latest_price < recent_low:  # Price broke recent low
            return 'sell'

    # If price is at support, wait for a break of recent high
    elif latest_price <= support[1]:
        recent_high = max(df_m15['high'].iloc[-10:])  # Get highest point in last 10 candles
        if latest_price > recent_high:  # Price broke recent high
            return 'buy'
    
    return None  # No confirmation

# Track trades and results
trades = []

# Function to simulate the backtest
def backtest(symbol, start_date, end_date):
    confirmed_buys = 0
    confirmed_sells = 0
    buy_tps = 0
    buy_sls = 0
    sell_tps = 0
    sell_sls = 0

    # Fetch the data in chunks
    df_h1 = get_data_in_chunks(symbol, timeframe_H1, start_date, end_date)
    df_m15 = get_data_in_chunks(symbol, timeframe_M15, start_date, end_date)

    if df_h1 is None or df_m15 is None:
        print("Data retrieval failed.")
        return

    # Calculate ATR for stop loss and take profit calculation using Pandas
    df_m15['ATR'] = calculate_atr(df_m15, atr_period)
    print(f"ATR: {df_m15['ATR'].tail(10)}")  # Debug

    # Create progress bar
    for i in tqdm(range(1, len(df_h1)-1), desc="Processing data", unit="bars"):
        # Find support and resistance for both timeframes
        support_h1, resistance_h1 = find_support_resistance(df_h1, lookback)
        support_m15, resistance_m15 = find_support_resistance(df_m15, lookback)

        # Invalidate zones if necessary for both timeframes
        if invalidate_zone(df_h1, support_h1, resistance_h1, invalidate_threshold):
            support_h1, resistance_h1 = None, None
        if invalidate_zone(df_m15, support_m15, resistance_m15, invalidate_threshold):
            support_m15, resistance_m15 = None, None
        
        # Check for confirmation using M15
        if support_h1 and resistance_h1:
            confirmation = check_m15_confirmation(support_h1, resistance_h1, df_m15)
            
            if confirmation == 'buy' and df_h1['close'].iloc[i] <= support_h1[1]:
                entry_price = df_m15['close'].iloc[i]
                stop_loss = support_h1[1] - (2 * df_m15['ATR'].iloc[i])  # Example SL based on ATR
                take_profit = entry_price + (2 * df_m15['ATR'].iloc[i])  # Example TP based on ATR
                
                trades.append({'entry': entry_price, 'stop_loss': stop_loss, 'take_profit': take_profit, 'direction': 'buy'})
                confirmed_buys += 1
            
            elif confirmation == 'sell' and df_h1['close'].iloc[i] >= resistance_h1[1]:
                entry_price = df_m15['close'].iloc[i]
                stop_loss = resistance_h1[1] + (2 * df_m15['ATR'].iloc[i])  # Example SL based on ATR
                take_profit = entry_price - (2 * df_m15['ATR'].iloc[i])  # Example TP based on ATR
                
                trades.append({'entry': entry_price, 'stop_loss': stop_loss, 'take_profit': take_profit, 'direction': 'sell'})
                confirmed_sells += 1

    # Exit logic: Check if the trade hits TP or SL
    for trade in trades:
        for i in range(len(df_m15)):
            if trade['direction'] == 'buy':
                if df_m15['close'].iloc[i] <= trade['stop_loss']:
                    print(f"Buy trade hit SL at {trade['stop_loss']}")
                    buy_sls += 1
                elif df_m15['close'].iloc[i] >= trade['take_profit']:
                    print(f"Buy trade hit TP at {trade['take_profit']}")
                    buy_tps += 1
            
            elif trade['direction'] == 'sell':
                if df_m15['close'].iloc[i] >= trade['stop_loss']:
                    print(f"Sell trade hit SL at {trade['stop_loss']}")
                    sell_sls += 1
                elif df_m15['close'].iloc[i] <= trade['take_profit']:
                    print(f"Sell trade hit TP at {trade['take_profit']}")
                    sell_tps += 1

    # Output summary
    print(f"Confirmed Buys: {confirmed_buys}, Confirmed Sells: {confirmed_sells}")
    print(f"Buy TP: {buy_tps}, Buy SL: {buy_sls}")
    print(f"Sell TP: {sell_tps}, Sell SL: {sell_sls}")

# Example run
start_date = datetime(2024, 12, 30)
end_date = datetime(2025, 2, 5)
backtest(symbol, start_date, end_date)

# Close the MT5 connection
mt5.shutdown()
