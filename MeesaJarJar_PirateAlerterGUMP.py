# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description: Pirate Alerter - Checks the map at a location.
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#

# USER CONFIG - Set the X and Y to be the location of where your Horizons Map
# appears on your 'ScanHorizon.png' image. 

mapX = 25
mapY = 910

# Optional Config - You can change the gump numbers and text colors if you desire.
gumpNumber = 6456262
alertGumpNumber = 64684864

# END CONFIG --------------------------------------------------#
import os
import clr

from System.Collections.Generic import List
from System import Byte, String
from System import Int32 as int
from System.Threading import Thread, ThreadStart

clr.AddReference("System.Drawing")
clr.AddReference("System.Windows.Forms")

from System.Drawing import Bitmap, Graphics, Imaging, Color
from System.Windows.Forms import Screen

RED = 32
GREEN = 68
WHITE = 1152
YELLOW = 2179

lightStatus = 'green'
scanning = True
redAlert = False
switchOn = False


def capture_specific_area(x, y, width, height):
    screenshot = Bitmap(width, height)
    screenGraphics = Graphics.FromImage(screenshot)
    screenGraphics.CopyFromScreen(x, y, 0, 0, Bitmap(width, height).Size)
    screenshot.Save("ScanHorizon.png", Imaging.ImageFormat.Png)
    return screenshot

def is_specific_red_present(image):
    target_color = Color.FromArgb(255, 222, 8, 0) 
    for x in range(image.Width):
        for y in range(image.Height):
            pixel = image.GetPixel(x, y)
            if pixel == target_color:
                return True
    return False

def updateAlertGump():
    global lightStatus, redAlert, switchOn, WHITE   
    gd = Gumps.CreateGump(True,False,False,False)
    Gumps.AddPage(gd, 0) 
    if scanning:
        if redAlert:
            if switchOn:
                Gumps.AddImage(gd,55,220,9804)
                switchOn = False
            else:
                
                Gumps.AddImage(gd,35,225,10840)
                Gumps.AddLabel(gd,35,230,WHITE,"*PIRATE ALERT*")
                switchOn = True
                
            Gumps.AddImage(gd,0,0,49)
            Gumps.AddImage(gd,42,54,601)
        else:
            Gumps.AddImage(gd,35,210,10820) 

    Gumps.SendGump(alertGumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)
    
def updateGump():
    global lightStatus, redAlert
    gd = Gumps.CreateGump(True,True,False,False)
    Gumps.AddPage(gd, 0)

    Gumps.AddImage(gd,0,0,52)
    Gumps.AddLabel(gd, 45, 10, 1152, 'Meesa Jar Jar`s')
    Gumps.AddLabel(gd, 40, 38, 1152, 'Pirate Alerter')

    Gumps.AddImageTiled(gd,5,55,175,38,5151)
    
    Gumps.AddImageTiled(gd,5,75,175,38,5157)
    
    if scanning == True:
            Gumps.AddLabel(gd, 80, 78, 2057, "STOP")
            Gumps.AddButton(gd, 40, 76, 4005, 4006, 4, 1, 0)  
    
    else:
            Gumps.AddLabel(gd, 80, 78, 2057, "START")
            Gumps.AddButton(gd, 40, 76, 4005, 4006, 3, 1, 0)  
            
    if lightStatus == 'red':
        Gumps.AddImage(gd,10,72,10850)
   
    elif lightStatus == 'green':
        Gumps.AddImage(gd,10,72,10830)
   
    elif lightStatus == 'none':
        Gumps.AddImage(gd,10,72,10810)

    Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)

Journal.Clear()
updateGump()

while True:
    Misc.Pause(1000)
    updateAlertGump()
    if scanning:
        
        if (Timer.Check('cantScan') == False):
            Player.ChatSay("Scan the Horizons")
            Misc.Pause(250)
            captured_image = capture_specific_area(mapX, mapY, 375, 375)
            if is_specific_red_present(captured_image):
                redAlert = True
                updateAlertGump()
                
            Timer.Create('cantScan',12000)

    gd = Gumps.GetGumpData(gumpNumber)

    if gd:

        if gd.buttonid == 0:
            gd.buttonid = -1
            Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)
            updateGump()
            
        if gd.buttonid == 3: # START
            gd.buttonid = -1
            scanning = True
            lightStatus = 'green'
            updateGump() 
            
            
        if gd.buttonid == 4: # STOP
            gd.buttonid = -1
            scanning = False
            lightStatus = 'red'
            updateGump()      
    

