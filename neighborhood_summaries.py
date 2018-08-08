# CS5010 Final Project
# Group #3 Asmodeus
# Andrew C. Evans
# ace8p
#
# Creating summary data using neighborhood data element. neighborhoods.py is completed first.
# Requires Full_data.csv, the full data set with latitude and longitude pairs from geocoding.

import pandas as pd
import numpy as np
import datetime

# Read in csv with latitudes and longitudes. Read in neighborhoods. Merge neighborhood into full #
full = pd.read_csv("Full_data.csv")
neighb = pd.read_csv("out.csv")
neighb = neighb[['input_string','neighborhood']]

df = pd.merge(full, neighb, how='left', on='input_string')

# Separate out DateIssued column into Date and Time columns
df['Date'] = df.DateIssued.str[:10]
df['Time'] = df.DateIssued.str[11:-5]

# Convert Date to datetime element #
df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format = True, errors='coerce')


# Get current date
date_current = pd.to_datetime(datetime.date.today())


# Make new dataframes for tickets given out in the past and in the "future"
future = df[df['Date'] > date_current]
current = df[df['Date'] < date_current]

# Make new columns for year and month
current['Year'] = current['Date'].dt.year
current['Month'] = current['Date'].dt.month

# Get rid of 1999 values; seem erroneous

current = current[current['Year'] > 1999]

# Group by neighborhood and violation description then violation description while replacing whitespace with nothing #
current.replace(' ', '', regex=True, inplace=True)
groupNeighb = current.groupby(['neighborhood','ViolationDescription']).agg(np.size).reset_index()

# Create a group by neighborhood only #
groupNeighb2 = current.groupby(['neighborhood']).agg(np.size).reset_index()

# Subset only the necessary columns for the grouped data sets. Rename RecordID to TotalTickets #
groupNeighb = groupNeighb[["neighborhood","ViolationDescription","RecordID"]]
groupNeighb.rename(columns={'RecordID': 'TotalTickets'}, inplace=True)
groupNeighb2 = groupNeighb2[["neighborhood","RecordID"]]
groupNeighb2.rename(columns={'RecordID': 'TotalTickets'}, inplace=True)

# Subset only the largest 15 neighborhoods in terms of TotalTickets #
groupNeighb2= groupNeighb2.nlargest(15, 'TotalTickets')

# Create a new dataset for each neighborhood and view the top 3 violation descriptions #
barracksRoad = groupNeighb[groupNeighb['neighborhood']=='BarracksRoad']
barracksRoad= barracksRoad.nlargest(3, 'TotalTickets')

barracksRugby = groupNeighb[groupNeighb['neighborhood']=='Barracks/Rugby']
barracksRugby= barracksRugby.nlargest(3, 'TotalTickets')

belmont = groupNeighb[groupNeighb['neighborhood']=='Belmont']
belmont= belmont.nlargest(3, 'TotalTickets')

fifeville = groupNeighb[groupNeighb['neighborhood']=='Fifeville']
fifeville= fifeville.nlargest(3, 'TotalTickets')

greenbrier = groupNeighb[groupNeighb['neighborhood']=='Greenbrier']
greenbrier= greenbrier.nlargest(3, 'TotalTickets')

jeffersonParkAvenue = groupNeighb[groupNeighb['neighborhood']=='JeffersonParkAvenue']
jeffersonParkAvenue= jeffersonParkAvenue.nlargest(3, 'TotalTickets')

johnsonVillage = groupNeighb[groupNeighb['neighborhood']=='JohnsonVillage']
johnsonVillage= johnsonVillage.nlargest(3, 'TotalTickets')

lewisMountain = groupNeighb[groupNeighb['neighborhood']=='LewisMountain']
lewisMountain= lewisMountain.nlargest(3, 'TotalTickets')

locustGrove = groupNeighb[groupNeighb['neighborhood']=='LocustGrove']
locustGrove= locustGrove.nlargest(3, 'TotalTickets')

marthaJefferson = groupNeighb[groupNeighb['neighborhood']=='MarthaJefferson']
marthaJefferson= marthaJefferson.nlargest(3, 'TotalTickets')

northDowntown = groupNeighb[groupNeighb['neighborhood']=='NorthDowntown']
northDowntown= northDowntown.nlargest(3, 'TotalTickets')

other = groupNeighb[groupNeighb['neighborhood']=='Other']
other= other.nlargest(3, 'TotalTickets')

ridgeStreet = groupNeighb[groupNeighb['neighborhood']=='RidgeStreet']
ridgeStreet= ridgeStreet.nlargest(3, 'TotalTickets')

roseHill = groupNeighb[groupNeighb['neighborhood']=='RoseHill']
roseHill= roseHill.nlargest(3, 'TotalTickets')

starrHill = groupNeighb[groupNeighb['neighborhood']=='StarrHill']
starrHill= starrHill.nlargest(3, 'TotalTickets')

tenthAndPage = groupNeighb[groupNeighb['neighborhood']=='TenthAndPage']
tenthAndPage= tenthAndPage.nlargest(3, 'TotalTickets')

theMeadows = groupNeighb[groupNeighb['neighborhood']=='TheMeadows']
theMeadows= theMeadows.nlargest(3, 'TotalTickets')

venable = groupNeighb[groupNeighb['neighborhood']=='Venable']
venable= venable.nlargest(3, 'TotalTickets')

woolenMills = groupNeighb[groupNeighb['neighborhood']=='WoolenMills']
woolenMills= woolenMills.nlargest(3, 'TotalTickets')


# Create a new dataset for two violation types and view the top 15 neighborhoods #
lefts = groupNeighb[groupNeighb['ViolationDescription']=='LTSidetoCurb']
lefts= lefts.nlargest(15, 'TotalTickets')

infromcurb = groupNeighb[groupNeighb['ViolationDescription']=='12InchesFromCurb']
infromcurb= infromcurb.nlargest(15, 'TotalTickets')