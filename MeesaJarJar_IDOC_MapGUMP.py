# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description: IDOC In-Game GUMP Map
# Meesa Jar Jar - PRIVATE SCRIPT - DO NOT SHARE
# If yousa have this, and Jar Jar didnt give it to you directly, yousa in BIG doo doo.
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#


# END CONFIG --------------------------------------------------#


from System.Collections.Generic import List
from System import String
from System import Int32 as int
import time
import urllib.request
import urllib.parse
import re
import csv
from math import sqrt


gumpNumber = 657164
Gumps.CloseGump(gumpNumber)
def find_nearest_location(filename, X, Y):
    X = int(X)
    Y = int(Y)
    closest_location = None
    min_distance = float('inf')
    pattern = r'\d+'
    
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            integers = re.findall(pattern, str(row))
            location_x = int(integers[-2])
            location_y = int(integers[-1])
            distance = sqrt((location_x - X) ** 2 + (location_y - Y) ** 2)
            if distance < min_distance:
                min_distance = distance
                closest_location = (integers[0], location_x, location_y, row[4])
                
    return closest_location

def set_atlas_go_values(X, Y):
    filename = './RazorEnhanced/Scripts/MeesaJarJar_RunebookAtlas_Coordinates.csv'
    closest_location = find_nearest_location(filename, X, Y)
    
    if closest_location:
        mySerial, myX, myY, myName = closest_location
        Misc.SetSharedValue("Atlas_Go", True)
        Misc.SetSharedValue("Atlas_Go_Serial", int(mySerial))
        Misc.SetSharedValue("Atlas_Go_Name", str(myName))
        Misc.SetSharedValue("Atlas_Go_RuneX", int(myX))
        Misc.SetSharedValue("Atlas_Go_RuneY", int(myY))
    else:
        print("No matching runebook found for the given coordinates.")

def unix_to_est_12hour(unix_timestamp):
    est = time.gmtime(int(unix_timestamp) - time.timezone + time.daylight * 3600)
    return time.strftime('%Y-%m-%d %I:%M:%S %p', est)

def fetch_url(url):
    #print("Fetching URL:",  url)
    with urllib.request.urlopen(url) as response:
        html = response.read().decode('utf-8')
        return html

def getHouseMasterLines():
    #print("getHouseMasterLines()")
    locationsx = []
    url = 'http://ec2-18-220-241-158.us-east-2.compute.amazonaws.com/displayAllHouseData.php'
    
    html_content = fetch_url(url)
    lines = html_content.split('<br>')
    
    for line in lines:
        line = line.split(',')
        if len(line) >= 5:
            if [line[0],line[1]] not in locationsx:
                if len(str(line)) > 10:
                    current_time = int(time.time())
                    decay_status = line[3].lower()
                    timestamp = int(line[4].split('|')[1])

                    if 'danger' in decay_status and current_time - timestamp <= 100000:
                        locationsx.append([line[0], line[1], line[3], line[4]])
                    elif 'greatly' in decay_status and current_time - timestamp <= 100000:
                        locationsx.append([line[0], line[1], line[3], line[4]])
                    elif 'fairly' in decay_status and current_time - timestamp <= 100000:
                        locationsx.append([line[0], line[1], line[3], line[4]])
                    elif 'somewhat' in decay_status and current_time - timestamp <= 72000:
                        locationsx.append([line[0], line[1], line[3], line[4]])
                    elif 'slightly' in decay_status and current_time - timestamp <= 86400:
                        locationsx.append([line[0], line[1], line[3], line[4]])
                    elif 'new' in decay_status and current_time - timestamp <= 90000:
                        locationsx.append([line[0], line[1], line[3], line[4]])
    #print("Count Lines:", len(lines))
    return lines, locationsx

