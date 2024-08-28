# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description: This script takes X and Y locations, along with
# type of ore, and creates a fake object in-game at that location
# that depicts the type of ore available at that node. 
# Set your filename to a .csv file that has ore locations listed
# in the following format: 1359,1996,0,bronze,bronze,green,0
#                            X , Y  ,0, type , type ,green,0
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#
filename = "C:/Program Files (x86)/UOForever/UO/Forever/Data/Client/BACKUP/ore_locations_markers.csv"
# END CONFIG --------------------------------------------------#

import random
import csv

def convert_packet_to_bytes(packet):
    byte_list = [int(value, 16) for value in packet]
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

packet = "F3 00 01 00 48 FC BB 12 19 B9 00 00 01 00 01 05 88 06 88 0A 00 04 15 20 00 00"  
packet_list = packet.split(" ")  


mapping = {
    "dull": "04 15",
    "agapite": "09 7e",
    "valorite": "05 44",
    "copper": "04 5f",
    "verite": "07 d2",
    "shadow": "04 55",
    "golden": "06 b7",
    "bronze": "06 d8",
    "iron": "00 00"
}
while True:
    Misc.Pause(1500)  
    with open(filename, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            fourth_column = row[3]
            if fourth_column in mapping:
                hue = mapping[fourth_column]
                X = int(row[0])
                Y = int(row[1])
                Z = int(int(row[2]) + 5)
                
                if Player.Position.X - 20 <= X <= Player.Position.X + 20:
                    if Player.Position.Y - 20 <= Y <= Player.Position.Y + 20:
                        packet = createItemAtLocation(X,Y,(Player.Position.Z +2),packet_list,hue)
                        Misc.Pause(10)