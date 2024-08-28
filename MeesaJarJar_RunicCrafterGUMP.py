# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! ------------#
# -------------------------------------------------------------#
# Description: Pull Runes for Specific Slayer Types and Imbue
# Items with ease!  Simply set your reliquary and crystal 
# workbench serials in the config and start!
# Special Thanks to Wisps/Nebu & Juggz for Code Contributions, 
# and the PWN Guild for testing for me!
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#

Player.HeadMessage(0,"Target Rune Reliquary")
reliquary = Target.PromptTarget("Please target the Rune Reliquary.", 1000)

Player.HeadMessage(0,"Target Crystal Workbench")
workbench = Target.PromptTarget("Please target the Crystal Workbench.", 1000)

# END CONFIG --------------------------------------------------#

from math import radians, cos, sin

import sys
gumpNumber = 1461346


slayer_data = {
    'Repond': {'Slayer Type': 'Super Slayer', 'Power Word Recipe': ['K', 'L', 'I', 'GL', 'E'], 'Parents': [], 'buttonid': 1000},
    'Ogre Thrashing': {'Slayer Type': 'Lesser Slayer', 'Power Word Recipe': ['K', 'L', 'E', 'CH'], 'Parents': ['Repond'], 'buttonid': 1001},
    'Orc Slaying': {'Slayer Type': 'Lesser Slayer', 'Power Word Recipe': ['V', 'E', 'S'], 'Parents': ['Repond'], 'buttonid': 1002},
    'Troll Slaughter': {'Slayer Type': 'Lesser Slayer', 'Power Word Recipe': ['D', 'I', 'R'], 'Parents': ['Repond'], 'buttonid': 1003},
    'Elemental Ban': {'Slayer Type': 'Super Slayer', 'Power Word Recipe': ['G', 'A', 'SH'], 'Parents': [], 'buttonid': 1004},
    'Blood Drinking': {'Slayer Type': 'Lesser Slayer', 'Power Word Recipe': ['SH', 'U'], 'Parents': ['Elemental Ban'], 'buttonid': 1005},
    'Earth Shatter': {'Slayer Type': 'Lesser Slayer', 'Power Word Recipe': ['ZH', 'U'], 'Parents': ['Elemental Ban'], 'buttonid': 1006},
    'Elemental Health': {'Slayer Type': 'Lesser Slayer', 'Power Word Recipe': ['P', 'N', 'L'], 'Parents': ['Elemental Ban'], 'buttonid': 1007},
    'Flame Dousing': {'Slayer Type': 'Lesser Slayer', 'Power Word Recipe': ['B', 'A'], 'Parents': ['Elemental Ban'], 'buttonid': 1008},
    'Summer Wind': {'Slayer Type': 'Lesser Slayer', 'Power Word Recipe': ['M', 'I'], 'Parents': ['Elemental Ban'], 'buttonid': 1009},
    'Vacuum': {'Slayer Type': 'Lesser Slayer', 'Power Word Recipe': ['F', 'A'], 'Parents': ['Elemental Ban'], 'buttonid': 1010},
    'Water Dissipation': {'Slayer Type': 'Lesser Slayer', 'Power Word Recipe': ['T', 'I'], 'Parents': ['Elemental Ban'], 'buttonid': 1011},
    'Exorcism': {'Slayer Type': 'Super Slayer', 'Power Word Recipe': ['B', 'A', 'K', 'R'], 'Parents': [], 'buttonid': 1012},
    'Balron Damnation': {'Slayer Type': 'Lesser Slayer', 'Power Word Recipe': ['V', 'A', 'NG'], 'Parents': ['Exorcism'], 'buttonid': 1013},
    'Daemon Dismissal': {'Slayer Type': 'Lesser Slayer', 'Power Word Recipe': ['ZH', 'A', 'J', 'D'], 'Parents': ['Exorcism'], 'buttonid': 1014},
    'Gargoyles Foe': {'Slayer Type': 'Lesser Slayer', 'Power Word Recipe': ['CH', 'E', 'Z'], 'Parents': ['Exorcism'], 'buttonid': 1015},
    'Arachnid Doom': {'Slayer Type': 'Super Slayer', 'Power Word Recipe': ['F', 'I', 'H', 'L', 'A'], 'Parents': [], 'buttonid': 1016},
    'Scorpions Bane': {'Slayer Type': 'Lesser Slayer', 'Power Word Recipe': ['GL', 'E'], 'Parents': ['Arachnid Doom'], 'buttonid': 1017},
    'Spiders Death': {'Slayer Type': 'Lesser Slayer', 'Power Word Recipe': ['NG', 'E'], 'Parents': ['Arachnid Doom'], 'buttonid': 1018},
    'Terathan': {'Slayer Type': 'Lesser Slayer', 'Power Word Recipe': ['M', 'U', 'T', 'A'], 'Parents': ['Arachnid Doom'], 'buttonid': 1019},
    'Reptilian Death': {'Slayer Type': 'Super Slayer', 'Power Word Recipe': ['P', 'U', 'N', 'T'], 'Parents': [], 'buttonid': 1020},
    'Dragon Slaying': {'Slayer Type': 'Lesser Slayer', 'Power Word Recipe': ['NG', 'A', 'N', 'L'], 'Parents': ['Reptilian Death'], 'buttonid': 1021},
    'Lizardman Slaughter': {'Slayer Type': 'Lesser Slayer', 'Power Word Recipe': ['NG', 'A'], 'Parents': ['Reptilian Death'], 'buttonid': 1022},
    'Ophidian': {'Slayer Type': 'Lesser Slayer', 'Power Word Recipe': ['K', 'I', 'H', 'L'], 'Parents': ['Reptilian Death'], 'buttonid': 1023},
    'Snakes Bane': {'Slayer Type': 'Lesser Slayer', 'Power Word Recipe': ['N', 'R', 'A'], 'Parents': ['Reptilian Death'], 'buttonid': 1024},
    'Silver': {'Slayer Type': 'Super Slayer', 'Power Word Recipe': ['N', 'E', 'CH', 'R', 'A'], 'Parents': [], 'buttonid': 1025},
    'Fey': {'Slayer Type': 'Super Slayer', 'Power Word Recipe': ['M', 'A', 'R'], 'Parents': [], 'buttonid': 1026}
}

