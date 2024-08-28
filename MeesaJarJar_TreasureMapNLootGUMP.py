# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description: Treasure Map N Loot - GUMP
# Simple gump that allows the user to go through the various
# stages of unlocking and processing a Treasure Map Chest. 
# Uses Lockpicking, and Remove Trap, along with Item ID or Wand
# Obviously always remove your Tmap Chest for the next person.
# It automatically gives you a rough minimum value of the
# items in the chest, so you can see what items are worth taking
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#


# END CONFIG --------------------------------------------------#

import re
from System.Collections.Generic import List
from System import Byte, Int32

protection_tiers = {'None': 0, 'Defence': 1, 'Guarding': 2, 'Hardening': 3, 'Fortification': 4, 'Invulnerability': 5}
durability_tiers = {'None': 0, 'Durable': 1, 'Substantial': 2, 'Massive': 3, 'Fortified': 4, 'Indestructible': 5}
damage_tiers     = {'None': 0, 'Ruin': 1, 'Might': 2, 'Force': 3, 'Power': 4, 'Vanquishing': 5}
gumpNumber = 863774 
sList = {}

minimized = True

def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)
    
def updateGump(): 
    global minimized
    gd = Gumps.CreateGump(True,True,False,False) 
    Gumps.AddPage(gd,1)

    if minimized == True:
        Gumps.AddImage(gd,20,-20,337)
        
        Gumps.AddBackground(gd,0,0,200,150,420)
        
        Gumps.AddImage(gd,40,-50,9808)
        Gumps.AddLabel(gd,45,-45,1152,"Meesa")
        
        Gumps.AddLabel(gd,45,-30,1800,"T-Map")
        Gumps.AddLabel(gd,45,-20,1800,"Thingy")
        
        Gumps.AddButton(gd,15,15,1535,1536,-97,1,0)
        Gumps.AddLabel(gd,45,16,1152,"Lockpick/Remove Trap")

        Gumps.AddButton(gd,15,35,1535,1536,-99,1,0)
        Gumps.AddLabel(gd,45,36,1152,"Process Chest")
        
        Gumps.AddButton(gd,15,55,1535,1536,-98,1,0)
        Gumps.AddLabel(gd,45,56,1152,"Dump to Ground")
        
        Gumps.AddButton(gd,15,75,1535,1536,-96,1,0)
        Gumps.AddLabel(gd,45,76,1152,"Chest to Chest")
        
        Gumps.AddButton(gd,15,95,1535,1536,-95,1,0)
        Gumps.AddLabel(gd,45,96,1152,"Transfer Regs")
        
        Gumps.AddButton(gd,15,115,1535,1536,-94,1,0)
        Gumps.AddLabel(gd,45,116,1152,"Transfer Gems")        
    else:
            
        sorted_items = sorted(sList.items(), key=lambda item: (not item[1][3], -item[1][2]))
        countPriority = sum(1 for item in sorted_items if item[1][3])
        max_char_length = max(len(item[1][0]) for item in sList.items())
        
        countx = 0
        for key, value in sorted_items:
            if value[2] > 250 or value[3] == True:
                countx += 1
        if countx > 0:        
            Gumps.AddBackground(gd,0,15,200,(countx * 20) + 10,420)    
            
        if countPriority> 0:
            Gumps.AddBackground(gd,-10,0,(5 * max_char_length),(countPriority * 20) + 30,440)   
           
        if countx == 0 and countPriority == 0:
           minimized = True
           
        index = 1
        heightOffset = 20
        for key, value in sorted_items:
            if value[2] > 250 or value[3] == True:
                if value[3] == True:
                    Gumps.AddImage(gd,5,heightOffset * index,1608)
                    Gumps.AddLabel(gd,45,heightOffset * index,1152, remove_html_tags(str(value[0])))
                    
                else:
                    Gumps.AddLabel(gd,75,heightOffset * index,64, remove_html_tags(str(value[0])))
                    Gumps.AddLabel(gd,45,heightOffset * index,1195,str(value[2]))
                    
                Gumps.AddButton(gd,15,heightOffset * index,1535,1536,key,1,0)
                
                for itemx in value[1]:
                    Gumps.AddTooltip(gd,1061114,str(itemx) ) 
                    
                
                index += 1

    Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)
    
def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)
    
def calculate_item_price(item_properties):
    durability_level = 0
    protection_level = 0
    damage_level = 0

    properties = item_properties.split(',')

    for prop in properties:
        clean_prop = prop.strip().replace('<BASEFONT COLOR=#FFFFFF>', '').replace('<BASEFONT COLOR=#FFFF00>', '').lower()

        for durability, level in durability_tiers.items():
            if durability.lower() in clean_prop:
                durability_level = level

        for protection, level in protection_tiers.items():
            if protection.lower() in clean_prop:
                protection_level = level
                
        if protection_level <= 0:
            for damage, level in damage_tiers.items():
                if damage.lower() in clean_prop:
                    protection_level = level

    price = (75 * durability_level) + (75 * protection_level)
    return price
    
