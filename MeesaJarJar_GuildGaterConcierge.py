# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# --WORK IN PROGRESS ------------------------------------------#
# -------------------------------------------------------------#
# Description: Guild Gating Bot - Hard Coded Book Names and Serials.
# Uses a butler and two chests, one for repair deeds and another 
# for weapons and armor to be dropped in to auto repair.
# Auto restocks from butler if set up properly. 
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#
gateSpamTimer = 30000

book_names = [1431013363,  1431013363,  1431013363] #Classic Dungeons, Exotic Dungeons, City Banks
book_serials = [0x43299B3B, 0x42B4D661, 0x43299B3B]
butlerSerial = 0x000CF2EB

lmRunebook = 0x450ECE84
restockContainer = 0x46FFCB6F
itemRepairContainer = 0x41500F7E
repairDeedContainer = 0x44132F95

# END CONFIG --------------------------------------------------#


import threading
import time
from System.Collections.Generic import List
from System import Int32 as int
from System import Byte

listingGates = False
total_gates = 0
delay = 650
repairDeedID = 0x14F0
# Location names
#locations_dungeons = ['Covetous', 'Deceit', 'Delucia Passage', 'Destard', 'Exodus', 'Fire', 'Hyloth', 'Ice', 'Orc Cave', 'Shame', 'Wind', 'Wrong', 'Khauldun {PvP]', 'Abyss', 'Asylum', 'Despise']
locations_classic_dungeons = ['Sewers', 'Covetous', 'Deceit', 'Despise', 'Destard','Fire','Hyloth','Ice','Khaldun','Orc Cave','Shame','Spider Cave','Terathan Keep','The Abyss','Wind','Wrong']
locations_exotic_dungeons = ['Ankh', 'Asylum','Delucia Passage','Exodus','Grinchs Area','Grotto','Montor','Booty Island','Dino Land','Temple of Snake','----','Fall Dungeon', 'Spring Dungeon','Summer Dungeon','Winter Dungeon','----']
locations_cities = ['East Bank', 'Brit Bank', 'Cove', 'Jhelom', 'Minoc', 'Moonglow', 'New Magincia', "Nujelm", 'Ocllo', "Serpents Hold", 'Skara Brae', 'Trinsic East', 'Trinsic West', 'Vesper', 'Wind', 'Yew']

ignoreMobileList = [0x0003A1EC, 0x001BB218]

def execute_send_action(chatType,location, location_list):
    global listingGates, book_serials
    sublistNumber = 0
    location = location.lower()
    print("Location is: ",location)
    print("Location List is: ",location_list)
    for sublist in location_list:
        print("Sublist:", sublist)
        i = 0
        for item in sublist:
            print("Item:", item)
            if location in item.lower() and len(location) >= 3:

                # Use the corresponding book name from the book_names list
                serial = book_serials[sublistNumber]
                print("Serial:", serial)
                if serial:
                    Journal.Clear()
                    if Player.Mana < 40:
                        Misc.Pause(750)

                        if chatType == 'Guild':
                            Player.ChatGuild("Sorry, low on Mana. Meditating and then I can gate!")
                        else:
                            
                            Player.ChatSay(1152, "Sorry, low on Mana. Meditating and then I can gate!")
                            
                        Player.UseSkill("Meditation")
                        while Player.Mana < 40:
                            Misc.Pause(1000)

                    if Player.Mana >= 40:
                        Misc.Pause(750)
                        if chatType == 'Guild':
                            Player.ChatGuild( "Gating to " + item.upper() + " now!")
                        else:
                            Player.ChatSay(1152, "Gating to " + item.upper() + " now!")
                            
                        testnum = 6 * (i + 1)
                        Misc.Pause(650)
                        Items.UseItem(serial)
                        Gumps.WaitForGump(1431013363, 10000)
                        Gumps.SendAction(1431013363, 6 * (i + 1))
                        return True
                        
            i = i + 1
        sublistNumber = sublistNumber + 1
    return False

