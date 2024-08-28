# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description: Gold Drop! Drop Gold, Rares, Runes, and Gate
# to your vendor location to gain some business! Comment lines
# on or off to determine what exactly you want to do. I did this
# around Brit as a fun way for new players to get some loot and
# have a fun experience!
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#

rareBag = 0x40A47634 #Bag with Rare Items to drop
runeBag = 0x40A47634 #Bag with Marked Recall Runes to drop
minDrop = 25 #Minimum Gold Drop Amount
maxDrop = 100 #Maximum Gold Drop Amount
# END CONFIG --------------------------------------------------#

import random
count = 0
while True:
    count += 1
    
    if count % 15 == 0:
        #Misc.Pause(250);
        #Player.ChatSay("HEY YOUSA, CHECK ALL BUILDINGS IN WEST BRIT FOR CHECKS!")
        #Misc.Pause(250);
#        Player.ChatSay("Meesa 25th DROP is a 5k CHECK YOUSA GUNNA BE RICH!!")
#        Misc.Pause(1000);        
        Player.ChatSay("Shop Meesa LINCOLN MALLMORIAL!")
        Misc.Pause(250)
        #Items.UseItem(Items.FindBySerial(0x40439361))
    
#    if count % 25 == 0:
#        Misc.Pause(675)
#        Player.ChatSay("HERE HAVE A CHECK!!!!")
#        check = Items.FindByID(0x14F0,0x0034,Player.Backpack.Serial,1,False)
#        try:
#            Items.MoveOnGround(check,1,Player.Position.X+1,Player.Position.Y,Player.Position.Z)   
#        except:
#            Misc.Pause(10)

#    if count % 33 == 0:
#        #Misc.Pause(675)
#        Player.ChatSay("REMEMBER: RECORD CORPORATE PROFIT IS STOLEN WORKER WAGES!")
#        Misc.Pause(675) 
#        #
#    if count % 65 == 0:
#        Player.ChatSay("Gating to Lincoln Mallmorial Rune Library and Vendor Mall!")
#        Misc.Pause(675)
#        Items.UseItem(0x42CABCA5)
#        Misc.Pause(100)
#        Gumps.WaitForGump(1431013363, 10000)
#        Gumps.SendAction(1431013363, 18)
#        Misc.Pause(675)
#    
#    if count % 45 == 0:
#        Misc.Pause(675)
#        Player.ChatSay("HERE HAVE MEESA RARE!!!!")
#        rare = Items.FindBySerial(rareBag).Contains[0]
#        Items.MoveOnGround(rare,1,Player.Position.X+1,Player.Position.Y,Player.Position.Z)   
       
#    if count % 20 == 0:
#        Misc.Pause(675)
#        Player.ChatSay("HERE HAVE MEESA RUNE!")
#        rune = Items.FindByID(0x1F14,0x0000,runeBag,1,False)
#        try:
#            Items.MoveOnGround(rune,1,Player.Position.X+1,Player.Position.Y,Player.Position.Z)   
#        except:
#    
#            Misc.Pause(10);
#
#               
    amount = random.randint(minDrop, maxDrop);
    Misc.Pause(675)
    try:
        gold = Items.FindByID(0x0EED,-1,Player.Backpack.Serial,2,True)
        Items.MoveOnGround(gold,amount,Player.Position.X+1,Player.Position.Y,Player.Position.Z)
    
    except:
        Player.HeadMessage(0, "OUT OF GOLD");
