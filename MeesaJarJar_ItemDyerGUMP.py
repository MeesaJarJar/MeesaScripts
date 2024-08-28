# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description: GUMP for dying stuff I guess? I dunno i dont remmeber
# writing this script at all.....
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#


# END CONFIG --------------------------------------------------#

from System.Collections.Generic import List
from System import String
from System import Int32 as int
from System.Threading import Thread, ThreadStart
import os

current_directory = os.getcwd()
print(f"The script is running in: {current_directory}")

gumpNumber = 46143174
selectedHue = 0

def updateGump():
    gd = Gumps.CreateGump()
    Gumps.AddPage(gd, 0)
    Gumps.AddImage(gd, 0, 0, 40010)
    Gumps.AddBackground(gd, -15, 35, 142, 21, 2501)
    Gumps.AddLabel(gd, -5, 35, 2057, "Dye Furniture")
    Gumps.AddLabel(gd, 5, 59, selectedHue, "Hue:")
    #print("XSELECT:", selectedHue)
    Gumps.AddTextEntry(gd, 30, 60, 50, 25, selectedHue, 0, str(selectedHue))  # Ensure the default value is set to selectedHue
    Gumps.AddButton(gd, 105, 35, 4005, 4006, 1, 1, 0)


    Gumps.AddBackground(gd, -15, 95, 142, 21, 2501)
    Gumps.AddBackground(gd, -15, 75, 142, 21, 2501)
    Gumps.AddButton(gd, 105, 79, 4005, 4006, 2, 1, 0)    
    Gumps.AddLabel(gd, -5, 79, 2058, "Copy Hue")

    
    Gumps.AddLabel(gd, -5, 95, 2057, "Move A to B")
    Gumps.AddLabel(gd, -5, 110, 2057, "Filtered by Type:")
    
    Gumps.AddButton(gd, 105, 110, 4005, 4006, 3, 1, 0) 
    
    Gumps.AddLabel(gd, 35, 3, 1152, 'Mommers')

    Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)

def dyeFurniture(color, itemToDye):
    changecolor(color)
    Misc.Pause(700)
    Items.UseItem(0x4633806D)
    Misc.Pause(700)
    Target.WaitForTarget(1000, False)
    Misc.Pause(700)
    Target.TargetExecute(itemToDye)

def changecolor(color):
    dyes_serial = 0x46338A1E
    dyeing_tub_serial = 0x4633806D

    dyes = Items.FindBySerial(dyes_serial)
    dyeTub = Items.FindBySerial(dyeing_tub_serial)

    Items.Message(dyeTub, 945, "New Color")
    Items.Message(dyeTub, color, "{}".format(color))
    Items.ChangeDyeingTubColor(dyes, dyeTub, color)

    
def grabHue():
        global selectedHue
        #print("GRABBING HUE");
        item = Target.PromptTarget("Select Item to Copy Hue:",0)
        myItem = Items.FindBySerial(item)
        selectedHue = myItem.Hue
        #print("CHANGED HUE:", selectedHue);

def moveAtoBFiltered():
    Player.HeadMessage(0,'Select Item Type to Transfer:')
    itemToTransfer = Target.PromptTarget('Select Item Type to Transfer:')
    if itemToTransfer == -1:
        print("FAILED TO SELECT, EXITING SCRIPT.");    
    itemType = Items.FindBySerial(itemToTransfer)
    itemType = itemType.ItemID
    
    Player.HeadMessage(0,'Select Container to Transfer FROM:')
    containerToOrganize = Target.PromptTarget('Select Container to Transfer FROM:')
    if containerToOrganize == -1:
        print("FAILED TO SELECT, EXITING SCRIPT.");
        
    Items.UseItem(containerToOrganize)
    idContainer = Items.FindBySerial(containerToOrganize)
    Misc.Pause(650)
    Player.HeadMessage(0,'Select Container to Transfer TO:')
    containerToSave = Target.PromptTarget('Select container to Transfer TO:')
    if containerToSave == -1:
        print("FAILED TO SELECT, EXITING SCRIPT.");
        sys.exit()
        
    Items.UseItem(containerToSave)
    saveCont = Items.FindBySerial(containerToSave)

    Misc.Pause(650)

    for item in idContainer.Contains:
            if itemType == item.ItemID:
                Items.Move(item, saveCont, -1);
                Misc.Pause(650);
            
    Player.HeadMessage(0,'Script Finished.');
    Misc.SendMessage('Script Finished.');
    
updateGump()

while True:
    Misc.Pause(500)
    gd = Gumps.GetGumpData(gumpNumber)

    if gd:
        #print("SelectedHue:", selectedHue)
        #print("BUTTON:", gd.buttonid)
        if gd.buttonid == 0:
            #print("User Tried to close GUMP")
            gd.buttonid = -1

            Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)
            updateGump()
            
        if gd.buttonid == 1:
            itemToDyeSerial = Target.PromptTarget("Select Item to Dye:", 0)
            itemToDye = Items.FindBySerial(itemToDyeSerial)
            #print("Length of text box entry:", len(Gumps.GetTextByID(gd, 0)))
            if len(Gumps.GetTextByID(gd, 0)) != 0:
                selectedHue = int(Gumps.GetTextByID(gd, 0))
                #print("Selected Hue from text box:", selectedHue)
                dyeFurniture(int(selectedHue), itemToDye)
            gd.buttonid = -1

            updateGump()
            
        if gd.buttonid == 2:
            grabHue()
            gd.buttonid = -1

            updateGump()

        if gd.buttonid == 3:
            moveAtoBFiltered()
            gd.buttonid = -1

            updateGump()            
            
            
            