rune_ids = {
    'A': 0x483B,
    'B': 0x483E,
    'CH': 0x4841,
    'D': 0x4844,
    'E': 0x4847,
    'F': 0x484A,
    'G': 0x484D,
    'H': 0x4850,
    'I': 0x4853,
    'J': 0x4856,
    'GL': 0x4859,
    'K': 0x485C,
    'L': 0x485F,
    'M': 0x4862,
    'NG': 0x4865,
    'N': 0x4868,   
    'P': 0x486B,
    'R': 0x486E,
    'SH': 0x4871,
    'S': 0x4874,
    'T': 0x4877,
    'U': 0x487A,    
    'V': 0x487D,
    'ZH': 0x4880,
    'Z': 0x4883
      
}

rune_numbers = {
    'A': 1,
    'B': 2,
    'CH': 3,
    'D': 4,
    'E': 5,
    'F': 6,
    'G': 7,
    'H': 8,
    'I': 9,
    'J': 10,
    'GL': 11,
    'K': 12,
    'L': 13,
    'M': 14,
    'NG': 15,
    'N': 16,   
    'P': 17,
    'R': 18,
    'SH': 19,
    'S': 20,
    'T': 21,
    'U': 22,    
    'V': 23,
    'ZH': 24,
    'Z': 25  
}

    
def updateGump():
    hue = 250
    gd = Gumps.CreateGump(True, True, False, False)
   
    Gumps.AddBackground(gd, 100, 100, 250, 715, 40000)
    Gumps.AddAlphaRegion(gd,100,100,250,650)

    Gumps.AddImage(gd,100,80,10506)

    Gumps.AddImageTiled(gd,110,80,250,36,10507)
    
    Gumps.AddImage(gd,350,80,10508)
    
    Gumps.AddHtml(gd,108,90,400,200,"<BASEFONT color=#ffa894 size=7>Meesa Jar Jar`s</BASEFONT><BASEFONT color=#f5fffe size=7> - Meesa Imbuesa</BASEFONT>",0,0)

    Gumps.AddBackground(gd,90,120,275,30,430)
    Gumps.AddHtml(gd,100,125,200,200,"<BASEFONT color=#ffffff size=7>Step 1 : Select Slayer Type</BASEFONT>",0,0)
    
    super_slayers = [(name, data) for name, data in slayer_data.items() if data['Slayer Type'] == 'Super Slayer']
    num_super_slayers = len(super_slayers)
   
    gumpStartX = 150
    gumpStartY = 150
    
    offsetX = 25
    offsetY = 21
    row = 0
    for i, (super_name, super_data) in enumerate(super_slayers):
        hue = hue + 8
        
        if selectedSlayerType == super_data['buttonid']:
            #Gumps.AddBackground(gd,gumpStartX + offsetX -15,  gumpStartY + (offsetY * row)-2,125,25,420)
            Gumps.AddBackground(gd,gumpStartX + offsetX + -75,  gumpStartY + (offsetY * row) -3,250,25,420)
            Gumps.AddLabel(gd, gumpStartX + offsetX,  gumpStartY + (offsetY * row), hue, super_name)
            Gumps.AddButton(gd,gumpStartX + offsetX -85,  gumpStartY + (offsetY * row)-8,9004,1608,super_data['buttonid'],1,0)
        else:
            Gumps.AddBackground(gd,gumpStartX + offsetX -15,  gumpStartY + (offsetY * row)-2,125,25,420)
            Gumps.AddLabel(gd, gumpStartX + offsetX,  gumpStartY + (offsetY * row), hue, super_name)
            Gumps.AddButton(gd,gumpStartX + offsetX -55,  gumpStartY + (offsetY * row)-2,31,1608,super_data['buttonid'],1,0)
        
        lesser_slayers = [(name, data) for name, data in slayer_data.items() if super_name in data.get('Parents', [])]
        num_lesser_slayers = len(lesser_slayers) 
        row = row + 1
        for j, (lesser_name, lesser_data) in enumerate(lesser_slayers):
            if selectedSlayerType == lesser_data['buttonid']:
                Gumps.AddBackground(gd,gumpStartX + offsetX + -75,  gumpStartY + (offsetY * row) ,250,25,430)
                #Gumps.AddImage(gd,gumpStartX + offsetX + -50,  gumpStartY + (offsetY * row) +2,50)
                Gumps.AddButton(gd,gumpStartX + offsetX -85,  gumpStartY + (offsetY * row)-8,9004,1608,lesser_data['buttonid'],1,0)
            else:
                Gumps.AddButton(gd,gumpStartX + offsetX -55,  gumpStartY + (offsetY * row)-2,31,1608,lesser_data['buttonid'],1,0)
            #Gumps.AddButton(gd,gumpStartX + offsetX -55,  gumpStartY + (offsetY * row)-2,31,1608,lesser_data['buttonid'],1,0)
            Gumps.AddLabel(gd, gumpStartX + offsetX + 10,  gumpStartY + (offsetY * row) +2, hue+1, lesser_name)
      
            row = row + 1
            
    Gumps.AddButton(gd,125,748,4005,4006,50,1,0)     
    Gumps.AddLabel(gd,150,750,1152,"  -  Select Item")
    
    #Gumps.AddButton(gd,125,773,4005,4006,50,1,0)     
    Gumps.AddLabel(gd,150,775,1152,"  -  Select Bag of Items")
    Gumps.AddBackground(gd,90,720,300,30,430)
    Gumps.AddHtml(gd,100,725,400,200,"<BASEFONT color=#ffffff size=7>Step 2 : Select Item or Bag of Items</BASEFONT>",0,0)
        
    Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)
    
