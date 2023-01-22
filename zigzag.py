#!/usr/bin/python3
import matplotlib
 
# Avoid FutureWarning: Pandas will require you to explicitly register matplotlib converters.


from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
 
import pandas as pd

## Klang
from Klang import Kl,Klang 
Klang.Klang_init()
## 

#设置字体 ，显示股票中文名称
matplotlib.rcParams["font.sans-serif"] = ['AR PL UKai CN']

# Load data from CSV file.
##########################
my_headers = ['datetime', 'open', 'high', 'low', 'close', 'volume']
my_dtypes = {'datetime': 'str', 'open': 'float', 'high': 'float', 'low': 'float', 
                                                'close': 'float', 'volume': 'int'}
my_parse_dates = ['datetime']

#
# load stock data by code
#
import sys

codename = "sh.600010" 

if len(sys.argv)>=1:
    codename = sys.argv[1]
display = 1
if len(sys.argv)>=2:
    display = int(sys.argv[2])

Kl.code(codename)
print(codename,Kl.cur_name)
loaded_data = Kl.day_df 
#print(loaded_data)

# Convert 'Timestamp' to 'float'.
#   Need time be in float days format - see date2num.
loaded_data['datetime'] = [mdates.date2num(np.datetime64(d)) for d in loaded_data['datetime']]
 
 
 
# Create zigzag trendline.
########################################
# Find peaks(max).
data_x = loaded_data['datetime'].values
data_y = loaded_data['close'].values
peak_indexes = signal.argrelextrema(data_y, np.greater)
peak_indexes = peak_indexes[0]
 
# Find valleys(min).
valley_indexes = signal.argrelextrema(data_y, np.less)
valley_indexes = valley_indexes[0]
 
 
# Merge peaks and valleys data points using pandas.
df_peaks = pd.DataFrame({'datetime': data_x[peak_indexes], 'zigzag_y': data_y[peak_indexes]})

df_valleys = pd.DataFrame({'datetime': data_x[valley_indexes], 'zigzag_y': data_y[valley_indexes]})
 
 
from bokeh.plotting import figure, output_file, show

output_file("images/" + codename+"_zigzag.html")
graph = figure(title = codename + "-" + Kl.cur_name + ' Prices - ZigZag trendline')

# name of the x-axis
graph.xaxis.axis_label = "日期"
  
# name of the y-axis
graph.yaxis.axis_label = "价格"

graph.line(data_x, data_y,line_dash = "dotdash",line_color="black")

graph.line(df_valleys['datetime'].values, df_valleys['zigzag_y'].values,line_color="blue")

graph.line(df_peaks['datetime'].values, df_peaks['zigzag_y'].values,line_color="red")
show(graph)


 
 
