# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# MeesaJarJar on Discord - Peace & Love! ------------#
# Meesa Stole Wisps Code --------------------------------------#

# -------------------------------------------------------------#

from System.Collections.Generic import List
from System import String
from System import Int32 as int
import os
import math
import re

# START CONFIG ------------------------------------------------#

gumpNumber = 313236
weaponType = 0x0F4B
weaponTypes = [ 0x0F4B, 0x13FF ] 
armorContSerial = 0x41C96668
weaponContSerial = 0x400B3F2B

# END CONFIG --------------------------------------------------#

minimized = True # Set True to start minimized.
slayer_dict = {
    "Vacuum": "Air Elemental, Summoned Air Elemental",
    "Repond": "Arctic Ogre Lord, Ogre, Ogre Lord, Brigands, Non-Player Humans, Cyclops, Titan, Ettin, Evil Mage, Evil Mage Lord, Frost Troll, Troll, Meer Captain, Meer Eternal, Meer Mage, Meer Warrior, Orc, Orc Bomber, Orc Brute, Orc Captain, Orcish Lord, Orcish Mage, Orcish Mine Overseer, Orc Leader, Orc Mine Bomber, Orc Miner, Ratman, Ratman Archer, Ratman Mage, Savage Rider, Savage Shaman, Savage, Troglodyte, Lummox Mage (Portal), Lummox War Hero (Portal), Lummox Warrior (Portal), Minotaur War Hero (Portal), Minotaur Warrior (Portal)",
    "Ogre Thrashing": "Arctic Ogre Lord, Ogre, Ogre Lord",
    "Orc Slaying": "Orc, Orc Bomber, Orc Brute, Orc Captain, Orcish Lord, Orcish Mage, Orcish Mine Overseer, Orc Leader, Orc Mine Bomber, Orc Miner",
    "Troll Slaughter": "Frost Troll, Troll",
    "Silver": "Ancient Lich, Lich, Lich Lord, Bogle, Bone Knight, Bone Mage, Skeleton, Skeletal Knight, Skeletal Mage, Darknight Creeper, Flesh Golem, Ghoul, Rotting Corpse, Zombie, Gore Fiend, Hell Steed, Skeletal Mount, Lady Of The Snow, Mummy, Pestilent Bandage, Revenant, Revenant Lion, Shadow Knight, Shade, Spectre, Wraith, Werewolf, Dream Wraith (Portal), Maddening Horror (Portal), Undead War Dog (Portal)",
    "Fey Slayer": "Centaur, CuSidhe, Ethereal Warrior, Kirin, Lord Oaks, Pixie, Phoenix Matriarch, Silvani, Treefellow, Unicorn, Wisp, ML Dryad, Satyr",
    "Elemental Ban": "Acid Elemental, Toxic Elemental, Poison Elemental, Greater Poison Elemental, Agapite Elemental, Bronze Elemental, Copper Elemental, Dull Copper Elemental, Golden Elemental, Iron Elemental, Shadow Iron Elemental, Valorite Elemental, Verite Elemental, Magnetite Elemental, Air Elemental, Summoned Air Elemental, Blood Elemental, Greater Blood Elemental, Blood Vortex, Crystal Elemental, Crystal Vortex, Earth Elemental, Summoned Earth Elemental, Deep Earth Elemental, Efreet, Fire Elemental, Summoned Fire Elemental, Magma Elemental, Pyroclastic Elemental, Ice Elemental, Snow Elemental, Kaze Kemono, RaiJu, Sand Vortex, Water Elemental, Summoned Water Elemental, Deep Water Elemental",
    "Blood Drinking": "Blood Elemental, Greater Blood Elemental, Blood Vortex",
    "Earth Shatter": "Agapite Elemental, Bronze Elemental, Copper Elemental, Dull Copper Elemental, Golden Elemental, Iron Elemental, Shadow Iron Elemental, Valorite Elemental, Verite Elemental, Magnetite Elemental, Crystal Vortex, Earth Elemental, Summoned Earth Elemental, Deep Earth Elemental, Greater Blood Elemental",
    "Elemental Health": "Poison Elemental, Greater Poison Elemental",
    "Flame Dousing": "Fire Elemental, Summoned Fire Elemental, Magma Elemental, Pyroclastic Elemental",
    "Summer Wind": "Snow Elemental, Ice Elemental",
    "Water Dissipation": "Water Elemental, Summoned Water Elemental, Deep Water Elemental",
    "Exorcism": "Abysmal Horror, Balron, Bone Daemon, Chaos Daemon, Arcane Daemon, Daemon, Summoned Daemon, Ice Fiend, Demon Knight, Shadow Knights, Devourer, Gargoyle, Stone Gargoyle, Burning Gargoyle, Fire Gargoyle, Flaming Gargoyle, Enslaved Gargoyle, Gargoyle Destroyer, Gargoyle Enforcer, Scorching Gargoyle, Smoldering Gargoyle, Gibberling, Horde Minion, Imp, Nether Imp, Burning Imp, Impaler, Ravager, Succubus, Devourer (Portal), Abysmal Horror (Portal), Dark Father (Portal), Moloch",
    "Balron Damnation": "Balron",
    "Daemon Dismissal": "Abysmal Horror, Balron, Bone Daemon, Chaos Daemon, Arcane Daemon, Daemon, Summoned Daemon, Ice Fiend, Demon Knight, Devourer, Gibberling, Horde Minion, Imp, Impaler, Ravager, Moloch",
    "Gargoyles Foe": "Fire Gargoyle, Gargoyle, Stone Gargoyle, Enslaved Gargoyle, Gargoyle Destroyer, Gargoyle Enforcer",
    "Arachnid Doom": "Abnormal Dread Spider, Dread Spider, Frost Spider, Giant Black Widow, Giant Spider, Mephitis, Scorpion, Terathan Avenger, Terathan Drone, Terathan Matriarch, Terathan Warrior",
    "Scorpions Bane": "Scorpion",
    "Spiders Death": "Dread Spider, Frost Spider, Giant Black Widow, Giant Spider, Mephitis, Abnormal Dread Spider",
    "Terathan": "Terathan Avenger, Terathan Drone, Terathan Matriarch, Terathan Warrior",
    "Reptilian Death": "Ancient Wyrm, Shadow Wyrm, White Wyrm, Deep Sea Serpent, Sea Serpent, Greater Dragon, Elder Dragon, Dragon, Dragon (Portal), Ancient Wyrm (Portal), Shadow Wyrm (Portal), Bahamut, Drake, Pathaleo Drake, Giant Ice Worm, Ice Serpent, Giant Serpent, Lava Serpent, Silver Serpent, Hiryu, Lesser Hiryu, Ice Snake, Lava Snake, Snake, Juka Lord, Juka Mage, Juka Warrior, Lizardman, Ophidian Archmage, Ophidian Knight, Ophidian Mage, Ophidian Matriarch, Ophidian Warrior, Reptalon, Serado, Serpentine Dragon, Skeletal Dragon, Swamp Dragon, Wyvern, Yamandon",
    "Dragon Slaying": "Ancient Wyrm, Shadow Wyrm, White Wyrm, Dragon (Portal), Ancient Wyrm (Portal), Shadow Wyrm (Portal), Bahamut, Greater Dragon, Elder Dragon, Dragon, Drake, Pathaleo Drake, Hiryu, Lesser Hiryu, Reptalon, Serpentine Dragon, Skeletal Dragon, Swamp Dragon, Wyvern",
    "Lizardman Slaughter": "Lizardman",
    "Ophidian": "Ophidian Archmage, Ophidian Knight, Ophidian Mage, Ophidian Matriarch, Ophidian Warrior",
    "Snakes Bane": "Deep Sea Serpent, Sea Serpent, Giant Ice Worm, Giant Serpent, Ice Serpent, Lava Serpent, Silver Serpent, Ice Snake, Lava Snake, Snake, Serado, Yamandon",
    "Abyss": "Balron, Blood Elementals, Pyroclastic Elementals, Unicorns, Wisps"  
}
super_slayer_types = [
    "No Armor",
    "Repond",
    "Silver",
    "Fey Slayer",
    "Elemental Ban",
    "Exorcism",
    "Arachnid Doom",
    "Reptilian Death"
]
REQUIRED_LAYERS = ["Head", "Gloves", "Neck", "Arms", "InnerTorso", "Pants"]

