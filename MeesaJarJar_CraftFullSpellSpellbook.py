# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description: Crafts 1 of every spell, and places it in a 
# spellbook. Uses Tinker to create tools.
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#
amountToMake = 100
restockContainer = 0x428FD30F
outputContainer = 0x408FB683

# END CONFIG --------------------------------------------------#

from System.Collections.Generic import List
#from System import Int32 as int

journalPause = 120
dragTime = 600
pen = 0x0FBF
scrolls = 0x0EF3
tink = 0x1EB8
penGump1 = 8
penGump2 = 163
tinkerTool = 0x1EB8
tinkKitGump1 = 8
tinkKigGump2 = 23
spellbook = 0x0EFA
ginseng = 0x0F85
garlic = 0x0F84
mandrake = 0x0F86
sulfash = 0x0F8C
bloodmoss = 0x0F7B
blackpearl = 0x0F7A
nightshade = 0x0F88
spiderssilk = 0x0F8D

scrollList = [                              
# First Circle                              
['Clumsy scroll',0x1F2E,4,1,2],
['Create Food scroll',0x1F2F,4,1,9],
['Feeblemind scroll',0x1F30,4,1,16],
['Heal scroll',0x1F31,4,1,23],
['Magic Arrow scroll',0x1F32,4,1,30],
['Night Sight scroll',0x1F33,4,1,37],
['Reactive Armor scroll',0x1F2D,4,1,44],
['Weaken scroll',0x1F34,4,1,51],
# Second Circle                             
['Agility scroll',0x1F35,6,8,2],
['Cunning scroll',0x1F36,6,8,9],
['Cure scroll',0x1F37,6,8,16],
['Harm scroll',0x1F38,6,8,23],
['Magic Trap scroll',0x1F39,6,8,30],
['Magic Untrap scroll',0x1F3A,6,8,37],
['Protection scroll',0x1F3B,6,8,44],
['Strength scroll',0x1F3C,6,8,51],
# Third Circle                              
['Bless scroll',0x1F3D,9,15,2],
['Fireball scroll',0x1F3E,9,15,9],
['Magic Lock scroll',0x1F3F,9,15,16],
['Poison scroll',0x1F40,9,15,23],
['Telekinesis scroll',0x1F41,9,15,30],
['Teleport scroll',0x1F42,9,15,37],
['Unlock scroll',0x1F43,9,15,44],
['Wall of Stone scroll',0x1F44,9,15,51],
# Fourth Circle                             
['Arch Cure scroll',0x1F45,11,22,2],
['Arch Protection scroll',0x1F46,11,22,9],
['Curse scroll',0x1F47,11,22,16],
['Fire Field scroll',0x1F48,11,22,23],
['Greater Heal scroll',0x1F49,11,22,30],
['Lightning scroll',0x1F4A,11,22,37],
['Mana Drain scroll',0x1F4B,11,22,44],
['Recall scroll',0x1F4C,11,22,51],
# Fifth Circle                              
['Blade Spirits scroll',0x1F4D,14,29,2],
['Dispel Field scroll',0x1F4E,14,29,9],
['Incognito scroll',0x1F4F,14,29,16],
['Magic Reflection scroll',0x1F50,14,29,23],
['Mind Blast scroll',0x1F51,14,29,30],
['Paralyze scroll',0x1F52,14,29,37],
['Poison Field scroll',0x1F53,14,29,44],
['Summon Creature scroll',0x1F54,14,29,51],
# Sixth Circle                              
['Dispel scroll',0x1F55,20,36,2],
['Energy Bolt scroll',0x1F56,20,36,9],
['Explosion scroll',0x1F57,20,36,16],
['Invisibility scroll',0x1F58,20,36,23],
['Mark scroll',0x1F59,20,36,30],
['Mass Curse scroll',0x1F5A,20,36,37],
['Paralyze Field scroll',0x1F5B,20,36,44],
['Reveal scroll',0x1F5C,20,36,51],
# Seventh Circle                                
['Chain Lightning scroll',0x1F5D,40,43,2],
['Energy Field scroll',0x1F5E,40,43,9],
['Flamestrike scroll',0x1F5F,40,43,16],
['Gate Travel scroll',0x1F60,40,43,23],
['Mana Vampire scroll',0x1F61,40,43,30],
['Mass Dispel scroll',0x1F62,40,43,37],
['Meteor Swarm scroll',0x1F63,40,43,44],
['Polymorph scroll',0x1F64,40,43,51],
# Eighth Circle                             
['Earthquake scroll',0x1F65,50,50,2],
['Energy Vortex scroll',0x1F66,50,50,9],
['Resurrection scroll',0x1F67,50,50,16],
['Summon Air Elemental scroll',0x1F68,50,50,23],
['Summon Daemon scroll',0x1F69,50,50,30],
['Summon Earth Elemental scroll',0x1F6A,50,50,37],
['Summon Fire Elemental scroll',0x1F6B,50,50,44],
['Summon Water Elemental scroll',0x1F6C,50,50,51]  
]                               
                                                   

