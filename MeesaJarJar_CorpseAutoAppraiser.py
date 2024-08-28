# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description: Auto Estimate Price of items on corpses.
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#


# END CONFIG --------------------------------------------------#

import re
from System.Collections.Generic import List
from System import Byte, Int32

protection_tiers = {'None': 0, 'Defence': 1, 'Guarding': 2, 'Hardening': 3, 'Fortification': 4, 'Invulnerability': 5}
durability_tiers = {'None': 0, 'Durable': 1, 'Substantial': 2, 'Massive': 3, 'Fortified': 4, 'Indestructible': 5}
damage_tiers     = {'None': 0, 'Ruin': 1, 'Might': 2, 'Force': 3, 'Power': 4, 'Vanquishing': 5}
gumpNumber = 1356163774 
sList = {}
def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)
def updateGump(): 
    gd = Gumps.CreateGump(True,True,False,False) 
    
    countx = 0
    for key, value in sList.items():
        #print(f"Key: {key}, Value: {value}")
        if Timer.Check("POPUP_" + str(item.Serial)) == True:
            if value[2] > 100:
                countx = countx + 1
    if countx > 0:        
        Gumps.AddBackground(gd,0,15,200,(countx * 20) + 50,420)    
    index = 1
    heightOffset = 20
    for key, value in sList.items():
        #print(f"Key: {key}, Value: {value}")
        
        
        if Timer.Check("POPUP_" + str(item.Serial)) == True:
            if value[2] > 100:
                Gumps.AddButton(gd,15,heightOffset * index,1535,1536,key,1,0)
                
                Gumps.AddLabel(gd,75,heightOffset * index,64, remove_html_tags(str(value[0])))
                for itemx in value[1]:
                    Gumps.AddTooltip(gd,1061114,str(itemx) ) 
                    
                Gumps.AddLabel(gd,45,heightOffset * index,64,str(value[2]))

            
        index = index + 1
    
        
    #Gumps.AddLabel(gd,45,80,64,str("123"))
    Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)

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
                
        if protection_level <=0:
            for damage, level in damage_tiers.items():
                if damage.lower() in clean_prop:
                    protection_level = level

    price = (75 * durability_level) + (75 * protection_level)
    return price
    
def IDWand():
    wandID = 0x0DF4

    wand = None

    if Player.CheckLayer("LeftHand"):
        wand = Player.GetItemOnLayer('LeftHand')
        if wand != None:
            if wand.ItemID != wandID:
                Player.UnEquipItemByLayer("LeftHand");
        if wand == None:
            wand = Items.FindByID(wandID,-1,Player.Backpack.Serial,1,0)
    if wand == None:
        print("ERROR NO ID WANDS")
        return False
    else:   
        Player.EquipItem(wand)
        return wand
def lootItem(itemSerial):
    Items.Move(itemSerial,Player.Backpack.Serial,-1)

while True:
    Misc.Pause(1000)   

    corpseFilter = Items.Filter()
    corpseFilter.OnGround = True 
    corpseFilter.RangeMin = 0 
    corpseFilter.RangeMax = 2 
    corpseList = Items.ApplyFilter(corpseFilter)
    if corpseList:
        for corpse in corpseList:
            if 'corpse' in corpse.Name:
                if Timer.Check('C_' + str(corpse.Serial)) == False:
                    Timer.Create('C_' + str(corpse.Serial),60000)
                    Items.Message(corpse,1151,"Opening Corpse")
                    Player.HeadMessage(0,"Opening Corpse") 
                    Items.UseItem(corpse)
                    Misc.Pause(250)
                    for item in corpse.Contains:
                        if 'unidentified' in str(item.Properties).lower():
                        
                            if Player.GetSkillValue("Item ID") == 100:
                                
                                Player.HeadMessage(0,"IDing Item")
                                Player.UseSkill("Item ID")
                                Misc.Pause(650)
                                Target.TargetExecute(item)
                                Misc.Pause(1000)
                            else:
                                myWand = IDWand()
                                if myWand != False:
                                    Items.UseItem(myWand,item)
                            #Player.UseSkill("Item ID",item,1000)
                        price = calculate_item_price(str(item.Properties).lower())
                        
                        sList[item.Serial] = [item.Name, item.Properties, price]
                        if Timer.Check("POPUP_" + str(item.Serial)) == False:
                            Timer.Create("POPUP_" + str(item.Serial),20000)
                        if price > 250:
                            
                            html_pattern = re.compile(r'<.*?>')
                            clean_name = re.sub(html_pattern, '', str(item.Name))
                          
                            Player.ChatSay(1150,"Get the " + remove_html_tags(str(item.Name)) + ' - it is worth ' + str(price))
                            Items.Message(corpse,1151,str(clean_name)  + " - " +  str(price) + ' Gold')
                            print(clean_name, price)
                
    gd = Gumps.GetGumpData(gumpNumber)
    if gd:

        if gd.buttonid >= 1:
            
            lootItem(gd.buttonid)

            Timer.Create('POPUP_' + str(gd.buttonid),10)

            gd.buttonid = -1 
            Misc.Pause(250)
    
              
            Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)
    updateGump()
                