def getSingleHouseLines(houseSerial):
    #print(f"Entering getSingleHouseLines with houseSerial: {houseSerial}")
    slocations = []
    surl = 'http://ec2-18-220-241-158.us-east-2.compute.amazonaws.com/displaySingleHouseData.php?serial=' + str(houseSerial)
    #print(f"Fetching URL: {surl}")
    
    shtml_content = fetch_url(surl)
    #print(f"Fetched HTML content: {shtml_content[:100]}...")  # Print the first 100 characters for brevity
    
    shtml_content = shtml_content.split('<br>')
    #print(f"Split HTML content into lines: {len(shtml_content)} lines found")
    
    for index, sline in enumerate(shtml_content):
        #print(f"Processing line {index}: {sline}")
        sline = sline.split(',')
        #print(f"Split line into components: {sline}")
        
        if len(sline) > 1:
            timestamp = sline[4].split('|')[1]
            readable_time = unix_to_est_12hour(timestamp)
            #print(f"Converted timestamp {timestamp} to readable time {readable_time}")
            
            if [sline[0], sline[1]] not in slocations:
                slocations.append([str(sline[0]), str(sline[1]), str(sline[3]), readable_time])
                #print(f"Appended to slocations: {slocations[-1]}")
    
    #print(f"Exiting getSingleHouseLines with {len(slocations)} locations found")
    return slocations

def updatePlayerLocation():
    #print("updatePlayerLocation")
    surl = f'http://ec2-18-220-241-158.us-east-2.compute.amazonaws.com/updatePlayerPosition.php?x={urllib.parse.quote(str(Player.Position.X))}&y={urllib.parse.quote(str(Player.Position.Y))}&playername={urllib.parse.quote(str(Player.Name))}&playerserial={urllib.parse.quote(str(Player.Serial))}'
    fetch_url(surl)

def getPlayerLocations():
    surl = 'http://ec2-18-220-241-158.us-east-2.compute.amazonaws.com/displayPlayerLocationsData.php'
    shtml_content = fetch_url(surl)
    shtml_content = shtml_content.split('<br>')

    players_dict = {}
    
    for sline in shtml_content:
        sline = sline.split(',')
        if len(sline) >= 5:
            key = str(sline[3])
            players_dict[key] = [str(sline[0]), str(sline[1]), key, sline[4]]

    players = list(players_dict.values())
    return players

def rescale_coordinates(x, y, original_width=5120, original_height=4096, new_width=768, new_height=614):
    x = int(x)
    y = int(y)
   
    x_scale = new_width / original_width
    y_scale = new_height / original_height

    new_x = x * x_scale
    new_y = y * y_scale

    return new_x, new_y
    
def trackingArrow():
    print("SEL:", selectedLocation)
    Player.TrackingArrow(selectedX,selectedY,True,selectedLocation)
        
updatePlayerLocation()

pLocations = getPlayerLocations()
locations = []
lines = []
showDanger = True
showGreatly = True
showFairly = True
showAll = True
showBackground = True
lines, locations = getHouseMasterLines()
offsetMapX = 150
minimized = True
offsetMenuX = 8
selectedX = 0
selectedY = 0
singleLocationLines = []
currentlyTrackedHouse = None


