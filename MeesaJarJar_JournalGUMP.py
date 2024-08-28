# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# --WORK IN PROGRESS ------------------------------------------#
# -------------------------------------------------------------#
# Description: Journal Filtering System 
# Filter Journal Types and Other Options, in a resizeable gump.
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#


# END CONFIG --------------------------------------------------#

from System.Collections.Generic import List
from System import String
from System import Int32 as int
from datetime import datetime
from collections import OrderedDict
import os

gumpNumber = 4554577
resizing = False;
startX = 100
startY = 0
resizeWidth = 200
resizeHeight = 400
startMousePosX = 0
startMousePosY = 0
lastWidth = 200
lastHeight = 400
journalListStrings = []
journalListStringsWithTime = []
showFilters = True;
showChat    = True;
debugON     = False;
auctioneers_list = ["Fay", "Shane", "Tony", "Little Bo Peach", "Nevada", "Tonks", "Thundarr", "Dragon Rider", "bAdNaMe", "Phnogg", "RubberDucky", "G-", "TheRiddler"]
filterChatTypes = OrderedDict([
    ("System", True),    
    ("Regular", True),
    
    ("Guild", True),
    ("Alliance", True),    
    
    #("Yell", True),       
    #("Whisper", True),
 
    ("Emote", False),
    ("Label", False),
    ("Focus", False),
    ("Spell", False),

    ("Party", False),
    #("Encoded", True),
    #("Special", True)
])

chat_types = list(filterChatTypes.keys())

filterChatTypesAdditional = {
    "Player": True,
    "Auctioneers": True,
    "Spam": True

}

chat_types_additional = list(filterChatTypesAdditional.keys())

def getJournalFiltered():
    global journalListStrings, journalListStringsWithTime
    journalList = Journal.GetJournalEntry(-1)
    
    journalList = journalList[::-1]
 
    journalListStrings = []
    journalListStringsWithTime = []
    for journalEntry in journalList:
        
        hideEntry = False
        fixedType = None
        
        if journalEntry.Type == 'Yell' or journalEntry.Type == 'Whisper' or journalEntry.Type == 'Regular' or journalEntry.Type == 'Special' or journalEntry.Type == 'Encoded':
            
            if filterChatTypes['Regular'] == False:
                hideEntry = True
                
        else:
            if filterChatTypes[journalEntry.Type] == False:

                hideEntry = True
              
        if filterChatTypesAdditional['Player'] == False:
            if journalEntry.Name == Player.Name:
                hideEntry = True
        
        if [journalEntry.Type, journalEntry.Color, journalEntry.Name, journalEntry.Serial, journalEntry.Text] in journalListStrings and filterChatTypesAdditional['Spam'] == False :    
            hideEntry = True
                
        if journalEntry.Name in auctioneers_list and filterChatTypesAdditional['Auctioneers'] == False :
            hideEntry = True
        if len(journalEntry.Text.strip()) == 0:
            hideEntry = True
            
        if hideEntry == False:
            
            
            if journalEntry.Type == 'Yell' or journalEntry.Type == 'Whisper' or journalEntry.Type == 'Regular' or journalEntry.Type == 'Special' or journalEntry.Type == 'Encoded':
                fixedType = 'Regular'  
                
            if fixedType != None:
                journalListStrings.append([fixedType, journalEntry.Color, journalEntry.Name, journalEntry.Serial, journalEntry.Text]);
                journalListStringsWithTime.append([fixedType, journalEntry.Color, journalEntry.Name, journalEntry.Serial, journalEntry.Text, journalEntry.Timestamp]);
            else:
                journalListStrings.append([journalEntry.Type, journalEntry.Color, journalEntry.Name, journalEntry.Serial, journalEntry.Text]);
                journalListStringsWithTime.append([journalEntry.Type, journalEntry.Color, journalEntry.Name, journalEntry.Serial, journalEntry.Text, journalEntry.Timestamp]);
 
                

