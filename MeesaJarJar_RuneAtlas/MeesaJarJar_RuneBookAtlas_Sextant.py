from System.Collections.Generic import List
from System import String
from heapq import heappop, heappush

import math
import random
import csv

gumpNumber = 161461
sextant = [0, 0, 'N', 0, 0, 'E']

coords = [0, 0]
LordBritishThrone = [1624, 1323]
WorldSize = [4096, 5120]
TilesPerDegree = [WorldSize[0] / 360.0, WorldSize[1] / 360.0]

def getMIBCoords():
    Player.HeadMessage(0, "Select MIB to Extract Coordinates From:")
    mibSerial = Target.PromptTarget("Select MIB", 0)
    mib = Items.FindBySerial(mibSerial)
    x = 0
    y = 0
    if mib:
        if mib.ItemID == 0x14EC:
            itemType = 'TMAP'
        else:
            itemType = 'MIB'

        Items.WaitForProps(mib, 5000)
        props = str(mib.Properties)

        while 'Location' not in props:
            Misc.Pause(250)
            Items.UseItem(mib)
            Items.WaitForProps(mib, 5000)
            props = str(mib.Properties)

        start_index = props.find('Location: (') + len('Location: (')
        end_index = props.find(')', start_index)

        if start_index > 0 and end_index > start_index:
            coordinates = props[start_index:end_index]
            coordinates = coordinates.replace(" ", "")  # Remove any spaces if present
            x_str, y_str = coordinates.split(',')

            x = int(x_str)
            y = int(y_str)

            Misc.SetSharedValue('Atlas_Go_MIBX', x)
            Misc.SetSharedValue('Atlas_Go_MIBY', y)
            return x, y
        else:
            print("ERROR: Could not find coordinates in the properties.")

        if itemType != 'TMAP':
            Items.UseItem(mib)
            Gumps.WaitForGump(1426736667, 3000)
            gumpLines = Gumps.GetLineList(1426736667)
            partOne, partTwo = gumpLines[0].split(',')
            deg1, sec1, dir1 = splitToPieces(partOne)
            deg2, sec2, dir2 = splitToPieces(partTwo)
            Gumps.CloseGump(0)
            y = convertDegreesToDecimal(deg1, sec1, dir1)
            x = convertDegreesToDecimal(deg2, sec2, dir2)
            Misc.SetSharedValue('Atlas_Go_MIBX', x)
            Misc.SetSharedValue('Atlas_Go_MIBY', y)
        else:
            print("ERROR DOING TMAP EXTRACT")
        return x, y
    else:
        print("FAILED!")
        x = 0
        y = 0
    return x, y

def convert_packet_to_bytes(packet):
    byte_list = []
    for value in packet:
        try:
            # Ensure that each value is a string before converting it to an integer
            byte_list.append(int(str(value), 16))
        except ValueError:
            print("Invalid hexadecimal value in packet:", value)
            print("Original packet:", packet)
            return None
    return byte_list



def createItemAtLocation(itemx, itemy, itemz, packet_list, hue):
    randidint = random.randrange(0, 10000000)

    i_loc_x = hex(itemx)
    i_loc_y = hex(itemy)
    i_loc_z = hex(itemz)

    if len(i_loc_x) < 6:
        i_loc_x = i_loc_x.replace("0x", "0x0")
    if len(i_loc_y) < 6:
        i_loc_y = i_loc_y.replace("0x", "0x0")
    if len(i_loc_z) < 6:
        i_loc_z = i_loc_z.replace("0x", "0x0")

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
    #packet_list[21] = int(hues[0], 16)
    #packet_list[22] = int(hues[1], 16)
    packet_list[21] = int(str(hues[0]), 16)
    packet_list[22] = int(str(hues[1]), 16)



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
    #("DEBUG XYZ:", X, Y, Z)
    #print("DEBUG packet_list:", packet_list)
    packet = createItemAtLocation(X, Y, Z, packet_list, hue)
    
def splitToPieces(location):
    degree, secTemp = location.split('\xb0')
    seconds, direction = secTemp.split('\x27')
    return int(degree), int(seconds), direction

