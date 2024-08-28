# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description: Donation Coin Buying Bank Bot - Automatically
# buy Donation Coins from players at a specific price, safely,
# at the bank! Yousa gunna be so rich!
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#
donoItemID = 0x0EED
donoHue = 0x0481
donoName = 'Forever Donation Coins'
donoProperties = ['Forever Donation Coins','Blessed', 'Weight:', 'Pure White']

# END CONFIG --------------------------------------------------#

def isDono(item):
    if item.ItemID == 3821 and item.Hue == 1153 :
        return True
    else:
        return False
        
def dumpChecks():
    checks = Items.FindAllByID(0x14F0,0x0034,Player.Backpack.Serial,1,False)
    if checks:
        Misc.Pause(650)
        Player.ChatSay("bank")
        for check in checks:
            Misc.Pause(650)
            Items.Move(check,Player.Bank,1)
        Player.ChatSay("deposit")
        
Player.ChatSay("bank") 
Player.ChatSay("deposit")
while True:
    Misc.Pause(1000)
    dumpChecks()
    
    if Timer.Remaining("donoBuyer") >= 1:
        Misc.NoOperation()
    else:
        Timer.Create("donoBuyer",20000)
        Player.ChatSay(1151,"Buying DONO! Sell me Donation Coins fully automated!")
        Misc.Pause(250)
        Player.ChatSay(1151,"Yousa trade Meesa Dono,meesa give you a check! Paying 275k / 1k Dono!")
        
    if Trade.TradeList():
        for exchange in Trade.TradeList():
            print("Trade:", exchange.NameTrader)
            tradeCont = Items.FindBySerial(exchange.ContainerTrader)
            Items.WaitForContents(tradeCont,1000)
            Items.WaitForProps(tradeCont,1000)
            
            if len(tradeCont.Contains) > 1:
                Player.ChatSay(1151,"Sorry, yousa need ONE stack of da donation coins at a time plez!")
                Misc.Pause(100)
                Trade.Cancel(exchange.TradeID)
                print("Cancelling trade due to multiple items in trade.")
                break
        
            for item in tradeCont.Contains:
                Items.WaitForContents(item,1000)
                Items.WaitForProps(item,1000)
                
                itemIsDono = isDono(item)
                
                if itemIsDono:
                    
                    print(str(item.Name) +" is Dono?: " + str(itemIsDono))
                    print("Found " + str(item.Amount) + " donation coins.")
                    donoPrice = 275
                    amountToMakeCheckFor = donoPrice * item.Amount
                    
                    if amountToMakeCheckFor < 5000:
                        Misc.Pause(100)
                        Player.ChatSay(1151,"Sorry, Meesa cant be buyin less than 5000 Meesa Gold worth of Dono :( ")
                        Misc.Pause(100)
                        Player.ChatSay(1151,"We be tryin` again when yousa get a little more! ")
                        Misc.Pause(100)
                        Trade.Cancel(exchange.TradeID)
                        print("Cancelling trade due to too low DONO attempt.")
                        break


                    if amountToMakeCheckFor > 1000000:
                        Misc.Pause(100)
                        Player.ChatSay(1151,"Sorry, Meesa cant be buyin dat much dono at a time! Try less. :( ")
                        Misc.Pause(100)
                        Player.ChatSay(1151,"We be tryin` again when yousa sell a little less at a time! ")
                        Misc.Pause(100)
                        Trade.Cancel(exchange.TradeID)
                        print("Cancelling trade due to too HIGH dono attempt.")
                        break

                        
                    checkInTradeAlready = False
                    checkInTradeAlready = Items.FindByID(0x14F0,0x0034,exchange.ContainerMe,1,False)
                    
                    print(amountToMakeCheckFor)
                    print("debug checkInTradeAlready:", checkInTradeAlready)
                    if checkInTradeAlready == False or checkInTradeAlready == None:
                                
                        Misc.Pause(250)
                        Player.ChatSay("check " + str(amountToMakeCheckFor))
                        Misc.Pause(650)
                        Player.ChatSay("bank")  
                        Misc.Pause(250)  
                        check = Items.FindByID(0x14F0,0x0034,Player.Bank.Serial,1,False)
                        
                        if check:
                            
                            for prop in check.Properties:
                                if 'value' in str(prop):
                                    value = int(str(prop).split(":")[1].replace(",", "").strip())
                                    if value == amountToMakeCheckFor:
                                        
                                        Items.Move(check,exchange.ContainerMe,1)
                                        Player.ChatSay(1151,"Okay, that looks about right! Meesa Accept!")
                                        Trade.Accept(exchange.TradeID,True)
                                    
                else:
                    print("TRADE HAS NON DONO ITEM. CANCELLING TRADE.")
                    Trade.Cancel(exchange.TradeID)
                    Player.ChatSay(1151,"Sorry, Yousa cant be putting in non dono items in da trade silly!")
                    dumpChecks()
                    break
                