def is_super_slayer(slayer_type):
    return slayer_type in super_slayer_types
    
def get_slayer_tooltip(slayer_type):
    return slayer_dict.get(slayer_type, "No data available for this slayer type.")
  
def check_durability(item):
    if item.Durability > 0:
        return item.Durability, item.MaxDurability
    return None, None    
    
def strip_tags(prop):
    return re.sub(r'<.*?>', '', prop)
    

def _cache_armor_props(container):
    cache = []
    for it in container.Contains:
        Items.WaitForProps(it, 1000)
        props = [strip_tags(p).strip().lower() for p in Items.GetPropStringList(it)]
        cache.append((it, it.Layer, props))
    return cache

def _has_full_slayer_set(props_cache, slayer_name):
    sl = slayer_name.lower()
    picked = {}  # layer -> item
    for it, layer, props in props_cache:
        if layer in REQUIRED_LAYERS and layer not in picked:
            if any(sl in p for p in props):
                picked[layer] = it
    missing = [ly for ly in REQUIRED_LAYERS if ly not in picked]
    return (len(missing) == 0, missing, picked)

def check_all_slayer_suits_in_chest():
    global armorContSerial
    status = {}

    if armorContSerial is None:
        armorContSerial = Target.PromptTarget("Select Container with Armor.", 0)

    armor_container = Items.FindBySerial(armorContSerial)
    if not armor_container:
        Misc.SendMessage("Armor container not found.", 33)
        return status

    # Open container so props are fresh
    Items.UseItem(armor_container); Misc.Pause(650)
    Misc.Pause(650)
    props_cache = _cache_armor_props(armor_container)

    for slayer in super_slayer_types:
        if slayer == "No Armor":
            continue
        complete, missing, _ = _has_full_slayer_set(props_cache, slayer)
        status[slayer] = {"complete": complete, "missing": missing}
        if complete:
            Misc.SendMessage(f"[{slayer}] Full suit READY.", 62)
        else:
            miss_txt = ", ".join(missing) if missing else "unknown"
            Misc.SendMessage(f"[{slayer}] Missing: {miss_txt}", 33)

    return status
    
