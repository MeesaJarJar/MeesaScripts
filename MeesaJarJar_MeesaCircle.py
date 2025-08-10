# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# MeesaJarJar on Discord - Peace & Love! ------------#
# Meesa Stole Wisps Code --------------------------------------#

# -------------------------------------------------------------#
from System.Collections.Generic import List
from System import String
from System import Int32 as int
import os
import math

import time
import re

# START CONFIG ------------------------------------------------#

gumpNumber = 4266528 
gumpX = 1325
gumpY = 720
itemTypesToTrack = [0x0E21,0x0F07,0x0F0C,0x0F0B,0x0F08,0x0F0D] 
LOW_DURABILITY_THRESHOLD = 20
CRITICAL_DURABILITY = 3 
# END CONFIG --------------------------------------------------#

# Thresholds


BASE_GUMP_WIDTH = 200  
CHAR_WIDTH = 7
GUMP_ID = 992921

# Weapon charge thresholds
WPN_GREEN = 500
WPN_ORANGE = 200
WPN_RED = 1

# Empowered gear thresholds
CHARGES_GREEN = 300
CHARGES_YELLOW = 100
CHARGES_RED = 1

# Slayer names
slayer_properties = [
    'Silver', 'Reptilian Death', 'Elemental Ban', 'Repond', 'Exorcism', 'Arachnid Doom', 'Fey Slayer',
    'Balron Damnation', 'Daemon Dismissal', 'Orc Slaying', 'Blood Drinking', 'Troll Slaughter',
    'Ogre Thrashing', 'Dragon Slaying', 'Earth Shatter', 'Elemental Health', 'Flame Dousing',
    'Summer Wind', 'Vacuum', 'Water Dissipation', 'Gargoyles Foe', 'Scorpions Bane', 'Spiders Death',
    'Terathan', 'Lizardman Slaughter', 'Ophidian', 'Snakes Bane'
]

# Layer mappings
layer_names = {
    "RightHand": "Right Hand", "LeftHand": "Left Hand", "Head": "Head",
    "Neck": "Neck", "Arms": "Arms", "InnerTorso": "Inner Torso",
    "MiddleTorso": "Middle Torso", "OuterTorso": "Outer Torso",
    "InnerLegs": "Inner Legs", "OuterLegs": "Outer Legs", "Pants": "Pants",
    "Shoes": "Feet", "Gloves": "Gloves", "Waist": "Waist", "Cloak": "Cloak",
    "Earrings": "Earrings", "Bracelet": "Bracelet", "Ring": "Ring", "Shirt": "Shirt"
}

layer_order = list(layer_names.keys())

# Data tracking
durabilities = {}
damage_increases = {}
total_damage_increase = 0
minimum_charges = None

def strip_tags(prop):
    return re.sub(r'<.*?>', '', prop)

def get_slayer_and_charges(item):
    Items.WaitForProps(item, 1000)
    prop_list = Items.GetPropStringList(item)
    stripped_prop_list = [strip_tags(prop).strip() for prop in prop_list]

    slayer_type = next((prop for prop in stripped_prop_list if any(slayer in prop for slayer in slayer_properties)), None)
    charges_line = next((prop for prop in stripped_prop_list if 'charges' in prop.lower()), None)

    return slayer_type, charges_line

def check_damage_increase(item):
    Items.WaitForProps(item, 1000)
    tooltip = Items.GetPropStringList(item)
    for line in tooltip:
        if "Damage Increase" in line:
            match = re.search(r"Damage Increase: (\d+)%", line)
            if match:
                return int(match.group(1))
    return None

def check_durability(item):
    if item.Durability > 0:
        return item.Durability, item.MaxDurability
    return None, None

def get_equipped_items():
    equipped_items = {}
    for layer in layer_order:
        item = Player.GetItemOnLayer(layer)
        if item:
            equipped_items[layer] = item.Serial
    return equipped_items