def execute_lm_gate(total_gates):
    global listingGates
    if Timer.Check('spamTimer') == False:
        Misc.SendMessage("Total Gates: " + str(total_gates))
        while listingGates:
            Misc.Pause(1000)
        Player.ChatSay(1152, "Yousa say `Gate` and the Dungeon, City, or LM for meesa Rune Library!")
        Misc.Pause(2000)
        while listingGates:
            Misc.Pause(1000)        
        Player.ChatSay(1152, "Yousa say `List Gates` to see all meesa places we be gating to!")
        Misc.Pause(2000)
#        while listingGates:
#            Misc.Pause(1000)        
#        Player.ChatSay(495, "Yousa also might be sayings `Regs` to get a FREE bag of meesa Reagents!")
        
def openAllChests():
    Misc.Pause(650)
    repairContainer = Items.FindBySerial(itemRepairContainer)
    Items.UseItem(repairContainer)
    
    Misc.Pause(650)
    deedContainer = Items.FindBySerial(repairDeedContainer)
    Items.UseItem(deedContainer)
    
    Misc.Pause(650)
    regsContainer = Items.FindBySerial(restockContainer)
    Items.UseItem(regsContainer)    
    
def repairItemsInChest():
    Misc.Pause(650)
    repairContainer = Items.FindBySerial(itemRepairContainer)
    deedContainer = Items.FindBySerial(repairDeedContainer)
    if repairContainer and deedContainer:
        
        #Items.UseItem(repairContainer)
        #Misc.Pause(650)

        #Items.UseItem(repairContainer)
        #Misc.Pause(650)
        for item in repairContainer.Contains:
            #print(item)
            if item.Durability < item.MaxDurability:
                Player.ChatSay(1152,"Repairing an Item!")
                print("Found Item to repair. ") 
                repairDeed = Items.FindByID(0x14F0,-1,repairDeedContainer,1,False)
                if repairDeed == None:
                    Player.ChatSay(1152,"ERROR - NO REPAIR DEEDS IN CONTAINER!")
                    return False
                else:
                    print("Found Repapir Deed.")
                    Misc.Pause(650)
                    Items.Move(repairDeed,Player.Backpack.Serial,-1)  
                    Misc.Pause(650)  
                    Items.Move(item,Player.Backpack.Serial,-1)  
                    Misc.Pause(650)  
                    Items.UseItem(repairDeed)
                    Misc.Pause(250)
                    Target.TargetExecute(item)
                    Misc.Pause(650)
                    Items.Move(item,repairContainer,-1)  
                    print("Done Repairing Item.")

def check_timer_exists_or_create(name, total_gates, found_guild_gate):
    if Timer.Check(name) == True:
        remaining_time = round(Timer.Remaining(name) / 1000)
        Misc.SendMessage("Sorry, but " + str(name) + " has " + str(remaining_time) + " seconds remaining before they can ask for another gate.")
        if found_guild_gate:
            Player.ChatSay(1152, "Sorry, but " + str(name) + " has " + str(remaining_time) + " seconds remaining before they can ask for another gate.")
        else:
            Player.ChatGuild("Sorry, but " + str(name) + " has " + str(remaining_time) + " seconds remaining before they can ask for another gate.")
        canGate = False
        Journal.Clear()
    else:
        canGate = True
        print("Creating Timer for Player")
        Player.ChatSay(495, "You can gate again in " +  str(gateSpamTimer) + "ms!")
        Timer.Create(name, gateSpamTimer, "Timer for " + str(name) + " is now expired. They may now ask for another gate.")
    return total_gates, canGate

def listTheGates(all_locations, found_guild_gate):
    global listingGates
    listingGates = True

    Misc.Pause(1000)
    if found_guild_gate:
            
        Player.ChatGuild("Here are the places we can gate to:")
        all_locations_text = ', '.join([item for sublist in all_locations for item in sublist])
        items_list = all_locations_text.split(',')
        chunk_size = 5
        chunks = [items_list[i:i+chunk_size] for i in range(0, len(items_list), chunk_size)]
        for chunk in chunks:
            Misc.Pause(1000)
            Player.ChatGuild(' | '.join(chunk))
        listingGates = False
    else:
        Player.ChatSay(495, "Here are the places we can gate to:")
        all_locations_text = ', '.join([item for sublist in all_locations for item in sublist])
        items_list = all_locations_text.split(',')
        chunk_size = 5
        chunks = [items_list[i:i+chunk_size] for i in range(0, len(items_list), chunk_size)]
        for chunk in chunks:
            Misc.Pause(1000)
            Player.ChatSay(1152, ' | '.join(chunk))
        listingGates = False        

