# connecting to the mt5

# import MetaTrader5 as mt5

# # Connect to MetaTrader 5
# if not mt5.initialize():
#     print("MT5 connection failed")
#     mt5.shutdown()
# else:
#     print("Connected to MT5")

# # Shutdown MT5 connection
# mt5.shutdown()



# test to fecth symbols with bid/ask price

# import MetaTrader5 as mt5

# # Connect to MetaTrader 5
# if not mt5.initialize():
#     print("MT5 connection failed")
#     mt5.shutdown()
#     quit()

# print("Connected to MT5")

# # Fetch market data for a symbol (e.g., EURUSD)
# symbol = "EURUSD"

# # Get symbol info
# info = mt5.symbol_info(symbol)
# if info is None:
#     print(f"Failed to get symbol info for {symbol}")
# else:
#     print(f"Symbol: {info.name}, Bid: {info.bid}, Ask: {info.ask}")

# # Shutdown MT5 connection
# mt5.shutdown()







# feetching datasets

# import MetaTrader5 as mt5
# import pandas as pd
# from datetime import datetime

# # Connect to MetaTrader 5
# if not mt5.initialize():
#     print("MT5 connection failed")
#     mt5.shutdown()
#     quit()

# print("Connected to MT5")

# # Define symbol and timeframe
# symbol = "EURUSD"
# timeframe = mt5.TIMEFRAME_H1  # 15-minute candles
# num_bars = 10  # Number of candles to fetch

# # Get historical candlestick data
# rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, num_bars)

# if rates is None:
#     print("Failed to get historical data")
# else:
#     # Convert data to Pandas DataFrame
#     df = pd.DataFrame(rates)
#     df['time'] = pd.to_datetime(df['time'], unit='s')  # Convert timestamp

#     print(df[['time', 'open', 'high', 'low', 'close']])

# # Shutdown MT5 connection
# mt5.shutdown()




# plotting the charts using mplfinnave baseed on information received

# import MetaTrader5 as mt5
# import pandas as pd
# import mplfinance as mpf
# from datetime import datetime

# # Connect to MetaTrader 5
# if not mt5.initialize():
#     print("MT5 connection failed")
#     mt5.shutdown()
#     quit()

# print("Connected to MT5")

# # Define symbol and timeframe
# symbol = "EURUSD"
# timeframe = mt5.TIMEFRAME_H1  # 15-minute candles
# num_bars = 100  # Number of candles to fetch

# # Get historical candlestick data
# rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, num_bars)

# if rates is None:
#     print("Failed to get historical data")
# else:
#     # Convert data to Pandas DataFrame
#     df = pd.DataFrame(rates)
#     df['time'] = pd.to_datetime(df['time'], unit='s')  # Convert timestamp

#     # Set the 'time' column as the index
#     df.set_index('time', inplace=True)

#     # Plot the candlestick chart
#     mpf.plot(df, type='candle', style='charles', title=f'{symbol} Candlestick Chart', ylabel='Price')

# # Shutdown MT5 connection
# mt5.shutdown()





# Now dtecting support and resistance areas - this works but it identifies a simgle touch of these 
# support / rsistance zones, tje code below ensures it highlights areas instead of exact price


# import MetaTrader5 as mt5
# import pandas as pd
# import mplfinance as mpf
# from datetime import datetime

# # Connect to MetaTrader 5
# if not mt5.initialize():
#     print("MT5 connection failed")
#     mt5.shutdown()
#     quit()

# print("Connected to MT5")

# # Define symbol and timeframe
# symbol = "EURUSD"
# timeframe = mt5.TIMEFRAME_H1  # Hourly candles
# num_bars = 100  # Number of candles to fetch

# # Get historical candlestick data
# rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, num_bars)

# if rates is None:
#     print("Failed to get historical data")
# else:
#     # Convert data to Pandas DataFrame
#     df = pd.DataFrame(rates)
#     df['time'] = pd.to_datetime(df['time'], unit='s')  # Convert timestamp
#     df.set_index('time', inplace=True)

#     # Calculate support and resistance levels
#     window = 20  # Lookback window size
#     support_levels = pd.Series(index=df.index, dtype='float64')  # Initialize empty support series
#     resistance_levels = pd.Series(index=df.index, dtype='float64')  # Initialize empty resistance series