def convertDegreesToDecimal(degree, seconds, direction):
    result = 0
    if direction.lower() == 'w':
        result = (LordBritishThrone[1] - (seconds / 60.0) * TilesPerDegree[1] - degree * TilesPerDegree[1]) % WorldSize[1]
    elif direction.lower() == 'e':
        result = (LordBritishThrone[1] + (seconds / 60.0) * TilesPerDegree[1] + degree * TilesPerDegree[1]) % WorldSize[1]
    elif direction.lower() == 'n':
        result = (LordBritishThrone[0] - (seconds / 60.0) * TilesPerDegree[0] - degree * TilesPerDegree[0]) % WorldSize[0]
    elif direction.lower() == 's':
        result = (LordBritishThrone[0] + (seconds / 60.0) * TilesPerDegree[0] + degree * TilesPerDegree[0]) % WorldSize[0]
    return int(result) + 1

def convertDecimalToDegrees(decimal, axis):
    degrees = 0
    minutes = 0
    direction = ''

    if axis.lower() == 'latitude':
        if decimal >= LordBritishThrone[0]:
            direction = 's'
            offset = decimal - LordBritishThrone[0]
        else:
            direction = 'n'
            offset = LordBritishThrone[0] - decimal

        degrees = int(offset // TilesPerDegree[0])
        minutes = int((offset % TilesPerDegree[0]) * 60.0 / TilesPerDegree[0])

    elif axis.lower() == 'longitude':
        if decimal >= LordBritishThrone[1]:
            direction = 'e'
            offset = decimal - LordBritishThrone[1]
        else:
            direction = 'w'
            offset = LordBritishThrone[1] - decimal

        degrees = int(offset // TilesPerDegree[1])
        minutes = int((offset % TilesPerDegree[1]) * 60.0 / TilesPerDegree[1])

    return degrees, minutes, direction

def distance_between_points(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def updateGump():
    gd = Gumps.CreateGump(True, True, False, False)
    Gumps.AddPage(gd, 0)

    Gumps.AddImage(gd, 48, 0, 5536)

    Gumps.AddBackground(gd, 20, 25, 150, 25, 5120)
    Gumps.AddBackground(gd, 20, 50, 150, 25, 5120)
    Gumps.AddBackground(gd, 20, 110, 142, 25, 5120)
    Gumps.AddBackground(gd, 150, 25, 50, 25, 440)
    Gumps.AddBackground(gd, 150, 50, 50, 25, 440)

    Gumps.AddLabel(gd, 35, 10, 1152, "Degrees")
    Gumps.AddLabel(gd, 100, 10, 1152, "Minutes")
    Gumps.AddImage(gd, 30, 25, 2443)
    Gumps.AddTextEntry(gd, 50, 28, 50, 23, 1153, 8855, str(sextant[0]))
    Gumps.AddImage(gd, 30 + 63, 25, 2443)
    Gumps.AddTextEntry(gd, 50 + 63, 28, 50, 23, 1153, 8856, str(sextant[1]))
    Gumps.AddLabel(gd, 163, 25, 1152, str(sextant[2]).upper())
    Gumps.AddButton(gd, 180, 25, 254, 254, 1, 1, 0)
    Gumps.AddTooltip(gd, 1061114, "Change North / South")

    Gumps.AddImage(gd, 30, 50, 2443)
    Gumps.AddTextEntry(gd, 50, 28 + 25, 50, 23, 1153, 8857, str(sextant[3]))
    Gumps.AddImage(gd, 30 + 63, 50, 2443)
    Gumps.AddTextEntry(gd, 50 + 63, 28 + 25, 50, 23, 1153, 8858, str(sextant[4]))
    Gumps.AddLabel(gd, 163, 52, 1152, str(sextant[5]).upper())

    Gumps.AddButton(gd, 180, 50, 254, 254, 2, 1, 0)
    Gumps.AddTooltip(gd, 1061114, "Change East / West")
    Gumps.AddButton(gd, 40, 75, 1687, 1688, 4, 1, 0)
    Gumps.AddTooltip(gd, 1061114, "Convert X Y Coords to Sextant.")
    Gumps.AddButton(gd, 108, 75, 1689, 1690, 5, 1, 0)

    Gumps.AddTooltip(gd, 1061114, "Convert Sextant Coords to X Y.")
    Gumps.AddButton(gd, 74, 67, 1691, 1692, 3, 1, 0)
    Gumps.AddTooltip(gd, 1061114, "Set to Player`s Position.")

    Gumps.AddButton(gd, 150, 75, 2002, 2001, 6, 1, 0)
    Gumps.AddTooltip(gd, 1061114, "Read from MIB")

    Gumps.AddBackground(gd, 45, 87, 25, 25, 9400)
    Gumps.AddBackground(gd, 112, 87, 25, 25, 9400)

    Gumps.AddLabel(gd, 52, 92, 1152, "X")
    Gumps.AddLabel(gd, 119, 92, 1152, "Y")

    Gumps.AddImage(gd, 30, 110, 2443)
    Gumps.AddImage(gd, 90, 110, 2443)

    Gumps.AddTextEntry(gd, 43, 113, 50, 23, 570, 8859, str(coords[0]))
    Gumps.AddTextEntry(gd, 108, 113, 50, 23, 570, 8860, str(coords[1]))

    Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)

Misc.Pause(700)
coords = [Player.Position.X, Player.Position.Y]
x_decimal = int(coords[0])
y_decimal = int(coords[1])

latitude_degrees, latitude_minutes, latitude_direction = convertDecimalToDegrees(coords[0], 'latitude')
longitude_degrees, longitude_minutes, longitude_direction = convertDecimalToDegrees(coords[1], 'longitude')

sextant = [latitude_degrees, latitude_minutes, latitude_direction, longitude_degrees, longitude_minutes, longitude_direction]

updateGump()
while True:
    Misc.Pause(100)
    locationX = int(Misc.ReadSharedValue('Atlas_Go_MIBX'))
    locationY = int(Misc.ReadSharedValue('Atlas_Go_MIBY'))
    #print("DEBUG locationX:", locationX)
    #print("DEBUG locationY:", locationY)
    if distance_between_points(locationX, locationY, Player.Position.X, Player.Position.Y) < 16:
        drawFakeItemAtSpot(locationX + 3, locationY)

    gd = Gumps.GetGumpData(gumpNumber)

    if gd:
        if gd.buttonid == 0:
            gd.buttonid = -1
            break

        if gd.buttonid == 1:
            if sextant[2] == 'n':
                sextant[2] = 's'
            else:
                sextant[2] = 'n'

            gd.buttonid = -1
            updateGump()

        if gd.buttonid == 2:
            if sextant[5] == 'e':
                sextant[5] = 'w'
            else:
                sextant[5] = 'e'

            gd.buttonid = -1
            updateGump()

        if gd.buttonid == 3:
            gd.buttonid = -1
            coords = [Player.Position.X, Player.Position.Y]
            latitude_degrees, latitude_minutes, latitude_direction = convertDecimalToDegrees(coords[0], 'latitude')
            longitude_degrees, longitude_minutes, longitude_direction = convertDecimalToDegrees(coords[1], 'longitude')

            sextant = [latitude_degrees, latitude_minutes, latitude_direction, longitude_degrees, longitude_minutes, longitude_direction]
            updateGump()

        if gd.buttonid == 4:
            gd.buttonid = -1

            coords[0] = int(Gumps.GetTextByID(gd, 8859))
            coords[1] = int(Gumps.GetTextByID(gd, 8860))

            latitude_degrees, latitude_minutes, latitude_direction = convertDecimalToDegrees(coords[0], 'latitude')
            longitude_degrees, longitude_minutes, longitude_direction = convertDecimalToDegrees(coords[1], 'longitude')

            sextant = [latitude_degrees, latitude_minutes, latitude_direction, longitude_degrees, longitude_minutes, longitude_direction]
            updateGump()

        if gd.buttonid == 5:
            gd.buttonid = -1

            degNS = int(Gumps.GetTextByID(gd, 8855))
            minNS = int(Gumps.GetTextByID(gd, 8856))
            degWE = int(Gumps.GetTextByID(gd, 8857))
            minWE = int(Gumps.GetTextByID(gd, 8858))

            sextant = [degNS, minNS, sextant[2], degWE, minWE, sextant[5]]

            x = convertDegreesToDecimal(sextant[0], sextant[1], sextant[2])
            y = convertDegreesToDecimal(sextant[3], sextant[4], sextant[5])
            coords = [x, y]

            updateGump()

        if gd.buttonid == 6:
            x, y = getMIBCoords()
            coords = [x, y]

            latitude_degrees, latitude_minutes, latitude_direction = convertDecimalToDegrees(int(coords[0]), 'latitude')
            longitude_degrees, longitude_minutes, longitude_direction = convertDecimalToDegrees(int(coords[1]), 'longitude')

            sextant = [latitude_degrees, latitude_minutes, latitude_direction, longitude_degrees, longitude_minutes, longitude_direction]

            gd.buttonid = -1
            updateGump()
