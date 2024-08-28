# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description: IDOC Scanner 
# Meesa Jar Jar - PRIVATE SCRIPT - DO NOT SHARE
# If yousa have this, and Jar Jar didnt give it to you directly, yousa in BIG doo doo.
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#


# END CONFIG --------------------------------------------------#

import math
import time
import urllib.request
import urllib.parse
import threading

masterListFile = 'MeesaHouseDecayMasterList.csv'

def find_latest_timestamps_for_serial(csv_file, serial):
    latest_timestamps = {
        'like new': 0,
        'slightly worn': 0,
        'somewhat worn': 0,
        'fairly worn': 0,
        'greatly worn': 0,
        'in danger of collapsing': 0
    }
    
    with open(csv_file, 'r', encoding="utf8") as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) >= 5:  
                file_serial = int(parts[4].strip().split('|')[0])
                if file_serial == serial:
                    decay_status = str(parts[3].strip())
                    timestamp_info = parts[4].strip().split('|')
                    if len(timestamp_info) == 2:
                        timestamp = int(timestamp_info[1])  
                        if decay_status in latest_timestamps:
                            if timestamp > latest_timestamps[decay_status]:
                                latest_timestamps[decay_status] = timestamp
    
    return latest_timestamps


def fetch_url(url):
    with urllib.request.urlopen(url) as response:
        html = response.read().decode('utf-8')  
        return html
        
def post_data(line, filename):
    #print("Line:", line)
    #print("filename:", filename)
    url = 'http://ec2-18-220-241-158.us-east-2.compute.amazonaws.com/updateHouse.php'
    data = {
        'data': line,
        'filename': filename
    }
    data = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(url, data=data, method='POST')
    
    try:
        with urllib.request.urlopen(req) as response:
            result = response.read().decode()
            print(result)
    except urllib.error.URLError as e:
        print(f'Error: {e.reason}')

def post_data_async(line, filename):
    thread = threading.Thread(target=post_data, args=(line, filename))
    thread.start()
    
while Player.Connected == True:
    Misc.Pause(250)
#
#    if Timer.Check('refreshMapMarkers') == False:
#        print("Refreshing Map Markers.")
#        try:
#            CUO.LoadMarkers()
#            Timer.Create('refreshMapMarkers',10000)
#        except:
#            print("Failed Load Markers.")           
#        
    itemFilter = Items.Filter()
    itemFilter.RangeMin = 0
    itemFilter.RangeMax = 15
    itemFilter.CheckIgnoreObject = True

    itemList = Items.ApplyFilter(itemFilter)

    for item in itemList:
        
        if Timer.Check("decay_" + str(item.Serial)) == False:
            Items.WaitForProps(item,1000)
            
            properties_str = [str(prop) for prop in item.Properties]
            current_timestamp = int(time.time())
            
            if "this structure" in str(properties_str).lower():
            
                timestamp = int(time.time())

                if 'condition' in str(item.Properties).lower():
                    for prop in item.Properties:
                        if 'condition' in str(prop).lower():
                            colon_index = str(prop).lower().find(':')
                            condition = str(prop).lower()[colon_index + 2:].strip()    
                            
                            if 'danger' in str(condition):
                                Player.HeadMessage(1150, "MEESA FOUND AN IDOC!")
                            if 'greatly worn' in str(condition):
                                Player.HeadMessage(1150, "MEESA FOUND A GREATLY!")                            

                            serial_to_find = item.Serial

                            foundOne = False
                            foundTwo = False
                            
                            if Timer.Check("update_" + str(item.Serial)) == False:
                               
                                #latest_timestamps = find_latest_timestamps_for_serial(csv_file_path, serial_to_find)
                            
                                Timer.Create("update_" + str(item.Serial),60000)

                                post_data_async((str(item.Position.X) + ',' + str(item.Position.Y) + ',0,' + str(condition).replace("this structure is ", "").rstrip(".") + ','+ str(item.Serial) + '|'  + str(timestamp) + ',0'),masterListFile)
                                
                                Items.Message(item,0x0000,"Updated:" + condition)
                                Player.HeadMessage(1150,"Updated:" + condition)
                                Misc.Pause(100)

                            