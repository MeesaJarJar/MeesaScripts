# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description: Bid Tracker for Live Auctions!
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#


# END CONFIG --------------------------------------------------#
import time
import re
import random
alliance_guild_party_list = ['[Alliance]', '[Guild]', '[Party]']    
auctioneers_list = ["System:","Fay:", "Shane:", "Tony:", "Little Bo Peach:", "Nevada:", "Tonks:", "Thundarr:", "Dragon Rider:", "bAdNaMe:", "Phnogg", "RubberDucky:", "G-:", "TheRiddler:"]
bid_ignore_list = ["point.","points","pointer","check","Community Auction begins", "Thy current bank balance is", "Bank container has", "stored in credit", "The world will save in", "World save complete", "total of thy purchase", "The hue of that is", "You see:"]

filteredLines = []
goodLines = []

gumpNumber = 99559911
globalCount = 0
currentBid = ""
status = "   Ready!"
usernameColorsInts = {'test': 500}
bidder = None

Journal.Clear()

Player.ChatSay("10k miioonnnhhhhhhhhnnnnn");
Misc.Pause(250);
Player.ChatSay("20k miiiillioonnnhhhhhhnnn");
Misc.Pause(250);
Player.ChatSay("30 k miiiillioonhhhnnnnn");
Misc.Pause(250);
Player.ChatSay("40 K miillioonnnhhhhhhhhnnnnn" );
Misc.Pause(250);
Player.ChatSay("50 K miiiillioonnnhhhhhhhhnnnnn");
Misc.Pause(250);
Player.ChatSay("60 K");
Misc.Pause(250);
Player.ChatSay("70 K");
Misc.Pause(250);
Player.ChatSay("80 K");
Misc.Pause(250);
Player.ChatSay("90 K");
Misc.Pause(250);
Player.ChatSay("100 K");
Misc.Pause(250);
Player.ChatSay("110 K");
Misc.Pause(250);

def rotate_string(s, iterations):
    #("ROTATING STRING");
    if not s:
        return ""
    s = s + " - "
    length = len(s)
    for _ in range(iterations):
        s = s[1:] + s[0]
    return s[:30]
    
def colorDictionaryAdd(username):
    global usernameColorsInts
    if username not in usernameColorsInts:
        usernameColorsInts[username] = random.randint(0, 1000)
    return usernameColorsInts

def processJournal():
    global goodLines, currentBid, usernameColorsInts
    
    bids = []
    journalEntries = Journal.GetJournalEntry(time.time() - 2000000)

    for line in journalEntries:
        
        skipLine = False;
        
        try:
            
            for auctioneer in auctioneers_list:
                if auctioneer.lower() in str(line.Name.lower()) + ":" :
                    skipLine = True;
                    
            for bid_ignore in bid_ignore_list:
                if bid_ignore.lower() in str(line.Text.lower()): 
                    skipLine = True;  
                    
            for alliance_guild_party in alliance_guild_party_list:
                if alliance_guild_party.lower() in str(line.Type.lower()):
                    skipLine = True;  
            
                    
            if skipLine == False:   
                

                bid_pattern = r'\b(\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?(?:\s?[kKmM]?)?)\b'

                match = re.search(bid_pattern, line.Text)
                if match:
                    bid_amount = match.group(1)
                    #print(f"Line: '{line.Text.lower().encode('utf-8')}', Bid: {bid_amount}")


                    if [line.Type, line.Name, line.Text, line.Serial] not in bids:

                        
                        charname = line.Name.lower().strip()

                        colorDictionaryAdd(str(charname));
                        
                        bids.append([line.Type, line.Name, line.Text, line.Serial]);

#                else:
#                    filteredLines.append(line.strip().lower());
#                        
#            else:
#                filteredLines.append(line[1].strip().lower());
                   
        except Exception as e: 
            

            print("******* ERROR ******** Did not process journal line properly. Something failed.");
            print("ERROR:",e)
            Misc.Pause(10)
   
    return bids 

    
