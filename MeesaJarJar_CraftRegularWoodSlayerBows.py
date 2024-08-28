# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description: Regular Wood Slayer Bow Crafter   
# 1. Set the serials for your beetle and trash barrel.
# 2. Ensure you have wood in your inventory.
# 3. Use two runebooks: 
#    - First with your HOME RUNE at position one.
#    - Second with the Brit crafting area and trash barrel.
# 4. Designate a drop-off container for finished bows.
# 5. Designate a restock container for wood and ingots.
# 6. Ensure both containers are accessible from your rune location.

# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#
dropOffContainer = 0x405F2472 
restockContainer = 0x436FD4F8 

runebook = 0x41F86AD4
 
beetle = 0x0005D75C
beetlePack = 0x40B4CBE5
trashbarrel = 0x4007B816

maxIronIngotsBeetleAmount = 50
maxWoodBeetleAmount = 100

slayerTypes = ['Silver','Reptilian Death','Elemental Ban','Repond','Exorcism','Arachnid Doom','Fey Slayer',
    'Balron Damnation','Daemon Dismissal','Orc Slaying','Dragon Slaying'] 

# END CONFIG --------------------------------------------------#

import sys
tinkKit = 0x1EB8
fletcherTool = 0x1022
woodItemID = 0x1BDD # 0x1BDD is logs, 0x1BD7 is boards
totalCraftedSlayers = 0
playerWoodMax = 100

def goHome():
    Misc.Pause(650)
    print("Meesa Going Home.");
    Player.HeadMessage(0,"Meesa Going Home.")
    Misc.Pause(650);
    Items.UseItem(runebook)
    Misc.Pause(650);
    Gumps.WaitForGump(1431013363, 3000)
    Gumps.SendAction(1431013363, 5)
    Misc.Pause(2000);
    print("WAITING 5 SECONDS TO DEBUG RECALL")
    Misc.Pause(5000)

def goBritCrafting():
    Misc.Pause(650)
    print("Meesa Going to Brit Crafting.");
    Player.HeadMessage(0,"Meesa Going to Brit Crafting.")
    Misc.Pause(650);
    Items.UseItem(runebook)
    Misc.Pause(650);
    Gumps.WaitForGump(1431013363, 3000)
    Gumps.SendAction(1431013363, 11)
    Misc.Pause(2000);
    print("WAITING 5 SECONDS TO DEBUG RECALL")
    Misc.Pause(5000)
    
def restockToBeetle():
    Misc.Pause(650)
    Player.HeadMessage(0,"Meesa Dumping Crafted Bows.")    
    dumpBows()
    Misc.Pause(650)
    Player.HeadMessage(0,"Meesa Restocking Wood and Iron Ingots to Beetle.") 
    restockCont = Items.FindBySerial(restockContainer)
    Items.UseItem(restockCont)
    Misc.Pause(650)
    
    Mobiles.UseMobile(Mobiles.FindBySerial(Player.Serial))

    Misc.Pause(1000)
    Misc.WaitForContext(beetle, 10000)
    Misc.Pause(1000)
    Misc.ContextReply(beetle, 10)
    Misc.Pause(1000)
    
    wood = Items.FindByID(woodItemID,0x0000,beetlePack,2,False)
    if wood:
        print("Found wood in beetle pack.")
        if wood.Amount < maxWoodBeetleAmount:
            difference = maxWoodBeetleAmount - wood.Amount
            restockWood = Items.FindByID(woodItemID,0x0000,restockContainer,2,False)
            if restockWood:
                if difference > restockWood.Amount:
                    difference = restockWood.Amount
                Misc.Pause(650)   
                Items.Move(restockWood,beetle,difference)
                Misc.Pause(650)
            else:
                print("MEESA HAVE NO MORE WOOD! ERROR!")
                sys.exit()
    else:
        restockWood = Items.FindByID(woodItemID,0x0000,restockContainer,2,False)
        Misc.Pause(650)   
        Items.Move(restockWood,beetle,maxWoodBeetleAmount)
        Misc.Pause(650)
   
                
    ironIngots = Items.FindByID(0x1BF2,0x0000,beetlePack,2,False)
    if ironIngots:
        print("Found ironIngots in beetle pack.")
        if ironIngots.Amount < maxIronIngotsBeetleAmount:
           print("NEed to restock iron ingots.")
           difference = maxIronIngotsBeetleAmount - ironIngots.Amount     
           restockIronIngots = Items.FindByID(0x1BF2,0x0000,restockContainer,2,False)
           if restockIronIngots:
                print("BBB")
                if difference > restockIronIngots.Amount:
                    difference = restockIronIngots.Amount
                Misc.Pause(650)   
                Items.Move(restockIronIngots,beetle,difference)
                Misc.Pause(650)
           else:
                print("MEESA HAVE NO MORE IRON INGOTS! ERROR!")
                sys.exit()
                
    else:

        restockIronIngots = Items.FindByID(0x1BF2,0x0000,restockContainer,2,False)
        Misc.Pause(650)   
        Items.Move(restockIronIngots,beetle,maxIronIngotsBeetleAmount)
        Misc.Pause(650) 
        
    Misc.Pause(650)     
    Mobiles.UseMobile(beetle)
    Misc.Pause(650)            
    
    
