#import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = [20, 4]
#read and change to datetime
dataframe = '/Users/scottgleave/Downloads/Parking_Tickets.csv'

def readdatetime(df):
    df = pd.read_csv(df)
    df['Date'] = df.DateIssued.str[:10]
    df['Time'] = df.DateIssued.str[11:-5]
    # Hormat the Hour column to have padded zeroes
    df['Hour'] = pd.to_datetime(df['Time'], format= '%H:%M:%S' ).dt.hour
    df['Hour'] = df.Hour.map("{:02}".format)
    # Add column that takes into account if this the time is midnight, then output the hour of the TimeIssued column
    df['Hour'] = np.where(df.eval("Time == '00:00:00'"), df.TimeIssued.str[:2], df.Hour)
    #read data to tickets df and create column for year
    tickets = df
    tickets['year'] = tickets.Date.str[:4]
    return tickets

tickets = readdatetime(dataframe)

#find rows with appeals and create new df.  Count values for appeal status categories
def findappeals(tickets):
    appeal = tickets.dropna(subset=['AppealDate'])
    appealcounts = pd.value_counts(appeal['AppealStatus'].values, sort=False)
    print(appealcounts) #TEST print out totals for each group for sanity check
    appeal['ViolationDescription'] = appeal['ViolationDescription'].str.strip()
    return appeal

appeal = findappeals(tickets)
print(appeal)

#get percentages for appeal status categories
def appealperc(appealdf):
    return(appealdf.AppealStatus.value_counts(normalize=True))
appealcountsumm = appealperc(appeal)
print(appealcountsumm)

#what percent of appeals were successful by type of offense?

#get value counts for violationdescription
appealcountsbyoffense = pd.value_counts(appeal['ViolationDescription'].values, sort=False)
#newdataframe with only appeals that were granted
appealsgranted = appeal[(appeal['AppealStatus'] == 'granted')]
#get value counts for violationdescription for appeals that were granted
appealcountsgranted = pd.value_counts(appealsgranted['ViolationDescription'].values, sort=False)
#combine values count dfs and calculate percentage of appeals granted by violation description
appealgranteddf = pd.concat([appealcountsbyoffense, appealcountsgranted], axis=1)
appealgranteddf['perc'] = appealgranteddf[1]/appealgranteddf[0]
appealgranteddf = appealgranteddf.sort_values(by=['perc'])
#TEST print appeal granted df to make sure looks ok
print(appealgranteddf)

#create chart for appeal success breakdown and save chart
def appealsuccchart(appealgranteddf):
    appealgranteddfshort = appealgranteddf[(appealgranteddf[0] > 200)] #filter out lowest appeals
    appealgranteddfshort = appealgranteddfshort.sort_values(by=['perc']) #sort df
    ind = appealgranteddfshort.index.values
    fig, ax = plt.subplots()
    ax.barh(ind,appealgranteddfshort['perc'],  align='center',
            color='green')
    ax.set_xlabel('Percentage of appeals grant')
    plt.rcParams['figure.figsize'] = [10, 10]
    plt.tight_layout()
    plt.savefig('appealsuccess.png')
    return 

appealsuccchart(appealgranteddf)

#Create df to figure out how percentage of appeals granted changed over time

#value counts by year for total appeals
def countbyyear(appeal):
    appealbyyear = pd.value_counts(appeal['year'].values, sort = False)
    #value counts by year for appeals granted
    appealgrantbyyear = pd.value_counts(appealsgranted['year'].values, sort = False)
    #combine value count dfs and calculate yearly percentage granted
    appealsuccessyear = pd.concat([appealbyyear, appealgrantbyyear], axis=1)
    appealsuccessyear['perc'] = appealsuccessyear[1]/appealsuccessyear[0]
    return appealsuccessyear, appealbyyear

appealsuccessyear,appealbyyear = countbyyear(appeal)

#pendings by year
#new df for pending tickets, then perform value count
def pendingdf(tickets):
    pending = tickets[(tickets['AppealStatus'] == 'pending')]
    pendingbyyear = pd.value_counts(pending['year'].values, sort = True)
    return pendingbyyear
pendingbyyear = pendingdf(tickets)
print(pendingbyyear)

#time between request and decision on appeal