def updateGump():
    global goodLines, currentBid, usernameColorsInts
    
    gd = Gumps.CreateGump(True,True,True,False);
    

    Gumps.AddPage(gd, 0);

    tileSizeW = 84

    tileSizeLW = 241

    offsetX = 0
    offsetY = 0
    
    Gumps.AddImage(gd,0,0,1249)
    
    Gumps.AddImage(gd,30,140,1460)
    Gumps.AddImage(gd,30+50,140,1462)

    for y in range(1,5):
        
        
        Gumps.AddImage(gd,30,140 + (y*50),1463)
        Gumps.AddImage(gd,30+50,140 + (y*50),1465)

    Gumps.AddImage(gd,30,375,1466)
    Gumps.AddImage(gd,30+50,375,1468)
    
    textStartX = 75
    textStartY = 150

    textRowPadding = 25
    count = 0
    
    goodLines = processJournal();
    goodLines.reverse();


    for i in range(0,8):
        for x in range(1,7):
            Gumps.AddImage(gd,90+ (x*36),143+ (i*36),39929) 
            
        
        Gumps.AddImage(gd,105 + (x*36),143 + (i*36),39930)  
    
    for chatline in goodLines:
        
        if count < 10:
            
            if str(chatline[1]) + " : " + str(chatline[2]) == currentBid:
                Gumps.AddImage(gd,textStartX,textStartY  + (textRowPadding * count),1756)
                
                Gumps.AddImage(gd,textStartX,textStartY  + (textRowPadding * count)+10,1762)
                
                Gumps.AddImage(gd,textStartX+262,textStartY  + (textRowPadding * count),1757)
                Gumps.AddImage(gd,textStartX+262,textStartY  + (textRowPadding * count)+10,1763)
                Gumps.AddImage(gd,textStartX-55,textStartY  + (textRowPadding * count),1227)
                
            
            if len(str(chatline[1]) + " : " + str(chatline[2])) > 30:
            
                Gumps.AddLabel(gd,textStartX + 60,textStartY + 5 + (textRowPadding * count),usernameColorsInts[chatline[1].lower()],rotate_string(str(chatline[1]) + " : " + str(chatline[2]), int(globalCount)))
            else:
                
                testx = Gumps.AddLabel(gd,textStartX + 60,textStartY + 5 + (textRowPadding * count),usernameColorsInts[chatline[1].lower()],str(chatline[1]) + " : " + str(chatline[2]))
                Gumps.AddTooltip(testx,1) 
                
            Gumps.AddButton(gd, textStartX-30,textStartY + (textRowPadding * count), 1423, 1423, 1000 + count, 1, 0)
            
            Gumps.AddButton(gd, textStartX-5,textStartY + (textRowPadding * count), 1424, 1424, 2000 + count, 1, 0)
            Gumps.AddTooltip(gd,2000) 
            Gumps.AddButton(gd, textStartX + 20,textStartY + (textRowPadding * count), 1425, 1425, 3000 + count, 1, 0)
            
            count+=1;
            

    Gumps.AddImage(gd,100,30,1764)
    
    Gumps.AddLabel(gd,135,45,1152,'Current Highest Bid')

 
    
    Gumps.AddImage(gd,50,75,1755)
    Gumps.AddImage(gd,50+18,75,1756)
    Gumps.AddImage(gd,50+18+270,75,1757)

    
    Gumps.AddImage(gd,50,93,1761)
    Gumps.AddImage(gd,50+18,93,1762)
    Gumps.AddImage(gd,50+18+270,93,1763)
    

    Gumps.AddLabel(gd,115,83,1152, str(currentBid))
    
    Gumps.AddImage(gd,50,30+75,1755)
    Gumps.AddImage(gd,50+18,30+75,1756)
    Gumps.AddImage(gd,50+18+270,30+75,1757)

    
    Gumps.AddImage(gd,50,30+93,1761)
    Gumps.AddImage(gd,50+18,30+93,1762)
    Gumps.AddImage(gd,50+18+270,30+93,1763)
    

    Gumps.AddLabel(gd,155,83+30,1152, str(status))    
    
    Gumps.AddImage(gd,25,410,10600)
    for t in range(1,9):
        
        Gumps.AddImage(gd,25+(35*t),410,10601)
    
    Gumps.AddImage(gd,300,410,10602)
    
    Gumps.AddButton(gd,118,415,40018,40028,4,1,0) # RESET BTN
    Gumps.AddLabel(gd,130,418,0,'RESET') 
    
    Gumps.AddButton(gd,50,415,40018,40028,3,1,0) # PAUSE BTN
    Gumps.AddLabel(gd,62,418,0,'PAUSE')
    
    Gumps.AddButton(gd,220,414,40030,40020,5,1,0) # SOLD BTN
    Gumps.AddLabel(gd,266,417,0,'SOLD')

    Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)

