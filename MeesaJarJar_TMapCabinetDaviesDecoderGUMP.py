# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description: Tmap Decoder - Cabinet and Davies Locker
# Grabs Tmaps from the Tmap Cabinet based on selected level.
# Decodes all maps of a selected Tmap level that are available.
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#
mapStorageCabinet = 0x40652D66
davies = 0x412F7956
minimized = True # Start Minimized?

# END CONFIG --------------------------------------------------#

from System.Collections.Generic import List
from System import String
from System import Int32 as int
from System.Threading import Thread, ThreadStart
import os

gumpNumber = 45373783 
gumpid =  847126683

delay = 650
selectedLevel = 1 #default 1
inventory = {}
def toggleMinimize():
    global minimized
    minimized = not minimized
    #updateGump()
    
def updateGump(): 
    global minimized

    if minimized == True:
 
        offsetX = 0
        offsetY = 0        
        gd = Gumps.CreateGump(True,True,False,False)
        Gumps.AddPage(gd, 0);
        Gumps.AddBackground(gd,25+offsetX,85+offsetY,65,65,420)
        
        Gumps.AddButton(gd,35+offsetX,90+offsetY,2002,2002,95,1,0)
        Gumps.AddLabel(gd,53+offsetX,95+offsetY,33,"LM")

        Gumps.AddLabel(gd,40+offsetX,106+offsetY,1152,"Tmap")
        
        Gumps.AddLabel(gd,39+offsetX,119+offsetY,1152,"Decoder")
        
        Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)
        
    else:

        gd = Gumps.CreateGump(True,True,True,False)
        Gumps.AddBackground(gd,0,0,170,140,420)

        Gumps.AddBackground(gd,-20 + (selectedLevel * 25),5,30,38,420)

        Gumps.AddButton(gd,10,10,1424,1424,101,1,0)
        Gumps.AddButton(gd,35,10,1425,1425,102,1,0)
        Gumps.AddButton(gd,60,10,1426,1426,103,1,0)
        Gumps.AddButton(gd,85,10,1427,1427,104,1,0)
        Gumps.AddButton(gd,110,10,1428,1428,105,1,0)
        Gumps.AddButton(gd,135,10,1429,1429,106,1,0)

        Gumps.AddBackground(gd,10,75,160,25,450)
        Gumps.AddLabel(gd,40,77,449,"Get a Map")
        Gumps.AddButton(gd,5,75,4005,4005,1,1,0)
        
        Gumps.AddBackground(gd,10,95,160,25,450)
        Gumps.AddLabel(gd,40,97,449,"Decode Maps in BP")    
        Gumps.AddButton(gd,5,95,4005,4005,2,1,0)
        
        Gumps.AddBackground(gd,10,115,160,25,450)
        Gumps.AddLabel(gd,40,117,449,"Get/Decode a LVL")
        Gumps.AddButton(gd,5,115,4005,4005,3,1,0)
        
        Gumps.AddBackground(gd,5,42,160,25,450)
        if inventory:
            Gumps.AddLabel(gd,10,45,48,str(inventory[1]))
            Gumps.AddLabel(gd,35,45,48,str(inventory[2]))
            Gumps.AddLabel(gd,65,45,48,str(inventory[3]))
            Gumps.AddLabel(gd,85,45,48,str(inventory[4]))
            Gumps.AddLabel(gd,110,45,48,str(inventory[5]))
            Gumps.AddLabel(gd,135,45,48,str(inventory[6]))
        
        Gumps.AddBackground(gd,0,140,175,40,430)
        Gumps.AddLabel(gd,5,145,1901,"Made by: Meesa Jar Jar")
        Gumps.AddLabel(gd,5,160,1901,"Shop @ Lincoln Mallmorial!")
        
        Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)

def getMap():
    Player.HeadMessage(0,"Getting a Map!")
    Misc.Pause(delay)
    Items.UseItem(mapStorageCabinet)
    Misc.Pause(100)
    Gumps.WaitForGump(847126683, 10000)
    Gumps.SendAction(847126683, 109 + selectedLevel)
    
