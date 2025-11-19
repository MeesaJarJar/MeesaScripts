# Meesa Lost All Meesa Scripts :( -----------------------------#
# Check out Meesa Site at https://meesajarjar.shop/  ----------#
# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# MesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description: Creates 4 dragable icons for N S E W directionals
# allowing the user to place them over or around the CUO
# map that does not have the cardinal directions displayed.
# MUST BE USED with the uploaded gump files for 
# 0x3E80.png through 0x3E83.png place within the 'override'
# folder in UOForever directory. You must restart client after.
#
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#
gumpNumber = 8675306
# END CONFIG --------------------------------------------------#

def updateGumps():
    
    gd = Gumps.CreateGump(True,True,False,False)  

    Gumps.AddImage(gd,0,20,0x3E80) 
    Gumps.AddLabel(gd,20,65,1152,"North")
    Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)
    
    gd = Gumps.CreateGump(True,True,False,False)  
    Gumps.AddImage(gd,0,20,0x3E81) 
    Gumps.AddLabel(gd,20,65,1152,"South")
    Gumps.SendGump(gumpNumber+1, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)  
    
    gd = Gumps.CreateGump(True,True,False,False)  
    Gumps.AddImage(gd,0,20,0x3E83) 
    Gumps.AddLabel(gd,20,65,1152,"West")
    Gumps.SendGump(gumpNumber+2, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)  
    
    gd = Gumps.CreateGump(True,True,False,False)  
    Gumps.AddImage(gd,0,20,0x3E82) 
    Gumps.AddLabel(gd,20,65,1152,"East")
    Gumps.SendGump(gumpNumber+3, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)   
    
updateGumps()
while True:
    Misc.Pause(3000)
    gd = Gumps.GetGumpData(gumpNumber)
    if gd:
        if gd.buttonid == -1:
            updateGumps()
        if gd.buttonid == 0:
            gd.buttonid = -1