def clearBackpackOfRunes():
    for item in Player.Backpack.Contains:
        if 'letter' in str(item.Properties).lower():
            Misc.Pause(350)
            Items.Move(item,reliquary,1)
    Misc.Pause(1000)
    
def check_inventory(item_id):
    item = Items.FindByID(item_id, 0x0027, Player.Backpack.Serial, 1, False)
    if item:
        return item.Serial  
    else:
        return False  

def check_slayer_type(slayer_type):
    if slayer_type in slayer_data:
        power_word_recipe = slayer_data[slayer_type]['Power Word Recipe']
        present_runes = []
        missing_runes = []

        for rune in power_word_recipe:
            rune_id = rune_ids.get(rune)
            if rune_id:
                result = check_inventory(rune_id)
                if result:
                    present_runes.append(rune)
                else:
                    print("Missing a rune, getting now.")
                    getRune(rune)
                    Misc.Pause(100)
                    #missing_runes.append(rune)
                    present_runes.append(rune)


    else:
        print(f"Slayer Type '{slayer_type}' not found in slayer_data.")

def getRune(letter):
    Misc.Pause(650)
    Items.UseItem(reliquary)
    Misc.Pause(650)
    letterIndex = rune_numbers[letter]
    buttonToClick = letterIndex * 3 + 18488
    
    print("Trying to click:", buttonToClick)
    Gumps.WaitForGump(0x6057f914,1000)
    Gumps.SendAction(0x6057f914,buttonToClick)
    Misc.Pause(650)
    