def re_equip_items(equipped_items):
    for layer, serial in equipped_items.items():
        item = Items.FindBySerial(serial)
        if item and not Player.GetItemOnLayer(layer):
            Player.EquipItem(item)
            Misc.Pause(300)

def repair_item(item, layer, equipped_items):
    repair_deed = Items.FindByID(0x14F0, -1, Player.Backpack.Serial)
    if repair_deed:
        Journal.Clear()
        Items.Move(item, Player.Backpack.Serial, 1)
        Misc.Pause(300)
        Items.UseItem(repair_deed)
        Target.WaitForTarget(2000)
        Target.TargetExecute(item.Serial)
        Misc.Pause(300)
        if Journal.Search("You repair the item") or Journal.Search("The item has been repaired"):
            print(f"Repaired {strip_tags(item.Name)}")
            Misc.Pause(600)
        else:
            print(f"Failed to repair {strip_tags(item.Name)}")
        re_equip_items(equipped_items)
        Misc.Pause(300)
    else:
        print("No repair deed found!")

def calculate_empowered_totals():
    global total_damage_increase, minimum_charges
    total_damage_increase = 0
    minimum_charges = None
    for info in damage_increases.values():
        total_damage_increase += info['damage_increase']
        if minimum_charges is None or info['charges'] < minimum_charges:
            minimum_charges = info['charges']

def calculate_text_width(text):
    return len(text) * CHAR_WIDTH

def clean_item_name(name):
    return re.sub(r'<[^>]+>', '', name)
    
def update_gump():
    Misc.Pause(100)
    Gumps.CloseGump(GUMP_ID)
    max_text_width = BASE_GUMP_WIDTH

    for layer in layer_order:
        if layer in durabilities:
            info = durabilities[layer]
            base_text = f"{layer_names[layer]}: {strip_tags(info['name'])}: {info['current']}/{info['max']}"
            width = calculate_text_width(base_text)
            if width > max_text_width:
                max_text_width = width + 30

    gd = Gumps.CreateGump()
    Gumps.AddPage(gd, 0)
    Gumps.AddLabel(gd,0,0,0,"  ")
    y_offset = 5
    y_offset += 2

    for layer in layer_order:
        if layer in durabilities:
            info = durabilities[layer]
            item = Items.FindBySerial(info['serial'])
            #print("ItemID:", item.ItemID)
            item_name = strip_tags(info['name'])
            current = info['current']
            max_ = info['max']
            percent = int((current / max_) * 100)
            percent_str = f"{percent:02d}%"
            durability_line = f"{percent_str}"
            #durability_line = f"{layer_names[layer]}: {item_name}: {current}/{max_}"
            #durability_line = f"{current}/{max_}"
            color = 1152

            is_weapon = layer in ['RightHand', 'LeftHand']
            slayer_text = None
            slayer_color = 0
            if is_weapon:
                slayer, charges = get_slayer_and_charges(item)
                if charges:
                    match = re.search(r'\d+', charges)
                    if match:
                        charge_val = int(match.group())
                        if charge_val >= WPN_GREEN:
                            slayer_color = 88
                        elif charge_val >= WPN_ORANGE:
                            slayer_color = 53
                        else:
                            slayer_color = 33
                        slayer_text = f"{slayer}: {charge_val}" if slayer else charges

            block_height = 40
            if slayer_text:
                block_height += 20
                
            Gumps.AddBackground(gd,10,y_offset-5,50,30,420)
            Gumps.AddAlphaRegion(gd,10,y_offset-5,50,30)
            Gumps.AddItem(gd, 10, y_offset, item.ItemID, item.Hue)
            Gumps.AddLabel(gd, 15, y_offset+20, color, durability_line)
            
            y_offset += 50

            if slayer_text:
                
                Gumps.AddLabel(gd, 5, y_offset-10, slayer_color, slayer_text.split(":")[0])
                Gumps.AddLabel(gd, 15, y_offset+10, slayer_color, slayer_text.split(":")[1])
                y_offset += 40
                
    for idx, s in enumerate(gd.gumpStrings):
        if not isinstance(s, str):
            print(f"Non-string value in gumpStrings at {idx}: {s}")
            return  # Exit early to avoid crashing

    if gd.gumpDefinition is None or not isinstance(gd.gumpDefinition, str):
        print("Invalid gumpDefinition detected")
        return
        
    
    Gumps.AddImage(gd,45,0,1609) 
    Gumps.AddTooltip(gd,3012171,str("Click & Drag Here to Move"))
    
    Gumps.SendGump(GUMP_ID, Player.Serial, 1000, 400, gd.gumpDefinition, gd.gumpStrings)
