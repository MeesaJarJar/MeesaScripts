# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description: Simple stealing script that targets high value
# items such as fragments, relics. Demonstration Script
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#


# END CONFIG --------------------------------------------------#

from System.Collections.Generic import List
from System import Int32 as int
from System import Byte
running = True

Misc.Pause(1000)
Player.UseSkill("Stealing")

while running == True:
    if Target.HasTarget() == False:
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
    mobileFilter.Notorieties = List[Byte](bytes([1])) 

    foundMobiles = Mobiles.ApplyFilter(mobileFilter)

    targetMobile = Mobiles.Select(foundMobiles,"Nearest")

    if targetMobile and targetMobile.Backpack:
        
            Items.OpenAt(targetMobile.Backpack, 100, 100)
        
            for item in targetMobile.Backpack.Contains:
                
                if 'relic' in item.Name.lower() or 'scroll of' in item.Name.lower() or  'fragment' in item.Name.lower() or  'portal focus' in item.Name.lower() or  'animal taming' in item.Name.lower():
                    if 'forbidden' not in item.Name.lower():
                        Player.HeadMessage(62,"FOUND: " + str(item.Name))
                        Player.HeadMessage(65,"STEALING NOW!")
                        
                        Target.TargetExecute(item)
                        running = False