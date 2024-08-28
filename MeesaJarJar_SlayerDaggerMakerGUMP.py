# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description: # Slayer Dagger Maker - Load up your beetle with
# iron ingots, grab a tinker kit, use your Tinker/Blacksmith and 
# run the script, and use the ingame GUMP!
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#


# END CONFIG --------------------------------------------------#

from System.Collections.Generic import List
from System import String
from System import Int32 as int
from System.Threading import Thread, ThreadStart
import os

gumpNumber = 134515342 

dragTime = 600

tinkertool = 0x1EB8
tinkKitGump1 = 8
tinkKitGump2 = 23

bsHammer = 0x13E3
bsHammerGump1 = 8
bsHammerGump2 = 93

ironIngots = 0x1BF2

resources = [[ironIngots, 50]]

Player.HeadMessage(66,'Yousa Gotta Target da Beetle')
beetle = Target.PromptTarget()

Player.HeadMessage(66,'Yousa be targeting an item in da Beetles Backpackin')
beetleContainer = Items.FindBySerial(Target.PromptTarget())
beetleContainer = beetleContainer.RootContainer
totalSlayersCrafted = 0
totalDaggersCrafted = 0
Misc.SetSharedValue('totalSlayersCrafted',totalSlayersCrafted)
Misc.SetSharedValue('totalDaggersCrafted',totalDaggersCrafted)
                    
BSList = [

[36,16,0x0F52],#Dagger

]
slayers = ['Silver', 'Reptilian Death', 'Elemental Ban', 'Repond', 'Exorcism', 'Arachnid Doom', 'fey slayer', "Ogre Thrashing", "Orc Slaying", "Troll Slaughter", "Blood Drinking", "Earth Shatter",
                 "Elemental Health", "Flame Dousing", "Summer Wind", "Vacuum", "Water Dissipation",  
                 "Balron Damnation", "Daemon Dismissal", "Gargoyles Foe", "Scorpions Bane", "Spiders Death",
                 "Terathan", "Dragon Slaying", "Lizardman Slaughter", "Ophidian", "Snakes Bane"]
                 

def updateGump(): 
    gd = Gumps.CreateGump(True,True,False,False) 
    #Gumps.AddImage(gd,0,0,22003)
    Gumps.AddBackground(gd,0,15,120,90,420)
    Gumps.AddImage(gd,80,80,9004)
    myDaggers = Misc.ReadSharedValue('totalDaggersCrafted')
    mySlayers = Misc.ReadSharedValue('totalSlayersCrafted')
    myIngots = Misc.ReadSharedValue('totalIngotsInBeetle')
    Gumps.AddLabel(gd,10,20,1152,str("Slayers:"))
    Gumps.AddLabel(gd,10,40,1158,str("Daggers:"))
    Gumps.AddLabel(gd,10,60,64,str("Beetle Ingots:"))
    Gumps.AddLabel(gd,65,20,1152,str(mySlayers))
    Gumps.AddLabel(gd,65,40,1158,str(myDaggers))
    Gumps.AddLabel(gd,45,80,64,str(myIngots))
    Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)
    
def tinkCraft (gump1, gump2):
    Gumps.CloseGump(949095101)
    currentTink = Items.FindByID(tinkertool,0x0000,Player.Backpack.Serial)
    
    if Gumps.CurrentGump() != 949095101:
        Items.UseItem(currentTink)
    Gumps.WaitForGump(949095101, 1500)
    Gumps.SendAction(949095101, gump1)
    Gumps.WaitForGump(949095101, 1500)
    Gumps.SendAction(949095101, gump2)
    Gumps.WaitForGump(949095101, 1500)
    Misc.Pause(600)
    
def restockList(beetle,container,resources):
    worldSave()
    if Player.Mount:
        Mobiles.UseMobile(Player.Serial)
        Misc.Pause(dragTime)
        
    Misc.WaitForContext(beetle, 2000)
    Misc.ContextReply(beetle, 10)
    
    beetleIngots = Items.FindByID(ironIngots,0x0000,container,1,False)
    if beetleIngots != None:
        
        Misc.SetSharedValue('totalIngotsInBeetle',beetleIngots.Amount)
    for resource in resources:
        worldSave()
        restockResource = Items.FindByID(resource[0], -1, container)

        if Items.BackpackCount(resource[0], -1) < resource[1]:
            
            difference = resource[1] - Items.BackpackCount(resource[0], -1)
            if restockResource:
                Items.Move(restockResource, Player.Backpack, difference)
            Misc.Pause(dragTime)
            
    Mobiles.UseMobile(beetle)
    Misc.Pause(dragTime)    
    
