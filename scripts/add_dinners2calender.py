import datetime
import time
import sys
from dateutil.rrule import DAILY, rrule,  MO, TU, WE, TH, SU
import calendar
import re
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools


#Read the list of dinnerss
dinners = []
links =[]
with open('../middager.md','r') as fp:
    for line in fp:    
        if '###' in line:
            #Extract only the dinner names
            m =  re.search(':(.+)$',line)
            if m:                
                dinners.append([m.group(1).strip(),''])                
        if '[' in line:
            #Extract link and add it to the las dinner
            m =  re.search('\((.*)\)$',line)
            if m:                
                dinners[-1][1] = m.group(1).strip()
        

dinners = dinners*54


#Make a list of dates, dinners and day of week
first_dinner_day = datetime.datetime(2018,12,30)
last_dinner_day = first_dinner_day+datetime.timedelta(365-2)
daynames = calendar.day_name
dates_with_dinners = rrule(DAILY,dtstart = first_dinner_day,
                           until=last_dinner_day,byweekday= (MO,TU,WE,TH,SU))
dinner_events = []
uke = 1
for i,date in enumerate(dates_with_dinners):
    dinner_events.append(['uke'+str(uke),date,
                          calendar.day_name[date.weekday()],
                          dinners[i][0],dinners[i][1]])
    if (i+1)%5 == 0:
        uke += 1
        if uke > 4:
            uke = 1

 
    
#Connect to google calendar API and fill in dinner for each day
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
store = file.Storage('token.json')
creds = store.get()    
service = build('calendar', 'v3', http=creds.authorize(Http()))

#Get all events in calender Middagsplan
middags_plan_id ='dj0nplik36u3mj78a8vjno7u2s@group.calendar.google.com'
before = datetime.datetime(2018,1,1).isoformat()+'Z'
events_result = service.events().list(calendarId=middags_plan_id, timeMin=before,
                                    maxResults=1000, singleEvents=True,
                                    orderBy='startTime').execute()

#Delete all existing middager in calender Middagsplan

for i in range(0,len(events_result['items'])):
    event = events_result['items'][i]
    service.events().delete(calendarId=middags_plan_id, eventId=event['id']).execute() 
    print('Delete dinner '+str(i+1) + ' of '+str(len(events_result['items'])),end='\r')
print('Deleted '+str(len(events_result['items']))+' dinners                                         ')
#Add all dinner_events in dinner_dates

#Dinner event template 
single_event = {  
  'summary': 'Torsk',
  'location': 'Holmlia',
  'description': 'Middag',
  'start': {
    'date': '2019-01-27'    
  },
  'end': {
    'date': '2019-01-27'    
  },  
  'reminders': {
    'useDefault': False,
    'overrides': [      
      {'method': 'popup', 'minutes': 60*24*1},
    ],
  },
}

#Add all dinner_events to the calendra
for i,dinner_event in enumerate(dinner_events):     
    single_event['summary'] = dinner_event[3]
    single_event['description']='Dinner for ' + dinner_event[0]+'\n'+dinner_event[4]
    single_event['start']['date'] = dinner_event[1].date().isoformat() 
    single_event['end']['date'] = dinner_event[1].date().isoformat() 
    event = service.events().insert(calendarId=middags_plan_id, body=single_event).execute()
    print('Add dinner '+str(i+1) + ' of '+str(len(dinner_events)),end='\r')
print('Added '+str(len(dinner_events))+' dinners                              ')








