# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description: Meesa Jar Jar`s MIB Extractor
# Processes all MIBs in first layer of backpack, adds to ingame map!
# Draws fun fake bubbles object at the spot the MIB is !
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#

MibFileName = 'C:/Program Files (x86)/UOForever/UO/Forever/Data/Client/MIBCapture.csv'

# END CONFIG --------------------------------------------------#


import math
import random
import csv
import os


LordBritishThrone = [1624, 1323]
WorldSize = [4096, 5120]
TilesPerDegree = [WorldSize[0] / 360.0, WorldSize[1] / 360.0]
# END MIB Processor CONFIG

def worldSave():
    if Journal.SearchByType('The world will save in 1 minute.', 'Regular'):
        Misc.SendMessage('Pausing for world save', 33)
        while not Journal.SearchByType('World save complete.', 'Regular'):
            Misc.Pause(500)
        Misc.Pause(2500)
        Misc.SendMessage('Continuing run', 33)
        Journal.Clear()

def splitToPieces(location):
    degree, secTemp = location.split('\xb0')
    seconds, direction = secTemp.split('\x27')
    return int(degree), int(seconds), direction

def convertDegreesToDecimal(degree, seconds, direction):
    result = 0
    if direction.lower() == 'w':
        result = (LordBritishThrone[1] - (seconds / 60.0) * TilesPerDegree[1] - degree * TilesPerDegree[1]) % WorldSize[1]
    if direction.lower() == 'e':
        result = (LordBritishThrone[1] + (seconds / 60.0) * TilesPerDegree[1] + degree * TilesPerDegree[1]) % WorldSize[1]
    if direction.lower() == 'n':
        result = (LordBritishThrone[0] - (seconds / 60.0) * TilesPerDegree[0] - degree * TilesPerDegree[0]) % WorldSize[0]
    if direction.lower() == 's':
        result = (LordBritishThrone[0] + (seconds / 60.0) * TilesPerDegree[0] + degree * TilesPerDegree[0]) % WorldSize[0]
    return int(result) + 1

def GetDecimalCoordinates(mib):
    print(mib)
    x = -1
    y = -1
    Items.UseItem(mib)
    Gumps.WaitForGump(0, 3000)
    if Gumps.HasGump():
        texts = Gumps.LastGumpGetLineList()
        location = texts[len(texts) - 1]
        z = location.split(',')
        Player.HeadMessage(54, str(z[1]))
        NSloc, EWloc = location.split(',')
        deg1, sec1, dir1 = splitToPieces(NSloc)
        deg2, sec2, dir2 = splitToPieces(EWloc)
        Gumps.CloseGump(0)
        Misc.SendMessage("deg: {} sec: {} dir: {}".format(deg1, sec1, dir1))
        Misc.SendMessage("deg: {} sec: {} dir: {}".format(deg2, sec2, dir2))
        x = convertDegreesToDecimal(deg2, sec2, dir2)
        y = convertDegreesToDecimal(deg1, sec1, dir1)
        return x, y
    else:
        Misc.SendMessage("Gump did not Open for mib 0x{:x}".format(mib.Serial))
    return x, y

    
def convert_packet_to_bytes(packet):
    byte_list = []
    for value in packet:
        try:
            byte_list.append(int(value, 16))
        except ValueError:
            print("Invalid hexadecimal value in packet:", value)
            print("Original packet:", packet)
            return None
    return byte_list

def createItemAtLocation(itemx,itemy,itemz,packet_list,hue):
    randidint = random.randrange(0,10000000)

    i_loc_x = hex(itemx) 
    i_loc_y = hex(itemy)
    i_loc_z = hex(itemz)

    if len(i_loc_x) < 6:
        i_loc_x = i_loc_x.replace("0x","0x0")
    if len(i_loc_y) < 6:
        i_loc_y = i_loc_y.replace("0x","0x0")    
    if len(i_loc_z) < 6:
        i_loc_z = i_loc_z.replace("0x","0x0") 

    x1 = i_loc_x[2:4]  
    x2 = i_loc_x[4:6]  
    y1 = i_loc_y[2:4]  
    y2 = i_loc_y[4:6]  
    z = i_loc_z 
    
    hues = hue.split(" ")

    packet_list[5] = hex(randidint)[2:].zfill(2)
    packet_list[15] = x1
    packet_list[16] = x2
    packet_list[17] = y1
    packet_list[18] = y2
    packet_list[19] = z
    packet_list[21] = hues[0]
    packet_list[22] = hues[1]
    
    byte_list = convert_packet_to_bytes(packet_list)
    
    PacketLogger.SendToClient(byte_list)
    
    return packet_list

