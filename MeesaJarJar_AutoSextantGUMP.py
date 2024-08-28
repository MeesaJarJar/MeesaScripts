# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description: X/Y Location and Sextant Coordinate GUMP
# Displays the location of the player in both X/Y and Sextant Coordinates
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#


# END CONFIG --------------------------------------------------#

from System.Collections.Generic import List
from System import String
from System import Int32 as int

posns = "N"
posew = "E"
gumpNumber = 25416

def sextantToCoords(degNS, minNS, dirNS, degWE, minWE, dirWE):
    degNS = int(degNS)
    minNS = int(minNS)
    degWE = int(degWE)
    minWE = int(minWE)

    off_x = 1319
    off_y = 1621

    max_x = 5120
    max_y = 4096

    tile_deg_x = max_x / 360.0
    tile_deg_y = max_y / 360.0

    tile_min_x = tile_deg_x / 60.0
    tile_min_y = tile_deg_y / 60.0

    # Calculate world coordinates
    x = (degWE * tile_deg_x) + (minWE * tile_min_x)
    y = (degNS * tile_deg_y) + (minNS * tile_min_y)

    # Adjust for direction
    x = off_x + (x if dirWE == 'E' else -x)
    y = off_y + (y if dirNS == 'S' else -y)

    # Handle wrap-around logic
    x = x % max_x
    y = y % max_y

    # Round coordinates to nearest integer
    x = int(round(x))
    y = int(round(y))

    return (x, y)


def coordinatesToSextant(x, y):
    off_x = 1323
    off_y = 1624
    
    max_x = 5120 
    max_y = 4096 
    
    # correct for "round world"
    x = x % max_x 
    y = y % max_y 
    
    if x < off_x:
        dirWE = 'W'
        x = off_x - x
    else:
        dirWE = 'E'
        x = x - off_x
    
    if y < off_y:
        dirNS = 'N'
        y = off_y - y
    else:
        dirNS = 'S'
        y = y - off_y
        
    tile_deg_x = max(max_x // 360, 1)  # Ensure no zero division
    tile_deg_y = max(max_y // 360, 1)  # Ensure no zero division

    tile_min_x = max(tile_deg_x // 60, 1)  # Also protect against zero here
    tile_min_y = max(tile_deg_y // 60, 1)  # Also protect against zero here

    degWE = x // tile_deg_x
    minWE = (x % tile_deg_x) // tile_min_x

    degNS = y // tile_deg_y
    minNS = (y % tile_deg_y) // tile_min_y
    
    return degNS, minNS, dirNS, degWE, minWE, dirWE



def updateGump():
    playerX = Player.Position.X
    playerY = Player.Position.Y
    
    degNS, minNS, dirNS, degWE, minWE, dirWE = coordinatesToSextant(playerX, playerY)
    sextant = [ degNS, minNS, dirNS, degWE, minWE, dirWE ]
    recorded = sextantToCoords(degNS, minNS, dirNS, degWE, minWE, dirWE)
    
    gd = Gumps.CreateGump(True, True, False, False)
    Gumps.AddPage(gd, 0)
    
   
    Gumps.AddBackground(gd,0,0,150,105,5150)
    
    Gumps.AddImage(gd,-10,0,52)
    Gumps.AddHtml(gd,35,4,150,45,"<i>Auto Sextant</i>",False,False)
    Gumps.AddLabel(gd, 38, 30, 1152, "{} ° {} ' {}".format(sextant[0], sextant[1], sextant[2]))
    Gumps.AddLabel(gd, 38, 45, 1152, "{} ° {} ' {}".format(sextant[3], sextant[4], sextant[5]))

    
    Gumps.AddLabel(gd,38,60,1152,str(recorded))
    Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)

while True:
    Misc.Pause(250)  
    updateGump()