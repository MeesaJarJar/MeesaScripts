# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description: WORK IN PROGRESS - 
# I dont remember making this, and i dont know what it does.
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#


# END CONFIG --------------------------------------------------#
import threading
import time
from System.Collections.Generic import List
from System import Int32 as int
from System import Byte

gumpNumber = 542461 
myTarget = None
def updateGump(): 

    gd = Gumps.CreateGump(True,True,False,False) 
    Gumps.AddPage(gd,1)

  
    Gumps.AddImage(gd,20,-20,337)
    
    Gumps.AddBackground(gd,0,0,200,105,420)
    
    Gumps.AddImage(gd,40,-50,9808)
    Gumps.AddLabel(gd,45,-45,1152,"Meesa")
    
    Gumps.AddLabel(gd,45,-30,1800,"Target")
    Gumps.AddLabel(gd,45,-20,1800,"Thingy")
    Gumps.AddLabel(gd,-35,15,1152,"Target:")
    Gumps.AddButton(gd,15,15,1535,1536,96,1,0)
    
    
    Gumps.AddLabel(gd,45,16,1152,str(myTarget))

    
   
    Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)
    
def findTargetAndMessage():
    mobileFilter = Mobiles.Filter()
    mobileFilter.Enabled = True
    mobileFilter.RangeMin = -1
    mobileFilter.RangeMax = 16
    mobileFilter.CheckLineOfSight = False
    mobileFilter.IsGhost = False  
    mobileFilter.Notorieties = List[Byte](bytes([1,2,3,4,5,6])) 


    foundMobiles = Mobiles.ApplyFilter(mobileFilter)
    if myTarget != None:
            
        for mobile in foundMobiles:
            #print("MOB:", mobile.Name)
            
            if mobile.Name == myTarget.split('|')[2]:
                    #print(mobile.Name, "IS TARGET!")
                    Mobiles.Message(mobile,33,"* IS TARGET *",100)
                    break
                
                    
updateGump()   

    
Journal.Clear()
while True:
    Misc.Pause(100)
    findTargetAndMessage()
    gd = Gumps.GetGumpData(gumpNumber)
    if gd:
        print(gd.buttonid)
        if gd.buttonid == 96:
            print("BUTTON CLICKED!")
            target = Mobiles.FindBySerial(Target.PromptTarget("Select a Target:",0))
            
            
            Player.ChatParty('|JARJAR|' + str(target.Name) + '|')
            gd.buttonid = -1
            updateGump()
            Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)
            
    
        else:
            gd.buttonid = -1
            
            
            Misc.Pause(1000)
            jarjar = None
            #jarjar = Journal.Search("|JARJAR|")
            
            
            jList = Journal.GetTextByType('Party',False)
            Journal.Clear()
            for line in jList:
                if '|JARJAR|' in str(line):
                    myTarget = str(line)
            updateGump()
            Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)
            
    
 
        