def tinkCraft (gump1, gump2):
    Gumps.CloseGump(949095101)
    currentTink = Items.FindByID(tinkerTool,0x0000,Player.Backpack.Serial, True, False)
    if Gumps.CurrentGump() != 949095101:
        Items.UseItem(currentTink)
    Gumps.WaitForGump(949095101, 1500)
    Gumps.SendAction(949095101, gump1)
    Gumps.WaitForGump(949095101, 1500)
    Gumps.SendAction(949095101, gump2)
    Gumps.WaitForGump(949095101, 1500)
    Misc.Pause(journalPause)   

def craftScroll(scroll_Name, scroll_Type, scroll_Cost, scroll_Gump1, scroll_Gump2,newBook):
    Journal.Clear()
    Misc.Pause(1500)
    while Player.Mana < scroll_Cost:
        Player.UseSkill("Meditation")
        Misc.Pause(3000)
        
    Gumps.CloseGump(949095101)
    currentPen = Items.FindByID(pen,0x0000,Player.Backpack.Serial, True, False)
    if Gumps.CurrentGump() != 949095101:
        Items.UseItem(currentPen)
    Gumps.WaitForGump(949095101, 1500)
    Gumps.SendAction(949095101, scroll_Gump1)
    Gumps.WaitForGump(949095101, 1500)
    Gumps.SendAction(949095101, scroll_Gump2)
    Gumps.WaitForGump(949095101, 1500)
    Misc.Pause(600)
    Journal.WaitJournal("You have received a",5000)
    Misc.Pause(600)
    Journal.Clear()
    craftedScroll = Items.FindByID(scroll_Type,0x0000,Player.Backpack.Serial,True,False)
    if craftedScroll:
        Misc.Pause(600)
        Items.Move(craftedScroll,newBook.Serial,1)
        Misc.Pause(journalPause)
    
def restockIfNeeded():
    reagentList = [ginseng,garlic,mandrake,sulfash,bloodmoss,blackpearl,nightshade,spiderssilk]
    Misc.Pause(journalPause)
    
    while Items.BackpackCount(tinkerTool, -1) < 3:
        print("You have less than 4 tinker tools. Crafting a new one.")
        tinkCraft (tinkKitGump1, tinkKigGump2)
        Misc.Pause(journalPause)  
        
    while Items.BackpackCount(pen,-1) < 3:
        print("You have less than 4 pen. Crafting a new one.")
        tinkCraft(penGump1, penGump2)
        Misc.Pause(journalPause) 
        
    if Items.BackpackCount(scrolls, -1) < 100:
        print("Restocking Scrolls")
        difference = (100 - Items.BackpackCount(scrolls, -1))
        Misc.Pause(journalPause)
        scrollToMove = Items.FindByID(scrolls, 0x0000, restockContainer, True, False)
        Items.Move(scrollToMove,Player.Backpack,difference)
        Misc.Pause(journalPause)  
    Misc.Pause(journalPause)    
    for resource in reagentList:
        restockResource = Items.FindByID(resource, -1, restockContainer,True,False)
        
        if Items.BackpackCount(resource, -1) < 150:
            difference = 150 - Items.BackpackCount(resource, -1)
            Items.Move(restockResource, Player.Backpack.Serial, difference)
            Misc.Pause(dragTime)    
    Misc.Pause(600)    