#     for i in range(window, len(df) - window):
#         if df['low'].iloc[i] == min(df['low'].iloc[i - window:i + window]):
#             support_levels.iloc[i] = df['low'].iloc[i]  # Store support price at correct index

#         if df['high'].iloc[i] == max(df['high'].iloc[i - window:i + window]):
#             resistance_levels.iloc[i] = df['high'].iloc[i]  # Store resistance price at correct index

#     # Ensure that NaN values are ignored
#     support_plot = mpf.make_addplot(support_levels, scatter=True, marker='o', color='green', markersize=50)
#     resistance_plot = mpf.make_addplot(resistance_levels, scatter=True, marker='o', color='red', markersize=50)

#     # Plot the candlestick chart with support and resistance levels
#     plot_style = mpf.make_mpf_style(base_mpf_style='charles', rc={'font.size': 12})

#     mpf.plot(df, type='candle', style=plot_style, title=f'{symbol} H1 Candlestick Chart with Support & Resistance',
#              ylabel='Price', addplot=[support_plot, resistance_plot])

# # Shutdown MT5 connection
# mt5.shutdown()




# Code to ensure it highlights areas and not exact price -
import MetaTrader5 as mt5
import pandas as pd
import mplfinance as mpf
from datetime import datetime
import numpy as np

# Connect to MetaTrader 5
if not mt5.initialize():
    print("MT5 connection failed")
    mt5.shutdown()
    quit()

print("Connected to MT5")

# Define symbol and timeframe
symbol = "EURUSD"
timeframe = mt5.TIMEFRAME_H1  # Hourly candles
num_bars = 200  # Number of candles to fetch

# Get historical candlestick data
rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, num_bars)

if rates is None:
    print("Failed to get historical data")
else:
    # Convert data to Pandas DataFrame
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')  # Convert timestamp
    df.set_index('time', inplace=True)

    # Parameters
    window = 20  # Lookback window size
    zone_threshold = 0.002  # % threshold to group zones (adjustable)

    # Identify peaks and valleys
    support_levels = []
    resistance_levels = []

    for i in range(window, len(df) - window):
        local_low = min(df['low'].iloc[i - window:i + window])
        local_high = max(df['high'].iloc[i - window:i + window])

        if df['low'].iloc[i] == local_low:
            support_levels.append((df.index[i], df['low'].iloc[i]))

        if df['high'].iloc[i] == local_high:
            resistance_levels.append((df.index[i], df['high'].iloc[i]))

    # Convert to DataFrame
    support_df = pd.DataFrame(support_levels, columns=['time', 'price']).set_index('time')
    resistance_df = pd.DataFrame(resistance_levels, columns=['time', 'price']).set_index('time')

    # Function to group nearby levels into zones
    def group_zones(levels, threshold):
        levels = sorted(levels, key=lambda x: x[1])  # Sort by price
        zones = []
        temp_zone = [levels[0]]

        for i in range(1, len(levels)):
            if abs(levels[i][1] - temp_zone[-1][1]) <= threshold * levels[i][1]:  # Within zone threshold
                temp_zone.append(levels[i])
            else:
                zones.append(np.mean([p[1] for p in temp_zone]))  # Average price for zone
                temp_zone = [levels[i]]

        zones.append(np.mean([p[1] for p in temp_zone]))  # Add last zone
        return zones

    # Get support & resistance zones
    support_zones = group_zones(support_levels, zone_threshold)
    resistance_zones = group_zones(resistance_levels, zone_threshold)

    # Create horizontal lines for support and resistance zones
    hlines = [
        float(level) for level in support_zones
    ] + [
        float(level) for level in resistance_zones
    ]

    # Prepare plotting markers for each touch point
    # Ensure the x (dates) and y (prices) values have the same length
    support_plot = mpf.make_addplot(support_df['price'], scatter=True, marker='o', color='green', markersize=50)
    resistance_plot = mpf.make_addplot(resistance_df['price'], scatter=True, marker='o', color='red', markersize=50)

    # Plot chart with support and resistance
    plot_style = mpf.make_mpf_style(base_mpf_style='charles', rc={'font.size': 12})
    mpf.plot(df, type='candle', style=plot_style,
             title=f'{symbol} H1 Candlestick Chart with Multi-Touch Support & Resistance Zones',
             ylabel='Price',
             addplot=[support_plot, resistance_plot],
             hlines=hlines)

# Shutdown MT5 connection
mt5.shutdown()