def updateGump():
    global locations, pLocations, singleLocationLines, selectedX, selectedY
    if not Timer.Check("masterlistDL"):
        Timer.Create("masterlistDL",60000)
        locations = []
        lines, locations = getHouseMasterLines()

    if not Timer.Check("masterPlayerDL"):
        updatePlayerLocation()
        Timer.Create("masterPlayerDL",10000)
        pLocations = []
        pLocations = getPlayerLocations()
  
    gd = Gumps.CreateGump(True,True,False,False)
     
    if minimized == True:
        Gumps.AddBackground(gd, 625, -5, 225, 35, 420)
        Gumps.AddLabel(gd,offsetMenuX + 635,4,1150,"Meesa Jar Jar`s IDOC MAP")
        Gumps.AddButton(gd, offsetMenuX + 810, int(0), 1605, 1605, -58, 1, 0)
        
    else:
        Gumps.AddImage(gd, 150, 0, 33)
        Gumps.AddBackground(gd,0,-25,800,35,420)
        Gumps.AddLabel(gd, int(32), int(-16), 1152, "Filter: On/Off")
        Gumps.AddButton(gd, offsetMenuX + 775, int(0), 1605, 1605, -58, 1, 0)
        
        if showDanger:
            Gumps.AddButton(gd, offsetMenuX + int(10), int(30), 42070, 42070, -50, 1, 0)
            #Gumps.AddButton(gd, offsetMenuX + int(100), int(30), 42072, 42072, -50, 1, 0)
        else:
            Gumps.AddButton(gd, offsetMenuX + int(10), int(30), 42071, 42071, -50, 1, 0)
            #Gumps.AddButton(gd, offsetMenuX + int(100), int(30), 42073, 42073, -50, 1, 0)
        Gumps.AddLabel(gd, offsetMenuX + int(30), int(30), 1152, "IDOC")
        
        if showGreatly:
            Gumps.AddButton(gd, offsetMenuX + int(10), int(60), 42070, 42070, -51, 1, 0)
            Gumps.AddButton(gd, offsetMenuX + int(100), int(60), 42072, 42072, -51, 1, 0)
        else:
            Gumps.AddButton(gd, offsetMenuX + int(10), int(60), 42071, 42071, -51, 1, 0)
            Gumps.AddButton(gd, offsetMenuX + int(100), int(60), 42073, 42073, -51, 1, 0)
        Gumps.AddLabel(gd, offsetMenuX + int(30), int(60), 1152, "Greatly")
        
        if showFairly:
            Gumps.AddButton(gd, offsetMenuX + int(10), int(90), 42070, 42070, -52, 1, 0)
            Gumps.AddButton(gd, offsetMenuX + int(100), int(90), 42072, 42072, -52, 1, 0)
        else:
            Gumps.AddButton(gd, offsetMenuX + int(10), int(90), 42071, 42071, -52, 1, 0)
            Gumps.AddButton(gd, offsetMenuX + int(100), int(90), 42073, 42073, -52, 1, 0)
        Gumps.AddLabel(gd, offsetMenuX + int(30), int(90), 1152, "Fairly")
       
#        if showAll:
#            Gumps.AddButton(gd, offsetMenuX + int(10), int(120), 42070, 42070, -53, 1, 0)
#            Gumps.AddButton(gd, offsetMenuX + int(100), int(120), 42072, 42072, -53, 1, 0)
#        else:
#            Gumps.AddButton(gd, offsetMenuX + int(10), int(120), 42071, 42071, -53, 1, 0)
#            Gumps.AddButton(gd, offsetMenuX + int(100), int(120), 42073, 42073, -53, 1, 0)
#        Gumps.AddLabel(gd, offsetMenuX + int(30), int(120), 1152, "All")
        
