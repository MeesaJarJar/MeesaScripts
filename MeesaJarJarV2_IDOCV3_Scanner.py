# Meesa Jar Jar - PRIVATE SCRIPT - DO NOT SHARE
# If yousa have this, and Jar Jar didnt give it to you directly, yousa in BIG doo doo. 
output_folder = r"C:\\Program Files (x86)\\UOForever\\UO\\ForeverOnline\\RazorEnhanced\\Scripts"

import math
import time
import urllib.request
import urllib.parse
import threading

masterListFile = 'MeesaHouseDecayMasterList.csv'

def post_player_position_async(player_x, player_y, player_serial, player_name, player_area):
    thread = threading.Thread(target=post_player_position, args=(player_x, player_y, player_serial, player_name, player_area))
    thread.start()

def post_player_position(player_x, player_y, player_serial, player_name, player_area):
    base_url = 'https://meesajarjar.shop/IDOC/updatePlayerPosition.php'
    params = {
        'x': player_x,
        'y': player_y,
        'playerserial': player_serial,
        'playername': player_name,
        'playerarea': player_area
    }
    
    url = base_url + '?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, method='GET')
    
    try:
        with urllib.request.urlopen(req) as response:
            result = response.read().decode()
            #print(f'[Position Update] Server response: {result}')  # <-- uncommented + labeled
    except urllib.error.URLError as e:
        print(f'[Position Update] Error: {e.reason}')  # <-- was already printing, added label

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

def getHouseMasterLines():
    url = 'https://meesajarjar.shop/IDOC/MeesaHouseDecayMasterList.csv'
    lines = []
    html_content = fetch_url(url)
    lines = html_content.splitlines()
    return lines
    
def fetch_url(url):
    with urllib.request.urlopen(url) as response:
        html = response.read().decode('utf-8')  
        return html
        
def post_data(line, filename):
    url = 'https://meesajarjar.shop/IDOC/post_update.php'
    data = {
        'data': line,
        'filename': filename
    }
    encoded_data = urllib.parse.urlencode(data).encode('utf-8')
    
    req = urllib.request.Request(
        url,
        data=encoded_data,
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            result = response.read().decode()
            #(f'[Post Data] Server response: {result}')  # <-- uncommented + labeled
    except urllib.error.URLError as e:
        print(f'[Post Data] Error: {e.reason}')  # <-- was already printing, added label


def post_data_async(line, filename):
    thread = threading.Thread(target=post_data, args=(line, filename))
    thread.start()
    
while Player.Connected == True:
    Misc.Pause(500)

    if Timer.Check("player_position_update") == False:
        Timer.Create("player_position_update", 30000) 
        
        post_player_position_async(
            Player.Position.X, 
            Player.Position.Y, 
            Player.Serial,
            Player.Name,
            Player.Area()
        )
        
        #Player.HeadMessage(1150, "Position updated!")
    itemFilter = Items.Filter()
    itemFilter.RangeMin = 0
    itemFilter.RangeMax = 18
    itemFilter.CheckIgnoreObject = True

    itemList = Items.ApplyFilter(itemFilter)

    for item in itemList:
        
        if Timer.Check("decay_" + str(item.Serial)) == False:
            Items.WaitForProps(item,750)
            
            properties_str = [str(prop) for prop in item.Properties]
            current_timestamp = int(time.time())
            
            if "this structure" in str(properties_str).lower() and 'danger' not in str(item.Name).lower():
            
                if 'danger' in str(properties_str).lower() :
                    Player.HeadMessage(1150, "MEESA FOUND AN IDOC!")
                    
                elif 'greatly' in str(properties_str).lower():
                
                    Player.HeadMessage(1150, "MEESA FOUND A GREATLY!")
                    
                timestamp = int(time.time())

                if 'condition' in str(item.Properties).lower():
                    for prop in item.Properties:
                        if 'condition' in str(prop).lower():
                            colon_index = str(prop).lower().find(':')
                            condition = str(prop).lower()[colon_index + 2:].strip()    

                            serial_to_find = item.Serial

                            foundOne = False
                            foundTwo = False
                            
                            if Timer.Check("update_" + str(item.Serial)) == False:
                               
                                Timer.Create("update_" + str(item.Serial),60000)

                                post_data_async((str(item.Position.X) + ',' + str(item.Position.Y) + ',0,' + str(condition).replace("this structure is ", "").rstrip(".") + ','+ str(item.Serial) + '|'  + str(timestamp) + ',0'),masterListFile)
                                
                                Items.Message(item,0x0000,"Updated:" + condition)
                                #Player.HeadMessage(1150,"Updated:" + condition)
                                Misc.Pause(100)