def restockReagents():
    #print("Restock Reagents Running")
    resources = [0x0F8C,0x0F88,0x0F7B,0x0F85,0x0F86,0x0F8D,0x0F7A,0x0F84]
    needRestock = False     
    for resource in resources:

        if Items.BackpackCount(resource, -1) < 30:
            needRestock = True
            
    if needRestock == True:
        Player.HeadMessage(0,"Restocking Regs")
        Misc.Pause(350)        
        Mobiles.UseMobile(butlerSerial)
        Misc.Pause(350)
        Gumps.SendAction(989312372, 6)
        Misc.Pause(350)
        
      #
#            restockResource = Items.FindByID(resource, -1, restockContainer)
#            
#            if restockResource:
#                print("Restocking:" + str(restockResource.Name));
#                difference = 30 - Items.BackpackCount(resource,0x0000);
#                Items.Move(restockResource, Player.Backpack, difference)
#                Misc.Pause(delay)
                
def makeReagentBag(targetSerialForTrade):
    
    if Timer.Check('regs:' + str(targetSerialForTrade)) == True:
    
        print("Sorry, you already asked for a reg bag recently. Yousa can ask again later.");
    else:    
        print("Making Reagent Bag.");
        Player.ChatSay(1152,"Meesa making yousa reagent bag.")
        Misc.Pause(650)
        Player.ChatSay(1152,"You have to be right next to me to get it.")
        resources = [0x0F8C,0x0F88,0x0F7B,0x0F85,0x0F86,0x0F8D,0x0F7A,0x0F84]

        openBank = False
        
        for resource in resources:
            
            if Items.BackpackCount(resource, -1) < 30:
                difference = 30 - Items.BackpackCount(resource,0x0000);
                restockResource = Items.FindByID(resource, -1, restockContainer)
                if restockResource:
                    print("Restocking:" + str(difference) + " of " + str(restockResource.Name));
                    Items.Move(restockResource, Player.Backpack, difference)
                    Misc.Pause(delay)
                    
        Player.ChatSay(1152,'[organizeme')    
        Misc.Pause(1000)
        
        reagentBag = Items.FindByName('Reagents',-1,Player.Backpack.Serial,1,False)
        if reagentBag:
            Items.Move(reagentBag,targetSerialForTrade,1)
            Misc.Pause(1000)
            tradeList = Trade.TradeList()
            if len(tradeList) > 0:
                trade = Trade.TradeList()[0]
                print(trade)
                Trade.Accept(trade.TradeID,True)
                
        else:
            print("ERROR: No Reagent Bag found.");
            
def checkManaAndMed():
        while Player.Mana < 50:
            Player.ChatSay(1152,"Meesa Meditating... one sec!")
            Player.HeadMessage(280,'Meditating. ')
            Player.UseSkill("Meditation")
            Misc.Pause(3000)

    
def checkForGhostPlayersAndRezThem():
    checkManaAndMed()
    mobileFilter = Mobiles.Filter()
    mobileFilter.Enabled = True
    mobileFilter.RangeMin = -1
    mobileFilter.RangeMax = 8
    mobileFilter.CheckLineOfSight = True
    mobileFilter.IsGhost = True  
    mobileFilter.Notorieties = List[Byte](bytes([1,2])) 

    foundMobiles = Mobiles.ApplyFilter(mobileFilter)
    for mobile in foundMobiles:

        if Timer.Check('rez:' + str(mobile.Serial)) == True:
            print("Have a Ghost but not rezzing because already tried to rez recently.")
          
        else:
            checkManaAndMed()
            Spells.CastMagery("Resurrection")
            Misc.Pause(3000)
            Target.TargetExecute(mobile.Serial)
            Timer.Create('rez:' + str(mobile.Serial), gateSpamTimer, "Rez Timer for " + str(mobile.Name) + " is now expired.")
        