def drawFakeItemAtSpot(X, Y):
    packet = "F3 00 01 00 48 FC BB 12 6E 7B 00 00 01 00 01 05 88 06 88 0A 00 04 15 20 00 00"  
    packet_list = packet.split(" ")  

    hue = "00 00"
    itemID = 0xB6D0
    X = int(X)
    Y = int(Y)
    Z = int(Player.Position.Z + 2)

    packet = createItemAtLocation(X,Y,Z,packet_list,hue)
def examplemain():
    if MibContainer is not None:
        for maybeMIB in MibContainer.Contains:
            if maybeMIB.ItemID == 0x099F and maybeMIB.Hue == 0x0:
                mib = maybeMIB
                Items.UseItem(mib.Serial)
                Misc.Pause(1000)
        Items.WaitForContents(MibContainer, 3000)
        with open(MibFileName, 'w') as file:
            file.write("3\n")
            for maybeMIB in MibContainer.Contains:
                if maybeMIB.ItemID == 0x14EE and maybeMIB.Hue == 0x0:
                    mib = maybeMIB
                    x, y = GetDecimalCoordinates(mib)
                    Misc.SendMessage("X: {}".format(x))
                    Misc.SendMessage("Y: {}".format(y))
                    file.write("+treasure: {} {} 0 {}\n".format(x, y, TargetName))
                if maybeMIB.ItemID == 0x14EE and maybeMIB.Hue == 0x0481:
                    mib = maybeMIB
                    x, y = GetDecimalCoordinates(mib)
                    Misc.SendMessage("X: {}".format(x))
                    Misc.SendMessage("Y: {}".format(y))
                    file.write("+treasure: {} {} 0 {}\n".format(x, y, "Ancient " + TargetName))

def distance_between_points(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    
def processSOS():
    with open(MibFileName, 'a') as file: 
        for mib in Player.Backpack.Contains:
            if mib.ItemID == 0x14EE:
                Items.UseItem(mib)
                Misc.Pause(800)
                x, y = GetDecimalCoordinates(mib)
                Player.HeadMessage(54, str(x))
                Player.HeadMessage(54, str(y))
                Misc.SendMessage("X: {}".format(x))
                Misc.SendMessage("Y: {}".format(y))
                z = str(x) + ',' + str(y) + ',0,' + str(mib) + ',mib,' + 'blue' + '3' + "\n"  
                Misc.Pause(100)
                print(z)
                Player.ChatSay(z)
                file.write(z)
                Misc.Pause(100)
                Gumps.SendAction(1426736667, 0)
                Misc.Pause(800)

mibs = []
if os.path.exists(MibFileName):
    os.remove(MibFileName)
    
if not os.path.exists(MibFileName):
    with open(MibFileName, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        #csvwriter.writerow(['0', '0'])  # Write a default row or leave empty if you prefer
    
processSOS()
print("MIBS PROCESSED IN BAG. ")
print("Displaying Bubbles at Locations indefinitely now. ")

print("Loading MIB CSV File.")
with open(MibFileName, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        if len(row) >= 2:  
            mibs.append([int(row[0]),int(row[1])])
            
Misc.Pause(2000)
CUO.LoadMarkers()

while Player.Connected == True:   
    Misc.Pause(1000)
    for mib in mibs:
        #print("RAWMIB:",mib)
          
        if distance_between_points(mib[0],mib[1], Player.Position.X, Player.Position.Y) < 16:
            drawFakeItemAtSpot(mib[0], mib[1])    
    