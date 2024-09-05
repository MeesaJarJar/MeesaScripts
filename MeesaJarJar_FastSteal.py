# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description: Simple stealing script that targets high value
# items such as fragments, relics. Demonstration Script
# This script works on a priority basis, meaning whatever is
# closest to the start of the stealableKeywords list, will be
# stolen first. 
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#

stealableKeywords = ['relic', 'portal focus', 'fragment', 'scroll of', 'epic', 'animal taming', 'rare']
reagents = ['blood moss', 'mandrake root', 'black pearl']
friendlyGuilds = ['lost', 'trin', 'pwn', 'bad', 'nsc', 'void', 's-b', 'yew', 'br', 'paws']
# END CONFIG --------------------------------------------------#

from System.Collections.Generic import List
from System import Int32 as int
from System import Byte
running = True
import re
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

Misc.Pause(1000)
Player.UseSkill("Stealing")

while running:
    Journal.Clear()
    if not Target.HasTarget():
        Player.UseSkill("Stealing")
    Misc.Pause(250)
    mobileFilter = Mobiles.Filter()
    mobileFilter.Enabled = True
    mobileFilter.RangeMin = 0
    mobileFilter.RangeMax = 1
    mobileFilter.CheckLineOfSight = False
    mobileFilter.IsGhost = False  
    mobileFilter.ZLevelMin = Player.Position.Z -10
    mobileFilter.ZLevelMax = Player.Position.Z +10
    mobileFilter.Notorieties = List[Byte](bytes([1,3,4,6])) 

    foundMobiles = Mobiles.ApplyFilter(mobileFilter)

    targetMobile = Mobiles.Select(foundMobiles, "Nearest")
    if targetMobile != None:
        targetMobileGuild = str(getGuildTagFromMobile(targetMobile)).lower()
    
    if targetMobile and targetMobile.Backpack and targetMobileGuild not in friendlyGuilds :
        
        print("Found Unfriendly Player in Guild:", targetMobileGuild)
        
        Items.OpenAt(targetMobile.Backpack, 100, 100)
        
        highestPriorityItem = None
        highestPriority = len(stealableKeywords)

        for item in targetMobile.Backpack.Contains:
            itemName = item.Name.lower()
            for priority, keyword in enumerate(stealableKeywords):
                if keyword in itemName and 'forbidden' not in itemName:
                    if priority < highestPriority:
                        highestPriorityItem = item
                        highestPriority = priority
                    break  

        if highestPriorityItem:
            Player.HeadMessage(62, "FOUND: " + str(highestPriorityItem.Name))
            Player.HeadMessage(65, "STEALING NOW!")
            Player.ChatSay(33,"MEESA STEAL YOUSA STUFF")
            Misc.Pause(100)
            Target.TargetExecute(highestPriorityItem)
            running = False
            Misc.Pause(250)
            if Journal.Search('fail to steal') == True:
                Player.HeadMessage(85, "Failed to Steal The Item")
                Player.ChatSay(33,"Woops, meesa failed to steal yo shit.")
