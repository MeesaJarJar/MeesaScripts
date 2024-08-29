# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# --WORK IN PROGRESS ------------------------------------------#
# -------------------------------------------------------------#
# Description: Proof of Concept showing how you can clone 
# parts of the maps items and recreate them easily elsewhere.
# Seems like it would be a good tool for GMs for making scenes
# if you can hone it in a bit, maybe do selectable areas.
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#


# END CONFIG --------------------------------------------------#

import random

def convert_packet_to_bytes(packet):
    byte_list = []
    for value in packet:
        if value:
            byte_list.append(int(value, 16))
        else:
            byte_list.append(0) 
    return byte_list

def createItemAtLocation(itemx, itemy, itemz, itemToDraw, hue):
    packet = "F3 00 01 00 48 FC BB 12 " + itemToDraw + " 00 00 01 00 01 05 88 06 88 0A 00 04 15 20 00 00"  
    packet_list = packet.split(" ")

    serial_hex = hex(random.randrange(0, 0xFFFFFF))[2:].zfill(6)

    i_loc_x = hex(itemx)[2:].zfill(4)
    i_loc_y = hex(itemy)[2:].zfill(4)
    i_loc_z = hex(itemz)[2:].zfill(2)

    x1 = i_loc_x[:2]
    x2 = i_loc_x[2:]
    y1 = i_loc_y[:2]
    y2 = i_loc_y[2:]

    hues = hue.split(" ")

    packet_list[5] = serial_hex[0:2]
    packet_list[6] = serial_hex[2:4]
    packet_list[7] = serial_hex[4:6]
    packet_list[15] = x1
    packet_list[16] = x2
    packet_list[17] = y1
    packet_list[18] = y2
    packet_list[19] = i_loc_z
    packet_list[21] = hues[0]
    packet_list[22] = hues[1]

    byte_list = convert_packet_to_bytes(packet_list)
    PacketLogger.SendToClient(byte_list)


def makeFakeObject(ItemID, ItemHue, ItemX, ItemY, ItemZ):
    itemID = f"{ItemID:04X}"  
    itemID = itemID[:2] + " " + itemID[2:] 

    itemHue = f"{ItemHue:04X}"  
    huePart1 = itemHue[:2]  
    huePart2 = itemHue[2:]  

    createItemAtLocation(ItemX, ItemY, ItemZ, itemID, f"{huePart1} {huePart2}")

itemDataFile = r"C:\Program Files (x86)\UOForever\UO\Forever\RazorEnhanced\Scripts\HouseLogTest.csv"
uniqueSerials = []
masterItems = []

Player.HeadMessage(0,"Run to where you wanna take a copy of all items +- 18 range of you.")
for z in range(0,5):
    Player.HeadMessage(0,str(z))
    Misc.Pause(1000)  
    
Misc.Pause(1000) 
Player.HeadMessage(0,"Scanning.") 
itemFilter = Items.Filter()
itemFilter.Enabled = True
itemFilter.IsCorpse = False 
itemFilter.OnGround = True 
itemFilter.RangeMin = 0 
itemFilter.RangeMax = 18 
itemsFilterList = Items.ApplyFilter(itemFilter) 
for item in itemsFilterList:
    if item.Serial not in uniqueSerials:
        uniqueSerials.append(item.Serial)
        masterItems.append(item)
        props = "|".join(Items.GetPropStringList(item.Serial))
        #write = Misc.AppendNotDupToFile(itemDataFile, str(item.ItemID) + "|" + str(item.Name) + "|" + str(item.Hue) + "|" + str(item.IsContainer))

Player.HeadMessage(0,"Done Scanning.")
Player.HeadMessage(0,"You have 5 seconds to move 15 spaces to the left where it will be recreated.")
Misc.Pause(5000)

Player.HeadMessage(0,"Recreating")
for item in masterItems:
    print("Attempting to make item with the fullowing inputs:")
    print(item.ItemID, item.Hue, item.Position.X-15, item.Position.Y, item.Position.Z)
    makeFakeObject(item.ItemID, item.Hue, item.Position.X-15, item.Position.Y, item.Position.Z)