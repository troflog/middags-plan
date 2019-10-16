#Written by Trond
import datetime
import time
from dateutil.rrule import DAILY, rrule,  MO, TU, WE, TH, SU
import calendar
import re

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
 
    


