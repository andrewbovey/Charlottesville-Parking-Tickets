import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('Parking_Tickets.csv')
df['Date'] = df.DateIssued.str[:10]
df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format = True, errors='coerce')
df.loc[:,'Year'] = df['Date'].dt.strftime('%Y')

df = df.drop(columns=['RecordID','TicketNumber','DateIssued', 'StreetName','StreetNumber','TimeIssued','ViolationDescription', 'Date', 
                      'WaiverRequestDate','WaiverGrantedDate','AppealDate','AppealGrantedDate','AppealStatus','Location','LicensePlateAnon'])
df.columns = ['State', 'Year']


state_counts = df.groupby(['Year'])['State'].value_counts()      #indexed by year and state, reduced to series 
droppedVA = df.drop(df[df.State == 'VA'].index)                  #drops VA from frame
Clean_States = droppedVA.loc[droppedVA['Year'].isin(['1999', '2088', '2097', '2208']) == False]  #drops bad from frame 

#Indexes by year and by state and adds the total number of tickets meeting those conditions
#while maintaining year and state columns                                                                              
new_clean = Clean_States.groupby(['Year', 'State']).agg(np.size).reset_index()
new_clean.columns = ['Year', 'State', 'Total Tickets']                            #Rewrites column names
top_five = new_clean.loc[new_clean['State'].isin(['MD', 'NC', 'PA', 'FL', 'NY'])] #5 States with most tickets

by_year = Clean_States.groupby(['Year'])['State'].agg(np.size).reset_index() #finds total number of out of state tickets each year
percent_year =  pd.concat([by_year['State'].pct_change(), by_year['Year']], axis=1)             #finds percent change each year 
percent_year = percent_year.drop([0])            #drops starting year 

#graph of percent change each year
plt.figure(figsize=(20,10))
plt.plot(percent_year['Year'], percent_year['State'], 'bo-')
plt.title('Percent Change Each Year')
plt.ylabel('Percent Change')
plt.xlabel('Year')
plt.savefig('perc.png')

#graph of total tickets each year
plt.figure(figsize=(20,10))
plt.plot(by_year['Year'], by_year['State'], 'bo-')
plt.xticks(by_year['Year'])
plt.title('Out of State Tickets Each Year')
plt.ylabel('Total Tickets')
plt.xlabel('Year')
plt.savefig('total.png')

#graph of total tickets each year for each of the top five non VA states with the most tickets
top_print = top_five.pivot(index='Year', columns='State', values='Total Tickets')
plt.figure(figsize=(20,10))
plt.plot(top_print)
plt.legend(('FL', 'MD', 'NC', 'NY', 'PA'),
           loc='upper right',  prop={'size': 20})
plt.title('Total Tickets for 5 Highest Frequency States')
plt.ylabel('Total Tickets')
plt.xlabel('Year')
plt.savefig('topfive.png')