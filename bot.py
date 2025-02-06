# trizl to print m15 minutes as well - works perfectly, a lile modification to be made - toimporve accuracy on 15m

# import MetaTrader5 as mt5
# import pandas as pd
# import time
# import winsound  # For sound alerts
# import matplotlib.pyplot as plt
# import mplfinance as mpf

# # Connect to MetaTrader 5
# if not mt5.initialize():
#     print("MT5 connection failed")
#     mt5.shutdown()
#     quit()

# print("Connected to MT5")

# # Define parameters
# symbol = "USDJPY"
# timeframe_H1 = mt5.TIMEFRAME_H1
# timeframe_M15 = mt5.TIMEFRAME_M15
# num_bars = 100  # Number of candles to fetch
# lookback = 20  # Lookback window for support/resistance

# # Function to get historical data
# def get_data(symbol, timeframe, bars):
#     rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, bars)
#     if rates is None:
#         return None
#     df = pd.DataFrame(rates)
#     df['time'] = pd.to_datetime(df['time'], unit='s')
#     df.set_index('time', inplace=True)
#     return df

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

# # Function to send MT5 notification
# def send_mt5_notification(message):
#     request = {
#         "action": mt5.TRADE_ACTION_DEAL,
#         "symbol": symbol,
#         "comment": message
#     }
#     mt5.order_send(request)

# # Function to check M15 confirmation
# def check_m15_confirmation(support, resistance):
#     df_m15 = get_data(symbol, timeframe_M15, 50)  # Get recent 50 candles
#     latest_price = df_m15['close'].iloc[-1]

#     # If price is at resistance, wait for a break of recent low
#     if latest_price >= resistance[1]:
#         recent_low = min(df_m15['low'].iloc[-10:])  # Get lowest point in last 10 candles
#         if latest_price < recent_low:  # Price broke recent low
#             print("Sell Confirmation! Price broke recent low at resistance.")
#             winsound.Beep(1000, 500)  # Sound alert
#             send_mt5_notification("Sell Alert! Price broke recent low at resistance.")

#     # If price is at support, wait for a break of recent high
#     elif latest_price <= support[1]:
#         recent_high = max(df_m15['high'].iloc[-10:])  # Get highest point in last 10 candles
#         if latest_price > recent_high:  # Price broke recent high
#             print("Buy Confirmation! Price broke recent high at support.")
#             winsound.Beep(1500, 500)  # Sound alert
#             send_mt5_notification("Buy Alert! Price broke recent high at support.")

# # Function to plot chart with highlighted support/resistance zones
# def plot_chart_with_zones(df, support, resistance, timeframe='H1'):
#     apds = []
    
#     if support and resistance:
#         support_zone = pd.Series([support[1]] * len(df), index=df.index)
#         resistance_zone = pd.Series([resistance[1]] * len(df), index=df.index)
        
#         apds.append(mpf.make_addplot(support_zone, color='green', secondary_y=False))
#         apds.append(mpf.make_addplot(resistance_zone, color='red', secondary_y=False))
    
#     plot_style = mpf.make_mpf_style(base_mpf_style='charles', rc={'font.size': 12})
    
#     mpf.plot(df, type='candle', style=plot_style, title=f'{symbol} {timeframe} Chart with Support & Resistance',
#              ylabel='Price', addplot=apds)

# # Main loop to monitor price
# while True:
#     # Fetch H1 and M15 data
#     df_h1 = get_data(symbol, timeframe_H1, num_bars)
#     df_m15 = get_data(symbol, timeframe_M15, num_bars)

#     if df_h1 is not None and df_m15 is not None:
#         # Find support and resistance for both timeframes
#         support_h1, resistance_h1 = find_support_resistance(df_h1, lookback)
#         support_m15, resistance_m15 = find_support_resistance(df_m15, lookback)
        
#         latest_price_h1 = df_h1['close'].iloc[-1]
#         latest_price_m15 = df_m15['close'].iloc[-1]

#         # Plot the charts with support/resistance zones for both H1 and M15
#         plot_chart_with_zones(df_h1, support_h1, resistance_h1, timeframe='H1')
#         plot_chart_with_zones(df_m15, support_m15, resistance_m15, timeframe='M15')

#         # Check price against support or resistance for both timeframes
#         if support_h1 is None or resistance_h1 is None or support_m15 is None or resistance_m15 is None:
#             print("No valid support or resistance levels found.")
#         else:
#             # Check for H1 and M15 price confirmations
#             if latest_price_h1 >= resistance_h1[1]:
#                 print(f"Price reached H1 resistance: {resistance_h1[1]}")
#                 winsound.Beep(2000, 500)  # Sound alert
#                 send_mt5_notification(f"Price at H1 resistance {resistance_h1[1]} - Watching for confirmation")
#                 check_m15_confirmation(support_h1, resistance_h1)