def craftBook():
    Misc.Pause(600)
    currentPen = Items.FindByID(pen,0x0000,Player.Backpack.Serial, True, False)
    if currentPen:
        if Gumps.CurrentGump() != 0x38920abd:
            Items.UseItem(currentPen.Serial)
        Gumps.WaitForGump(0x38920abd,1500)
        Gumps.SendAction(0x38920abd, 57)
        Gumps.WaitForGump(0x38920abd,1500)
        Gumps.SendAction(0x38920abd, 16)
        Misc.Pause(2000)
    else:
        Misc.SendMessage('Out of Pens, restocking and crafting a pen',33)
        restockIfNeeded()
        currentPen = Items.FindByID(pen,0x0000,Player.Backpack.Serial, True, False)
        if currentPen:
            if Gumps.CurrentGump() != 0x38920abd:
                Items.UseItem(currentPen.Serial)
            Gumps.WaitForGump(0x38920abd,1500)
            Gumps.SendAction(0x38920abd, 57)
            Gumps.WaitForGump(0x38920abd,1500)
            Gumps.SendAction(0x38920abd, 16)
            Misc.Pause(2000)
    newBook = Items.FindByID(spellbook,0x0000,Player.Backpack.Serial, True, False)      
    return newBook

rightHand = Player.CheckLayer('RightHand')

fullSpellbook = Items.FindByID(0x0EFA,0x0000,Player.Backpack.Serial)
if fullSpellbook:
    Items.WaitForProps(fullSpellbook, 500)
    if "64 Spells" in str(fullSpellbook.Properties):
        if not Player.CheckLayer("RightHand"):
            Player.HeadMessage(66,'Equiping full spellbook to not trash')
            Player.EquipItem(fullSpellbook)
            Misc.Pause(dragTime)
        else:
            Player.HeadMessage(33,'You have a full spellbook in your pack and cant equip to save it. Stopping.')
            Print("FAILED TO CLEAR SPELLBOOKS IN PACK - UNSAFE TO START.")
            sys.exit()
    
    
Items.UseItem(restockContainer)
Misc.Pause(journalPause)
Items.UseItem(outputContainer)   
Misc.Pause(journalPause)


for z in range(amountToMake):
    restockIfNeeded()       
    Misc.Pause(1000)
    newBook = craftBook()
    if newBook == None:
        Misc.Pause(1000)
        newBook = craftBook()
    Misc.Pause(1000)
    for scrollToMake in scrollList:
        
        scroll_Name = scrollToMake[0]
        scroll_Type = scrollToMake[1]
        scroll_Cost = scrollToMake[2] 
        scroll_Gump1 = scrollToMake[3]
        scroll_Gump2 = scrollToMake[4]
        print(scroll_Name,scroll_Type,scroll_Cost,scroll_Gump1,scroll_Gump2)
        
        Misc.Pause(journalPause)
        
        #check if you already have that type of scroll before you craft Item
        scroll_Check = Items.FindByID(scroll_Type,0x0000,Player.Backpack.Serial, True, False)
        if scroll_Check:
            #Move scroll to spellbook
            Misc.Pause(1000)
            print("Already have Scrolll: " + str(scroll_Name))
            Items.Move(scroll_Check,newBook,1)
            Misc.Pause(1000)
        else:
            #Craft scroll 
            print("Crafting Scroll: " + str(scroll_Name))
            craftScroll(scroll_Name, scroll_Type, scroll_Cost, scroll_Gump1, scroll_Gump2,newBook)

    #Move Full Spellbook to outputContainer 
    Items.Move(newBook,outputContainer,1)





