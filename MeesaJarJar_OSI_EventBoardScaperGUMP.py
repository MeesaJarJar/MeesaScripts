# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description: UO Event Board Ingame Viewer
# Displays this months upcoming events on OSI!
# NO CONFIG necessary, just run the script and a GUMP will appear!
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#

# END CONFIG --------------------------------------------------#


import http.client
import re
import sys
import os
from datetime import datetime, timedelta, timezone

os.environ['PYTHONIOENCODING'] = 'utf-8'

events = []
currentPage = 1
# Functions to replace fromisoformat for compatibility with Python versions < 3.7
def custom_fromisoformat(date_string):
    return datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S')

# Functions for .ics Parsing and Conversion to EST
def print_encoded(text):
    encodings_to_try = ['utf-8', 'ascii', 'windows-1252']
    
    for encoding in encodings_to_try:
        try:
            sys.stdout.buffer.write(text.encode(encoding, 'ignore'))
            break
        except UnicodeEncodeError:
            pass
            
def convert_time_to_est(time_string):
    # Split the input time string into components
    date_str, time_str = time_string.split('T')
    year, month, day = map(int, date_str.split('-'))
    hour, minute, second = map(int, time_str[:-6].split(':'))
    
    # Create a datetime object in UTC
    utc_time = datetime(year, month, day, hour, minute, second, tzinfo=timezone.utc)
    
    # Calculate the Eastern Time (ET) by subtracting 5 hours
    est_time = utc_time - timedelta(hours=-5)
    
    # Check if the time is in daylight saving time (EDT)
    is_dst = time_string.endswith('-04:00')
    
    # Determine the time zone abbreviation
    timezone_abbr = 'EDT' if is_dst else 'EST'
    #print("TIME ZONE IS:",timezone_abbr)
    # Format the time in the desired format
    formatted_time = est_time.strftime('%B %d @ %I:%M%p') + f" {timezone_abbr}"
    
    return formatted_time
            
def convert_to_standard_datetime_format(date_str):
    return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}T{date_str[9:11]}:{date_str[11:13]}:{date_str[13:15]}"
def replace_problematic_characters(text):
    # Define a dictionary of character replacements
    replacements = {
        '\x80': '',  # Replace character '\x80' with an empty string
        # Add more replacements as needed
    }

    # Use regular expressions to find and replace problematic characters
    for char, replacement in replacements.items():
        text = re.sub(char, replacement, text)

    return text
    
def extract_ics_events(ics_content):
    event_pattern = re.compile(
        r'BEGIN:VEVENT.*?DTSTART;TZID=(.*?):(.*?)\n'
        r'DTEND;TZID=(.*?):(.*?)\n.*?'
        r'SUMMARY:(.*?)\n'
        r'(DESCRIPTION:(.*?))?\n'
        r'URL:(.*?)\n',
        re.DOTALL
    )
    events_matches = event_pattern.findall(ics_content)
    parsed_events = []
    
    # UTC timezone object
    utc_zone = timezone.utc
    
    for match in events_matches:
        start_tz, start_date, end_tz, end_date, summary, _, description, url = match
        start_date_standard = convert_to_standard_datetime_format(start_date)
        end_date_standard = convert_to_standard_datetime_format(end_date)
        
        # Assuming a fixed offset for EST as UTC-5 (without accounting for daylight saving time)
        est_offset = timezone(timedelta(hours=-5))
        
        # Treat dates as UTC and then convert to EST
        start_dt = custom_fromisoformat(start_date_standard).replace(tzinfo=utc_zone).astimezone(est_offset)
        end_dt = custom_fromisoformat(end_date_standard).replace(tzinfo=utc_zone).astimezone(est_offset)
        
        parsed_events.append({
            'name': summary.strip(),
            'description': description.strip().replace('\\n', '\n'),
            'url': url.strip(),
            'startDate': start_dt.isoformat(),
            'endDate': end_dt.isoformat()
        })
    return parsed_events