def updateGump(): 
    gd = Gumps.CreateGump(True, True, False, False)
    offsetx = 70
    offsety = 5


    #Gumps.AddButton(gd,0,0,5587,5588,3,True,0)
    Gumps.AddTooltip(gd,3012171,str("Select Chest & Suit Up!"))
    idx = 0
    for slayer in super_slayer_types:
        
        if slayer in selectedSlayers:
            Gumps.AddBackground(gd,offsetx-3, -3+offsety + (20 * idx),150, 20, 308) 
            Gumps.AddBackground(gd,offsetx-3, -3+offsety + (20 * idx), 130, 20, 420) 
            Gumps.AddLabel(gd,offsetx+35,offsety + (20 * idx)-2,1152,slayer)
            Gumps.AddButton(gd,offsetx,offsety + (20 * idx)-2,1252,1254,idx,True,0)
        else:
            Gumps.AddBackground(gd,offsetx-3, -3+offsety + (20 * idx),150, 20, 308) 
            Gumps.AddBackground(gd,offsetx-3, -3+offsety + (20 * idx),30, 20, 458) 
            Gumps.AddBackground(gd,offsetx-3, -3+offsety + (20 * idx), 130, 20, 425) 
            #Gumps.AddAlphaRegion(gd,offsetx-3, -3+offsety + (20 * idx), 200, 20)
            Gumps.AddLabel(gd,offsetx+35,offsety + (20 * idx)-2,1150,slayer)
            Gumps.AddButton(gd,offsetx,offsety + (20 * idx)-2,1252,1254,idx,True,0)
        if slayer != "No Armor":    
            stat = slayerSuitStatus.get(slayer, {})
            img_id = 2361 if stat.get("complete") else 2360
            Gumps.AddImage(gd, offsetx -5, offsety + (20 * idx) - 2, img_id)
        #if slayer == selectedSlayer:
        idx = idx + 1
    
    ct = 0  
    for weaponTypeItemID in weaponTypes:
        if weaponType == weaponTypeItemID:
            Gumps.AddBackground(gd,75 + (ct * 50),175,50,50,302)
            
            Gumps.AddItem(gd,75+ (ct * 50),185,weaponTypeItemID)
        else:
            Gumps.AddButton(gd,75+ (ct * 50),185,212,211,55,1,False)
            Gumps.AddItem(gd,75+ (ct * 50),185,weaponTypeItemID)
            #Gumps.AddImageTiledButton(gd,50+ (ct * 50),1,1,50,1,0,weaponTypeItemID,0,50,50,False)
            #Gumps.AddImageTiledButton(gd,x,y,normalID,pressedID,buttonID,type,param,itemID,hue,width,height,localizedTooltip)
        ct = ct + 1
        
    #Gumps.AddImage(gd,50,30,2084)
        
    Gumps.AddHtml(gd,-20+60,0,100,150,'<BASEFONT color=#fffccc size=7><b>M</b></BASEFONT>',False,False)  #  
    Gumps.AddHtml(gd,-10+60,10,100,150,'<BASEFONT color=#fffccc size=4><b>e</b></BASEFONT>',False,False)  #  
    Gumps.AddHtml(gd,-10+60,20,100,150,'<BASEFONT color=#fffccc size=4><b>e</b></BASEFONT>',False,False)  #  
    Gumps.AddHtml(gd,-10+60,30,100,150,'<BASEFONT color=#fffccc size=4><b>s</b></BASEFONT>',False,False)  #  
    Gumps.AddHtml(gd,-10+60,40,100,150,'<BASEFONT color=#fffccc size=4><b>a</b></BASEFONT>',False,False)  #  
    Gumps.AddHtml(gd,90,0-20,100,150,'<BASEFONT color=#fffccc size=5>Slayer Suit</BASEFONT>',False,False)# 
    Gumps.AddTooltip(gd,3012171,str("Click & Drag Here to Move"))
    Gumps.AddImage(gd,offsetx-3+105, -8+offsety,1609) 
    
    Gumps.AddButton(gd,170,175,22050,22052,-2,1,False)
    Gumps.AddTooltip(gd,3012171,str("Click to Suit Up."))
    
    Gumps.CloseGump(gumpNumber)
    Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)