def updateGump():
    global debugON, journalListStringsWithTime, showChat, showFilters, lastWidth, lastHeight, updateRate, filterChatTypes, journalListStrings,gumpNumber, resizeWidth, resizeHeight, resizing, startMousePosX, startMousePosY, journalListStrings

    gd = Gumps.CreateGump(True,True,False,False)
    Gumps.AddPage(gd, 0);

    startJournalX = 125
    startJournalY = 25
    filterSpacingHeight = 30;
    if Timer.Check('resizeTimer') == True:  
    
        resizeWidth = lastWidth + (Misc.MouseLocation().X - startMousePosX)
        resizeHeight = lastHeight + (Misc.MouseLocation().Y  - startMousePosY)
        
        #print("lastWidth:", lastWidth, 'lastHeight:', lastHeight, 'resizeWidth:', resizeWidth, 'resizeHeight:', resizeHeight, 'MouseX:', Misc.MouseLocation().X,'MouseY:', Misc.MouseLocation().Y  );
        
        Gumps.AddImageTiled(gd,startJournalX,startJournalY,resizeWidth ,resizeHeight-30,3004)

        gd.buttonid = -1
        
        Gumps.SendAction(gumpNumber, 0)
        Gumps.SendGump(gumpNumber, Player.Serial, 0, 0, gd.gumpDefinition, gd.gumpStrings)  
        
    else:
        updateRate = 750

        filterOptionsStartX = 25
        filterOptionsStartY = 25
        
        countx = 0
        
        if showFilters:
            Gumps.AddImageTiled(gd,5,0,115,430,3504)
            for filterType, filterTypeStatus in filterChatTypes.items():
                
                Gumps.AddLabel(gd,filterOptionsStartX+25,filterOptionsStartY +3 + (filterSpacingHeight * countx),0,filterType)
                
                if filterTypeStatus == False: 
                    Gumps.AddButton(gd,filterOptionsStartX - 15,filterOptionsStartY+ (filterSpacingHeight * countx),9720,9723,1000+countx,1,0)
                else:
                    Gumps.AddButton(gd,filterOptionsStartX - 15,filterOptionsStartY+ (filterSpacingHeight * countx),2152,2153,1000+countx,1,0)
                
                countx = countx + 1

            Gumps.AddImage(gd,-15,-5,10600)
            Gumps.AddImage(gd,55,-5,10602)
            Gumps.AddLabel(gd,15,0,0,"Filters")
            
            Gumps.AddImage(gd,-15,300,10600)
            Gumps.AddImage(gd,55,300,10602)
            Gumps.AddLabel(gd,15,303,0,"Other Filters")
            
            filterOptionsStartX = 25
            filterOptionsStartY = 65
            
            for filterType, filterTypeStatus in filterChatTypesAdditional.items():
                
                Gumps.AddLabel(gd,filterOptionsStartX+25,filterOptionsStartY +3 + (filterSpacingHeight * countx),0,filterType)
                
                if filterTypeStatus == False: 
                    Gumps.AddButton(gd,filterOptionsStartX - 15,filterOptionsStartY+ (filterSpacingHeight * countx),9720,9723,1000+countx,1,0)
                else:
                    Gumps.AddButton(gd,filterOptionsStartX - 15,filterOptionsStartY+ (filterSpacingHeight * countx),2152,2153,1000+countx,1,0)
                
                countx = countx + 1
            
            Gumps.AddImage(gd,-15,430,10600)
            Gumps.AddImage(gd,55,430,10602)
            
            Gumps.AddButton(gd,100,0,5600,5600,3,1,0)
        else:
            Gumps.AddImage(gd,-15,-5,10600)
            Gumps.AddImage(gd,55,-5,10602)
            Gumps.AddLabel(gd,15,0,0,"Show Filters")
            Gumps.AddButton(gd,100,0,5606,5606,3,1,0)
                
        journalEntryHeight = 20
        count = 0
        
        if showChat:
            Gumps.AddImage(gd,125,-5,10600)
            Gumps.AddImage(gd,190,-5,10602)
            Gumps.AddLabel(gd,160,0,0,"Chat")
            Gumps.AddButton(gd,235,0,5600,5600,4,1,0)  
            
            for journalEntry in journalListStringsWithTime:
                
                if startJournalY + (journalEntryHeight * count) < resizeHeight - journalEntryHeight:
                    if debugON == True:
                        
                        Gumps.AddHtml(gd,startJournalX,startJournalY + (journalEntryHeight * count),resizeWidth-25,25,str(journalEntry),True,False)
                    else:
                        dt_object = datetime.utcfromtimestamp(journalEntry[5])
                        
                        
                        Gumps.AddHtml(gd,startJournalX,startJournalY + (journalEntryHeight * count),resizeWidth-25,25,str('[' + dt_object.strftime('%H:%M:%S')) + '] ' + str(journalEntry[2]) + " : " + str(journalEntry[4]),True,False)
                    
                    
                    count = count + 1
  
            Gumps.AddButton(gd, startJournalX + resizeWidth-25,startJournalY + (journalEntryHeight * count), 2095, 2094, 2, 1, 0) #Resize Button
        else:
            Gumps.AddImage(gd,125,-5,10600)
            Gumps.AddImage(gd,190,-5,10602)
            Gumps.AddLabel(gd,160,0,0,"Show Chat")
            Gumps.AddButton(gd,235,0,5606,5606,4,1,0)               
    Gumps.CloseGump(gumpNumber)        
    Gumps.SendGump(gumpNumber, Player.Serial, 0, 0, gd.gumpDefinition, gd.gumpStrings)
       
updateGump()
updateRate = 450
while True:
    Misc.Pause(updateRate)

    gd = Gumps.GetGumpData(gumpNumber)
    #print(gd.buttonid);
    if gd:
        if gd.buttonid == 4:
            if showChat == True:
                showChat = False;
            else:
                showChat = True;
                
        if gd.buttonid == 3:
            if showFilters == True:
                showFilters = False;
            else:
                showFilters = True;
        
        if gd.buttonid == 2:
            updateRate = 100
            Timer.Create('resizeTimer', 2000)
            startMousePosX = Misc.MouseLocation().X
            startMousePosY = Misc.MouseLocation().Y
            
            lastWidth = resizeWidth
            lastHeight = resizeHeight

            gd.buttonid = -1
            
        if gd.buttonid >= 1000 and gd.buttonid <=1999:    

            if gd.buttonid <= (1000 + len(filterChatTypes)-1):
            
                if filterChatTypes[chat_types[gd.buttonid - 1000]] == True:
                    filterChatTypes[chat_types[gd.buttonid - 1000]] = False
                    
                else:
                    filterChatTypes[chat_types[gd.buttonid - 1000]] = True
            else:
                
                if filterChatTypesAdditional[chat_types_additional[gd.buttonid - 1000 - len(filterChatTypes)]] == True:
                    filterChatTypesAdditional[chat_types_additional[gd.buttonid - 1000 - len(filterChatTypes)]] = False
                    
                else:
                    filterChatTypesAdditional[chat_types_additional[gd.buttonid - 1000 - len(filterChatTypes)]] = True

        Gumps.CloseGump(gumpNumber)        
        Gumps.SendGump(gumpNumber, Player.Serial, 0, 0, gd.gumpDefinition, gd.gumpStrings)     
        updateGump()
        getJournalFiltered()