#             elif latest_price_h1 <= support_h1[1]:
#                 print(f"Price reached H1 support: {support_h1[1]}")
#                 winsound.Beep(2000, 500)  # Sound alert
#                 send_mt5_notification(f"Price at H1 support {support_h1[1]} - Watching for confirmation")
#                 check_m15_confirmation(support_h1, resistance_h1)

#             if latest_price_m15 >= resistance_m15[1]:
#                 print(f"Price reached M15 resistance: {resistance_m15[1]}")
#                 winsound.Beep(2000, 500)  # Sound alert
#                 send_mt5_notification(f"Price at M15 resistance {resistance_m15[1]} - Watching for confirmation")
#                 check_m15_confirmation(support_m15, resistance_m15)

#             elif latest_price_m15 <= support_m15[1]:
#                 print(f"Price reached M15 support: {support_m15[1]}")
#                 winsound.Beep(2000, 500)  # Sound alert
#                 send_mt5_notification(f"Price at M15 support {support_m15[1]} - Watching for confirmation")
#                 check_m15_confirmation(support_m15, resistance_m15)

#     time.sleep(60)  # Wait 1 minute before checking again

# # Shutdown MT5 connection
# mt5.shutdown()






# built to check for invalid zones, correction on right 15m zones - WORKS PERFECTLY WELL , BELOW IS ONLY IMPROVEMENT ADDING SL AND TP

# import MetaTrader5 as mt5
# import pandas as pd
# import time
# import winsound  # For sound alerts
# import matplotlib.pyplot as plt
# import mplfinance as mpf

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
# num_bars = 100  # Number of candles to fetch
# lookback = 20  # Lookback window for support/resistance
# invalidate_threshold = 3  # Number of consecutive candles for invalidation

# # Function to get historical data
# def get_data(symbol, timeframe, bars):
#     rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, bars)
#     if rates is None:
#         return None
#     df = pd.DataFrame(rates)
#     df['time'] = pd.to_datetime(df['time'], unit='s')
#     df.set_index('time', inplace=True)
#     return df

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
#     # Check for break of support
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
#                 print(f"Support at {support_price} invalidated by {consecutive_bearish} bearish candles.")
#                 return True
#     # Check for break of resistance
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
#                 print(f"Resistance at {resistance_price} invalidated by {consecutive_bullish} bullish candles.")
#                 return True
#     return False  # No invalidation


# # Function to send MT5 notification
# def send_mt5_notification(message):
#     request = {
#         "action": mt5.TRADE_ACTION_DEAL,
#         "symbol": symbol,
#         "comment": message
#     }
#     mt5.order_send(request)

# # Function to check M15 confirmation
# def check_m15_confirmation(support, resistance):
#     df_m15 = get_data(symbol, timeframe_M15, 50)  # Get recent 50 candles
#     latest_price = df_m15['close'].iloc[-1]

#     # If price is at resistance, wait for a break of recent low
#     if latest_price >= resistance[1]:
#         recent_low = min(df_m15['low'].iloc[-10:])  # Get lowest point in last 10 candles
#         if latest_price < recent_low:  # Price broke recent low
#             print("Sell Confirmation! Price broke recent low at resistance.")
#             winsound.Beep(1000, 500)  # Sound alert
#             send_mt5_notification("Sell Alert! Price broke recent low at resistance.")

#     # If price is at support, wait for a break of recent high
#     elif latest_price <= support[1]:
#         recent_high = max(df_m15['high'].iloc[-10:])  # Get highest point in last 10 candles
#         if latest_price > recent_high:  # Price broke recent high
#             print("Buy Confirmation! Price broke recent high at support.")
#             winsound.Beep(1500, 500)  # Sound alert
#             send_mt5_notification("Buy Alert! Price broke recent high at support.")

# # Function to plot chart with highlighted support/resistance zones
# def plot_chart_with_zones(df, support, resistance, timeframe='H1'):
#     apds = []
    
#     if support and resistance:
#         support_zone = pd.Series([support[1]] * len(df), index=df.index)
#         resistance_zone = pd.Series([resistance[1]] * len(df), index=df.index)
        
#         apds.append(mpf.make_addplot(support_zone, color='green', secondary_y=False))
#         apds.append(mpf.make_addplot(resistance_zone, color='red', secondary_y=False))
    
