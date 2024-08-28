# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description: Fake Item Creation Script - Demonstration that
# Draws objects in-game in the client that only show to user. 
# These objects disappear as soon as you leave range of sight.
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#

drawItemID = '07 BA' 

# END CONFIG --------------------------------------------------#

import random

def convert_packet_to_bytes(packet):
    byte_list = [int(value, 16) for value in packet]
    return byte_list

def createItemAtLocation(itemx,itemy,itemz,itemToDraw,hue):
  
    packet = "F3 00 01 00 48 FC BB 12 " + itemToDraw + " 00 00 01 00 01 05 88 06 88 0A 00 04 15 20 00 00"  
    packet_list = packet.split(" ")  

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


hueMapping = { # Hue Map

    "default": "00 00"
}

X = Player.Position.X
Y = Player.Position.Y - 5 #Draw 5 tiles North of Player
Z = Player.Position.Z

hue = hueMapping['default']

path = PathFinding.GetPath(Player.Position.X+5,Player.Position.Y,True)
print(path)
for point in path:
    print(point.X, point.Y)
    createItemAtLocation(point.X,point.Y,Player.Position.Z ,drawItemID,hue)
    Misc.Pause(100)