#sort dataframe by date and remove last 10 rows to remove incorrect dates that cannot be converted to datetime
#and convert to datetime
def appeallengthsumm(tickets):
    tickets = tickets.sort_values(by=['Date'], ascending = True)
    tickets = tickets[:-10]
    tickets['Date'] = pd.to_datetime(tickets['Date'])
    #sort dataframe by granted date, remove incorrect dates
    appealgrantdf = tickets.dropna(subset=['AppealGrantedDate'])
    appealgrantdf['tempcol'] = appealgrantdf.AppealGrantedDate.str[-4:]
    appealgrantdf = appealgrantdf.sort_values(by=['tempcol'], ascending = False)
    appealgrantdf = appealgrantdf[10:]
    #sort dataframe by granted date, remove incorrect dates
    appealgrantdf['tempcol'] = appealgrantdf.AppealDate.str[-4:]
    appealgrantdf = appealgrantdf.sort_values(by=['tempcol'], ascending = False)
    appealgrantdf = appealgrantdf[10:]
    #convert formats to datetime
    appealgrantdf['AppealDate'] = pd.to_datetime(appealgrantdf['AppealDate'])
    appealgrantdf['AppealGrantedDate'] = pd.to_datetime(appealgrantdf['AppealGrantedDate'])
    appealgrantdf = appealgrantdf.drop('tempcol', axis = 1)

    #figure out date range
    appealgrantdf['daylength'] = appealgrantdf['AppealGrantedDate'] - appealgrantdf['AppealDate']
    appealsummary = appealgrantdf['daylength'].describe()
    return appealsummary
appealsummary = appeallengthsumm(tickets)
print(appealsummary)

#cars successful with appeals multiple times

#create dataframe from granted, value count by license plate
successful = tickets[(tickets['AppealStatus'] == 'granted')]
successfulcount = pd.value_counts(successful['LicensePlateAnon'].values, sort=True)
successfulmean = successfulcount.mean()
print(successfulcount.head())
print(successfulmean)

#create plot of outliers
def plotoutliers(successfulcount):
    #pull highest six outliers and put into list
    plot1 = successfulcount[:6]
    ind2 = plot1.index.values
    plot1 = plot1.tolist()
    print(plot1)

    #plot outliers
    indstr = [str(x) for x in ind2]
    fig2, ax2 = plt.subplots()
    ax2.bar(indstr,plot1,  align='center',
            color='blue')
    ax2.set_xlabel('License Plate Number')
    ax2.set_ylabel('Number of Successful Appeals')
    plt.rcParams['figure.figsize'] = [10, 10]
    plt.tight_layout()
    plt.savefig('Appeal Outliers.png')
    return

plotoutliers(successfulcount)

def appealsbyyear(ticket,appealbyyear):
    ticketsbyyear = pd.value_counts(tickets['year'].values, sort = False)
    #value counts by year for appeals granted
    appealgrantbyyear = pd.value_counts(appealsgranted['year'].values, sort = False)
    #combine value count dfs and calculate yearly percentage granted
    appealsuccesstotal = pd.concat([ticketsbyyear, appealgrantbyyear], axis=1)
    appealsuccesstotal['perc'] = appealsuccesstotal[1]/appealsuccesstotal[0]
    print(appealsuccesstotal)

    #percent appealed by year

    #count value of tickets by year, add to appeals by year, and calculate percentage
    ticketsbyyear = pd.value_counts(tickets['year'].values, sort = False)
    percentappealtime = pd.concat([appealbyyear, ticketsbyyear], axis=1)
    percentappealtime['perc'] = percentappealtime[0]/percentappealtime[1]
    percentappealtime

    #plot percent of yearly tickets appealed and percent of year tickets granted appeal
    x = percentappealtime.index.values
    x1 = appealsuccessyear.index.values
    y1 = percentappealtime['perc']
    y2 = appealsuccesstotal['perc']
    fig3, ax3 = plt.subplots()
    labels = ['Percent of Total Tickets Appeal Granted', 'Percent of Total Tickets Appealed']

    ax3.stackplot(x,y1, (y2-y1), labels = labels)
    ax3.legend(loc=1)
    ax3.set_ylabel('Percent of Total Tickets')
    plt.rc('axes', labelsize = 10)
    #plt.show()
    plt.rc('ytick', labelsize=10)

    plt.tight_layout()
    plt.savefig('appealsattempted.png')

    return

appealsbyyear(tickets, appealbyyear)

#percent appealed overall

#count value of tickets by year, add to appeals by year, and calculate percentage
ticketsbyyear = pd.value_counts(tickets['year'].values, sort = False)
percentappealtime = pd.concat([appealbyyear, ticketsbyyear], axis=1)
totalappealed = pd.Series(percentappealtime[0]).sum()
totaltickets = pd.Series(percentappealtime[1]).sum()
appealpercent = totalappealed/totaltickets

print(appealpercent)