#     plot_style = mpf.make_mpf_style(base_mpf_style='charles', rc={'font.size': 12})
    
#     mpf.plot(df, type='candle', style=plot_style, title=f'{symbol} {timeframe} Chart with Support & Resistance',
#              ylabel='Price', addplot=apds)

# # Main loop to monitor price
# while True:
#     # Fetch H1 and M15 data
#     df_h1 = get_data(symbol, timeframe_H1, num_bars)
#     df_m15 = get_data(symbol, timeframe_M15, num_bars)

#     if df_h1 is not None and df_m15 is not None:
#         # Find support and resistance for both timeframes
#         support_h1, resistance_h1 = find_support_resistance(df_h1, lookback)
#         support_m15, resistance_m15 = find_support_resistance(df_m15, lookback)
        
#         # Invalidate support/resistance if broken
#         if invalidate_zone(df_h1, support_h1, resistance_h1, invalidate_threshold):
#             support_h1, resistance_h1 = None, None  # Invalidate H1 zones
#         if invalidate_zone(df_m15, support_m15, resistance_m15, invalidate_threshold):
#             support_m15, resistance_m15 = None, None  # Invalidate M15 zones
        
#         latest_price_h1 = df_h1['close'].iloc[-1]
#         latest_price_m15 = df_m15['close'].iloc[-1]

#         # Plot the charts with support/resistance zones for both H1 and M15
#         plot_chart_with_zones(df_h1, support_h1, resistance_h1, timeframe='H1')
#         plot_chart_with_zones(df_m15, support_m15, resistance_m15, timeframe='M15')

#         # Check price against support or resistance for both timeframes
#         if support_h1 is None or resistance_h1 is None or support_m15 is None or resistance_m15 is None:
#             print("No valid support or resistance levels found.")
#         else:
#             # Check for H1 and M15 price confirmations
#             if latest_price_h1 >= resistance_h1[1]:
#                 print(f"Price reached H1 resistance: {resistance_h1[1]}")
#                 winsound.Beep(2000, 500)  # Sound alert
#                 send_mt5_notification(f"Price at H1 resistance {resistance_h1[1]} - Watching for confirmation")
#                 check_m15_confirmation(support_h1, resistance_h1)

#             elif latest_price_h1 <= support_h1[1]:
#                 print(f"Price reached H1 support: {support_h1[1]}")
#                 winsound.Beep(2000, 500)  # Sound alert
#                 send_mt5_notification(f"Price at H1 support {support_h1[1]} - Watching for confirmation")
#                 check_m15_confirmation(support_h1, resistance_h1)

#             if latest_price_m15 >= resistance_m15[1]:
#                 print(f"Price reached M15 resistance: {resistance_m15[1]}")
#                 winsound.Beep(2000, 500)  # Sound alert
#                 send_mt5_notification(f"Price at M15 resistance {resistance_m15[1]} - Watching for confirmation")
#                 check_m15_confirmation(support_m15, resistance_m15)

#             elif latest_price_m15 <= support_m15[1]:
#                 print(f"Price reached M15 support: {support_m15[1]}")
#                 winsound.Beep(2000, 500)  # Sound alert
#                 send_mt5_notification(f"Price at M15 support {support_m15[1]} - Watching for confirmation")
#                 check_m15_confirmation(support_m15, resistance_m15)

#     time.sleep(60)  # Wait for 1 minute before next check





# improvement with sl and tp -  Presumably this should work perfectly, i want to test now with past data to see accuracy

import MetaTrader5 as mt5
import pandas as pd
import time
import winsound  # For sound alerts
import matplotlib.pyplot as plt
import mplfinance as mpf

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
num_bars = 100  # Number of candles to fetch
lookback = 20  # Lookback window for support/resistance
invalidate_threshold = 3  # Number of consecutive candles for invalidation

# Function to get historical data
def get_data(symbol, timeframe, bars):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, bars)
    if rates is None:
        return None
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.set_index('time', inplace=True)
    return df

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
                print(f"Support at {support_price} invalidated by {consecutive_bearish} bearish candles.")
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
                print(f"Resistance at {resistance_price} invalidated by {consecutive_bullish} bullish candles.")
                return True
    return False  # No invalidation

# Function to send MT5 notification
def send_mt5_notification(message):
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "comment": message
    }
    mt5.order_send(request)