def IDWand():
    wand = None
    if Player.CheckLayer("LeftHand"):
        Player.UnEquipItemByLayer('LeftHand',650)
        
    if Player.CheckLayer("RightHand"):
        Player.UnEquipItemByLayer('RightHand',650)
        
    Misc.Pause(650)
    for item in Player.Backpack.Contains:
        if 'identification' in str(item.Properties).lower():
            #print("FOUND WAND, EQUIPPING!")
            Player.EquipItem(item)
            wand = item
            Misc.Pause(650)
            break
    if wand != None:
        return wand
    else:
        return False
    
def lootItem(itemSerial):
    try:
        Items.Move(itemSerial,Player.Backpack.Serial,-1)
    except:
        print("ERROR: Tried to move item but could not.")
        
def gemsToBag():
    gems = [0x0F19, 0x0F25, 0x0F13, 0x0F16, 0x0F21, 0x0F26, 0x0F15, 0x0F2D, 0x0F10]  
  
    fromBagSerial = Target.PromptTarget("Select Gems FROM Bag:",0) #Prompts the user to target a FROM bag.
    fromBagItem = Items.FindBySerial(fromBagSerial)

    toBagSerial = Target.PromptTarget("Select Gems TO Bag:",0) #Prompts the user to target a TO bag.
    toBagItem = Items.FindBySerial(toBagSerial)
    
    Items.UseItem(fromBagItem)#Opens the bag.
    Items.WaitForContents(fromBagItem,1000)
    
    for gem in gems:
        item = Items.FindByID(gem, -1, fromBagSerial)
        if item:
            Misc.Pause(350)     
            Items.Move(item, toBagSerial, -1, 0, 300)  
            
    Player.HeadMessage(1151,"Finished Gems To Bag.")      
    
def regsToBag():
    
    reagents = [0x0F8C,0x0F88,0x0F7B,0x0F85,0x0F86,0x0F8D,0x0F7A,0x0F84]
    
    fromBagSerial = Target.PromptTarget("Select Reagent FROM Bag:",0) #Prompts the user to target a FROM bag.
    fromBagItem = Items.FindBySerial(fromBagSerial)

    toBagSerial = Target.PromptTarget("Select Reagent TO Bag:",0) #Prompts the user to target a TO bag.
    toBagItem = Items.FindBySerial(toBagSerial)
    Items.UseItem(fromBagItem)#Opens the bag.
    Items.WaitForContents(fromBagItem,1000)
    for reg in reagents:
        restockResource = Items.FindByID(reg, -1, fromBagSerial)
        
        if restockResource:
            Misc.Pause(250)     
            Items.Move(restockResource, toBagSerial, -1, 0, 300)  
            
    Player.HeadMessage(1151,"Finished Regs To Bag.")      
            
def aToB(): #GROUND TARGET
    
    
    fromBagSerial = Target.PromptTarget("Select a bag / Item to move items FROM:",0) #Prompts the user to target a FROM bag.
    fromBagItem = Items.FindBySerial(fromBagSerial)

    groundTarget = Target.PromptGroundTarget("Select Ground Location to Dump:",1151)
    print("groundTarget:", groundTarget)
    if groundTarget and fromBagItem: #Makes sure both bags were selected and exist
        Items.UseItem(fromBagItem)#Opens the bag.
        Misc.Pause(650) #Pause for server delay between actions
        
        for item in fromBagItem.Contains: # Loop through items in the FROM bag
            
            Items.MoveOnGround(item,-1,groundTarget.X,groundTarget.Y,groundTarget.Z)
            
            Misc.Pause(650) #Pause for server delay between actions
        print("ERROR: Tried to move item but could not.")
        
def chestToChest():
    
    fromBagSerial = Target.PromptTarget("Select a bag to move items FROM:",0) #Prompts the user to target a FROM bag.
    fromBagItem = Items.FindBySerial(fromBagSerial)

    toBagSerial = Target.PromptTarget("Select a bag to move items TO:",0) #Prompts the user to target a TO bag.
    toBagItem = Items.FindBySerial(toBagSerial)
 
    if fromBagItem and toBagItem: #Makes sure both bags were selected and exist
        Items.UseItem(fromBagItem)#Opens the bag.
        Misc.Pause(650) #Pause for server delay between actions
        
        for item in fromBagItem.Contains: # Loop through items in the FROM bag
            Items.Move(item,toBagItem,-1) # Move item from the FROM bag to the TO bag
            Misc.Pause(100) #Pause for server delay between actions
         
            
