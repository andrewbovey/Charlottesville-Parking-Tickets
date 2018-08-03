# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 11:24:01 2018

@author: Henry
"""
import pandas as pd
from geopy.geocoders import GoogleV3
import warnings 
warnings.filterwarnings('ignore')

address = input("Enter your street address:  ")
print("Geocoding address...")

df = pd.read_csv('Full_Data.csv')
df.ViolationDescription = df.ViolationDescription.str.strip()
latlong = df[['latitude','longitude']]
latlongunique = latlong.drop_duplicates()
latlongunique = latlongunique.reset_index(drop=True)
temp = pd.DataFrame()

try:
    geolocator = GoogleV3(user_agent="ParkingTicketLookup")
    LocationGeocoded = geolocator.geocode(address)
    LocationCoor = [LocationGeocoded.latitude, LocationGeocoded.longitude]
    InputLat = LocationCoor[0]
    InputLong = LocationCoor[1]
    for x, y in latlongunique.iterrows():
        if (abs(y[0] - InputLat) <= .000224625) and (abs(y[1] - InputLong) <= .00029245):
            temp = temp.append(latlongunique.iloc[x])
    if temp.empty:
        print('No parking ticket records for this location.')
    else:
        same = pd.merge(df, temp, left_on = ('latitude','longitude'), right_on = ('latitude','longitude'))
        print(str(len(same)) + ' parking tickets for this location on record.') 
        print(same.ViolationDescription.value_counts())
     
except AttributeError:
    print("Address was not recognized.")
except:
    print("Geocode Server is currently down.")



# .001 lat = .069 mi
# .001 long = .053 mi

# 20 M in lat = .0001797
# 20 M in long = .00023396