#        if showBackground:
#            Gumps.AddButton(gd, offsetMenuX + int(10), int(150), 42070, 42070, -54, 1, 0)
#            Gumps.AddButton(gd, offsetMenuX + int(100), int(150), 42072, 42072, -54, 1, 0)
#        else:
#            Gumps.AddButton(gd, offsetMenuX + int(10), int(150), 42071, 42071, -54, 1, 0)
#            Gumps.AddButton(gd, offsetMenuX + int(100), int(150), 42073, 42073, -54, 1, 0)

        
        Gumps.AddLabel(gd, 200, -15, 1150, str("Player (X,Y):"))
        Gumps.AddLabel(gd, 350, -15, 1152, str(Player.Position.X))
        Gumps.AddLabel(gd, 300, -15, 1150, "X : ")
        Gumps.AddLabel(gd, 450, -15, 1152, str(Player.Position.Y))
        Gumps.AddLabel(gd, 400, -15, 1150, "Y : ")

        startY = 650
        offsetY = 25
        index = 0

        keywords = ["danger", "greatly", "fairly", "somewhat", "slightly", "new"]
        last_occurrence = {keyword: None for keyword in keywords}

        for item in singleLocationLines:
            for keyword in keywords:
                if keyword in str(item).strip().lower():
                    last_occurrence[keyword] = item

        decayLineHeight = 20
        index = 1
        for keyword in keywords:
            index += 1
            last_item = last_occurrence[keyword]
            if last_item:
                Gumps.AddLabel(gd, 25, 140 + (decayLineHeight * index), 1152, str(keyword) + ' : ' + str(last_item[3]))
            else:
                Gumps.AddLabel(gd, 25, 140 + (decayLineHeight * index), 1152, str(keyword) + ' : ')

        for location in locations:
            locX, locY = rescale_coordinates(location[0], location[1])
            houseSerial = str(location[3]).split('|')[0]
            logTimestamp = str(location[3]).split('|')[1]
            currentTime = int(time.time())
            if showAll:
                if (int(currentTime) - int(logTimestamp)) > 86400:
                    #Gumps.AddButton(gd, offsetMapX + int(locX), int(locY), 5020, 5020, int(houseSerial), 1, 0)
                    Gumps.AddImage(gd,offsetMapX + int(locX), int(locY),5020)
                else:
                    #Gumps.AddButton(gd, offsetMapX + int(locX), int(locY), 1686, 1686, int(houseSerial), 1, 0)
                    Gumps.AddImage(gd,offsetMapX + int(locX), int(locY),1686)
                Gumps.AddTooltip(gd, 3012171, str(location[0]))
                Gumps.AddTooltip(gd, 3012171, str(location[1]))
                Gumps.AddTooltip(gd, 3012171, str(location[2]))
                Gumps.AddTooltip(gd, 3012171, unix_to_est_12hour(str(location[3]).split('|')[1]))

        for location in locations:
            locX, locY = rescale_coordinates(location[0], location[1])
            houseSerial = str(location[3]).split('|')[0]
            logTimestamp = str(location[3]).split('|')[1]
            
            if showDanger and 'danger' in str(location).lower():
                Gumps.AddButton(gd, offsetMapX + int(locX), int(locY), 11412, 11412, int(houseSerial), 1, 0)
                Gumps.AddTooltip(gd, 3012171, str(location[0]))
                Gumps.AddTooltip(gd, 3012171, str(location[1]))
                Gumps.AddTooltip(gd, 3012171, str(location[2]))
                Gumps.AddTooltip(gd, 3012171, unix_to_est_12hour(str(location[3]).split('|')[1]))
            elif showGreatly and 'greatly' in str(location).lower():
                Gumps.AddButton(gd, offsetMapX + int(locX), int(locY), 2361, 2361, int(houseSerial), 1, 0)
                Gumps.AddTooltip(gd, 3012171, str(location[0]))
                Gumps.AddTooltip(gd, 3012171, str(location[1]))
                Gumps.AddTooltip(gd, 3012171, str(location[2]))
                Gumps.AddTooltip(gd, 3012171, unix_to_est_12hour(str(location[3]).split('|')[1]))
            elif showFairly and 'fairly' in str(location).lower():
                Gumps.AddButton(gd, offsetMapX + int(locX), int(locY), 2362, 2362, int(houseSerial), 1, 0)
                Gumps.AddTooltip(gd, 3012171, str(location[0]))
                Gumps.AddTooltip(gd, 3012171, str(location[1]))
                Gumps.AddTooltip(gd, 3012171, str(location[2]))
                Gumps.AddTooltip(gd, 3012171, unix_to_est_12hour(str(location[3]).split('|')[1]))

        playerX = int(Player.Position.X)
        playerY = int(Player.Position.Y)
        playerX, playerY = rescale_coordinates(playerX, playerY)
        
        Gumps.AddImage(gd, offsetMapX + int(playerX-4), int(playerY-4), 2103)

        currentTime = int(time.time())
        for LMWorker in pLocations:
            if int(LMWorker[3]) > int(currentTime - 60):
                workerX, workerY = rescale_coordinates(LMWorker[0], LMWorker[1])
                workerName = str(LMWorker[2]).replace('&quot;', '"')#"
                Gumps.AddImage(gd, offsetMapX + int(workerX - 4), int(workerY) - 4, 2103)
                Gumps.AddLabel(gd, offsetMapX + int(workerX) - 50, int(workerY) - 24, 1152, workerName)
        
        if selectedX != 0 and selectedY != 0:
            Gumps.AddLabel(gd, 25, 300, 1152, "RECALL")
            Gumps.AddLabel(gd, 25, 320, 1152, "TO HOUSE")
            Gumps.AddButton(gd, 100, 300, 1540, 1539, -55, 1, 0)
            
            Gumps.AddLabel(gd, 25, 340, 1152, "TRACK")
            Gumps.AddLabel(gd, 25, 360, 1152, "HOUSE")
            Gumps.AddButton(gd, 100, 340, 1540, 1539, -56, 1, 0)
    Gumps.CloseGump(gumpNumber)
    Gumps.SendGump(gumpNumber, Player.Serial, 100, 100, gd.gumpDefinition, gd.gumpStrings)

