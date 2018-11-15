
# coding: utf-8

# # Assignment 2
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv`. The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.
# 
# Each row in the assignment datafile corresponds to a single observation.
# 
# The following variables are provided to you:
# 
# * **id** : station identification code
# * **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
# * **element** : indicator of element type
#     * TMAX : Maximum temperature (tenths of degrees C)
#     * TMIN : Minimum temperature (tenths of degrees C)
# * **value** : data value for element (tenths of degrees C)
# 
# For this assignment, you must:
# 
# 1. Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
# 2. Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
# 3. Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
# 4. Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.
# 
# The data you have been given is near **Ann Arbor, Michigan, United States**, and the stations the data comes from are shown on the map below.

# In[78]:

import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd

def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))

    station_locations_by_hash = df[df['hash'] == hashid]

    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8,8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    return mplleaflet.display()

# leaflet_plot_stations(400,'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89')


# In[128]:

import numpy as np

# Load data
df = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')

# Sort data by date
df.sort_values(['ID', 'Date'], inplace=True)

# Remove leap day
df['Year'] = df['Date'].apply(lambda x: (x[:4]))
df['Month-Date'] = df['Date'].apply(lambda x: (x[5:]))
# df = df.drop(df['Month-Date'] == '02-29')
df = df[df['Month-Date'] != '02-29']
# df.head(660)

# Find max and min from 2005-2014
max_df = df[(df['Element'] == 'TMAX') & (df['Year'] != '2015')].groupby('Month-Date')
min_df = df[(df['Element'] == 'TMIN') & (df['Year'] != '2015')].groupby('Month-Date')
max_df = max_df.max()
min_df = min_df.min()

# Find max and min in 2015
max_df_15 = df[(df['Element'] == 'TMAX') & (df['Year'] == '2015')].groupby('Month-Date')
min_df_15 = df[(df['Element'] == 'TMIN') & (df['Year'] == '2015')].groupby('Month-Date')
max_df_15 = max_df_15.max()
min_df_15 = min_df_15.min()

max_df = max_df.ix[:, ['Data_Value']]
min_df = min_df.ix[:, ['Data_Value']]
max_df_15 = max_df_15.ix[:, ['Data_Value']]
min_df_15 = min_df_15.ix[:, ['Data_Value']]
max_df.head(66)

# Get the final max and min 
f_max = np.where(max_df_15['Data_Value'] > max_df['Data_Value'])
f_min = np.where(min_df_15['Data_Value'] < min_df['Data_Value'])

# Start to plot the graph
plt.figure()
plt.plot(min_df.values, 'r', label='Low Temp \'05-\'14')
plt.plot(max_df.values, 'g', label='High Temp \'05-\'14')

plt.scatter(f_min, min_df_15.iloc[f_min], s = 10, c = 'b', label = 'Low Temp \'15')
plt.scatter(f_max, max_df_15.iloc[f_max], s = 10, c = 'm', label = 'High Temp \'15')

plt.title('Temperature Summary in Ann Arbor, Michigan, USA')
plt.xlabel('Day of a year')
plt.ylabel('Temperature (tenths of degrees C)')
plt.gca().axis([0, 366, -500, 500])
plt.xticks(range(0, len(min_df), 20), min_df.index[range(0, len(min_df), 20)], rotation = '45')
plt.gca().fill_between(range(len(min_df)), min_df['Data_Value'], max_df['Data_Value'], facecolor = 'yellow', alpha = 0.5)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.legend(loc='best', frameon=True)

plt.show()


# In[ ]:



