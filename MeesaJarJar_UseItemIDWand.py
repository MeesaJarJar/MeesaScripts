# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! ------------#
# -------------------------------------------------------------#
# Description: Use Item ID Wand
# Unequips Left and Right hand items, selects a ItemID wand
# from the Players backpack, and uses it, prompting target cursor
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#


# END CONFIG --------------------------------------------------#

from System.Collections.Generic import List
from System import Int32 as int
from System import Byte
import math
import random
import re
import csv
import os

for item in Player.Backpack.Contains:
    if 'wand' in item.Name:
        Timer.Create("idwandsleep",4000)
        
        if Player.CheckLayer("RightHand"):
            Player.UnEquipItemByLayer("RightHand",650)
            Misc.Pause(250) 
            
        if Player.CheckLayer("LeftHand"):
            Player.UnEquipItemByLayer("LeftHand",650)
            Misc.Pause(250)
            
        Misc.Pause(250)
        Player.EquipItem(item) 
        Misc.Pause(1000)  
        Items.UseItem(item)
        break



                 
                