def checkForGhostPetsAndRezThem():
    checkManaAndMed()
    mobileFilter = Mobiles.Filter()
    mobileFilter.Enabled = True
    mobileFilter.RangeMin = -1
    mobileFilter.RangeMax = 1
    mobileFilter.CheckLineOfSight = True
    #mobileFilter.IsGhost = True  
    mobileFilter.IsHuman = False
    mobileFilter.Notorieties = List[Byte](bytes([1,2])) 

    foundMobiles = Mobiles.ApplyFilter(mobileFilter)
    #print("DEBUG CheckGhosts:", foundMobiles)
    for mobile in foundMobiles:
        #print(mobile.Name)
        
        if mobile.Hits == 0:
            
            if Timer.Check('rez:' + str(mobile.Serial)) == True:
                print("Have a Ghost but not rezzing because already tried to rez recently.")
              
            else:
                checkManaAndMed()
                
                bandaids = Items.FindByID(0x0E21,-1,Player.Backpack.Serial,1,False)
                if bandaids:
                    Items.UseItem(bandaids)
                    Misc.Pause(650)
                    Target.TargetExecute(mobile)
                    
                Timer.Create('rez:' + str(mobile.Serial), 15000, "Rez Timer for " + str(mobile.Name) + " is now expired.")
            
    
def checkForLowHealthPlayersAndHealThem():
    checkManaAndMed()
    mobileFilter = Mobiles.Filter()
    mobileFilter.Enabled = True
    mobileFilter.RangeMin = -1
    mobileFilter.RangeMax = 8
    mobileFilter.CheckLineOfSight = True
    mobileFilter.IsGhost = False  
    mobileFilter.Notorieties = List[Byte](bytes([1,2])) 

    foundMobiles = Mobiles.ApplyFilter(mobileFilter)

    mobileList = []
    for mobile in foundMobiles:

        mobileSerial = mobile.Serial
        mobileName = mobile.Name
        if mobile.Hits < mobile.HitsMax or mobile.Poisoned == True:
            mobileList.append([mobile, mobile.Hits, mobile.Poisoned])

    mobileList = sorted(mobileList, key=lambda x: x[1])

    mobileList = sorted(mobileList, key=lambda x: not x[2], reverse=True)

    
    if Player.Hits < (Player.HitsMax * 0.90) or Player.Poisoned == True:
            checkManaAndMed()
            if (Player.Poisoned == True):
                if Target.HasTarget():
                    Target.Cancel()
                Player.HeadMessage(280,'Curing. ')
                Spells.CastMagery("Cure")
                Misc.Pause(1000)
                Target.TargetExecute(Player.Serial)
            
            if (Player.Hits < Player.HitsMax * 0.90):
                if Target.HasTarget():
                    Target.Cancel()
                Player.HeadMessage(280,'Healing. ')
                Spells.CastMagery("Greater Heal")
                Misc.Pause(1000)
                Target.TargetExecute(Player.Serial)
                
    if mobileList:
        for injuredMobile in mobileList:
            if injuredMobile[0].Hits >= 1:
                Player.HeadMessage(280,'Injured: ' + injuredMobile[0].Name )
                restockReagents()
                if injuredMobile[0].Poisoned == True:
                    if Target.HasTarget():
                        Target.Cancel()
                    Player.HeadMessage(280,'Curing. ')
                    #Spells.CastMagery("Cure")
                    #Misc.Pause(1000)
                    #Target.TargetExecute(injuredMobile[0])
                    Spells.CastMagery("Cure",injuredMobile[0],3000)
                
                if injuredMobile[0].Hits < injuredMobile[0].HitsMax:
                    if Target.HasTarget():
                        Target.Cancel()
                    Player.HeadMessage(280,'Healing. ')
                    #Spells.CastMagery("Greater Heal")
                    #Misc.Pause(1000)
                    #Target.TargetExecute(injuredMobile[0])
                    Spells.CastMagery("Greater Heal",injuredMobile[0],3000)
                   

                break                

            
                
