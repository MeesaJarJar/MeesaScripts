# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description: JAR JAR MAP
# Simple Clickable Map GUMP that intefaces with the Runebook Atlas
# to automatically recall or gate directly to locations all 
# across the overland map
# START CONFIG ------------------------------------------------#

# END CONFIG --------------------------------------------------#
import clr
clr.AddReference('System.Drawing')
from System.Drawing import Bitmap, Color, Graphics, Pen

import heapq  
from math import sqrt  
import math
import random
import csv
import re
from math import sqrt

def find_runebook(filename, X, Y):
    X = int(X)
    Y = int(Y)
    pattern = r'\d+'
    #print("Trying to find runebook with x y of ", X, Y)
    
    closest_distance = float('inf')
    closest_match = None
    
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        
        for row in reader:
            integers = re.findall(pattern, str(row))
            
            try:
                location_x = int(integers[-2])
                location_y = int(integers[-1])
                distance = sqrt((location_x - X) ** 2 + (location_y - Y) ** 2)
                
                if distance < closest_distance:
                    closest_distance = distance
                    closest_match = (integers[0], location_x, location_y, row[4])
            except (ValueError, IndexError):
                continue
        
    if closest_match:
        #print("FOUND CLOSEST MATCH IN THE FILE!")
        return closest_match
    
    #print("End of find_runebook, did we find it?: False")
    return None, None, None, None




def create_minimap(bmp, path, scale=0.1):
    mini_width = int(bmp.Width * scale)
    mini_height = int(bmp.Height * scale)
   
    mini_map = Bitmap(mini_width, mini_height)
    g = Graphics.FromImage(mini_map)

    for x in range(mini_width):
        for y in range(mini_height):
            original_x = int(x / scale)
            original_y = int(y / scale)
            pixel_color = bmp.GetPixel(original_x, original_y)
            mini_map.SetPixel(x, y, pixel_color)

    path_pen = Pen(Color.Red, 1)
    for i in range(len(path) - 1):
        start = (int(path[i][0] * scale), int(path[i][1] * scale))
        end = (int(path[i + 1][0] * scale), int(path[i + 1][1] * scale))
        g.DrawLine(path_pen, start[0], start[1], end[0], end[1])

    return mini_map
    
def resizeLarger(smaller_x, smaller_y):
    smaller_map_size = 383  
    larger_map_width = 5120
    larger_map_height = 4096

    larger_x = (smaller_x * larger_map_width + smaller_map_size // 2) // smaller_map_size
    larger_y = (smaller_y * larger_map_height + smaller_map_size // 2) // smaller_map_size

    return larger_x, larger_y
def resizeSmaller(larger_x, larger_y):
    smaller_map_size = 383  
    larger_map_width = 5120
    larger_map_height = 4096

    smaller_x = (larger_x * smaller_map_size + larger_map_width // 2) // larger_map_width
    smaller_y = (larger_y * smaller_map_size + larger_map_height // 2) // larger_map_height

    return smaller_x, smaller_y
def twirl():
    for z in range(0,7):
        if   Player.Direction == "North": Player.Run("East")
        elif Player.Direction == "East":  Player.Run("South")
        elif Player.Direction == "South":  Player.Run("West")
        elif Player.Direction == "West": Player.Run("North")
        
        elif Player.Direction == "North": Player.Run("Up")
        elif Player.Direction == "Up":  Player.Run("Right")
        elif Player.Direction == "Right":  Player.Run("Down")
        elif Player.Direction == "Down": Player.Run("Left")
        elif Player.Direction == "Left": Player.Run("North")
        Misc.Pause(10)
    
def updateGumpMap():
    status = 0
    
    gd = Gumps.CreateGump()
    Gumps.AddPage(gd, 0)
    gumpHeight = 383
    gumpWidth = 383
    
    smallerMapWidth = 383
    smallerMapHeight = 383
    
    Gumps.AddBackground(gd, -5, -5, 390, 390, 420) 
    Gumps.AddImage(gd,0,0,5593)
    Gumps.AddImage(gd,370,150,1262)
    Gumps.AddImage(gd,380,0,1227)
    
    relativeX, relativeY = resizeSmaller(Player.Position.X, Player.Position.Y)
    relativeCX, relativeCY = resizeSmaller(clickLocX, clickLocY)
    relativeRX, relativeRY = resizeSmaller(lastRecallLocX, lastRecallLocY)
    count = 1
   
    identifier = 0

    for z in range(0, 383):
        for t in range(0, 383):
            if z % 8 == 0 and t % 8 == 0:
                Gumps.AddButton(gd, z, t, 0x94, 0x94, identifier, 1, 0)
                button_positions[identifier] = (z, t) 
                identifier += 1

    Gumps.AddImage(gd, relativeX, relativeY, 1209)
    Gumps.AddLabel(gd, relativeX + 20, relativeY, 924, "You")

    
    Gumps.AddImage(gd, relativeCX, relativeCY, 2361)
    Gumps.AddLabel(gd, relativeCX + 20, relativeCY, 920, "Target Clicked")

    Gumps.AddImage(gd, relativeRX, relativeRY, 9008)
    Gumps.AddLabel(gd, relativeRX + 20, relativeRY+20, 920, "Closest Location")
    
    
    Gumps.SendGump(gumpMapNumber, Player.Serial, 40, 40, gd.gumpDefinition, gd.gumpStrings)
    

locX = ''
locY = ''
gumpMapNumber = 867865
button_positions = {}  
identifier = 0 
clickLocX = 0
clickLocY = 0
lastRecallLocX = 0
lastRecallLocY = 0
updateGumpMap()
while True:
    if Timer.Check('upMap') == False:
        Timer.Create('upMap',4000)
        #print("Updating from Timer.")
        updateGumpMap()
        
    Misc.Pause(100)
    gdx = Gumps.GetGumpData(gumpMapNumber)
    
    if gdx and gdx.buttonid != -1:
        if gdx.buttonid in button_positions:
            Player.ChatSay(1151,"Go Go Jar Jar - Runebook Atlas!")
            twirl()
            # Get downscaled coordinates
            x, y = button_positions[gdx.buttonid]
            #print(f"USER CLICKED ON BUTTON AT {x}, {y}")

            # Convert the downscaled coordinates to full-scale coordinates
            full_x, full_y = resizeLarger(x, y)
            #print(f"Converted downscaled coordinates ({x}, {y}) to full-scale coordinates ({full_x}, {full_y})")
            clickLocX = full_x
            clickLocY = full_y
            # Use the full-scale coordinates for the runebook search
            mySerial, myX, myY, myName = find_runebook("MasterRunebookCoordinates.csv", full_x, full_y)
            #print("Result:", mySerial, myX, myY, myName)
            lastRecallLocX = myX
            lastRecallLocY = myY
            Misc.SetSharedValue("Atlas_Go", True)
            Misc.SetSharedValue("Atlas_Go_Serial", int(mySerial))
            Misc.SetSharedValue("Atlas_Go_Name", str(myName))
            Misc.SetSharedValue("Atlas_Go_RuneX", int(myX))
            Misc.SetSharedValue("Atlas_Go_RuneY", int(myY))
            
            gdx.buttonid = -1  
            
            start_point = (Player.Position.X, Player.Position.Y)
            end_point = (full_x, full_y)
            #print("Converted To:", end_point)

            updateGumpMap()
        else:
            print(f"Invalid button ID: {gdx.buttonid}")
