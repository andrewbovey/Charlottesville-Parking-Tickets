import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import seaborn


# Read in csv

df = pd.read_csv("./Parking_Tickets.csv", )


# Separate out DateIssued column into Date and Time columns

df['Date'] = df.DateIssued.str[:10]
df['Time'] = df.DateIssued.str[11:-5]

# Format the Hour column to have padded zeroes

df['Hour'] = pd.to_datetime(df['Time'], format= '%H:%M:%S' ).dt.hour
df['Hour'] = df.Hour.map("{:02}".format)


# Add column that takes into account if this the time is midnight, then output the hour of the TimeIssued column

df['Hour'] = np.where(df.eval("Time == '00:00:00'"), df.TimeIssued.str[:2], df.Hour)


#df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format = True, errors='ignore')

df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format = True, errors='coerce')


# Get current date and make new dataframes for tickets given out in the past 
# (make two of these for use in different parts of program) and in the "future"

date_current = pd.to_datetime(datetime.date.today()) 

future = df[df['Date'] > date_current]
current = df[df['Date'] < date_current]
past = df[df['Date'] < date_current]


# Change Hour column in current dataframe to numeric data

current['Hour'] = pd.to_numeric(current['Hour'])


# Drop anything in current dataframe of hour 24 or higher

future_hour = current[current['Hour'] >= 24]
current = current[current['Hour'] < 24]


# Group current dataframe by hour and drop unnecessary columns
# Basically only need one and Hour, chose to keep RecordID

current = current.drop(columns=['TicketNumber', 'DateIssued', 'StreetName', 'TimeIssued', 'StreetNumber', 'LicenseState', 'WaiverRequestDate', 'WaiverGrantedDate', 'AppealDate', 'AppealGrantedDate', 'ViolationDescription', 'Location',  'LicensePlateAnon', 'Date', 'Time', 'AppealStatus'])

grouped_by_hour = current.groupby('Hour')


# Get counts for each variable in grouped dataframe

grouped_by_hour_counts = grouped_by_hour.agg(np.size)


# Plot it!

axhour = grouped_by_hour_counts.plot(legend=False, title="Total Tickets by Hour").set_ylabel("Total Number of Tickets")
fighour = axhour.get_figure()
fighour.savefig('Tickets by Hour.png', dpi=1000)

# Clear figure (just for TDD purposes)

plt.clf()


# Make new columns for year and month

past['Year'] = past['Date'].dt.year
past['Month'] = past['Date'].dt.month


# Get rid of 1999 values; seem erroneous

past = past[past['Year'] > 1999]


# Group by year then plot counts

grouped_by_year = past.groupby(['Year']).size()
axyear = grouped_by_year.plot(title="Number of Tickets by Year", xticks=[2000,2004,2008,2012,2016,2020]).set_ylabel("Number of Tickets")

figyear = axyear.get_figure()
figyear.savefig('Tickets by Year.png', dpi=1000)


# Group by year then violation description while replacing whitespace with nothing


current.replace(' ', '', regex=True, inplace=True)
groupby_year_viol = past.groupby(['Year','ViolationDescription']).agg(np.size).reset_index()

# Create dataframe to only keep top 5 results each year (for easier reading of graph)

top5 = groupby_year_viol.groupby('Year').head(50)
top5 = top5.sort_values(['Year','RecordID'])
top5 = top5.groupby('Year').tail(5)

# Drop unnecessary columns
 
top5 = top5[['Year','ViolationDescription','TicketNumber']]


# Rename columns

top5.columns = ['Year','ViolationDescription','TotalTickets']


# Set grouped dataframe to a shorter name for easier test/coding

gyv = top5


# Initialize seaborn and DISTINCTIVE COLOR LIST. Very difficult to find, so I just hardcoded it myself.
# This list is roughly unnecessary at this point, but if you'd like to display all ViolationDescriptions,
# it becomes very necessary

seaborn.set(style='ticks')

# distinct_colors = ['#000000','#FF0000','#00FF00','#0000FF','#FF00FF','#00FFFF','#800000','#008000','#000080','#808000','#800080','#008080','#C0C0C0','#808080','#9999FF','#993366','#FFFFCC','#660066','#FF8080','#0066CC','#FF6600','#FFFF00', '#003300','#993366','#339966','#FF99CC','#FFFF99']

some_colors = ['#59FFA0', '#FF4242', '#FB62F6', '#645DD7', '#41BA75', '#FF9797', '#FCA9FA', '#AAA6E9', '#2E2B62', '#741E1E']                   


# Set seaborn palette to DISTINCTIVE COLOR LIST
seaborn.set_palette(some_colors)


# Plot with seaborn, explicitly setting xticks and asking for a legend 
# while color coding the ViolationDescription values

fg = seaborn.FacetGrid(data=gyv, hue='ViolationDescription', aspect=1.5)
fg.fig.suptitle("Top 5 Violations Each Year")
fg.map(plt.scatter, 'Year', 'TotalTickets').add_legend().set(xticks=[2000,2004,2008,2012,2016,2020])

fg.savefig("Top 5 Violations Each Year", dpi=1000)