def checkForLowHealthPetsAndHealThem():
    checkManaAndMed()
    mobileFilter = Mobiles.Filter()
    mobileFilter.Enabled = True
    mobileFilter.RangeMin = -1
    mobileFilter.RangeMax = 8
    mobileFilter.CheckLineOfSight = True
    mobileFilter.IsGhost = False  
    mobileFilter.IsHuman = False
    mobileFilter.Notorieties = List[Byte](bytes([1,2])) 

    foundMobiles = Mobiles.ApplyFilter(mobileFilter)

    mobileList = []
    for mobile in foundMobiles:

        mobileSerial = mobile.Serial
        mobileName = mobile.Name
        if mobile.Hits < mobile.HitsMax or mobile.Poisoned == True:
            if mobile.Hits >= 1:
                mobileList.append([mobile, mobile.Hits, mobile.Poisoned])

    mobileList = sorted(mobileList, key=lambda x: x[1])

    mobileList = sorted(mobileList, key=lambda x: not x[2], reverse=True)

    
    if Player.Hits < (Player.HitsMax * 0.90) or Player.Poisoned == True:
            checkManaAndMed()
            if (Player.Poisoned == True):
                if Target.HasTarget():
                    Target.Cancel()
                Player.HeadMessage(280,'Curing. ')
                Spells.CastMagery("Cure", Player.Serial, 3000)
                #Misc.Pause(1000)
                #Target.TargetExecute(Player.Serial)
            
            if (Player.Hits < Player.HitsMax * 0.90):
                if Target.HasTarget():
                    Target.Cancel()
                Player.HeadMessage(280,'Healing. ')
                Spells.CastMagery("Greater Heal", Player.Serial, 3000)
                #Misc.Pause(1500)
                #Target.TargetExecute(Player.Serial)
                
    if mobileList:
        for injuredMobile in mobileList:
            try:
                if injuredMobile[0].Hits >= 1:
                        
                    Player.HeadMessage(280,'Injured: ' + injuredMobile[0].Name, injuredMobile.Hits, injuredMobile.HitsMax )
                    restockReagents()
                    if injuredMobile[0].Poisoned == True:
                        if Target.HasTarget():
                            Target.Cancel()
                        Player.HeadMessage(280,'Curing. ')
                        Spells.CastMagery("Cure",injuredMobile[0], 3000)
                        #Misc.Pause(1000)
                        #Target.TargetExecute(injuredMobile[0])
                    
                    if injuredMobile[0].Hits < injuredMobile[0].HitsMax:
                        if Target.HasTarget():
                            Target.Cancel()
                        Player.HeadMessage(280,'Healing. ')
                        #Spells.CastMagery("Greater Heal")
                        Spells.CastMagery("Greater Heal",injuredMobile[0], 3000)
                        #Misc.Pause(1000)
                        #Target.TargetExecute(injuredMobile[0])

                    break                
            except:
                print("FAILED WITH INJURED MOBILE HITS CHECK")
                print("Debug:", injuredMobile)