def unlockAndRemoveTrap():
    Player.HeadMessage(1151,"Target Treasure Chest")
    tar = Target.PromptTarget("Target Chest",0)
    tmapChest = Items.FindBySerial(tar)
    lockpick = None
    if tmapChest != None:
        lockpick = Items.FindByID(0x14FC,-1,Player.Backpack.Serial,1,False)
        if lockpick != None:
            while Journal.Search('quickly yields') == False and Journal.Search('unlock that!') == False:
                Items.UseItem(lockpick)
                Misc.Pause(1000)
                Target.TargetExecute(tmapChest)
                
        Misc.Pause(1000)
        while Journal.Search('remove the trigger') == False and Journal.Search('appear to be trapped') == False:
            Player.UseSkill("Remove Trap")
            Misc.Pause(650)
            Target.TargetExecute(tmapChest)
            Misc.Pause(1000)
        Player.HeadMessage(1151,"Done Unlocking & Removing Trap")
            
    
def processChest():
    Player.HeadMessage(1151,"Target Treasure Chest")
    tar = Target.PromptTarget("Target Chest",0)
    
    
    tmapChest = Items.FindBySerial(tar)
    if tmapChest != None:
        if tmapChest.IsContainer == False:
            tmapChest = tmapChest.Container
            tmapChest = Items.FindBySerial(tmapChest)
            
    if tmapChest != None:
        Player.HeadMessage(1151,"Processing Treasure Chest")
        Misc.Pause(1000)   
        Items.UseItem(tmapChest)
        Misc.Pause(1000)
        myWand = IDWand()
        for item in tmapChest.Contains:
            priorityItem = False
            
            if 'unidentified' in str(item.Properties).lower():
                if Player.GetSkillValue("Item ID") == 100:
                    Player.HeadMessage(0,"IDing Item")
                    Player.UseSkill("Item ID")
                    Misc.Pause(650)
                    Target.TargetExecute(item)
                    Misc.Pause(650)
                else:
                    
                    if myWand != False:
                        #print("MY WAND:", myWand)
                        #print("TARGET:", item)
                        Player.HeadMessage(1151, "Using wand on" + remove_html_tags(str(item.Name)))
                        Items.UseItem(myWand)
                        Misc.Pause(650)
                        Target.TargetExecute(item.Serial)
                        
                        #Items.UseItem(myWand,item)
                        Misc.Pause(650)

            price = calculate_item_price(str(item.Properties).lower())
            
            priorityStrings = ['relic', 'fragment', 'treasure map', 'portal focus', 'gold coin', 'recipe scroll','archway', 'perk']   
            Items.WaitForProps(item,1000) 
            propString = str(item.Properties).lower()
            for priorityString in priorityStrings:
                if priorityString in propString:
                    priorityItem = True
                        
            if priorityItem == True:
                sList[item.Serial] = [item.Name, item.Properties, price, True]
            else:
                sList[item.Serial] = [item.Name, item.Properties, price, False]    
        Player.HeadMessage(1151,"Done Processing Treasure Chest")        

lastReset = 0        
updateGump()   
while True:             
    Misc.Pause(1000)
    lastReset = lastReset + 1
    gd = Gumps.GetGumpData(gumpNumber)
    if gd:
        if gd.buttonid == -98:
            aToB()
            gd.buttonid = -1
            updateGump()
            Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)
            
        if gd.buttonid == -97:
            unlockAndRemoveTrap()
            
            updateGump()
            gd.buttonid = -1
            Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)
        
        if gd.buttonid == -96:
            chestToChest()
            gd.buttonid = -1
            updateGump()
            Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)
            
        if gd.buttonid == -95:
            regsToBag()
            gd.buttonid = -1
            updateGump()
            Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)
            
        if gd.buttonid == -94:
            gemsToBag()
            gd.buttonid = -1
            updateGump()
            Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)
                                                                                          
        if gd.buttonid == -99:
            if minimized == True:
                processChest()
                minimized = False
                gd.buttonid = -1
                Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)
                updateGump() 
            else:
                minimized = True
                updateGump()   
                
        if gd.buttonid >= 1:
            Player.HeadMessage(1151,"Looting " + str(remove_html_tags(sList[gd.buttonid][0])))
            lootItem(gd.buttonid)
            if gd.buttonid in sList:
                del sList[gd.buttonid]
            gd.buttonid = -1 
            Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)
            updateGump()
            
        elif gd.buttonid == 0:
            gd.buttonid = -1
            minimized = True
            Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)
            updateGump()
        else:
            gd.buttonid = -1
            Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)
            updateGump()
        if lastReset >= 10:
            lastReset = 0
            Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)
            updateGump()