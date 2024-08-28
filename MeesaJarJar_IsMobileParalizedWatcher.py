# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description: Meesa Jar Jars Mobile Paralized Watcher
#  - Be notified when a mobile is paralized around you! 
# Displays a message above a mobiles head if it is paralyzed.
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#


# END CONFIG --------------------------------------------------#

from System.Collections.Generic import List
from System import Int32 as int
from System import Byte
import math
import random

mobileFilter = Mobiles.Filter()
mobileFilter.Enabled = True
mobileFilter.RangeMin = -1
mobileFilter.RangeMax = 16
mobileFilter.CheckLineOfSight = True
mobileFilter.IsGhost = False  
mobileFilter.Notorieties = List[Byte](bytes([1,2,3,4,5,6])) 

while True:

    Misc.Pause(500)
   
    foundMobiles = Mobiles.ApplyFilter(mobileFilter)
    
    for mobile in foundMobiles:
        if mobile.Paralized == True:
            if Timer.Check(str(mobile.Serial) + '_PARA') == False:
                Timer.Create(str(mobile.Serial) + '_PARA', 6000)
                
                print(mobile.Name, "IS PARALYZED!")
                Mobiles.Message(mobile,33,"* IS PARALYZED *",100)
            
            
            
            