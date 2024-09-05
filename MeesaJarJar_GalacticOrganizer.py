# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description: This script is experimental and new. Probably not
# the best, but its a fun proof of concept! Goal is to scan
# your house level by level and get a full searchable inventory
# that you can then export and search externally in excel etc.
# Writes to MeeaHouseInventory.csv
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#

# END CONFIG --------------------------------------------------#


import math
import random, csv, re
def remove_html_tags(text):
    return re.sub(r'<[^>]*>', '', text)
    
def change_page(increase=True):
    global gumpPage
    gumpPage += 1 if increase else -1
    gumpPage = max(1, min(gumpPage, len(masterItemDict) // maxItemsPerPage + 1))

class JarJarItem:
    def __init__(self, item):
        # Setting all necessary attributes
        self.amount = item.Amount
        self.container = item.Container
        self.container_opened = item.ContainerOpened
        self.contains = item.Contains
        self.corpse_number_items = item.CorpseNumberItems
        self.deleted = item.Deleted
        self.direction = item.Direction
        self.durability = item.Durability
        self.grid_num = item.GridNum
        self.hue = item.Hue
        self.is_bag_of_sending = item.IsBagOfSending
        self.is_container = item.IsContainer
        self.is_corpse = item.IsCorpse
        self.is_door = item.IsDoor
        self.is_in_bank = item.IsInBank
        self.is_lootable = item.IsLootable
        self.is_potion = item.IsPotion
        self.is_resource = getattr(item, 'IsResource', False)
        self.is_searchable = item.IsSearchable
        self.is_two_handed = item.IsTwoHanded
        self.is_virtue_shield = item.IsVirtueShield
        self.item_id = item.ItemID
        self.layer = item.Layer
        self.light = item.Light
        self.max_durability = item.MaxDurability
        self.movable = item.Movable
        self.name = item.Name
        self.on_ground = item.OnGround
        self.position = item.Position
        self.properties = item.Properties
        self.root_container = item.RootContainer
        self.serial = item.Serial
        self.updated = item.Updated
        self.visible = item.Visible
        self.weight = item.Weight

def save_to_csv(filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = [
            'serial', 'amount', 'container', 'container_opened', 'contains', 'corpse_number_items', 'deleted',
            'direction', 'durability', 'grid_num', 'hue', 'is_bag_of_sending', 'is_container', 'is_corpse', 'is_door',
            'is_in_bank', 'is_lootable', 'is_potion', 'is_resource', 'is_searchable', 'is_two_handed', 'is_virtue_shield',
            'item_id', 'layer', 'light', 'max_durability', 'movable', 'name', 'on_ground', 'position', 'properties',
            'root_container', 'updated', 'visible', 'weight'
        ]
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for item in masterItemDict.values():
            writer.writerow({
                'serial': item.serial,
                'amount': item.amount,
                'container': item.container,
                'container_opened': item.container_opened,
                'contains': item.contains,
                'corpse_number_items': item.corpse_number_items,
                'deleted': item.deleted,
                'direction': item.direction,
                'durability': item.durability,
                'grid_num': item.grid_num,
                'hue': item.hue,
                'is_bag_of_sending': item.is_bag_of_sending,
                'is_container': item.is_container,
                'is_corpse': item.is_corpse,
                'is_door': item.is_door,
                'is_in_bank': item.is_in_bank,
                'is_lootable': item.is_lootable,
                'is_potion': item.is_potion,
                'is_resource': item.is_resource,
                'is_searchable': item.is_searchable,
                'is_two_handed': item.is_two_handed,
                'is_virtue_shield': item.is_virtue_shield,
                'item_id': item.item_id,
                'layer': item.layer,
                'light': item.light,
                'max_durability': item.max_durability,
                'movable': item.movable,
                'name': item.name,
                'on_ground': item.on_ground,
                'position': str(item.position),
                'properties': ', '.join(map(str, item.properties)),
                'root_container': item.root_container,
                'updated': item.updated,
                'visible': item.visible,
                'weight': item.weight
            })

def alternate_direction(direction):
    return 'East' if Player.Position.X % 2 == 0 else 'West' if direction in ['North', 'South'] else 'North' if Player.Position.Y % 2 == 0 else 'South'

def navigate_to(x_target, y_target):
    failure_count = 0
    while True:
        current_pos = Player.Position
        dx, dy = x_target - current_pos.X, y_target - current_pos.Y
        direction = ('East' if dx > 0 else 'West') if abs(dx) > abs(dy) else ('South' if dy > 0 else 'North')
        direction = direction if failure_count < 3 else alternate_direction(direction)
        expected_pos = Point2D(current_pos.X + (1 if direction == 'East' else -1 if direction == 'West' else 0),
                               current_pos.Y + (1 if direction == 'South' else -1 if direction == 'North' else 0))
        if Player.Walk(direction) and (Player.Position.X == expected_pos.X and Player.Position.Y == expected_pos.Y):
            failure_count = 0
        else:
            failure_count += 1
            continue
        if Player.Position.X == x_target and Player.Position.Y == y_target:
            break

def explore_container(container):
    Misc.Pause(400)
    Items.WaitForProps(container, 500)
    Items.WaitForContents(container, 500)
    masterItemDict[container.Serial] = JarJarItem(container)
    for item in container.Contains:
        if item.IsContainer:
            explore_container(item)
        else:
            Items.WaitForProps(item, 500)
            Items.WaitForContents(item, 500)
            masterItemDict[item.Serial] = JarJarItem(item)

def weesaScan():
    Player.HeadMessage(1151, "Okay, weesa gunna scan now, okey day?")
    itemFilter = Items.Filter()
    itemFilter.RangeMin = 0 
    itemFilter.RangeMax = 12

    itemList = sorted(Items.ApplyFilter(itemFilter), key=lambda x: distance(Player.Position, x.Position))
    itemList = [item for item in itemList if abs(item.Position.Z - Player.Position.Z) <= 5]
    
    for item in itemList:
        Items.WaitForProps(item, 500)
        if item.Serial not in masterItemDict:
            masterItemDict[item.Serial] = JarJarItem(item)
        else:
            # Update the item details if needed (e.g., in case properties change)
            existing_item = masterItemDict[item.Serial]
            if existing_item.updated != item.Updated:  # Example condition to update an item
                masterItemDict[item.Serial] = JarJarItem(item)

        if item.IsContainer:
            errorTry = 0
            while Player.DistanceTo(item) > 2 and errorTry < 20:  # Consider adjusting this to include Z-axis check
                Misc.Pause(500)
                Items.Message(item, 1151, "SELECTED CONTAINER")
                Player.HeadMessage(1151, f"Navigating to Container at {item.Position.X},{item.Position.Y},{item.Position.Z}")
                
                while errorTry < 10 and Player.DistanceTo(item) > 1:
                    Misc.Pause(500)
                    errorTry += 1
                    Player.PathFindTo(item.Position.X + random.choice([-1, 0, 1]), item.Position.Y + random.choice([-1, 0, 1]), item.Position.Z)
            Misc.Pause(500)

            # If pathfinding succeeded, explore the container
            if errorTry < 20 and Player.DistanceTo(item) < 2:
                explore_container(item)
            else:
                #print("Failed to reach destination container.")
                Player.HeadMessage(0,"Weesa in big doo-doo, dat container failed scannin!")
    Player.HeadMessage(0,"Yousa Done Scannin! Yousa have fun now!")
    gumpPage = 1
    filterItems(str(nameSearchText), str(propertiesSearchText))
def toggleViewType():
    global listStyle
    listStyle = 'grid' if listStyle == 'list' else 'list'
    
def filterItems(nameTextToFind='', propertiesTextToFind=''):

    global filteredItemDict
    
    #print("Trying to filter:", nameTextToFind, propertiesTextToFind)
    filteredItemDict = {}
    
    nameTextToFind = nameTextToFind.lower()
    propertiesTextToFind = propertiesTextToFind.lower()
    
    for serial, item in masterItemDict.items():
        name_match = nameTextToFind in item.name.lower() if nameTextToFind else True
        properties_match = any(propertiesTextToFind in str(prop).lower() for prop in item.properties) if propertiesTextToFind else True
        
        if name_match and properties_match:
            filteredItemDict[serial] = item
            
    updateGump(filtered=True)  # Update the gump with the filtered items


def distance(p1, p2):
    return math.sqrt((p1.X - p2.X)**2 + (p1.Y - p2.Y)**2)
    
def updateGump(filtered=False):
    global selectedItemIndex, listStyle
    gd = Gumps.CreateGump(True, True, False, False)
    Gumps.AddPage(gd, 0)
    
    if minimized:
        Gumps.AddImage(gd,295,-20,8003)
        Gumps.AddImage(gd,387,-50,1619)
        Gumps.AddImage(gd,280,-28,8000)

        Gumps.AddBackground(gd, 310,-18,295,15,3000)
        #Gumps.AddHtml(gd,313,-21,400,50,"<BASEFONT color=#03befc size=7>★Meesa Jar Jar`s Galactic Organizer★</basefont>",False,False)
        Gumps.AddHtml(gd,315,-20,400,50,"<BASEFONT color=#000000 size=7>★Meesa Jar Jar`s Galactic Organizer★</basefont>",False,False)
        
        Gumps.AddImage(gd,444,8,1609)
        
        Gumps.AddButton(gd, 450, 13, 1605, 1606, 36, 1, 0)
    else:
            
        Gumps.AddImage(gd,280,-28,8000)
        Gumps.AddBackground(gd, 310,-18,295,15,3000)
        #Gumps.AddHtml(gd,313,-21,400,50,"<BASEFONT color=#03befc size=7>★Meesa Jar Jar`s Galactic Organizer★</basefont>",False,False)
        Gumps.AddHtml(gd,315,-20,400,50,"<BASEFONT color=#000000 size=7>★Meesa Jar Jar`s Galactic Organizer★</basefont>",False,False)
        
        #Gumps.AddImage(gd,300,-150,1737)
        
        Gumps.AddBackground(gd, 250, 0, 400, 100, 5150)
        #Gumps.AddBackground(gd, 200, 100, 550, 550, 420)
        
        Gumps.AddImage(gd,250,0,9780)
        Gumps.AddButton(gd, 510, 50, 1534, 1533, 6, 1, 0)
        Gumps.AddLabel(gd, 535, 51, 1152, "Save CSV")
        Gumps.AddTooltip(gd, 1060658, 'Save All Items to CSV File (Excel Style)')
        Gumps.AddButton(gd, 510, 25, 1532, 1531, 7, 1, 0)
        Gumps.AddLabel(gd, 535, 26, 1152, "Scan +- 12")
        Gumps.AddTooltip(gd, 1060658, 'Scan items and containers within 18 tiles of the player.')
        

        itemsToDisplay = filteredItemDict if filtered else masterItemDict
        
        total_items = len(itemsToDisplay)
        
        #Gumps.AddBackground(gd,435,48,50,25,5170)
        Gumps.AddBackground(gd,420,25,80,50,5170)
        Gumps.AddLabel(gd, 443, 27, 1152, "Items:")
        Gumps.AddLabel(gd, 449, 50, 1259, str(total_items))
        startIndex, endIndex = maxItemsPerPage * (gumpPage - 1), min(maxItemsPerPage * gumpPage, total_items)
        keys_on_page = list(itemsToDisplay.keys())[startIndex:endIndex]
        grid_width, grid_height, grid_rows, grid_cols = 500, 500, 10, 10
        count = 0
        height = (int(len(keys_on_page)/10) + 1) * 64
        height = max(200, min(height, 550))  # Enforce minimum of 200 and maximum of 500

        Gumps.AddBackground(gd, 200, 100, 550, height, 420)

        for key in keys_on_page:
            row, col = count // grid_cols, count % grid_cols
            item = itemsToDisplay[key]
            posX, posY = 200 + col * grid_width // grid_cols + grid_width // grid_cols // 2, 100 + row * grid_height // grid_rows + grid_height // grid_rows // 2
            
            if key == selectedItemSerial:
                Gumps.AddBackground(gd, posX - 4, posY - 4, 58, 58, 420)
                
            Gumps.AddImageTiledButton(gd, posX, posY, 2353, 2353, item.serial, Gumps.GumpButtonType.Reply, 1, item.item_id, item.hue, 0, 0)
            for bah in item.properties:
                Gumps.AddTooltip(gd, 1060658, str(bah))
                
            Gumps.AddTooltip(gd, 1060658, str(item.position))
            count += 1
        
        if selectedItemSerial and selectedItemSerial in itemsToDisplay:
            #if not itemsToDisplay[selectedItemSerial].is_container:  # Only display if its not a container
                Gumps.AddBackground(gd, 725, 110, 250, 40 + (25 * len(itemsToDisplay[selectedItemSerial].properties)), 430)
                countRow = 0
                for prop in itemsToDisplay[selectedItemSerial].properties:
                    Gumps.AddHtml(gd, 750, 125 + (countRow * 25), 200, 25, str(prop), True, False)
                    Gumps.AddTooltip(gd, 1060658, str(prop))
                    countRow += 1

        Gumps.AddBackground(gd,250,75,200,40,420)
        Gumps.AddLabel(gd,265,85,1150,"Name:")
        Gumps.AddTextEntry(gd,305,85,200,50,1152,98,nameSearchText)
        
        Gumps.AddBackground(gd,450,75,200,40,420)
        Gumps.AddLabel(gd,465,85,1150,"Properties:")
        Gumps.AddTextEntry(gd,535,85,200,50,1152,99,propertiesSearchText)  
      
        Gumps.AddBackground(gd,623,78,78,32,9200)
        Gumps.AddButton(gd,630,81,2423,2422,97,1,0) # APPLY BUTTON
        
        
        #Gumps.AddLabel(gd, 525, 26, 1152, "Toggle View")
        #Gumps.AddTooltip(gd, 1060658, f"Toggle View - Current: {listStyle}")
        #Gumps.AddButton(gd, 500, 25, 1540, 1539, 8, 1, 0)
        
        #Gumps.AddBackground(gd,315,20,108,60,83)
        Gumps.AddButton(gd, 300, 50, 5538, 5539, 4, 1, 0)
        Gumps.AddButton(gd, 275, 50, 1542, 1541, 34, 1, 0)
        Gumps.AddLabel(gd, 335, 25, 1152, "Page:")
        Gumps.AddLabel(gd, 325, 50, 1152, str(gumpPage))
        Gumps.AddLabel(gd, 342, 50, 1152, f"of {total_items // maxItemsPerPage + 1}")
        Gumps.AddButton(gd, 380, 50, 5540, 5541, 5, 1, 0)
        Gumps.AddButton(gd, 400, 50, 1540, 1539, 35, 1, 0)
        Gumps.AddImage(gd,180,90,9780)
        Gumps.AddButton(gd, 610, 0, 1605, 1606, 36, 1, 0)
        Gumps.AddHtml(gd,325,3,400,50,"<BASEFONT color=#000000 size=1>https://github.com/MeesaJarJar/MeesaScripts/</basefont>",False,False)
    Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)


gumpNumber, gumpPage, delay, rowHeight, maxItemsPerPage = 35135768, 1, 650, 25, 100
masterItemDict, subitemCurrentPage, listStyle = {}, 1, 'list'
itemFilter = Items.Filter()
itemFilter.RangeMin = 0 
itemFilter.RangeMax = 12

itemList = Items.ApplyFilter(itemFilter)

for item in itemList:
    if item.Position.Z  >= (Player.Position.Z -1) and item.Position.Z <= (Player.Position.Z + 18):
        masterItemDict[item.Serial] = JarJarItem(item)
        
minimized = True
selectedItemIndex, selectedItemSerial = None, None
nameSearchText = ''
propertiesSearchText = ''
updateGump()
filterItems(nameSearchText, propertiesSearchText)
while True: 
    Misc.Pause(100)
    gd = Gumps.GetGumpData(gumpNumber)
    if gd and gd.buttonid != -1:
        #print(gd.buttonid)
        if gd.buttonid == 4:
            change_page(False)
        elif gd.buttonid == 5:
            change_page(True)
        elif gd.buttonid == 6:
            save_to_csv("MeeaHouseInventory.csv")
        elif gd.buttonid == 7:
            weesaScan()
        elif gd.buttonid == 8:
            toggleViewType()
        elif gd.buttonid == 34:
            gumpPage = 1
            filterItems(str(nameSearchText), str(propertiesSearchText))
        elif gd.buttonid == 35:
            for myint in range(1, 100): 
                change_page(True)
        elif gd.buttonid == 36:
            if minimized == True:
                minimized = False
            else:
                minimized = True
        elif gd.buttonid == 97:
            nameSearchText = Gumps.GetTextByID(gd, 98)
            propertiesSearchText = Gumps.GetTextByID(gd, 99)
            gumpPage = 1
            filterItems(str(nameSearchText), str(propertiesSearchText))
            
        elif gd.buttonid >= 1000000:
            selectedItemSerial = gd.buttonid
            if Items.FindBySerial(gd.buttonid):
                Items.Message(gd.buttonid, masterItemDict[gd.buttonid].hue, remove_html_tags(str(masterItemDict[gd.buttonid].name)))
            else:
                Player.HeadMessage(1150, "Selected Item Outside of Sight Range")
        updateGump(filtered=True)