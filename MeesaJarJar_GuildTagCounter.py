# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description: This script counts the bank sitters around you
# and gives you a count for each guild tag. Also displays the tag
# above the players briefly.
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#
updateDelay = 10000 # Time, in MS, between the gump updating
# and the count re-calculating and displaying the tags. 10000 
# means 10 seconds.
# END CONFIG --------------------------------------------------#

import re
from System.Collections.Generic import List
from System import Int32 as int
from System import Byte
import random

sorted_guild_counts = {}
guild_hues = {}  
gumpNumber = 164493

def processBankSitters():
    global sorted_guild_counts, guild_hues
    mobileFilter = Mobiles.Filter()
    mobileFilter.Enabled = True
    mobileFilter.RangeMin = -1
    mobileFilter.RangeMax = 50
    mobileFilter.CheckLineOfSight = False
    mobileFilter.IsGhost = False  
    mobileFilter.Notorieties = List[Byte](bytes([1,2,3,4,5,6])) 

    foundMobiles = Mobiles.ApplyFilter(mobileFilter)

    guild_counts = {}

    for mobile in foundMobiles:
        if 'skeletal' not in str(mobile.Name).lower() and 'skeleton' not in str(mobile.Name).lower():
            guildTag = getGuildTagFromMobile(mobile)
            if guildTag:
                if 'No guild tag found.' not in guildTag:
                    if guildTag in guild_counts:
                        guild_counts[guildTag] += 1
                    else:
                        guild_counts[guildTag] = 1
                        guild_hues[guildTag] = random.randint(0, 4000)

                    hue = guild_hues[guildTag]
                    Mobiles.Message(mobile, hue, guildTag, 1000)
                else:
                    print("No guild tag found.")

    sorted_guild_counts = sorted(guild_counts.items(), key=lambda item: item[1], reverse=True)
        
def getGuildTagFromMobile(mobile):
    try:
        properties_string = str(mobile.Properties[0])
        tags = re.findall(r'\[([^\]]+)\]', properties_string)
        if tags:
            return tags[-1]
        else:
            return None
    except (AttributeError, IndexError) as e:
        print(f"Error extracting guild tag: {e}")
        return None

def updateGump():
    gd = Gumps.CreateGump(True,True,False,False)  
    Gumps.AddBackground(gd,-15,20,25,265,420)

    text = "Yousa Bank Sittin Counter"
    x_position = -10  
    y_position = 20  
    y_offset = 10   

    for index, letter in enumerate(text):
        Gumps.AddLabel(gd, x_position, y_position + (index * y_offset), 1152, str(letter))

    counter = 0
    rowHeight = 15
    total = len(sorted_guild_counts)

    for guild, count in sorted_guild_counts:
        Gumps.AddBackground(gd,0,counter * rowHeight + 30, 75, rowHeight+6, 450)

        hue = guild_hues[guild]
        
        Gumps.AddLabel(gd,10,counter * rowHeight+30,hue,f"{guild}:")
        Gumps.AddLabel(gd,50,counter * rowHeight+30,hue,f"{count}")
        counter += 1
    
    Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)

processBankSitters()    
Gumps.SendAction(gumpNumber,0)
updateGump()

while True:
    Misc.Pause(10000)# 
    
    gd = Gumps.GetGumpData(gumpNumber)

    if gd:
        if gd.buttonid == -1:
            processBankSitters()
            updateGump()
        if gd.buttonid == 0:
            gd.buttonid = -1
            
        if gd.buttonid != -1:
            print("Pressed Button: ",gd.buttonid)
             

          
                
        