# Function to check M15 confirmation
def check_m15_confirmation(support, resistance):
    df_m15 = get_data(symbol, timeframe_M15, 50)  # Get recent 50 candles
    latest_price = df_m15['close'].iloc[-1]

    # If price is at resistance, wait for a break of recent low
    if latest_price >= resistance[1]:
        recent_low = min(df_m15['low'].iloc[-10:])  # Get lowest point in last 10 candles
        if latest_price < recent_low:  # Price broke recent low
            print("Sell Confirmation! Price broke recent low at resistance.")
            winsound.Beep(1000, 500)  # Sound alert
            send_mt5_notification("Sell Alert! Price broke recent low at resistance.")

    # If price is at support, wait for a break of recent high
    elif latest_price <= support[1]:
        recent_high = max(df_m15['high'].iloc[-10:])  # Get highest point in last 10 candles
        if latest_price > recent_high:  # Price broke recent high
            print("Buy Confirmation! Price broke recent high at support.")
            winsound.Beep(1500, 500)  # Sound alert
            send_mt5_notification("Buy Alert! Price broke recent high at support.")

# Function to plot chart with highlighted support/resistance zones
def plot_chart_with_zones(df, support, resistance, timeframe='H1'):
    apds = []
    
    if support and resistance:
        support_zone = pd.Series([support[1]] * len(df), index=df.index)
        resistance_zone = pd.Series([resistance[1]] * len(df), index=df.index)
        
        apds.append(mpf.make_addplot(support_zone, color='green', secondary_y=False))
        apds.append(mpf.make_addplot(resistance_zone, color='red', secondary_y=False))
    
    plot_style = mpf.make_mpf_style(base_mpf_style='charles', rc={'font.size': 12})
    
    mpf.plot(df, type='candle', style=plot_style, title=f'{symbol} {timeframe} Chart with Support & Resistance',
             ylabel='Price', addplot=apds)

# Main loop to monitor price
while True:
    # Fetch H1 and M15 data
    df_h1 = get_data(symbol, timeframe_H1, num_bars)
    df_m15 = get_data(symbol, timeframe_M15, num_bars)

    if df_h1 is not None and df_m15 is not None:
        # Find support and resistance for both timeframes
        support_h1, resistance_h1 = find_support_resistance(df_h1, lookback)
        support_m15, resistance_m15 = find_support_resistance(df_m15, lookback)
        
        # Invalidate support/resistance if broken
        if invalidate_zone(df_h1, support_h1, resistance_h1, invalidate_threshold):
            support_h1, resistance_h1 = None, None  # Invalidate H1 zones
        if invalidate_zone(df_m15, support_m15, resistance_m15, invalidate_threshold):
            support_m15, resistance_m15 = None, None  # Invalidate M15 zones
        
        latest_price_h1 = df_h1['close'].iloc[-1]
        latest_price_m15 = df_m15['close'].iloc[-1]

        # Plot the charts with support/resistance zones for both H1 and M15
        plot_chart_with_zones(df_h1, support_h1, resistance_h1, timeframe='H1')
        plot_chart_with_zones(df_m15, support_m15, resistance_m15, timeframe='M15')

        # Check price against support or resistance for both timeframes
        if support_h1 is None or resistance_h1 is None or support_m15 is None or resistance_m15 is None:
            print("No valid support or resistance levels found.")
        else:
            # Check for H1 and M15 price confirmations
            if latest_price_h1 >= resistance_h1[1]:
                print(f"Price reached H1 resistance: {resistance_h1[1]}")
                winsound.Beep(2000, 500)  # Sound alert
                send_mt5_notification(f"Price at H1 resistance {resistance_h1[1]} - Watching for confirmation")
                check_m15_confirmation(support_h1, resistance_h1)

            elif latest_price_h1 <= support_h1[1]:
                print(f"Price reached H1 support: {support_h1[1]}")
                winsound.Beep(2000, 500)  # Sound alert
                send_mt5_notification(f"Price at H1 support {support_h1[1]} - Watching for confirmation")
                check_m15_confirmation(support_h1, resistance_h1)

            if latest_price_m15 >= resistance_m15[1]:
                print(f"Price reached M15 resistance: {resistance_m15[1]}")
                winsound.Beep(2000, 500)  # Sound alert
                send_mt5_notification(f"Price at M15 resistance {resistance_m15[1]} - Watching for confirmation")
                check_m15_confirmation(support_m15, resistance_m15)

            elif latest_price_m15 <= support_m15[1]:
                print(f"Price reached M15 support: {support_m15[1]}")
                winsound.Beep(2000, 500)  # Sound alert
                send_mt5_notification(f"Price at M15 support {support_m15[1]} - Watching for confirmation")
                check_m15_confirmation(support_m15, resistance_m15)

    time.sleep(60)  # Wait for 1 minute before next check


# Done with implementation of the scrip