def draw_health_circle(gd, center_x, center_y, radius, health_percent, thickness=4):
    """
    Draw a circular health indicator as a thick arc from 0 to health_percent * 360 degrees.
    'thickness' sets how many pixels wide the arc is.
    """
    total_degrees = int(360 * health_percent)
    for deg in range(0, total_degrees):
        angle_rad = math.radians(deg - 90)  # Start at 12 o'clock
        for t in range(-thickness//2, thickness//2 + 1):
            # Offset the radius for thickness
            r = radius + t
            x = int(center_x + r * math.cos(angle_rad))
            y = int(center_y + r * math.sin(angle_rad))
            hue = calculate_hue(Player.Hits, Player.HitsMax)
            Gumps.AddImage(gd, x, y, 6001, hue)

def draw_circle(radius):
    points = set()
    x = radius
    y = 0
    err = 0
    while x >= y:
        points.update({
            (x, y), (y, x), (-y, x), (-x, y),
            (-x, -y), (-y, -x), (y, -x), (x, -y)
        })
        if err <= 0:
            y += 1
            err += 2*y + 1
        if err > 0:
            x -= 1
            err -= 2*x + 1
    return points

def draw_half_circle(radius, center_x, center_y, hue):
    points = set()
    x = radius
    y = 0
    err = 0
    while x >= 0:
        points.update({
            (center_x - x, center_y + y),  
            (center_x - y, center_y + x),
            (center_x + y, center_y + x),
            (center_x + x, center_y + y)
        })
        if err <= 0:
            y += 1
            err += 2*y + 1
        if err > 0:
            x -= 1
            err -= 2*x + 1
    return [(point, hue) for point in points]

def calculate_hue(player_hits, player_hits_max):
    percentage_missing = (player_hits_max - player_hits) / float(player_hits_max)
    hue_green = 371
    hue_red = 331
    hue = int(hue_green + (hue_red - hue_green) * percentage_missing)
    return hue


def updateGump():
    global hue, switch
    try:
        gd = Gumps.CreateGump(True, True, True, False) 
        radius = 120
        center_x = 0  
        center_y = -40  
 
        if Player.HitsMax > 0:
            health_percent = Player.Hits / float(Player.HitsMax)
        else:
            health_percent = 0

        draw_health_circle(gd, center_x, center_y, 100, health_percent, thickness=4)

        #for t in range(75, 80): 
#            circle_points = draw_circle(t)
#            if Player.HitsMax > 0:
#                hue = int(calculate_hue(Player.Hits, Player.HitsMax))
#            if switch:
#                switch = False
#            else:
#                switch = True
#            for point in circle_points:
#                Gumps.AddImage(gd, int(point[0] + center_x), int(point[1] + center_y), 6001, hue)
#
        itemsToTrack = itemTypesToTrack
        angle_start = -180    # Start at 10:30 oclock
        angle_end = 0      # End at 1:30 o'clock 
        if len(itemsToTrack) > 1:
            angle_step = (angle_end - angle_start) / float(len(itemsToTrack) - 1)
        else:
            angle_step = 0
        item_angles = [angle_start + i * angle_step for i in range(len(itemsToTrack))]

        for i, trackable in enumerate(itemsToTrack):
            angle_rad = math.radians(item_angles[i])
            item_x = center_x + (radius+20) * math.cos(angle_rad)  
            item_y = center_y + (radius+20) * math.sin(angle_rad)+25

            countTrackable = Items.BackpackCount(trackable, 0x0000)
            Gumps.AddLabel(gd, int(item_x), int(item_y), 1152, str(countTrackable)) 
            Gumps.AddImage(gd, int(item_x), int(item_y - 20), 11400 if countTrackable > 5 else 11410)  
            Gumps.AddItem(gd, int(item_x - 10), int(item_y - 38), trackable, 0x0000)  
            
        for idx, s in enumerate(gd.gumpStrings):
            if not isinstance(s, str):
                print(f"Non-string value in gumpStrings at {idx}: {s}")
                break
                
        if Player.Poisoned == True:
            Gumps.AddLabel(gd, int(center_x-15), int(center_y+40), 1152, str("POISONED")) 
        if Player.Paralized == True:
            Gumps.AddLabel(gd, int(center_x-15), int(center_y+20), 1152, str("PARALIZED")) 
        Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)
        CUO.MoveGump(gumpNumber, gumpX - 50, gumpY - 50)
    except Exception as e:
        Misc.SendMessage("Error in updateGump: " + str(e), 33)
        
    
