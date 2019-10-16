#--------TEST GOOGLE CALENDER API--------  
# k_3gA4K5ViUFXghH8f3iyATY
#1078313357944-g5urm7a73e5clo4pevl18rnqg4t2sl7m.apps.googleusercontent.com


import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import re


"""Shows basic usage of the Google Calendar API.
Prints the start and name of the next 10 events on the user's calendar.
"""
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
store = file.Storage('token.json')
creds = store.get()
 
    
service = build('calendar', 'v3', http=creds.authorize(Http()))

middags_plan_id ='lnkhjhbril50ul2uclct4e0cms@group.calendar.google.com'
page_token = None
while True:
  calendar_list = service.calendarList().list(pageToken=page_token).execute()
  for calendar_list_entry in calendar_list['items']:
    if re.match('.*Middag.*',calendar_list_entry['summary']) is not None:
      test = calendar_list_entry['id'] 
    print(calendar_list_entry['summary'])
  page_token = calendar_list.get('nextPageToken')
  if not page_token:
    break
print(test)
print(middags_plan_id)




# Call the Calendar API
now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
print('Getting the upcoming 10 events')
events_result = service.events().list(calendarId='primary', timeMin=now,
                                    maxResults=10, singleEvents=True,
                                    orderBy='startTime').execute()
events = events_result.get('items', [])
if not events:
    print('No upcoming events found.')
for event in events:
    start = event['start'].get('dateTime', event['start'].get('date'))
    print(start, event['summary'])

# Create an event
event = {  
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
event = service.events().insert(calendarId=middags_plan_id, body=event).execute()
print( 'Event created: %s' % (event.get('htmlLink')))


#Delete all entries in my regualar calendar
before = datetime.datetime(2018,1,1).isoformat()+'Z'
events_result = service.events().list(calendarId=middags_plan_id, timeMin=before,
                                    maxResults=500, singleEvents=True,
                                    orderBy='startTime').execute()
for i in range(0,len(events_result['items'])):
  event = events_result['items'][i]
  service.events().delete(calendarId=middags_plan_id, eventId=event['id']).execute()                 

#service.events().delete(calendarId='primary', eventId=event['id']).execute()
