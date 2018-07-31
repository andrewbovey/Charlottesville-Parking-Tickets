import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt


# Read in csv

df = pd.read_csv("./Parking_Tickets.csv", )


# Separate out DateIssued column into Date and Time columns

df['Date'] = df.DateIssued.str[:10]
df['Time'] = df.DateIssued.str[11:-5]

# Hormat the Hour column to have padded zeroes

df['Hour'] = pd.to_datetime(df['Time'], format= '%H:%M:%S' ).dt.hour
df['Hour'] = df.Hour.map("{:02}".format)


# Drop unwanted columns (for easier testing). Deffo drop this line later

df = df.drop(columns=['RecordID','TicketNumber','DateIssued', 'StreetName','StreetNumber','LicenseState','WaiverRequestDate','WaiverGrantedDate','AppealDate','AppealGrantedDate','ViolationDescription','AppealStatus','Location','LicensePlateAnon'])


# Add column that takes into account if this the time is midnight, then output the hour of the TimeIssued column

df['Hour'] = np.where(df.eval("Time == '00:00:00'"), df.TimeIssued.str[:2], df.Hour)


#df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format = True, errors='ignore')

df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format = True, errors='coerce')


# Get current date

date_current = pd.to_datetime(datetime.date.today())


# Make new dataframes for tickets given out in the past and in the "future"

future = df[df['Date'] > date_current]
current = df[df['Date'] < date_current]


"""
# Print out some examples of the two

print("\nCurrent date is " + str(date_current) + ". \nFirst, we show the beginning and end of the dataframe with dates in the past:\n")
print(current.head(2))
print(current.tail(2))
print("\n\n Now we show the beginning and end of the dataframe with dates in the future: \n")
print(future.head(2))
print(future.tail(2))

"""

# Change Hour column in current dataframe to numeric data

current['Hour'] = pd.to_numeric(current['Hour'])


# Drop anything in current dataframe of hour 24 or higher

future_hour = current[current['Hour'] >= 24]
current = current[current['Hour'] < 24]


# Group current dataframe by hour 

grouped_by_hour = current.groupby('Hour')


# Get counts for each variable in grouped dataframe

grouped_by_hour_counts = grouped_by_hour.agg(np.size)


# Plot it!

grouped_by_hour_counts.plot()


# Make new columns for year and month

current['Year'] = current['Date'].dt.year
current['Month'] = current['Date'].dt.month

# Group by year then plot counts

grouped_by_year = current.groupby('Year')
grouped_by_year_counts = grouped_by_year.agg(np.size)
grouped_by_year_counts.plot()

print(current.head())