def gate_manager(total_gates):
    global listingGates
    #print("Gate Manager is now running.")
    Timer.Create('spamTimer', 10)
    Misc.Pause(20)
    print("Opening Chests to Start.")
    openAllChests()
    while True:
        #print("Gate Manager is looping.")
        Journal.Clear()
        Misc.Pause(1000)
        checkManaAndMed()
        restockReagents()
        checkForGhostPlayersAndRezThem()
        checkForLowHealthPlayersAndHealThem()
        
        checkForGhostPetsAndRezThem()
        checkForLowHealthPetsAndHealThem()

        if Timer.Check('spamTimer') == False:
            #print("SpamTimer is false. Starting Thread.")
            thread = threading.Thread(target=execute_lm_gate, args=(total_gates,))
            thread.start()
            Misc.Pause(500)
            Timer.Create('spamTimer', 30000)
        #else:
            #print("SpamTimer is true, so not making new thread.")

        listGates = Journal.GetLineText("List Gates", True)
        if not listGates:
            listGates = Journal.GetLineText("list gates", True)

        if listGates:
            splitLine = listGates.split(':')
            name = splitLine[0]
            if name != Player.Name and name not in ignoreMobileList:
                found_guild_gate = Journal.SearchByType('list gates', 'Guild') or Journal.SearchByType('List Gates', 'Guild')
                print(name + " has asked to list the gates.")
                all_locations = [locations_classic_dungeons, locations_exotic_dungeons, locations_cities]
                thread = threading.Thread(target=listTheGates, args=(all_locations,found_guild_gate))
                thread.start()
                Journal.Clear()
                
        regs = Journal.GetLineText("regs", True)

        if not regs:
            regs = Journal.GetLineText("REGS", True)
        if not regs:
            regs = Journal.GetLineText("Regs", True)
        if not regs:
            regs = Journal.GetLineText("Reagents", True)
        if not regs:
            regs = Journal.GetLineText("reagents", True)
        if regs:
            
            splitLine = regs.split(':')
            
            if splitLine[0] != Player.Name:
                name = splitLine[0]
                
                mobileFilter = Mobiles.Filter()
                mobileFilter.Enabled = True
                mobileFilter.RangeMin = -1
                mobileFilter.RangeMax = 8
                mobileFilter.CheckLineOfSight = True
                mobileFilter.IsGhost = False  
                mobileFilter.Notorieties = List[Byte](bytes([1,2])) 
                mobileFilter.Name = name
                foundMobiles = Mobiles.ApplyFilter(mobileFilter)

                if foundMobiles:
                    if foundMobiles[0].Serial not in ignoreMobileList:
                        if Player.DistanceTo(Mobiles.FindBySerial(foundMobiles[0].Serial)) > 1:
                            Player.ChatSay(1152,"Sorry, you are too far away for me to give you a bag, come closer and ask again.")
                        else:
                            makeReagentBag(foundMobiles[0].Serial)
                else:
                    print("FAILED TO GET PERSON THAT ASKED FOR REAGENT BAG.")
                    
        lineAndName = Journal.GetLineText("LM", True)
        if not lineAndName:
            lineAndName = Journal.GetLineText("lm", True)
        
        if lineAndName:
            splitLine = lineAndName.split(':')
            if splitLine[0] != Player.Name:
                name = splitLine[0]
                found_guild_gate = Journal.SearchByType('lm', 'Guild') or Journal.SearchByType('LM', 'Guild')
                found_local_gate = Journal.SearchByType('lm', 'Local') or Journal.SearchByType('LM', 'Local')
        
        
        
                total_gates, canGate = check_timer_exists_or_create(name, total_gates, found_guild_gate)
                if canGate == True:
                    Spells.CastMagery("Gate Travel")
                    Misc.Pause(750)
                    if found_guild_gate:
                        Player.ChatGuild("Sure, gating now. Thank you for visiting us!")
                    else:
                        Player.ChatSay(1152, "Sure, gating now. Thank you for visiting us!")
                        
                    Target.WaitForTarget(10000, False)
                    Target.TargetExecute(lmRunebook)
                    total_gates += 1
                    Journal.Clear()

                    
        found_guild_gate = Journal.SearchByType('gate', 'Guild') or Journal.SearchByType('Gate', 'Guild')
        found_local_gate = Journal.SearchByType('gate', 'Local') or Journal.SearchByType('Gate', 'Local')
        
        gate_location = Journal.GetLineText("gate", True)
        if not gate_location:
            gate_location = Journal.GetLineText("Gate", True)
        if gate_location:
            

                
            splitLine = gate_location.split(':')
            name = splitLine[0]
            if name == Player.Name or name == "System":
                Misc.Pause(10)
            else:
                print("Someone said gate that is not the player.")
                if "gate" in gate_location.lower():
                    cleanedLine = splitLine[1].lower().strip()
                    if cleanedLine[0].lower().strip() == 'g':
                        total_gates, canGate = check_timer_exists_or_create(name, total_gates, found_guild_gate)
                        location = splitLine[1].lower().split("gate", 1)[-1].strip()
                        print("They want to be gated to " + location + " and canGate is " + str(canGate))
                        if canGate:
                                
                            
                            if found_guild_gate:
                            
                                execute_send_action('Guild',location, [locations_classic_dungeons, locations_exotic_dungeons, locations_cities])
                            else:
                                execute_send_action('Regular',location, [locations_classic_dungeons, locations_exotic_dungeons, locations_cities])
                        
                            
            Journal.Clear()
            
        repairItemsInChest()
#Player.ChatSay(99,'Please open Meesa Bank')

            
total_gates = 0
listingGates = False
Timer.Create('spamTimer', 1000)  
gate_manager(total_gates)
