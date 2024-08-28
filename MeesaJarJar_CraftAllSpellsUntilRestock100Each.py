# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description: Auto Estimate Price of items on corpses.
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#
journalPause = 120
dragTime = 600
maxInventory = 100 # Amount of Spells to have maximum of each.
restockContainer = 0x428FD30F
outputContainer = 0x408FB683
container = Items.FindBySerial(0x41D14FA9)
# END CONFIG --------------------------------------------------#

from System.Collections.Generic import List
#from System import Int32 as int

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

ingots = 0x1BF2
      
scrollList = [  
    ['clumsy', 0x1F2E, 4, 1, 2],
    ['create food', 0x1F2F, 4, 1, 9],
    ['feeblemind', 0x1F30, 4, 1, 16],
    ['heal', 0x1F31, 4, 1, 23],
    ['magic arrow', 0x1F32, 4, 1, 30],
    ['night sight', 0x1F33, 4, 1, 37],
    ['reactive armor', 0x1F2D, 4, 1, 44],
    ['weaken', 0x1F34, 4, 1, 51],

    ['agility', 0x1F35, 6, 8, 2],
    ['cunning', 0x1F36, 6, 8, 9],
    ['cure', 0x1F37, 6, 8, 16],
    ['harm', 0x1F38, 6, 8, 23],
    ['magic trap', 0x1F39, 6, 8, 30],
    ['magic untrap', 0x1F3A, 6, 8, 37],
    ['protection', 0x1F3B, 6, 8, 44],
    ['strength', 0x1F3C, 6, 8, 51],

    ['bless', 0x1F3D, 9, 15, 2],
    ['fireball', 0x1F3E, 9, 15, 9],
    ['magic lock', 0x1F3F, 9, 15, 16],
    ['poison', 0x1F40, 9, 15, 23],
    ['telekinisis', 0x1F41, 9, 15, 30],
    ['teleport', 0x1F42, 9, 15, 37],
    ['unlock', 0x1F43, 9, 15, 44],
    ['wall of stone', 0x1F44, 9, 15, 51],

    ['archcure', 0x1F45, 11, 22, 2],
    ['arch protection', 0x1F46, 11, 22, 9],
    ['curse', 0x1F47, 11, 22, 16],
    ['fire field', 0x1F48, 11, 22, 23],
    ['greater heal', 0x1F49, 11, 22, 30],
    ['lightning', 0x1F4A, 11, 22, 37],
    ['manadrain', 0x1F4B, 11, 22, 44],
    ['recall', 0x1F4C, 11, 22, 51],

    ['blade spirits', 0x1F4D, 14, 29, 2],
    ['dispel field', 0x1F4E, 14, 29, 9],
    ['incognito', 0x1F4F, 14, 29, 16],
    ['magic reflection', 0x1F50, 14, 29, 23],
    ['mind blast', 0x1F51, 14, 29, 30],
    ['paralyze', 0x1F52, 14, 29, 37],
    ['poison field', 0x1F53, 14, 29, 44],
    ['summon creature', 0x1F54, 14, 29, 51],

    ['dispel', 0x1F55, 20, 36, 2],
    ['energy bolt', 0x1F56, 20, 36, 9],
    ['explosion', 0x1F57, 20, 36, 16],
    ['invisibility', 0x1F58, 20, 36, 23],
    ['mark', 0x1F59, 20, 36, 30],
    ['mass curse', 0x1F5A, 20, 36, 37],
    ['paralyze field', 0x1F5B, 20, 36, 44],
    ['reveal', 0x1F5C, 20, 36, 51],

    ['chain lightning', 0x1F5D, 40, 43, 2],
    ['energy field', 0x1F5E, 40, 43, 9],
    ['flamestrike', 0x1F5F, 40, 43, 16],
    ['gate travel', 0x1F60, 40, 43, 23],
    ['mana vampire', 0x1F61, 40, 43, 30],
    ['mass dispel', 0x1F62, 40, 43, 37],
    ['meteor storm', 0x1F63, 40, 43, 44],
    ['polymorph', 0x1F64, 40, 43, 51],

    ['earthquake', 0x1F65, 50, 50, 2],
    ['energy vortex', 0x1F66, 50, 50, 9],
    ['resurrection', 0x1F67, 50, 50, 16],
    ['summon air elemental', 0x1F68, 50, 50, 23],
    ['summon daemon', 0x1F69, 50, 50, 30],
    ['summon earth elemental', 0x1F6A, 50, 50, 37],
    ['summon fire elemental', 0x1F6B, 50, 50, 44],
    ['summon water elemental', 0x1F6C, 50, 50, 51]
]

def dumpCraftedScrolls():
    for item in Player.Backpack.Contains:
        if 'scroll' in item.Name.lower() or 'summon daemon' in item.Name.lower() or 'recall' in item.Name.lower():
            if 'blank' not in item.Name and 'rune' not in item.Name:
                
                Misc.Pause(650)
                Items.Move(item,container,-1)
        
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

def craftScroll(scroll_Name, scroll_Type, scroll_Cost, scroll_Gump1, scroll_Gump2):
    Journal.Clear()
    #
    if Player.Mana < scroll_Cost:
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
    #Misc.Pause(600)
    Journal.Clear()

    