def getEvents():
    # Main Execution and HTTP request

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "max-age=0",
        "Cookie": "cookielawinfo-checkbox-necessary=yes; cookielawinfo-checkbox-non-necessary=yes; PHPSESSID=hs63hc1nkji2tq0mvj5n2u3",
        "DNT": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Chromium";v="115", "Google Chrome";v="115", "Not=A?Brand";v="99"',
        "sec-ch-ua-mobile": "0",
        "sec-ch-ua-platform": "Windows"
    }

    url = "uo.com"
    conn = http.client.HTTPSConnection(url)
    ics_events = None
    try:
        method = "GET"
        path = "/events/?ical=1&tribe_display=month"
        conn.request(method, path, headers=headers)
        response = conn.getresponse()

        if response.status == 200:
            document_text = response.read().decode("ISO-8859-1")
            ics_events = extract_ics_events(document_text)
            
            return ics_events
        else:
            print(f"Failed to retrieve the document. Status code: {response.status}")
    finally:
        conn.close()



from System.Collections.Generic import List
from System import String
from System import Int32 as int
from System.Threading import Thread, ThreadStart
import os

current_directory = os.getcwd()
print(f"The script is running in: {current_directory}")

gumpNumber = 656464
totalPages = 1
perPage = 6
currentPage = 1
def updateGump():
    global events, currentPage, totalPages, perPage
    if Gumps.HasGump(gumpNumber):
        Gumps.CloseGump(gumpNumber)
    gd = Gumps.CreateGump()
    Gumps.AddPage(gd, 0)

    Gumps.AddImage(gd, 0, 0, 52)
    Gumps.AddBackground(gd, 0, 75, 142, 21, 2501)
    Gumps.AddLabel(gd, 5, 75, 0, " Update Events")
    Gumps.AddButton(gd, 135, 75, 4005, 4006, 1, 1, 0)

    Gumps.AddButton(gd, 35, 35, 4014, 4016, 2, 1, 0)
    Gumps.AddButton(gd, 125, 35, 4005, 4006, 3, 1, 0)
    
    Gumps.AddLabel(gd,73,37,2062,"Page: " + str(currentPage))
    
    offsetY = 100
    

    # Filter out events that have already passed
    events = [event for event in events if is_today_or_future_event(event)]

    count = 0
    totalPages = len(events)/perPage
    
    for event in events[perPage * (currentPage - 1):perPage * currentPage]:
        count = count + 1
        
        #print("Start:", event['startDate']);
        toWrite = "Start: " + convert_time_to_est(event['startDate']) + " | End: " + convert_time_to_est(event['endDate']) + "<br><b>" + event['name'] + "</b><br>" + event['description']
        Gumps.AddHtml(gd, 3, offsetY * count, 700, 100, toWrite, True, True)

    Gumps.AddLabel(gd, 50, 3, 1152, 'UO Event Board')
    Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)

def is_today_or_future_event(event):
    timestamp_offset = timezone(timedelta(hours=-4))
    timestamp_str = event['endDate']
    date_str, time_offset_str = timestamp_str.split('T')
    offset_str = time_offset_str.split('-')[1]
    year, month, day = map(int, date_str.split('-'))
    hour, minute, second = map(int, time_offset_str[:8].split(':'))
    offset_hours, offset_minutes = map(int, offset_str.split(':'))
    offset = timedelta(hours=offset_hours, minutes=offset_minutes)
    timestamp_datetime = datetime(year, month, day, hour, minute, second, tzinfo=timezone.utc) - offset
    current_datetime_utc = datetime.now(timezone.utc)
    current_datetime = current_datetime_utc.astimezone(timestamp_offset)
    today = datetime(current_datetime.year, current_datetime.month, current_datetime.day, tzinfo=timestamp_offset)
    return timestamp_datetime >= today
    
if Gumps.HasGump(gumpNumber):
    Gumps.CloseGump(gumpNumber)
events = getEvents()
updateGump()
while True:
    Misc.Pause(1000)
    gd = Gumps.GetGumpData(gumpNumber)
    if gd:
        if gd.buttonid == 0:
            events = []
            gd.buttonid = -1
            updateGump()
                    
        if gd.buttonid == 1:
            Player.HeadMessage(66, 'Updating Event Details')
            events = getEvents()
            
            gd.buttonid = -1
            updateGump()
            
        if gd.buttonid == 2:
            Player.HeadMessage(66, 'Page Back')
            
            if currentPage == 1:
                currentPage = 1
            else:
                currentPage = currentPage - 1
              
            gd.buttonid = -1
            updateGump()
            
        if gd.buttonid == 3:
            Player.HeadMessage(66, 'Page Forward')
            
            if currentPage >= int(len(events) / perPage):
                currentPage = int(len(events) / perPage)
            else:
                currentPage = currentPage + 1
              
            gd.buttonid = -1
            updateGump()            