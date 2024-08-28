# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description: Runebook Filler - Fills your runebook library
# runebooks with recall scrolls so that people can use it without
# having to have reagents! 
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#


# END CONFIG --------------------------------------------------#

from System.Collections.Generic import List
from System import String
from System import Int32 as int
from System.Threading import Thread, ThreadStart
from System import Environment
import clr
clr.AddReference('System.Drawing')
from System.Drawing.Imaging import *

def parse_charges(input_string):
    # Splitting the string by colon
    parts = input_string.split(':')

    # Further splitting the second part by slash
    charges = parts[1].strip().split('/')

    # Converting the current number of charges to integer
    current_charges = int(charges[0])
    max_charges = charges[1]
    return current_charges, max_charges

itemFilter = Items.Filter()
itemFilter.OnGround = True 
itemFilter.RangeMin = 0 
itemFilter.RangeMax = 12 
itemFilter.CheckIgnoreObject = True
itemFilter.Graphics = List[int]([0x22C5])

itemList = Items.ApplyFilter(itemFilter)

for item in itemList:
    if item.Position.Z >= Player.Position.Z:
        for prop in item.Properties:
            if 'Charges' in str(prop):
            
                charges,maxCharges = parse_charges(str(prop))
                if int(charges) < int(maxCharges):
                    print(item.Name)
                    print(charges,maxCharges,"Player Going to:", item.Position.X,item.Position.Y, Player.Position.Z)
                    Items.Message(item,0,item.Name)
                    Player.PathFindTo(item.Position.X,item.Position.Y,item.Position.Z)
                    
                    while Player.DistanceTo(item) > 1:
                        Misc.Pause(250);
                    
                    recalls = Items.FindByID(0x1F4C,0x0000,Player.Backpack.Serial,1,False)
                    if recalls:
                        print("Found Recalls.")
                        
                        Misc.Pause(100)
                        print("Moving Recalls");
                        Items.Move(recalls,item,-1)
                        Misc.Pause(100);
                    else:
                        print("**********NO RECALLS - *** FAILURE");