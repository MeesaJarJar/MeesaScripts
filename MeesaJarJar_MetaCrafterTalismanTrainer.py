# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description: Crafting script for making tailoring objects
# to level the Crafter Meta Talisman. Unattended crafting that
# levels Talisman is against the rules, you MUST ATTEND this. 
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#


# END CONFIG --------------------------------------------------#

from System.Collections.Generic import List
#from System import Int32 as int

dragTime = 600

tinkertool = 0x1EB8
tinkKitGump1 = 8
tinkKigGump2 = 23

sewingKit = 0x0F9D
sewingKitGump1 = 8
sewingKitGump2 = 44

scissor = 0x0F9F
scissorGump1 = 8
scissorGump2 = 2

ironIngots = 0x1BF2
cloth = 0x1766
resources = [[cloth, 250], [ironIngots, 50]]

Player.HeadMessage(66,'Target Beetle')
beetle = Target.PromptTarget()

Player.HeadMessage(66,'Target an Item in Beetles Backpack')
beetleContainer = Items.FindBySerial(Target.PromptTarget())
beetleContainer = beetleContainer.RootContainer

tailoringList = [
#Format of Tailoring is Gump1, Gump2, ItemID of what you want to make.

#HATS
[1,2,0x1544],#skullcap
[1,9,0x1540],#bandana
[1,16,0x1713],#floppy hat
[1,23,0x1715],#cap
[1,30,0x1714],#wide-brim hat
[1,37,0x1717],#straw hat
[1,44,0x1716],#tall straw hat
[1,51,0x1718],#wizards hat
[1,58,0x1719],#bonnet
[1,65,0x171A],#feathered hat
[1,72,0x171B],#tricorne hat
[1,79,0x171C],#jester hat
#SHIRTS
[8,2,0x1F7B],#doublet
[8,9,0x1517],#shirt
[8,16,0x1EFD],#fancy shirt
[8,23,0x1FA1],#tunic
[8,30,0x1FFD],#surcoat
[8,37,0x1F01],#plain dress
[8,44,0x1F00],#fancy dress
[8,51,0x1515],#cloak
[8,58,0x1F03],#robe
[8,65,0x1F9F],#jester suit
#PANTS
[15,2,0x152E],#short pants
[15,9,0x1539],#long pants
[15,16,0x1537],#kilt
[15,23,0x1516],#skirt
#Misc
[22,2,0x1541],#body sash
[22,9,0x153B],#half apron
[22,16,0x153D]#full apron
#[22,30,0x175D]#oil cloth
]

def tinkCraft (gump1, gump2):
    Gumps.CloseGump(949095101)
    #currentTink = FindItem(tinkertool,Player.Backpack)
    
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
    
    Misc.SendMessage("RESTOCKING RESOURCES")
    #Check if player is mounted on beetle. If they are, dismount.
    if Player.Mount:
        Mobiles.UseMobile(Player.Serial)
        Misc.Pause(dragTime)
        
    #Open Beetles Backpack
    Misc.WaitForContext(0x00035D2E, 2000)
    Misc.ContextReply(0x00035D2E, 10)
    
    #Loop through resources. resource[0] is ItemID and resource[1] is amount to have in pack.
    for resource in resources:
        
        restockResource = Items.FindByID(resource[0], -1, container)

        if Items.BackpackCount(resource[0], -1) < resource[1]:
            
            difference = resource[1] - Items.BackpackCount(resource[0], -1)
            if restockResource:
                Items.Move(restockResource, Player.Backpack, difference)
            Misc.Pause(dragTime)
            
    #Remount Beetle
    Mobiles.UseMobile(beetle)
    Misc.Pause(dragTime)    
    
def checkTools():
    Misc.SendMessage("CHECKING TOOLS")
    #Check to make sure we have enough Sewing Kits. If we dont, then craft them via tinkering.
    # always have 2 tinker kits
    while Items.BackpackCount(tinkertool, -1) < 2:
        tinkCraft (tinkKitGump1, tinkKigGump2)
        Misc.Pause(600)
        tinkCraft (tinkKitGump1, tinkKigGump2)    
        Misc.Pause(600)
        
    # always have 4 Sewing Kits
    while Items.BackpackCount(sewingKit, -1) < 4:
        tinkCraft (sewingKitGump1, sewingKitGump2)
        Misc.Pause(600)
        
    # always have scissors
    while Items.BackpackCount(scissor, -1) < 1:
        tinkCraft (scissorGump1, scissorGump2)
        Misc.Pause(600)
    

def tailorCraft (gump1, gump2, itemType):

    for X in range(0,25):
        
        checkTools()
        worldSave()
        Misc.Pause(500)
        Misc.SendMessage("Selecting Sewing Kit.")
        currentSewing = Items.FindByID(sewingKit, 0x0000, Player.Backpack.Serial) 
        
        # Sewing Kit must be in backpack main pouch and not subcontainer. Can be programmed to include subcontainers.
        Misc.Pause(1000)
        Misc.SendMessage("Crafting Item: " + str(gump1) + ',' + str(gump2))
        Items.UseItem(currentSewing)
        Gumps.WaitForGump(949095101, 1500)
        Gumps.SendAction(949095101, gump1)
        Gumps.WaitForGump(949095101, 1500)
        Gumps.SendAction(949095101, gump2)
        Gumps.WaitForGump(949095101, 1500)
        Misc.SendMessage("Finished Crafting") 
        Misc.Pause(1000)

        currentCraftedItem = Items.FindByID(itemType, -1, Player.Backpack.Serial)
        scissors = Items.FindByID(scissor, 0x0000, Player.Backpack.Serial)
        
        # Scissors must be in backpack main pouch and not subcontainer. Can be programmed to include subcontainers.
        Misc.SendMessage("Using Scissors")
        Items.UseItem(scissors)
        Target.WaitForTarget(1000, False)
        Misc.Pause(1250)
        Target.TargetExecute(currentCraftedItem)
        Misc.Pause(750)
        Misc.SendMessage("Done with Scissors.")

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
for itemToCraft in tailoringList:
    restockList(beetle,beetleContainer,resources)
    tailorCraft(itemToCraft[0],itemToCraft[1],itemToCraft[2]) 