def dumpBows():
    print("Meesa dumpin bows!")
    bows = Items.FindAllByID(0x26C2,-1,Player.Backpack.Serial,2,False)
    if bows:
        for bow in bows:
            Items.Move(bow,dropOffContainer,1)
            Misc.Pause(650)
            
def restockFromBeetle():
    print("Meesa getting off beetle!")
    Mobiles.UseMobile(Mobiles.FindBySerial(Player.Serial))

    Misc.Pause(1000)
    Misc.WaitForContext(beetle, 10000)
    Misc.Pause(1000)
    Misc.ContextReply(beetle, 10)
    Misc.Pause(1000)
    
    
    print("Restocking Wood from Beetle")
    Player.HeadMessage(0,"Meesa Restocking Wood from Beetle")
    wood = Items.FindByID(woodItemID,0x0000,Player.Backpack.Serial,2,False)
    if wood:
        print("FOUND WOOD ON PLAYER")
        if wood.Amount < 100:
            difference = 100 - wood.Amount
            restockWood = Items.FindByID(woodItemID,0x0000,beetlePack,2,False)
            if restockWood:
                print("FOUND WOOD ON BEETLE")
                if difference > restockWood.Amount:
                    difference = restockWood.Amount
                Misc.Pause(650)   
                Items.Move(restockWood,Player.Backpack.Serial,difference)
                Misc.Pause(650)
            else:
                print("MEESA HAVE NO MORE WOOD! ERROR!")
                sys.exit()
    else:
        restockWood = Items.FindByID(woodItemID,0x0000,restockContainer,2,False)
        Misc.Pause(650)   
        Items.Move(restockWood,Player.Backpack.Serial,maxWoodBeetleAmount)
        Misc.Pause(650)            
        
    print("Restocking Iron from Beetle")
    Player.HeadMessage(0,"Meesa Restocking Iron Ingots from Beetle")
    ironIngots = Items.FindByID(0x1BF2,0x0000,Player.Backpack.Serial,2,False)
    if ironIngots:
        print("Found Iron Ingots on Player")
        if ironIngots.Amount < 50:
           difference = 50 - ironIngots.Amount     
           restockIronIngots = Items.FindByID(0x1BF2,0x0000,beetlePack,2,False)
           
           
           if restockIronIngots:
                print("Found Iron Ingots on beetle")
                if difference > restockIronIngots.Amount:
                    difference = restockIronIngots.Amount
                Misc.Pause(650)   
                Items.Move(restockIronIngots,Player.Backpack.Serial,difference)
                Misc.Pause(650)
           else:
                print("MEESA HAVE NO MORE IRON INGOTS! ERROR!")
                sys.exit()
                
    else:
        
        restockIronIngots = Items.FindByID(0x1BF2,0x0000,beetlePack,2,False)
        if restockIronIngots:
            
            print("HAVE Ingots on beetle to restock player with.")
        else:
            print("NO INGOTS FOUND on beetle to restock player with.")
            
        Misc.Pause(650)   
        Items.Move(restockIronIngots,Player.Backpack.Serial,maxIronIngotsBeetleAmount)
        Misc.Pause(650) 
                      
    Misc.Pause(650)     
    Mobiles.UseMobile(beetle)
    Misc.Pause(650)
    