def restockIfNeeded():
    reagentList = [ginseng,garlic,mandrake,sulfash,bloodmoss,blackpearl,nightshade,spiderssilk]
    #Misc.Pause(journalPause)
    if Items.BackpackCount(ingots, -1) < 50:
        #print("Restocking Ingots")
        difference = (100 - Items.BackpackCount(ingots, -1))
        Misc.Pause(journalPause)
        ingotsToMove = Items.FindByID(ingots, 0x0000, restockContainer, True, False)
        Items.Move(ingotsToMove,Player.Backpack,difference)
        Misc.Pause(journalPause)  

        
    while Items.BackpackCount(tinkerTool, -1) < 3:
        print("You have less than 4 tinker tools. Crafting a new one.")
        tinkCraft (tinkKitGump1, tinkKigGump2)
        Misc.Pause(journalPause)  
        
    while Items.BackpackCount(pen,-1) < 3:
        print("You have less than 4 pen. Crafting a new one.")
        tinkCraft(penGump1, penGump2)
        Misc.Pause(journalPause) 
        
    if Items.BackpackCount(scrolls, -1) < 50:
        #print("Restocking Scrolls")
        difference = (100 - Items.BackpackCount(scrolls, -1))
        Misc.Pause(journalPause)
        scrollToMove = Items.FindByID(scrolls, 0x0000, restockContainer, True, False)
        Items.Move(scrollToMove,Player.Backpack,difference)
        Misc.Pause(journalPause)  
        

    #Misc.Pause(journalPause)    
    for resource in reagentList:
        restockResource = Items.FindByID(resource, -1, restockContainer,True,False)
        
        if Items.BackpackCount(resource, -1) < 150:
            difference = 150 - Items.BackpackCount(resource, -1)
            Items.Move(restockResource, Player.Backpack.Serial, difference)
            Misc.Pause(dragTime)    
    #Misc.Pause(600)    


from collections import defaultdict

# List of all spell names in lower case
spell_names = [
    "clumsy", "create food", "feeblemind", "heal", "magic arrow", "night sight",
    "reactive armor", "weaken", "agility", "cunning", "cure", "harm", "magic trap",
    "magic untrap", "protection", "strength", "bless", "fireball", "magic lock",
    "poison", "telekinisis", "teleport", "unlock", "wall of stone", "archcure",
    "arch protection", "curse", "fire field", "greater heal", "lightning", "manadrain",
    "recall", "blade spirits", "dispel field", "incognito", "magic reflection", "mind blast",
    "paralyze", "poison field", "summon creature", "dispel", "energy bolt", "explosion",
    "invisibility", "mark", "mass curse", "paralyze field", "reveal", "chain lightning",
    "energy field", "flamestrike", "gate travel", "mana vampire", "mass dispel", "meteor storm",
    "polymorph", "earthquake", "energy vortex", "resurrection", "summon air elemental",
    "summon daemon", "summon earth elemental", "summon fire elemental", "summon water elemental"
]

# Initialize inventory dictionary with all spell names set to zero
inventory = defaultdict(int, {spell_name: 0 for spell_name in spell_names})

def parse_item_name(item_name):
    parts = item_name.split(' ')
    if parts[0].isdigit():
        quantity = int(parts[0])
        # Remove 'scroll' and trim whitespace
        name = ' '.join(parts[1:]).replace("scroll", "").strip().lower()
    else:
        quantity = 1  # default quantity if not specified
        # Remove 'scroll' and trim whitespace
        name = item_name.replace("scroll", "").strip().lower()
    return quantity, name

dumpCraftedScrolls();
for item in container.Contains:
    print(f"Raw item name: {item.Name}")  # Debugging line
    quantity, scroll_name = parse_item_name(item.Name)
    
    print(f"Parsed item name: {scroll_name}, Quantity: {quantity}") 
    if scroll_name not in spell_names:
        print(f"Unrecognized item: {scroll_name}")  # Debugging line
    else:
        inventory[scroll_name] += quantity
# Display the full inventory including spells with zero count


Items.UseItem(container)        
Misc.Pause(journalPause)        
            
Items.UseItem(restockContainer)
Misc.Pause(journalPause)
Items.UseItem(outputContainer)   
Misc.Pause(journalPause)


restockIfNeeded()       
Misc.Pause(1000)

for spell_name in spell_names:
    print(f"{inventory[spell_name]} {spell_name} scroll(s)")
    #if inventory[spell_name < 10:

for scrollToMake in scrollList:
    dumpCraftedScrolls();
    restockIfNeeded() 
    scroll_Name = scrollToMake[0]
    #print("Starting:",scroll_Name);
    #print("Iventory of ",scroll_Name,inventory[scroll_Name])
    
    scroll_Type = scrollToMake[1]
    scroll_Cost = scrollToMake[2] 
    scroll_Gump1 = scrollToMake[3]
    scroll_Gump2 = scrollToMake[4]
    #print(scroll_Name,scroll_Type,scroll_Cost,scroll_Gump1,scroll_Gump2)
    
    Misc.Pause(journalPause)

    if inventory[scroll_Name] < maxInventory:
        print("Crafting",(maxInventory - inventory[scroll_Name])," Scrolls: " + str(scroll_Name))
    
        for z in range(0,(maxInventory - inventory[scroll_Name])):
            craftScroll(scroll_Name, scroll_Type, scroll_Cost, scroll_Gump1, scroll_Gump2)
