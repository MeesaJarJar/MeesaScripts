# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! ------------#
# ---WORK IN PROGRESS -----------------------------------------#
# Description: Simple Stealing GUMP - Broken, will fix at some
# point in time. Idea was to have a clickable interface, since
# automated stealing takes the joy out of it. 
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#

badNames     = ['sapphire','runebook','scissors',"newbied","blessed","arrow",'potion','clean bandage','scribe', 'tongs', 'ethereal', 'tool kit', 'sewing kit', 'fletching', 'nightshade', 'ginseng','garlic','black pearl','blood moss', 'sulfour', 'mandrake root','froe','skullcap','empty bottle']
rareNames = ['power','vanquishing']
slayerNames = ['Silver','Reptilian Death','Elemental Ban','Repond','Exorcism','Arachnid Doom','Fey Slayer',
    'Balron Damnation','Daemon Dismissal','Orc Slaying','Dragon Slaying'] 

# END CONFIG --------------------------------------------------#
from System.Collections.Generic import List
from System import Int32 as int
from System import Byte

gumpItems = []
stealItem    = None;
targetMobile = None;

badTypes = []

def updateBadTypesList():
    global badTypes
    badTypes = []
    with open(r'C:\Program Files (x86)\UOForever\UO\Forever\Data\Client\stolen_hidden_types.txt', 'r') as file:
        for line in file:
            badTypes.append(line.strip());
    file.close()

def hideType(itemType):
    global badTypes
    
    file_path = r'C:\Program Files (x86)\UOForever\UO\Forever\Data\Client\stolen_hidden_types.txt'
    with open(file_path, 'r') as file:
        lines = file.readlines()

    line_exists = any(line.strip() == (str(itemType)) for line in lines)

    if not line_exists:
        with open(file_path, 'a') as file:
            file.write(str(itemType) + '\n')
            print("Line added successfully.")
    else:
        print("Line already exists in the file.")
        
    #updateGump()
    

    
def updateGump():
    global gumpItems
    gumpNumber = 997799
    startX  = 10;
    startY  = 10;
    offsetX = 10;
    offsetY = 50;
    count   = 0;
    
    gd = Gumps.CreateGump();
    Gumps.AddPage(gd, 0);
    gumpHeight = 35
    gumpWidth = 300
    if len(gumpItems) > 0:
        gumpHeight = 100 + 85 * len(gumpItems)-1;
        
    Gumps.AddBackground(gd, 0, 0, gumpWidth, gumpHeight, 9200)   

    Gumps.AddLabel(gd,10,10,0,"Stealable Items:")

    for item in gumpItems:
        
        slayerItem = False;
        for slayerName in slayerNames:
            if slayerName.lower() in str(item.Properties).lower():
                #print("FOUND SLAYERNAME:",slayerName.lower());
                slayerItem = True;
                
        if slayerItem:
            
            Gumps.AddImage(gd,offsetX -105,offsetY+28,496)
            Gumps.AddLabel(gd,offsetX -95,offsetY+28,32,"SLAYER")
            Gumps.AddImage(gd,offsetX -45,offsetY+12,4502)
            slayerItem = False;
        
        rareItem = False;        
        for rareName in rareNames:
            if rareName.lower() in str(item.Properties).lower():
                #print("FOUND RARENAME:",rareName.lower());
                rareItem = True;
                
        if rareItem:
            
            Gumps.AddImage(gd,offsetX -115,offsetY+58,496)
            Gumps.AddLabel(gd,offsetX -110,offsetY+58,32,"VANQ/PWR")
            Gumps.AddImage(gd,offsetX -45,offsetY+43,4502)    
            
        Gumps.AddItem(gd,offsetX,offsetY+25,item.ItemID,item.Hue);
        Gumps.AddButton(gd,offsetX + 15,offsetY+60,4001,4001,2000 + count,4000,0)#HideType
        Gumps.AddButton(gd,offsetX + 250,offsetY+25,4001,4001,1000 + count,4000,0) 

        html_content = "<br>".join(str(entry) for entry in item.Properties);
        
        Gumps.AddHtml(gd,offsetX + 45 ,offsetY + 20 ,200,75,html_content,9200,True);
        
        offsetY += 75;
        count +=1; 
    
    Gumps.SendGump(gumpNumber, Player.Serial, 120, 120, gd.gumpDefinition, gd.gumpStrings)



def steal():
    global stealItem, targetMobile
    
    #print("stealItem:",stealItem,'targetMobile:',targetMobile);
    if targetMobile != None:
        if stealItem != None:
            Player.UseSkill("Stealing")
            Target.WaitForTarget(10000, False)
            Target.TargetExecute(stealItem)
            
            stealItem =  None
            targetMobile = None
            Player.HeadMessage(0,"RUN - TRIED TO STEAL - RUN!")
            Misc.Pause(200);
            
detectHiddenTimeout = 2750
detectHiddenTimer = Timer.Create("detectHiddenTimer",detectHiddenTimeout)     
       