def addMapToDavies(map):
    Player.HeadMessage(0,"Dumping a Map to Davies!")
    Misc.Pause(delay)
    Items.UseItem(davies)
    Misc.Pause(100)
    Gumps.WaitForGump(3738072638, 10000)
    Gumps.SendAction(3738072638, 1000)
    Target.WaitForTarget(10000, False)
    
    Target.TargetExecute(map.Serial)
    Misc.Pause(1500)
    Target.TargetExecute(Player.Serial)
    Misc.ClearDragQueue()
    Gumps.CloseGump(3738072638)

def decodeMapsInPack(): 
    Player.HeadMessage(0,"Decoding Maps!")
    maps = []
    for item in Player.Backpack.Contains:
        if item.ItemID == 0x14EC and 'tattered' in item.Name.lower():
            maps.append(item.Serial)
    while True:
        if len(maps) > 0:
            for map_serial in maps[:]:
                map_item = Items.FindBySerial(map_serial)
                processingMap = True
                while processingMap == True:
                    if map_item and 'tattered' in map_item.Name.lower():
                        Items.UseItem(map_item)
                        Misc.Pause(650)
                    else:
                        Player.HeadMessage(0,"Decoded a map.")
                        addMapToDavies(map_item)
                        maps.remove(map_serial)
                        processingMap = False
        else:
            
            break
           

def extract_number(mystring):
    mystring = str(mystring)
    start_index = mystring.find('<BIG>')
    if start_index == -1:
        return 0  # Return 0 instead of None if start tag is not found
    
    start_index += len('<BIG>')
    end_index = mystring.find('</BIG>', start_index)
    if end_index == -1:
        return 0  # Return 0 instead of None if end tag is not found
    
    number_str = mystring[start_index:end_index]

    colon_index = number_str.find(':')
    if colon_index != -1:
        number_str = number_str[:colon_index]

    number_str = number_str.strip()
    if number_str.isdigit():
        return int(number_str)
    else:
        return 0  # Return 0 instead of None if the string is not a digit


def updateTmapCabinetInventory():
    Misc.Pause(delay)
    Items.UseItem(mapStorageCabinet)
    Misc.Pause(1000)
    gump_lines = Gumps.GetLineList(gumpid)
    count = 0
    inventory = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    if gump_lines:
        for line in gump_lines:

            if 'Completed Maps' in str(line):
                break
            if 'plainly' in str(line):
                inventory[1] = extract_number(gump_lines[count - 1 ])
            if 'expertly' in str(line):
                inventory[2] = extract_number(gump_lines[count - 1 ])
            if 'adeptly' in str(line):
                inventory[3] = extract_number(gump_lines[count - 1 ])
            if 'cleverly' in str(line):
                inventory[4] = extract_number(gump_lines[count - 1 ])
            if 'deviously' in str(line):
                inventory[5] = extract_number(gump_lines[count - 1 ])
            if 'ingeniously' in str(line):
                inventory[6] = extract_number(gump_lines[count - 1 ])
            count = count + 1   
            
    Gumps.SendAction(gumpid, 0)        
    return inventory            
        
inventory = updateTmapCabinetInventory()            
updateGump()

while True: 
    Misc.Pause(100)
    gd = Gumps.GetGumpData(gumpNumber)

    if gd:
        #if gd.buttonid != -1:
            #print("Pressed Button: ",gd.buttonid)
        if gd.buttonid == 0:
            #print("Button 0 Pressed.")
            gd.buttonid = -1
            minimized = True
            
            
            Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)
            updateGump()
        if gd.buttonid == 1:
                gd.buttonid = -1
                getMap()
                inventory = updateTmapCabinetInventory()  
                Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)
                updateGump()
                
        if gd.buttonid == 2:
                gd.buttonid = -1
                decodeMapsInPack()
                Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)
                updateGump()
   
        if gd.buttonid == 3:
                gd.buttonid = -1
                inventory = updateTmapCabinetInventory()  
                countToGet = inventory[selectedLevel]
                
                for z in range(0, countToGet-1):
                    getMap()
                    if z % 10 == 0:
                        Player.HeadMessage(0,"Got 10 Maps, decoding these then I will get more.")
                        decodeMapsInPack()
                    
                decodeMapsInPack()
                
                Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)
                updateGump()
                
        if gd.buttonid >= 100:
                selectedLevel = gd.buttonid - 100
                gd.buttonid = -1
                Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)
                updateGump()
                

        if gd.buttonid == 95:
            gd.buttonid = -1   
            minimized = False
            inventory = updateTmapCabinetInventory()  
            Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)
            updateGump()