def checkTools():
   
    while Items.BackpackCount(tinkertool, -1) < 2:
        tinkCraft (tinkKitGump1, tinkKitGump2)
        Misc.Pause(600)
        tinkCraft (tinkKitGump1, tinkKitGump2)    
        Misc.Pause(600)

    while Items.BackpackCount(bsHammer, -1) < 3:
        tinkCraft (bsHammerGump1, bsHammerGump2)
        Misc.Pause(600)
        

def BSCraft (gump1, gump2, itemType):
    global totalDaggersCrafted
    global totalSlayersCrafted
    while Player.Connected == True:
        updateGump() 
        if Items.BackpackCount(ironIngots,-1) < 10:
            restockList(beetle,beetleContainer,resources)
            if Items.BackpackCount(ironIngots,-1) < 10:
                print("SCRIPT ENDED - OUT OF IRON INGOTS")
                break
        checkTools()
        worldSave()
        Misc.Pause(650)
        currentBSHammer = Items.FindByID(bsHammer, -1, Player.Backpack.Serial) 

        Items.UseItem(currentBSHammer)
        Gumps.WaitForGump(949095101, 1500)
        Gumps.SendAction(949095101, gump1)
        Gumps.WaitForGump(949095101, 1500)
        Gumps.SendAction(949095101, gump2)
        Gumps.WaitForGump(949095101, 1500)

        Misc.Pause(1000)
        daggers = Items.FindAllByID(itemType,-1,Player.Backpack.Serial,1,0)
        if daggers != None:
            for currentCraftedItem in daggers:
                keep = False
                if currentCraftedItem != None:
                    
                    Items.WaitForProps(currentCraftedItem,1000)
                    for slayer in slayers:
                        if str(slayer) in str(currentCraftedItem.Properties) or 'Unidentified' in str(currentCraftedItem.Properties):
                            keep = True
                            
                    if keep == True:
                        totalSlayersCrafted = totalSlayersCrafted + 1
                        totalDaggersCrafted = totalDaggersCrafted + 1
                        print("---------------------********-------------------------")
                        print("-------Slayers / Daggers Crafted: " + str(totalSlayersCrafted) + ' / ' + str(totalDaggersCrafted) + "-----------")
                        print("---*** FOUND SLAYER <---------------------------------")
                        print("---------------------********-------------------------")
                        print("---------------------********-------------------------")

                        if Player.Mount:
                            Mobiles.UseMobile(Player.Serial)
                            Misc.Pause(dragTime)
                            
                        Items.Move(currentCraftedItem,beetleContainer,-1)
                        Misc.Pause(dragTime)
                        Mobiles.UseMobile(beetle)
                        Misc.Pause(dragTime)    
                        
                    else:
                        totalDaggersCrafted = totalDaggersCrafted + 1
                        currentBSHammer = Items.FindByID(bsHammer, -1, Player.Backpack.Serial) 
                        Items.UseItem(currentBSHammer)
                        Misc.Pause(650)
                        Gumps.SendAction(949095101, 14)
                        Misc.Pause(650)
                        Target.TargetExecute(currentCraftedItem)
                        
                    Misc.SetSharedValue('totalSlayersCrafted',totalSlayersCrafted)
                    Misc.SetSharedValue('totalDaggersCrafted',totalDaggersCrafted)

def worldSave():
    if Journal.SearchByType('The world is saving, please wait.', 'System' ):
        Misc.SendMessage('Pausing for world save', 33)
        while not Journal.SearchByType('World save complete.', 'System'):
            Misc.Pause(1000)
        Misc.SendMessage('Continuing', 33)
        Journal.Clear()
        
        
worldSave()
restockList(beetle,beetleContainer,resources)
worldSave()
checkTools()
worldSave()        
for itemToCraft in BSList:
    restockList(beetle,beetleContainer,resources)
    BSCraft(itemToCraft[0],itemToCraft[1],itemToCraft[2]) 