def getCloseTarget():
    global targetMobile, detectHiddenTimeout, gumpItems
    #print("Finding close targets.");
    mobileFilter = Mobiles.Filter()
    mobileFilter.Enabled = True
    mobileFilter.RangeMin = 0
    mobileFilter.RangeMax = 1
    mobileFilter.CheckLineOfSite = False
    mobileFilter.IsGhost = False  
    mobileFilter.ZLevelMin = Player.Position.Z
    mobileFilter.ZLevelMax = Player.Position.Z
    mobileFilter.Notorieties = List[Byte](bytes([1])) 

    foundMobiles = Mobiles.ApplyFilter(mobileFilter)

    targetMobile = Mobiles.Select(foundMobiles,"Nearest")
    
    if targetMobile != None:
        #print("Got Target:", targetMobile);
        getItemsTarget()
    else:
        #print("No Close Targets, Detecting Hidden.");
        targetMobile = None
        stealItem = None
        gumpItems = []
#        if Timer.Check('detectHiddenTimer') == False:
#            Player.UseSkill("Detecting Hidden")
#            Misc.Pause(200)
#            Target.Self()
#            Misc.Pause(200)
#            detectHiddenTimer = Timer.Create("detectHiddenTimer",detectHiddenTimeout)

def getItemsTarget():
    global targetMobile, gumpItems, badNames, badTypes
    gumpItems = []
    
    if targetMobile and targetMobile.Backpack:
        
        Items.OpenAt(targetMobile.Backpack, 100, 100)
        Misc.Pause(250)    
        for item in targetMobile.Backpack.Contains:
            
            ignoreItem = False

            for badName in badNames:
                if badName.lower() in str(item.Properties).lower():
                    ignoreItem = True
            
            for slayerName in slayerNames:
                if slayerName.lower() in str(item.Properties).lower():
                    ignoreItem = False

            if "blessed" in str(item.Properties).lower():
                ignoreItem = True

            if "runebook" in str(item.Properties).lower():
                ignoreItem = True

            if "newbied" in str(item.Properties).lower():
                ignoreItem = True
                
            for badType in badTypes:
                #print("ItemID:", item.ItemID)
                if badType == int(item.ItemID):
                    ignoreItem = True
                    
            if ignoreItem == False:
                gumpItems.append(item)
                #print(item.Properties)
                
#            if item.IsContainer:
#                Misc.Pause(350);
#                
#                if "trap" not in str(item.Properties).lower():
#                    
#                    Items.UseItem(item)  # Open the container
#                    
#                    for nestedItem in item.Contains:
#                        ignoreNestedItem = False
#
#                        for badName in badNames:
#                            if badName.lower() in str(nestedItem.Properties).lower():
#                                ignoreNestedItem = True
#
#                        for slayerName in slayerNames:
#                            if slayerName.lower() in str(nestedItem.Properties).lower():
#                                ignoreNestedItem = False
#
#                        if "blessed" in str(nestedItem.Properties).lower():
#                            ignoreNestedItem = Trues
#
#                        if "runebook" in str(nestedItem.Properties).lower():
#                            ignoreNestedItem = True
#
#                        if "newbied" in str(nestedItem.Properties).lower():
#                            ignoreNestedItem = True
#
#                        if ignoreNestedItem == False:
#                            gumpItems.append(nestedItem)
#                            print(nestedItem.Properties)
        
    #updateGump()
updateBadTypesList()
getCloseTarget()
updateGump()  
     
while True:
    print('Running.')
    print(badTypes)
    gumpNumber = 997799;
    gd = Gumps.GetGumpData(gumpNumber)
    print("BUTTON:", gd.buttonid);
    
    
    if (gd.buttonid >= 2000 and gd.buttonid <= 2999):
        print("Player Pressed Hide Type Button:", gd.buttonid);
        Player.HeadMessage(0,"Player Pressed Hide Type Button:" + str(gd.buttonid))
        hideItem = gumpItems[gd.buttonid - 2000]
        itemType = hideItem.ItemID
        Player.HeadMessage(0,"Hiding Type:" + str(itemType))
        hideType(itemType)
        if itemType not in badTypes:
            badTypes.append(itemType)
        gd.buttonid = -1
        #updateGump()
            
    if (gd.buttonid >= 1000 and gd.buttonid <= 1999):
        print("Player Pressed Steal Button:", gd.buttonid);
        stealItem = gumpItems[gd.buttonid - 1000]
        Player.HeadMessage(0,"Trying to Steal: " + str(stealItem))
        gd.buttonid = -1
        #updateGump()

    if (gd.buttonid != -1):
        print("UNLINKED BUTTON PRESSED:", gd.buttonid)
        gd.buttonid = -1
        #updateGump()
        
    if Timer.Check('refreshTarget') == False: 
        Player.HeadMessage(0,"Scanning for Target")
        getCloseTarget()
        getItemsTarget()
        Timer.Create('refreshTarget',3000)
    steal()
    updateGump()
    Misc.Pause(500)
    #
    