updateGump()

while True:
    Misc.Pause(250)
    globalCount += 1;

    if bidder != '' and bidder != None:
        #Target.SetLast(bidder)
        
        #print("Bidder IS: ", bidder);
        if Timer.Check("bidHeadMessage") == False:

#            line1 = "* HIGHEST BIDDER *"
#            line3 = "\ ||| /"
#            line4 = "\ | /"
#            line5 = "\/"
#            
#            Mobiles.Message(bidder, 62, line1, 6000)
#            Mobiles.Message(bidder, 62, line3, 6000)
#            Mobiles.Message(bidder, 62, line4, 6000)
#            Mobiles.Message(bidder, 62, line5, 6000)
            
            Mobiles.Message(bidder, 62, "Highest\nBidder\n   ||||\n   V", 6000)
            
            
            Timer.Create('bidHeadMessage',4000)
        
        #Player.TrackingArrow(bidder.Position.X-1,bidder.Position.Y-1,True, bidder.Serial)
    #else:
        #print("CLEARING TRACKING ARROW");
        #Player.TrackingArrow(0,0,0,bidder.Serial)   
        #Target.ClearLast()
    gd = Gumps.GetGumpData(gumpNumber)
    if gd:
        
        if gd.buttonid == 3:
            
            if status != "   PAUSED!":
                laststatus = status
                status = "   PAUSED!"
                
            else:
                status = laststatus

            Player.ChatYell(93,status + ' - ' +currentBid )
            gd.buttonid = -1
            updateGump()
                    
        if gd.buttonid == 4:
            status = "RESETTING!"
            Player.ChatYell(93,status )
            gd.buttonid = -1
            currentBid = ""
            status = "   Ready!"
            bidder = None
            Journal.Clear();
            updateGump()
            
        if gd.buttonid == 5:
            status = "   SOLD!"
            Player.ChatYell(37,status + ' - ' +currentBid )
            gd.buttonid = -1
            updateGump()
                    
        if gd.buttonid >= 1000 and gd.buttonid <=1999:

            currentBid = str(goodLines[gd.buttonid-1000][1]) + " : " + str(goodLines[gd.buttonid-1000][2])
            bidder = Mobiles.FindBySerial(goodLines[gd.buttonid-1000][3])
            status = "Accepted Bid. ";
            
            Player.ChatYell(62,status+ ' - ' + currentBid)
            
            gd.buttonid = -1
            updateGump()

        if gd.buttonid >= 2000 and gd.buttonid <=2999:

            currentBid = str(goodLines[gd.buttonid-2000][1]) + " : " + str(goodLines[gd.buttonid-2000][2])
            bidder = Mobiles.FindBySerial(goodLines[gd.buttonid-2000][3])
            status = "Going Once";
            Player.ChatYell(52,status+ ' - ' + currentBid)
            gd.buttonid = -1
            updateGump()
            
        if gd.buttonid >= 3000 and gd.buttonid <=3999:
    
            currentBid = str(goodLines[gd.buttonid-3000][1]) + " : " + str(goodLines[gd.buttonid-3000][2])
            bidder = Mobiles.FindBySerial(goodLines[gd.buttonid-3000][3])
            status = "Going Twice";
            Player.ChatYell(42,status + ' - ' + currentBid)
            gd.buttonid = -1
            updateGump()    
            
    if Timer.Check("refreshJournal") == False:
        
        updateGump()
        
        Timer.Create("refreshJournal",1000)