def imbueBag():
    bagSerial = Target.PromptTarget("Select Bag to Imbue Items in:" ,1150)
    if bagSerial:
        bagContainer = Items.FindBySerial(bagSerial)
        if bagContainer:
            
            Misc.Pause(650)
            Items.UseItem(bagContainer)
            Misc.Pause(650)
            Items.WaitForContents(bagContainer,1000)
            for item in bagContainer.Contains:
                
                Misc.Pause(100)
                imbueItem(item.Serial)
                
                
    else:
        print("FAILED ERROR DID NOT SELECT ")
        
        sys.exit()

def imbueItem(item=None):

    print("AT THE START IMBUEITEM IS :", item)
    Misc.Pause(650)
    Items.UseItem(workbench)
    Misc.Pause(100)
    currentlySelectedButton = selectedSlayerType  
    name, recipe = get_slayer_data_by_buttonid(slayer_data, currentlySelectedButton)
    print("Name:", name)
    print("Recipe:", recipe)
    if name and recipe:
        check_slayer_type(name)
        partX = 1
        partY = 1
        offsetX = 25
        offx = 0
        for part in recipe:
            
            partItemID = rune_ids[part]
            print("Looking for: ", str(hex(partItemID)))
            
            partItem = Items.FindByID(partItemID,-1,Player.Backpack.Serial,1,False)
            
            if partItem:
                print("Moving" + str(partItem) + " to Workbench.")
                
                Items.Move(partItem, workbench, 1,5 + offx,20)
               
                Misc.Pause(650)
                offx = offx + 10
            else:
                Player.HeadMessage(0,"WE DID NOT GET A RUNE WE NEEDED. EXITING SCRIPT ERROR")
                print("Didnt find the rune we need...")
                print("ERROR - EXITING SCRIPT")
                sys.exit()
                break
            
        print("DONE Moving Parts. READY TO IMBUE!")    
        Player.HeadMessage(0,"Finished Grabbing Runes!")
        Misc.Pause(650)
        Items.UseItem(workbench)
        Gumps.WaitForGump(0xe32d6fe3, 1000)
        Gumps.SendAction(0xe32d6fe3, 1)  
        
        if item != None:
            Misc.Pause(350)
            Target.TargetExecute(item)
            
        else:
            Player.HeadMessage(0,"Select Item to Imbue:")
        
    else:
        print("ButtonID not found.")

def get_slayer_data_by_buttonid(slayer_data, buttonid):
    for name, attributes in slayer_data.items():
        if attributes['buttonid'] == buttonid:
            return name, attributes['Power Word Recipe']
    return None, None

selectedSlayerType = 1000
Items.UseItem(workbench)
Misc.Pause(100)

if Gumps.HasGump(gumpNumber):
    CUO.MoveGump(gumpNumber,400,400)
    
if Gumps.HasGump(3811405795):
    #cancel
    
    Gumps.SendAction(0xe32d6fe3, 2)
    Misc.Pause(100)
    
  
clearBackpackOfRunes()
updateGump()

while True: 
    Misc.Pause(100)
    
    gd = Gumps.GetGumpData(gumpNumber)

    if gd:
       
        if gd.buttonid != -1:
            print("Pressed Button: ",gd.buttonid)
            if gd.buttonid == 0:
                
                print("Closing Script.")
                sys.exit()
                #gd.buttonid = -1
                #Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)
                #updateGump()
                
        if gd.buttonid == 51:
            print("Select Bag")
            imbueBag()
            gd.buttonid = -1
            Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)
            updateGump()
            
        if gd.buttonid == 50:
            print("Select Item")
            imbueItem()
            gd.buttonid = -1
            Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)
            updateGump()
            
        if gd.buttonid >=1000 and gd.buttonid <=1999:
            selectedSlayerType = gd.buttonid
            print("selectedSlayerType:", selectedSlayerType)
            gd.buttonid = -1
            Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)
            updateGump()
               
    #updateGump()