updatePlayerLocation()
lines, locations = getHouseMasterLines()
singleLocationLines = []
selectedLocation = None
updateGump()
gd = Gumps.GetGumpData(gumpNumber)
gd.buttonid = -1
Gumps.CloseGump(gumpNumber)            
Gumps.SendGump(gumpNumber, Player.Serial, 100, 100, gd.gumpDefinition, gd.gumpStrings)
Gumps.SendAction(gumpNumber, 0)            
while Player.Connected:
   
    
    gd = Gumps.GetGumpData(gumpNumber)
    if gd and gd.buttonid != -1:
        if gd.buttonid == 0:
            gd.buttonid = -1
            
        elif gd.buttonid >= 1:
            #print("GREATER THAN 1")
            selectedLocation = gd.buttonid
            singleLocationLines = getSingleHouseLines(selectedLocation)
            
            #print("SPECIAL DEBUG *******")
            #print(singleLocationLines)
            #print("END SPECIAL *********")
            if len(singleLocationLines) >= 1:
                selectedX = int(singleLocationLines[0][0])
                selectedY = int(singleLocationLines[0][1])
                #print("selectedX:", selectedX, "selectedY:", selectedY)
                
                        
                gd.buttonid = -1
                Gumps.CloseGump(gumpNumber)
                Gumps.SendGump(gumpNumber, Player.Serial, 100, 100, gd.gumpDefinition, gd.gumpStrings)
            

            else:
                print("FAILED SINGLE LINE SELECTION LOCATION TEST")
            #gd.buttonid = -1
        else:
            if gd.buttonid == -50:
                showDanger = not showDanger
            elif gd.buttonid == -51:
                showGreatly = not showGreatly
            elif gd.buttonid == -52:
                showFairly = not showFairly
            elif gd.buttonid == -53:
                showAll = not showAll
            elif gd.buttonid == -54:
                showBackground = not showBackground    
            elif gd.buttonid == -55:
                if selectedX == 0 and selectedY == 0:
                    print("ERROR FAILED - DID NOT SELECT LOCATION")
                else:
                    set_atlas_go_values(selectedX, selectedY)
            elif gd.buttonid == -56:
                trackingArrow()
                
            elif gd.buttonid == -58: 
                if minimized:
                    minimized = False
                else:
                    minimized = True
            if gd.buttonid == 0:
                minimized = True
            Gumps.CloseGump(gumpNumber)       
            Gumps.SendGump(gumpNumber, Player.Serial, 100, 100, gd.gumpDefinition, gd.gumpStrings)
            gd.buttonid = -1
        
    updateGump()        
    Misc.Pause(1000)  
    