hue = 0
switch = True

 
itemToTrackSerial = 0
itemToTrack = None
if len(itemTypesToTrack) < 1:
        
    while itemToTrackSerial != -1:
        Player.HeadMessage(1150, "Select Items to Track on Yousa Circle HUD! (Press ESC when finished!)")
        itemToTrackSerial = Target.PromptTarget('Select Items to Track on Yousa Circle HUD!(Press ESC when finished!)', 1150)
        itemToTrack = Items.FindBySerial(itemToTrackSerial)
        if itemToTrack is not None:
            itemTypesToTrack.append(itemToTrack.ItemID)
        else:
            break

updateGump()
update_gump()

Misc.Pause(1000)
while Player.Connected:
    
    Misc.Pause(100)
    equipped_items = get_equipped_items()
    durabilities = {}
    damage_increases = {}
    
    for layer in layer_order:
        item = Player.GetItemOnLayer(layer)
        if item:
            Items.WaitForProps(item, 1000)
            cur, max_ = check_durability(item)
            if cur is not None:
                durabilities[layer] = {
                    'name': item.Name,
                    'current': cur,
                    'max': max_,
                    'serial': item.Serial
                }
                if cur <= CRITICAL_DURABILITY:
                    repair_item(item, layer, equipped_items)

            damage_increase = check_damage_increase(item)
            _, charges_line = get_slayer_and_charges(item)
            if damage_increase and charges_line:
                match = re.search(r'\d+', charges_line)
                if match:
                    damage_increases[layer] = {
                        'name': item.Name,
                        'damage_increase': damage_increase,
                        'charges': int(match.group())
                    }

    calculate_empowered_totals()
    try:
        update_gump()
    except:
        print("FUCKED UPDATE GUMP")
    Misc.Pause(1000)

    try:
        Misc.Pause(250)
        tar = Target.GetLastAttack()
        if tar:
            mob = Mobiles.FindBySerial(tar)
            if mob is not None and not mob.Deleted:
                try:
                    CUO.OpenMobileHealthBar(tar, gumpX-130, gumpY + 30, 0)
                except Exception as e:
                    Misc.SendMessage("Error opening health bar: " + str(e), 33)
            else:
                try:
                    CUO.CloseMobileHealthBar(tar)
                except:
                    pass
        else:
            try:
                CUO.CloseMobileHealthBar(tar)
            except:
                pass
        Misc.Pause(100)
        if Player.Connected:
            updateGump()
    except Exception as e:
        Misc.SendMessage("Loop error: " + str(e), 33)
        Misc.Pause(100)