selectedSlayers = set()
slayerSuitStatus = check_all_slayer_suits_in_chest()   
#selectedSlayer = "No Armor"
updateGump()

while True: 

    gd = Gumps.GetGumpData(gumpNumber)

    if gd and gd.buttonid != -1:
        print(gd.buttonid)
        if gd.buttonid == 55:
            if weaponType == weaponTypes[0]:
                weaponType = weaponTypes[1]
            else:
                weaponType = weaponTypes[0]
            print("Weapon Type Changed to:", weaponType)
            
        elif gd.buttonid == -2:
            
                if len(selectedSlayers) != 2 and len(selectedSlayers) != 1:
                    Player.HeadMessage(33, "Please select EXACTLY One or Two Slayer types.")
                    gd.buttonid = -1
                    updateGump()
                    continue

                    
                    
                Player.HeadMessage(0,"Starting Yousa Suittin!")
                #if super_slayer_types[gd.buttonid] != selectedSlayer:
                if armorContSerial == None:
                        
                    armorContSerial = Target.PromptTarget("Select Container with Armor.",0)
                armorContainer = Items.FindBySerial(armorContSerial)
                
                if weaponContSerial == None:
                    weaponContSerial = Target.PromptTarget("Select Container with Weapons.",0)
                weaponContainer = Items.FindBySerial(weaponContSerial) 
                
                Items.UseItem(armorContainer)
                Misc.Pause(650)
                
                Items.UseItem(weaponContainer)
                Misc.Pause(650)
                
                required_layers = {
                    "Head": None,
                    "Gloves": None,
                    "Neck": None,
                    "Arms": None,
                    "InnerTorso": None,
                    "Pants": None
                }
                if Player.CheckLayer("LeftHand"):
                    #print("LEFT")
                    Misc.Pause(650);
                    Player.UnEquipItemByLayer("LeftHand");
                    
                        
                if Player.CheckLayer("RightHand"):
                    #print("RIGHT")
                    Misc.Pause(650);
                    Player.UnEquipItemByLayer("RightHand");
                Misc.Pause(650);    
                for layer_name in required_layers:
                    item = Player.GetItemOnLayer(layer_name)
                    if item:
                        print(f"Unequipping: {item.Name} from {layer_name}")
                        Items.Move(item.Serial, armorContainer.Serial, 0)
                        Misc.Pause(500)
                Misc.Pause(650);
                for item in Player.Backpack.Contains:
                    Items.WaitForProps(item.Serial,1000)
                    if 'dragon scale' in str(Items.GetPropStringList(item)):
                            
                            Items.Move(item,armorContainer,1)
                            Misc.Pause(300)
                            
                    if item.ItemID == 0x0F4B or item.ItemID == 0x13FF:
                            Items.Move(item,weaponContainer,1)
                            Misc.Pause(300)
                            
                armorList = []
                for item in armorContainer.Contains:
                        Items.WaitForProps(item, 1000)
                        
                        
                        cur, max_ = check_durability(item)
                        if cur is not None:
                         
                            armorList.append([item.ItemID, item.Serial, item.Name, cur, max_])
                            

                #desired_slayer = super_slayer_types[gd.buttonid]  
                # Build a readable label from what's actually selected
                if len(selectedSlayers) == 1:
                    desired_slayer = next(iter(selectedSlayers))
                else:
                    desired_slayer = " + ".join(sorted(selectedSlayers))

                found_set = {}
                weaponMatch = None
                for item in weaponContainer.Contains:
                    Items.WaitForProps(item, 1000)
                    if item.ItemID == weaponType:
                            
                        prop_list = [strip_tags(p).strip().lower() for p in Items.GetPropStringList(item)]
                        
                        # Slayer match
                        #if any(desired_slayer.lower() in p for p in prop_list):
                        if any(slayer.lower() in p for slayer in selectedSlayers for p in prop_list):
                        #if all(any(slayer.lower() in p for p in prop_list) for slayer in selectedSlayers):

                            weaponMatch = item 
                            break
                        
                for item in armorContainer.Contains:
                    Items.WaitForProps(item, 1000)
                    prop_list = [strip_tags(p).strip().lower() for p in Items.GetPropStringList(item)]
                    
                    # Slayer match
                    #if any(slayer.lower() in p for slayer in selectedSlayers for p in prop_list):
                    if all(any(slayer.lower() in p for p in prop_list) for slayer in selectedSlayers):

                    #if any(desired_slayer.lower() in p for p in prop_list):
                        item_layer = item.Layer
                        if item_layer in required_layers and not found_set.get(item_layer):
                            found_set[item_layer] = item
                            #print(f"Found {desired_slayer} piece for {item_layer}: {item.Name}")
                Misc.Pause(650)
                # Step 4: Validation check
                missing = [layer for layer in required_layers if layer not in found_set]
                if missing:
                    print("ERROR: MISSING PIECE(S) OF ARMOR FOR THIS SET:", missing)
                    Player.HeadMessage(30,"ERROR: MISSING PIECE(S) OF ARMOR FOR " + str(desired_slayer)  + " : " + str(missing))
                    selectedSlayer = "No Armor"
                else:
                    #print("Full set found. Moving items to backpack.")
                    Player.HeadMessage(0,"Full Set Found. Equipping " + str(desired_slayer) + " suit.")
                    Misc.Pause(650)
                    for layer, item in found_set.items():
                        #Items.Move(item.Serial, Player.Backpack.Serial, 0)
                        #Misc.Pause(650);
                        Player.EquipItem(item.Serial)
                        Misc.Pause(500)
                    Misc.Pause(650)
                    if weaponMatch != None and weaponMatch != 0:
                            
                        Player.EquipItem(weaponMatch)
                    else:
                        Player.HeadMessage(0,"WARNING: Missing WEAPON!")
                    Player.HeadMessage(62,"Finished Equipping Suit. Yousa Good to GO!")

                   
                    #updateGump()
        elif gd.buttonid >=0:
                selected = super_slayer_types[gd.buttonid]
                if selected in selectedSlayers:
                    selectedSlayers.remove(selected)
                else:
                    if len(selectedSlayers) < 2:
                        selectedSlayers.add(selected)
                    else:
                        Player.HeadMessage(33, "Only two Slayer types allowed.")
                
        
        gd.buttonid = -1    
        Gumps.CloseGump(gumpNumber)
        Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)
        updateGump()            
    else:
        Misc.Pause(100)

    