def craftFletcherTool():
    Player.HeadMessage(0,"Meesa Crafting a Fletching Tool!")
    tinkTool = Items.FindByID(tinkKit,-1,Player.Backpack.Serial,1,0)
    if tinkTool:
            
        Items.UseItem(tinkTool)
        Misc.Pause(650)
        Gumps.SendAction(949095101, 8)
        Misc.Pause(650)
        Gumps.SendAction(949095101, 149)
        Misc.Pause(650)
    else:
       print("ERROR: FAILED TO FIND TINKER TOOL FOR CRAFTING!")
       sys.exit()
       
def restockRecallRegs():
    print("Meesa Restocking Reagents!")
    Misc.Pause(650)
    restockCont = Items.FindBySerial(restockContainer)
    Items.UseItem(restockCont)
    Misc.Pause(650)
    
    regs = [0x0F7B,0x0F7A,0x0F86]
    for reg in regs:
        print("Restocking: ", str(reg))
        regCount = Items.BackpackCount(reg,0x0000)
        if regCount < 30:
            regToRestock = Items.FindByID(reg,0x0000,restockCont,1,False)
            if regToRestock:
                difference = 30 - regCount
                Items.Move(regToRestock,Player.Backpack.Serial,difference)
                Misc.Pause(650)

goHome()
restockRecallRegs()
restockToBeetle()  
restockFromBeetle() 
restockToBeetle()   
goBritCrafting()    
count = 0 

while True:
    count+=1
    fletcherToolCount = Items.BackpackCount(fletcherTool,-1)
    
    if fletcherToolCount < 3:
        print("Less than 3 Fletching Tools, making another.")
        craftFletcherTool()

    if count % 50 == 0:
        goHome()
        restockToBeetle()  
        restockFromBeetle() 
        restockToBeetle()   
        goBritCrafting()  
        
    elif totalCraftedSlayers >= 3:    
        goHome()
        restockToBeetle()  
        restockFromBeetle() 
        restockToBeetle()   
        restockRecallRegs()
        goBritCrafting()  
        totalCraftedSlayers = 0

    if Items.BackpackCount(woodItemID,0x0000) < 12:
        restockFromBeetle()
        Misc.Pause(650)
        if Items.BackpackCount(woodItemID,0x0000) < 12:
            goHome()
            restockRecallRegs()
            restockToBeetle()  
            restockFromBeetle() 
            restockToBeetle()   
            goBritCrafting()    
           
    currentTool = Items.FindByID(0x1022,-1,Player.Backpack.Serial,2,False)

    if currentTool:
        Items.UseItem(currentTool)
        Misc.Pause(100)
        Gumps.SendAction(949095101, 15)
        Misc.Pause(1000)
    else:
        print("ERROR - MEESA DO NOT HAVE TOOL !")
        break
      
    Gumps.SendAction(949095101, 16)
    Misc.Pause(1500)
    Journal.WaitJournal('have received',3000)

    bows = Items.FindAllByID(0x26C2,0x0000,Player.Backpack.Serial,2,False)
    if bows:
        for bow in bows:
            slayer = False
            Items.WaitForProps(bow, 2000)
            
            for prop in slayerTypes:
                if prop.lower() in str(bow.Properties).lower():
                    slayer = True
                    
            if slayer != True:
                Items.Move(bow,trashbarrel,1)
                Misc.Pause(650)
            else:
                #getoffbeetle
                Player.HeadMessage(0,"Meesa found a Slayer!")
                totalCraftedSlayers +=1
                Mobiles.UseMobile(Mobiles.FindBySerial(Player.Serial))
                Misc.Pause(650)
                Items.Move(bow,beetle,1)
                Misc.Pause(650)
                Misc.WaitForContext(beetle, 10000)
                Misc.Pause(650)
                Misc.ContextReply(beetle, 10)
                Misc.Pause(650)
                Mobiles.UseMobile(beetle)
  