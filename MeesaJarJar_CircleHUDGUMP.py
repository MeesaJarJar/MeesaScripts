# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! ------------#
# -------------------------------------------------------------#
# Description: A Circle HUD that is meant to be displayed
# around the player that shows the players health, poison status
# and includes a simple counter for selected inventory items
# Simply start the script, select items you want displayed, and
# hit ESC to stop selecting. You will have to adjust the X and Y
# in the CONFIG to center it on your player.
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#
gumpX = 1325
gumpY = 720
# END CONFIG --------------------------------------------------#

from System.Collections.Generic import List
from System import String
from System import Int32 as int
from System.Threading import Thread, ThreadStart
import os
import math
gumpNumber = 426526 

def draw_circle(radius):
    points = set()
    x = radius
    y = 0
    err = 0

    while x >= y:
        points.add((x, y))
        points.add((y, x))
        points.add((-y, x))
        points.add((-x, y))
        points.add((-x, -y))
        points.add((-y, -x))
        points.add((y, -x))
        points.add((x, -y))

        if err <= 0:
            y += 1
            err += 2*y + 1
        if err > 0:
            x -= 1
            err -= 2*x + 1

    return points
    
def draw_half_circle(radius, center_x, center_y, hue):
    points = set()
    x = radius
    y = 0
    err = 0

    while x >= 0: 
        points.add((center_x - x, center_y + y))  
        points.add((center_x - y, center_y + x))
        points.add((center_x + y, center_y + x))
        points.add((center_x + x, center_y + y))

        if err <= 0:
            y += 1
            err += 2*y + 1
        if err > 0:
            x -= 1
            err -= 2*x + 1

    half_circle_points = [(point, hue) for point in points]

    return half_circle_points


def calculate_hue(player_hits, player_hits_max):

    percentage_missing = (player_hits_max - player_hits) / player_hits_max

    hue_green = 371
    hue_red = 331

    hue = int(hue_green + (hue_red - hue_green) * percentage_missing)
    
    return hue

    
hue = 0
switch = True
def updateGump(): 
    global hue, switch
    gd = Gumps.CreateGump(True,True,True,False) 

    radius = 100
    center_x = 0  
    center_y = -40  

    # Drawing the main circle
    for t in range(75,80): 
        circle_points = draw_circle(t)
        hue = calculate_hue(Player.Hits,Player.HitsMax)
        if switch:
            switch = False
        else:
            switch = True
            
        for point in circle_points:
            Gumps.AddImage(gd, int(point[0] + center_x), int(point[1] + center_y), 6001, hue)

    itemsToTrack = itemTypesToTrack

    angle_start = 45  
    angle_end = 180    
    angle_step = (angle_end - angle_start) / (len(itemsToTrack) - 1)

    item_angles = [angle_start + i * angle_step for i in range(len(itemsToTrack))]

    for i, trackable in enumerate(itemsToTrack):
        angle_rad = math.radians(item_angles[i])
        item_x = center_x + radius * math.cos(angle_rad)  
        item_y = center_y + radius * math.sin(angle_rad)  

        countTrackable = Items.BackpackCount(trackable, 0x0000)
        Gumps.AddLabel(gd, int(item_x), int(item_y), 1152, str(countTrackable)) 
        Gumps.AddImage(gd, int(item_x), int(item_y - 20), 11400 if countTrackable > 5 else 11410)  
        Gumps.AddItem(gd, int(item_x - 10), int(item_y - 38), trackable, 0x0000)  

    Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)
    CUO.MoveGump(gumpNumber, gumpX-50, gumpY-50)


        
itemTypesToTrack =  []   
itemToTrackSerial = 0
itemToTrack = None

while itemToTrackSerial != -1:
    Player.HeadMessage(1150,"Select Items to Track on Yousa Circle HUD! (Press ESC when finished!)")
    itemToTrackSerial = Target.PromptTarget('Select Items to Track on Yousa Circle HUD!(Press ESC when finished!)',1150)

    itemToTrack = Items.FindBySerial(itemToTrackSerial)
    if itemToTrack!= None:
        itemTypesToTrack.append(itemToTrack.ItemID)

    if itemToTrack == None:
        
        break
    
updateGump()

while Player.Connected == True: 
    try:
        Misc.Pause(250)
        tar = Target.GetLastAttack()
        if tar:
            mob = Mobiles.FindBySerial(tar)
            if mob:
                if mob.Deleted == False:
                
                    CUO.OpenMobileHealthBar(tar,gumpX,gumpY + 150,0)
                else:
                    CUO.CloseMobileHealthBar(tar)
            else:
                CUO.CloseMobileHealthBar(tar)    
        Misc.Pause(100)    
        updateGump()
    except:
        print("General Error - Unknown Cause!")
        Misc.Pause(100)