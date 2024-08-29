# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description: Meesa Rune Atlas
# -------------------------------------------------------------#

#  - Easy, automated traveling by recalling or gating used exclusively 
# with the Lincoln Mallmorial Rune Library on the UOForever Server.

# You MUST have MeesaAtlas*.pkl file in your Scripts folder alongside this script.
# You MUST have the script added to the Scripting -> Python tab of Razor Enhanced
# You MUST have the “Meesa Runebook”, given to you by Meesa Jar Jar ingame, and it must remain in your mainbackpack(not a subcontainer), untouched with exception of adding your “home” rune, named “home”, to the book.
# OR -- 
# At the front of Lincoln Mallmorial (One Screen East of Brit Moongate) there is a Red booked called Meesa LM Runebook
# You may create a copy of this book using a Runebook Copy Pen or Manually make the book yourself
# Your runes in a created book must be an EXACT MATCH to the runebook at LM for this to work, down to the color
# ------------------------------
#Simply search for a location, book name, or mob type, and then select a location to travel to! 

#Your character will automatically move to the selected Runebook,open it, and select the correct rune for you!

#If you are not at Lincoln Mallmorial, you will automatically be recalled or gated back to the library and then to your selected destination. 

# START CONFIG ------------------------------------------------#
atlasVersion = 427
scriptVersion = 05152024.01

# END CONFIG --------------------------------------------------#

import re
import random
import clr
import os
import System
import pickle
import math
import MeesaJarJar_JarJarAndDinoDNAIcons
clr.AddReference("System.Drawing")
from System.Collections.Generic import List
from System import Int32 as int
bgnum = 398
gumpid = 656648

class Atlas:
    def __init__(self):
        self.books = []
        self.Page = 1
        self.selected_book = None
        self.selectedRecall = True
        self.runeSearchText = ''
        self.titleSearchText = ''
        self.selectedFilter = 'book'
        self.meesaHome = ''
        self.meesaBank = ''
        self.meesaLM = ''
        self.meesaLMRunebook = None
        self.rune_history = [] 
        self.homeRune = None
        self.transparent = False 
        self.useRecallScrolls = False
        
    def debugg(self):

        self.print_all_entries()
    
    def lastPage(self):
       
        self.Page = (len(self.books) // 10) + 1
        
    def firstPage(self):
        self.Page = 1
        
    def decrease_page(self):
        if self.Page > 1:
            self.Page -= 1

    def increase_page(self):
        max_page = len(self.books) // 10
        if len(self.books) % 10 != 0:
            max_page += 1  
        if self.Page < max_page:
            self.Page += 1
        
    def add_book(self, LM, book_serial, book_name, mapped_numbers, sublist):  
        it = Items.FindBySerial(book_serial)
        itHue = 0
        if it:
            itHue =it.Hue 
  
        self.books.append({"hue": itHue, "LM": LM, "serial": book_serial, "name": book_name, "mapped_numbers": mapped_numbers, "sublist": sublist})

    def print_books_and_serials(self):
        print("Index - Book Serial")
        for index, book in enumerate(self.books):
            print(f"{index} - {book['serial']}")
            
    def remove_unicode(self,input_string):
        cleaned_string = re.sub(r'[^\x00-\x7F]+', '', input_string)
        cleaned_string = re.sub(r'[^A-Za-z]+', '', cleaned_string)
        return cleaned_string
    
    def print_all_entries(self):
        all_entries = []
        
        for book in self.books:
            for index, number in enumerate(book["mapped_numbers"]):
                all_entries.append(f"{book['name']} - Location {number}: {book['sublist'][index]}")

    def sort_books_by_name(self):
        self.books = sorted(self.books, key=lambda x: x['name'])
        
    def libraryStats(self):
        bookCount = 0
        runeCount = 0
        cc = 0
        for book in self.books:
            bookCount += 1
            proceed = True

            for rune in book["sublist"]:
                if proceed == False:
                    break

                
                if str(rune).lower() != str('empty'):  
                    runeCount += 1
                    
                if str(rune).lower() == str('empty'):
                    proceed = False
                    cc = cc + 1
                    
                
        return bookCount, runeCount

    def atlas_check_for_map_command(self):
        
        if Misc.ReadSharedValue('Atlas_Go') == True:
            
            Misc.SetSharedValue("Atlas_Go",False)
            tarSerial = Misc.ReadSharedValue("Atlas_Go_Serial")
            tarName = Misc.ReadSharedValue("Atlas_Go_Name")
            tarX = Misc.ReadSharedValue("Atlas_Go_RuneX")
            tarY = Misc.ReadSharedValue("Atlas_Go_RuneY")
            
            atlas.select_book_by_serial(tarSerial)
            
            distance = math.sqrt((Player.Position.X - lmrloc[0])**2 + (Player.Position.Y - lmrloc[1])**2 + (Player.Position.Z - lmrloc[2])**2)
            print("in atlas_check_for_map_command and distance is:", distance)
            if distance > 15:
                print("Calling recallMeesaLMRRunebook 0 to get to LMR ")
                atlas.recallMeesaLMRunebook(0)
                Misc.Pause(1500)
                print("in atlas_check about to navigate to safe spot after recalling to LM")
                navigate_to(1396,1965)
            else:
                print("Walking to LMR position because we are distance:", distance)
                navigate_to(1396,1965)
                
            print("Trying to find the book.")
            book = Items.FindBySerial(atlas.selected_book["serial"])
            if book:
                
                if book.Position.Z > 26: 
                    
                    zFloor = 27
                else:
                    zFloor = 7
                    
                if zFloor == 27:
                    print("Book is upstairs in atlas_check_for_map_command")
                    atlas.goUpstairs()
                    Misc.Pause(650)
                else:
                    print("Book is downstairs in atlas_check_for_map_command")
                print("Going to book now in atlas_check_for_map_command")
                navigate_to(book.Position.X,book.Position.Y)

                Misc.Pause(250)

                namesx = extractBookLocationNames(tarSerial)

                foundName = False
                count = 0
                for myName in namesx:
                    
                    pattern = re.compile(r'[\W_]+')

                   
                    if re.sub(pattern, '', str(myName)) == re.sub(pattern, '', str(tarName)):
                        foundName = True
                        print("About to call atlas.recallOrGate in atlas_check_for_map_command")
                        atlas.recallOrGate(atlas.selected_book, count)
                        pass
                    count = count + 1  
            Gumps.SendAction(gumpid,0)

    def select_book(self, book_name):
        for book in self.books:
            if book["name"] == book_name:
                self.selected_book = book
                break  
                
    def select_book_by_serial(self, serial):
        self.debugg()
        for book in self.books:
            
            if book["serial"] == serial:
                self.selected_book = book
                break 
                
    def goUpstairs(self):
        count = 0
        PathFinding.PathFindTo(1400,1956,7)
        navigate_to(1400,1956)
        
        PathFinding.PathFindTo(1395,1956,27)
        navigate_to(1395,1956)

                
    def recallOrGate(self, selected_book, button_index):
            canContinue = True
            if atlas.selectedRecall:
                action = 5 + (button_index * 6)  
                if atlas.useRecallScrolls:
                    action = 2 + (button_index * 6) 
            else:
                action = 6 + (button_index * 6)

            if atlas.selectedRecall == True:
                if Player.Mana < 11:
                    Player.HeadMessage(33,"You do not have enough mana. Cancelling request, try again." )
                    canContinue = False
                    
            if atlas.selectedRecall == False:
                if Player.Mana < 50:
                    canContinue = False
                    Player.HeadMessage(33,"You do not have enough mana. Cancelling request, try again." )
            atlas.select_book(selected_book)
            self.rune_history.append([atlas.selected_book,int(button_index), atlas.selected_book['sublist'][int(button_index)]])

            max_history_size = 10 
            if len(self.rune_history) > max_history_size:
                self.rune_history = self.rune_history[:max_history_size] 
            if canContinue:
                    
                if(selected_book["LM"] ):
                

                    distance = math.sqrt((Player.Position.X - lmrloc[0])**2 + (Player.Position.Y - lmrloc[1])**2 + (Player.Position.Z - lmrloc[2])**2)
                    if distance > 50:
                        print("In recallOrGate but the distance to LM is over 50, so recall to LM")
                        print("DISTANCE IS : ", distance)
                        atlas.recallMeesaLMRunebook(0)
                        Misc.Pause(1500)

                        navigate_to(1396,1965)
                    else:
                        print("Distance to lmrloc is less than 50, Distance:", distance)


                    book = Items.FindBySerial(selected_book["serial"])
                    if book:
                        
                        if book.Position.Z > 26: 
                            
                            zFloor = 27
                        else:
                            zFloor = 7
                            
                        if zFloor == 27 and Player.Position.Z == 7:
                            atlas.goUpstairs()
                            Misc.Pause(650)
                        print("navigate_to the book position is called in recall or gate funct")
                        if Player.DistanceTo(book) >= 2:
                            navigate_to(book.Position.X,book.Position.Y)
  
                        
                    else: 
                        print("FAILED TO FIND LM RUNEBOOK AT LM")   
                
                
                if atlas.useRecallScrolls:
                    recallScroll = Items.FindByID(0x1F4C,0x0000,Player.Backpack.Serial,1,False)
                    if recallScroll:
                        Misc.Pause(650)
                        Items.Move(recallScroll,selected_book["serial"],1)
                        
                Misc.Pause(650)
                Items.UseItem(selected_book["serial"]) 
                Misc.Pause(100)
                Gumps.WaitForGump(1431013363, 10000)
                Gumps.SendAction(1431013363, action)
                if atlas.selectedRecall == False:
                    Misc.Pause(3000)
                    gate = Items.FindByID(0x0F6C,0x0000,-1,3,False) 
                    if gate:
                      
                        Items.UseItem(gate) 
                        Misc.Pause(250)
                        if  3716879466 in Gumps.AllGumpIDs():
                            Gumps.SendAction(3716879466,1)
                        
                    else:
                        print("GATE NOT FOUND")
            closeRunebook()
            Gumps.SendAction(gumpid,0)
            
    def filter_books_by_search(self, search_string):
        search_lower = search_string.lower()
        filtered_books = []
        for book in self.books:
            
            if atlas.selectedFilter == 'book':
                if search_lower in book["name"].lower():
                    filtered_books.append(book)
            elif atlas.selectedFilter == 'rune':
                for entry in book["sublist"]:
                    if search_lower in str(entry).lower():
                        filtered_books.append(book)
                        break
        return filtered_books

    def select_books_by_search_text(self):

        if atlas.selectedFilter == 'book':
            if not self.titleSearchText.strip():
                return self.books
            return self.filter_books_by_search(self.titleSearchText)
            
        elif atlas.selectedFilter == 'rune':
            if not self.runeSearchText.strip():
                return self.books
            return self.filter_books_by_search(self.runeSearchText)  
            
        def sort_books_by_location(self):
            self.books = sorted(self.books, key=lambda x: (x['location']['x'], x['location']['y']))  


    def sort_item_list_by_position(self, itemList):
        itemList.sort(key=lambda item: (item.Position.X, item.Position.Y, item.Position.Z))
        
    def recallMeesaLMRunebook(self, index):
        print("THIS PORTION SHOULD GET YOU TO LM IF YOU ARE NOT THERE.")
        canContinue = True
        if atlas.selectedRecall == True:
            if Player.Mana < 11:
                Player.HeadMessage(31,"You do not have enough mana. Cancelling request, try again." )
                canContinue = False
        if atlas.selectedRecall == False:
            if Player.Mana < 50:
                Player.HeadMessage(31,"You do not have enough mana. Cancelling request, try again." )
                canContinue = False
 
        lmr = None 
        try:

            lmrSerial = int(self.meesaLMRunebook) if isinstance(self.meesaLMRunebook, str) else self.meesaLMRunebook
            lmr = Items.FindBySerial(lmrSerial)
        except:

            print(atlas.meesaLMRunebook)
        
        if lmr and canContinue: 
            Misc.Pause(650)
            Items.UseItem(lmr)
            Misc.Pause(100)
            Gumps.WaitForGump(1431013363, 650)
            if atlas.selectedRecall:
                action = 5 + (index * 6)  
                if atlas.useRecallScrolls:
                    action = 2 + (index * 6)      
            else:
                action = 6 + (index * 6)

            Gumps.SendAction(1431013363, action)

            while Journal.Search('needs time to'):
                Journal.Clear()
                Misc.Pause(650)
                
                Items.UseItem(lmr)
                Misc.Pause(100)
                Gumps.WaitForGump(1431013363, 650)
                Gumps.SendAction(1431013363, action) 
                
            if atlas.selectedRecall == False:
                chestIDS = [0x09AB, 0x0E40, 0x0E41, 0x0E42, 0x0E43, 0x0E7C, 0x16F4, 0x16F5, 0x1BC8, 0x1BC9, 0x1BCA, 0x1BCB, 0x1BCC, 0x1BCD, 0x1BCE, 0x1BCF, 0x22AC, 0x22AD, 0x22AE, 0x22AF, 0x22B0, 0x22B1, 0x2CBF, 0x2CC0, 0x2CC1, 0x2CC2, 0x2DF1, 0x2DF2, 0x2DF3, 0x32C3, 0x32CC, 0x32CD, 0x32CE, 0x32CF, 0x32D0, 0x32D1, 0x32D2, 0x32EF, 0x4910, 0x4911, 0x5365, 0x5536, 0x5537, 0x67DF, 0x67E0]
                Misc.Pause(3000)
                gate = Items.FindByID(0x0F6C,0x0000,-1,1,False) 
                if gate:
                    Items.UseItem(gate) 
                    if  3716879466 in Gumps.AllGumpIDs():
                        Gumps.SendAction(3716879466,1)

                else:
                    print("GATE NOT FOUND")
            
        else:
            print("FAILED TO RECALL! CHECK RUNEBOOK!")
            
        Misc.Pause(100)
        closeRunebook()
        print("NOW THE PLAYER SHOULD BE AT LINCOLN MALLMORIAL")

        
    def sort_books_by_name(self):
        self.books = sorted(self.books, key=lambda x: x['name'])
        
    def findLMRunebook(self):  
        playerRunebooks = Items.FindAllByID(0x22C5,0x0846,Player.Backpack.Serial,1,False)
        for rb in playerRunebooks:
            if rb.Name == 'Meesa LM Runebook':
                atlas.meesaLMRunebook = int(rb.Serial)
                atlas.homeRune = getRunebookHomeIndex(rb.Serial)
                break
                
        closeRunebook()
                
def numToBytes(num, size):
    return list(bytearray(int(num).to_bytes(size, byteorder='big')))

def sort_item_list_by_position(itemList):
    itemList.sort(key=lambda item: (item.Position.X, item.Position.Y, item.Position.Z)) 
    return itemList
    
def map_locations_to_numbers(locations):
    mapped_numbers = []
    for i in range(len(locations)):
        number = 5 + (i * 6)
        mapped_numbers.append(number)
    return mapped_numbers

def closeRunebook():
    if Gumps.AllGumpIDs():
        currentGumps = Gumps.AllGumpIDs()
        ALLGUMPIDS = [gumpID for gumpID in currentGumps]
        if 1431013363 in ALLGUMPIDS:
            Gumps.SendAction(1431013363, 0)
            
class Point2D:
    def __init__(self, x, y):
        self.X = x
        self.Y = y

def alternate_direction(direction):
    if direction in ['North', 'South']:
        return 'East' if Player.Position.X % 2 == 0 else 'West'
    else:
        return 'North' if Player.Position.Y % 2 == 0 else 'South'

def navigate_to(x_target, y_target):
    print("Navigating To:", x_target, y_target)
    failure_count = 0 

    while True:
        current_pos = Player.Position
        dx = x_target - current_pos.X
        dy = y_target - current_pos.Y

        if abs(dx) > abs(dy):
            primary_direction = 'East' if dx > 0 else 'West'
        else:
            primary_direction = 'South' if dy > 0 else 'North'

        direction = primary_direction if failure_count < 3 else alternate_direction(primary_direction)

        expected_pos = Point2D(
            current_pos.X + (1 if direction == 'East' else -1 if direction == 'West' else 0),
            current_pos.Y + (1 if direction == 'South' else -1 if direction == 'North' else 0)
        )

        move_success = Player.Walk(direction)
        new_pos = Player.Position
        if not move_success or (new_pos.X != expected_pos.X or new_pos.Y != expected_pos.Y):
            failure_count += 1
            continue
        else:
            failure_count = 0

        if new_pos.X == x_target and new_pos.Y == y_target:
            break
  
            
def load_atlas(filename):
    try:
        with open(filename, 'rb') as f:
            atlas = pickle.load(f)
        print(f"Atlas loaded from {filename}")
        if not hasattr(atlas, 'rune_history'):
            atlas.rune_history = []
        return atlas
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return None
    
def rgb_to_hue(r,g,b):
    #r, g, b = rgb
    max_color = max(r, g, b)
    min_color = min(r, g, b)
    if max_color == min_color:
        return 0

    delta = max_color - min_color

    if max_color == r:
        hue = (g - b) / delta
    elif max_color == g:
        hue = 2 + (b - r) / delta
    else:
        hue = 4 + (r - g) / delta

    hue *= 60
    if hue < 0:
        hue += 360

    return int(hue)   
    

    
    
White = 1152
Black = 2999
Peach = 2084
Orange = 42
Yellow = 53
Skin = 50
Red = 33


dinodnaimage = MeesaJarJar_JarJarAndDinoDNAIcons.dinodnaimage
jarjarimage = MeesaJarJar_JarJarAndDinoDNAIcons.jarjarimage
    
    
def toggle_gump_state():
    global minimized, bigX, bigY, littleX, littleY, gd
    currentX, currentY = gd.x, gd.y  

    if minimized:
        
        minimized = False
        littleX, littleY = currentX, currentY  
        CUO.MoveGump(gumpid,bigX,bigY)

    else:
        
        minimized = True
        bigX, bigY = currentX, currentY  
        CUO.MoveGump(gumpid,littleX,littleY)
        

    updateGump() 
    
    
def updateGump():

    offsetX = 200
    offsetY = 200
    if minimized == True:
        
        
        gd = Gumps.CreateGump(True,True,False,False)
        Gumps.AddPage(gd, 0);
        offsetDinoDNAX = 170
        offsetDinoDNAY = 275
        Gumps.AddBackground(gd,offsetDinoDNAX,offsetDinoDNAY,125,140,420)
        Gumps.AddBackground(gd,25+offsetX,85+offsetY,65,65,420)
        
        Gumps.AddButton(gd,35+offsetX,90+offsetY,11047,11047,95,1,0)
        Gumps.AddLabel(gd,53+offsetX,95+offsetY,33,"LM")

        Gumps.AddLabel(gd,40+offsetX,106+offsetY,1152,"Rune")
        
        Gumps.AddLabel(gd,39+offsetX,119+offsetY,1152,"Atlas")

        for loc in dinodnaimage:
            Gumps.AddImage(gd,int(loc[0] + offsetDinoDNAX),int(loc[1]+ offsetDinoDNAY),6000, loc[2])
            
        offsetJarJarX = 225
        offsetJarJarY = 345
        for loc in jarjarimage:
            Gumps.AddImage(gd,int(loc[0] + offsetJarJarX),int(loc[1]+ offsetJarJarY),6000, loc[2])
                    
        if minimized:    
            try:
                Gumps.SendGump(int(gumpid), Player.Serial, littleX, littleY, gd.gumpDefinition, gd.gumpStrings)
            except:
                    Misc.Pause(1)

        
        else:
            try:
                Gumps.SendGump(int(gumpid), Player.Serial, bigX, bigY, gd.gumpDefinition, gd.gumpStrings)
            except:
                    Misc.Pause(1)
 
    else:

        filtered_books = atlas.select_books_by_search_text()
            
        gd = Gumps.CreateGump(True,True,False,False)
        Gumps.AddPage(gd, 0)
        fastClickButtonsY = 385
        if atlas.transparent == False:
            Gumps.AddBackground(gd,-10,385,450,65,40000)
            
        Gumps.AddButton(gd,-5,fastClickButtonsY,5555,5556,8000,1,0)
        Gumps.AddTooltip(gd,1061114,str("Brit Crafting"))        

        Gumps.AddButton(gd,50,fastClickButtonsY,5549,5550,8001,1,0)
        Gumps.AddTooltip(gd,1061114,str("Brit Animal Trainer"))  

        Gumps.AddButton(gd,105,fastClickButtonsY,5569,5570,8002,1,0)
        Gumps.AddTooltip(gd,1061114,str("Brit Mage"))  

        Gumps.AddButton(gd,160,fastClickButtonsY,5563,5564,8003,1,0)
        Gumps.AddTooltip(gd,1061114,str("Brit Healer"))  

        Gumps.AddButton(gd,215,fastClickButtonsY,5589,5590,8004,1,0)
        Gumps.AddTooltip(gd,1061114,str("Brit Moongate")) 

        Gumps.AddButton(gd,270,fastClickButtonsY,5569,5570,8005,1,0)
        Gumps.AddTooltip(gd,1061114,str("Bucs Den Ankh/Healer ** WARNING RED AREA UNSAFE **"))   
        Gumps.AddImage(gd,290,fastClickButtonsY+15,495)

        Gumps.AddButton(gd,325,fastClickButtonsY,5561,5562,8006,1,0)
        Gumps.AddTooltip(gd,1061114,str("Talisman Statue")) 

        Gumps.AddButton(gd,380,fastClickButtonsY,5557,5558,8007,1,0)
        Gumps.AddTooltip(gd,1061114,str("Fire Roof Macro Spot"))  


        if atlas.transparent == True:
            Gumps.AddAlphaRegion(gd,0,0,10,10)
        else:
            Gumps.AddImage(gd,0,0,39923)
            
        
            

        offsetX = 125
        offsetY = 115
        rowHeight = 25
        maxItemsPerPage = 10
        count = 1
        county = 1
        if atlas.selected_book == None:
            Gumps.AddBackground(gd,250,25,150,300,9500)
            welcomeText = '''    <BASEFONT color=#fff1a1 size=7>Hey Yousa!</BASEFONT>
Meesa welcome yousa to da Meesa Rune Atlas for da <BASEFONT color=#ffa1a4 size=7>Lincoln Mallmorial Rune Library! </BASEFONT> At LM Rune Library, yousa can travel to ova<BASEFONT color=#2ac90a size=7> 500 runebooks</BASEFONT>, <BASEFONT color=#2ac90a size=7>5000 runes</BASEFONT> Meesa allow yousa to use da Force to auto find yousa book and rune, from anywhere, and recall or gate to yousa destination, far, far away. Okeday? 

First thingen, yousa gonna mark a rune to yousa <BASEFONT color=#0E5FC2 size=7>home location and be namin’ it ‘Home’</BASEFONT>. Then, yousa drop it on Meesa Runebook! Yousa must have dis runebook in your packy-pack. Make sure yousa don`t move da runes in da book, or <BASEFONT color=#4d070e size=7>yousa gonna break Meesa Atlas very, very bad!</BASEFONT>

Be needin` to go muy-muy fast? Da <BASEFONT color=#ffa1a4 size=7>biggo buttons in da bottom left</BASEFONT> gonna take yousa home or to da bank in no time! 

Yousa just gotta <BASEFONT color=#ffa1a4 size=7>type in da search bars</BASEFONT> on top to finds da book or rune yousa lookin’ for, and BAM- dere it is! Don’t forgets to use da shiny arrows to flip-flip through dem pages n` pages of books and runes.

Meesa Jar Jar makin` dis script to help yousa with all da runnin`round. So no more wastin` time, runnin` yousa feet ragged `cross Britannia. <BASEFONT color=#ffa1a4 size=7>Just point, click, and poof! Yousa there!</BASEFONT>

<BASEFONT color=#450815 size=7>If yousa needin` helps installin` or runnin` da script, yousa should be contactin` BabyBro on da Discord, okeday? He Helpin` yousa with da smooooth sailin`!</BASEFONT>

Biggo thanks to yousa for comin` and may da peace and love be with yousa, always! 

Special thanks to Meesa Wife: <BASEFONT color=#354E61 size=7>DinoDNA</BASEFONT>, who marked all of the runes and runs LM! 
Meesa also given` <BASEFONT color=#0EC23E size=7> muy muy big thanks to Aegwyn, RhythmDragon, Nebu/Wisps, Advct,</BASEFONT> and  <BASEFONT color=#2E5878 size=7>all the great folks at the Razor Enhanced Discord server</BASEFONT> for makin’ dis possible! '''
            
            
            Gumps.AddHtml(gd,255,35,160,225,welcomeText,False,True)
            
            
        for book_index, book in enumerate(filtered_books[(atlas.Page - 1) * 10:atlas.Page * 10], start=1):
            if count <= 10:
                Gumps.AddBackground(gd,20, 2+(count * rowHeight),180,25,9550)
                
                if atlas.selected_book == book:
                    Gumps.AddImage(gd, +10, (count * rowHeight)+2 , 93)
                    Gumps.AddImage(gd, 75, (count * rowHeight)+2 , 93)
                    Gumps.AddImage(gd, -20, (count * rowHeight)+2 , 92)
                    Gumps.AddImage(gd, +25, (count * rowHeight)+2 , 94)

                    Gumps.AddLabelCropped(gd, 50, 5+(count * rowHeight), 128, 10, 1152, book["name"])
                    
                    Gumps.AddTooltip(gd,1061114,str(book["name"]))
                    
                    for idx, sublist_item in enumerate(book["sublist"]):
                        if sublist_item.lower() == 'empty' or county >= 17:
                            break
                            
                        if str(atlas.runeSearchText).lower() in str(sublist_item).lower():
                            Gumps.AddBackground(gd,250, 32 + idx * int(rowHeight / 1.75),170,14,5120)
                            Gumps.AddLabelCropped(gd, 275, 30 + idx * int(rowHeight / 1.75), 128, 10, 1152, str(sublist_item))
                            Gumps.AddTooltip(gd,1061114,str(sublist_item))
                            Gumps.AddButton(gd, 250, 30 + idx * int(rowHeight / 1.75), 5540, 5542, 5000 + idx, 1, 0)
                            
                        else:
                            Gumps.AddLabelCropped(gd, 275, 30 + idx * int(rowHeight / 1.75), 128, 10, 0, str(sublist_item))
                            Gumps.AddTooltip(gd,1061114,str(sublist_item))
                            Gumps.AddButton(gd, 250, 30 + idx * int(rowHeight / 1.75), 5601, 5605, 5000 + idx, 1, 0)
                        
                        county = county + 1 
                else:
                    Gumps.AddButton(gd, 15,  4 + (count * rowHeight), 4005, 4006, book["serial"], 1, 0)

                    Gumps.AddLabelCropped(gd, 50, 5+(count * rowHeight), 128, 10, book['hue']-2, book["name"])
                    Gumps.AddTooltip(gd,1061114,str(book["name"]))
            count += 1

        Gumps.AddBackground(gd,15,-30,180,50,39925)
        if atlas.transparent == True:
            Gumps.AddAlphaRegion(gd,0,0,10,10)

        Gumps.AddLabel(gd,45,-20,1152,"Search Book Titles:")
       
        Gumps.AddBackground(gd,228,-30,180,50,39925)
        if atlas.transparent == True:
            Gumps.AddAlphaRegion(gd,0,0,10,10)
            Gumps.AddBackground(gd,48,272,142,22,3088)
            
        Gumps.AddBackground(gd,22,275,195,25,420)
        
        Gumps.AddButton(gd,50,275,1545,1546,96,1,0)
        Gumps.AddButton(gd,25,275,1541,1542,93,1,0)
        
        Gumps.AddLabel(gd, 75, 277, 1152, "Page:")
        Gumps.AddLabel(gd, 115, 277, 905, str(atlas.Page) + ' of ' + str((len(filtered_books) // 10) + 1 if len(filtered_books) % 10 != 0 else len(filtered_books) // 10))

        Gumps.AddButton(gd,195,275,1539,1540,94,1,0)
        Gumps.AddButton(gd,180,275,1543,1544,97,1,0) 
        Gumps.AddLabel(gd,258,-20,1152,"Search Rune Titles:")
        
        Gumps.AddBackground(gd,35,0,138,28,1755)
        Gumps.AddTextEntry(gd,50,5,105,25,1152,33,atlas.titleSearchText)        
        Gumps.AddButton(gd,160,3,2450,2451,44,1,0)
        Gumps.AddBackground(gd,250,0,138,28,1755)
        Gumps.AddTextEntry(gd,265,5,105,25,1152,34,atlas.runeSearchText)
        
        Gumps.AddButton(gd,375,3,2450,2451,45,1,0)

        Gumps.AddImage(gd,0,265,40115)
        Gumps.AddImage(gd,50,265,40119)
        Gumps.AddImage(gd,100,265,40117)

        Gumps.AddImage(gd,24,295,302)
        Gumps.AddImage(gd,200,295,304)
        
        Gumps.AddImage(gd,24,360,308)
        Gumps.AddImage(gd,200,360,310)
        
        Gumps.AddImage(gd,90,300,9153)
        
        Gumps.AddImageTiled(gd,91,300,4,75,9153)
        Gumps.AddImageTiled(gd,145,300,4,75,9153)

        Gumps.AddImageTiled(gd,40,294,160,16,303)
        Gumps.AddImageTiled(gd,40,360,160,16,309)
        
        Gumps.AddImageTiled(gd,24,310,16,50,305)
        Gumps.AddImageTiled(gd,200,310,16,50,307)  
        
        Gumps.AddButton(gd,40,310,2351,2351,301,1,0)
        Gumps.AddTooltip(gd,1061114,str("Go to Lincoln Mallmorial Rune Library"))
        Gumps.AddButton(gd,95,310,2351,2351,302,1,0)
        Gumps.AddTooltip(gd,1061114,str("Go to Brit Bank"))
        Gumps.AddButton(gd,150,310,2351,2351,303,1,0)
        Gumps.AddTooltip(gd,1061114,str("Go Home"))
        
        Gumps.AddLabel(gd, 45, 310, 1152, " incoln")
        Gumps.AddLabel(gd, 55, 325, 1152, " all")
        Gumps.AddLabel(gd, 46, 340, 1152, " orial")
        
        Gumps.AddLabel(gd, 44, 310, 33, "L")
        Gumps.AddLabel(gd, 51, 325, 33, "M")        
        Gumps.AddLabel(gd, 44, 340, 33, "M") 
        
        Gumps.AddLabel(gd, 105, 325, 1152, "Bank")
        Gumps.AddLabel(gd, 160, 325, 1152, "Home")
        
        offsetX = 250
        offsetY = 300
        if atlas.transparent == False:
            Gumps.AddBackground(gd, offsetX - 10, offsetY - 30, 165, 100, 39925)
 
        if atlas.selected_book == None:
            Gumps.AddLabel(gd, offsetX + 30, offsetY - 25, 1152, "Atlas Statistics")

            bookCount, runeCount = atlas.libraryStats() 
            Gumps.AddLabel(gd, offsetX + 30, offsetY , 1152, "Runebooks: " )
            Gumps.AddLabel(gd, offsetX + 100, offsetY , 68, str(bookCount) )
            
            Gumps.AddLabel(gd, offsetX + 30, offsetY+20 , 1152, "Runes: "  )
            Gumps.AddLabel(gd, offsetX + 75, offsetY+20 , 68, str(runeCount) )
        else:
            Gumps.AddLabel(gd, offsetX + 30, offsetY - 25, 1152, "Rune History :")    
            rowCount = 0
            for rune in atlas.rune_history : #reversed(): 

                Gumps.AddBackground(gd,250, offsetY + (15*rowCount),155,14,5120)
                Gumps.AddLabelCropped(gd, offsetX + 15, offsetY + (15*rowCount), 128, 10, 1152, str(rune[0]["sublist"][rune[1]]) + '|' + str(rune[2]) + "-" + str(rune[1]))

                Gumps.AddButton(gd, offsetX, offsetY + (15*rowCount), 5601, 5605, 9000 + rowCount, 1, 0)

                rowCount += 1
                if rowCount >= 4:  
                    break
    
        offsetJarJarX = 185
        offsetJarJarY = 15
        for loc in jarjarimage:
            Gumps.AddImage(gd,int(loc[0] + offsetJarJarX),int(loc[1]+ offsetJarJarY),6000, loc[2])
            

        if len(atlas.books) != 0:
            Gumps.AddImageTiled(gd,190,100,45,100,5174)
            
            Gumps.AddImageTiled(gd,190,75,45,38,5151)
            
            Gumps.AddImageTiled(gd,190,175,45,48,5177)
            
            Gumps.AddImage(gd,170,75,5170)
            
            Gumps.AddImage(gd,218,75,5172)
            
            Gumps.AddImage(gd,170,100,5173)
            Gumps.AddImage(gd,218,100,5175)    
            
            Gumps.AddImage(gd,170,175,5176)
            Gumps.AddImage(gd,218,175,5178)
            
            if atlas.selectedRecall == True:
                Gumps.AddImage(gd,187,97,2351,62)
                Gumps.AddImage(gd,187,150,2351,33)
                
                Gumps.AddImage(gd,160,105,9780,33)
                
                if atlas.useRecallScrolls == True:
                    Gumps.AddItem(gd,205,198,0x1F4C)
                    Gumps.AddTooltip(gd,1061114,str("Toggle Use Recall Scroll in Pack")) 
                    #Gumps.AddLabel(gd,192,200,1150,"Use")  
                    Gumps.AddButton(gd,192,200,11400,11402,400,1,0)
                    Gumps.AddTooltip(gd,1061114,str("Toggle Use Recall Scroll in Pack"))

                if atlas.useRecallScrolls == False:
                    Gumps.AddItem(gd,205,198,0x1F4C)
                    Gumps.AddTooltip(gd,1061114,str("Toggle Use Recall Scroll in Pack"))
                    #Gumps.AddLabel(gd,192,200,1150,"Use")  
                    Gumps.AddButton(gd,192,200,11410,11412,400,1,0)        
                    Gumps.AddTooltip(gd,1061114,str("Toggle Use Recall Scroll in Pack"))      
            else:
                Gumps.AddImage(gd,187,97,2351,33)
                Gumps.AddImage(gd,187,150,2351,62)

                Gumps.AddImage(gd,160,155,9780,33)
               
            Gumps.AddButton(gd,190,100,2271,2271,99,1,0)
            Gumps.AddButton(gd,190,153,2291,2291,98,1,0) 
            
        if atlas.transparent == True:

            Gumps.AddButton(gd,200,78,1531,1532,304,1,0)
            Gumps.AddTooltip(gd,1061114,str("Toggle Background Transparency"))     
        else:
            Gumps.AddButton(gd,200,78,1532,1531,304,1,0) 
            Gumps.AddTooltip(gd,1061114,str("Toggle Background Transparency"))  
            

        Gumps.AddLabel(gd,290,440,2033,"Created by Meesa Jar Jar")        
        Gumps.AddLabel(gd,310,450,2035,"Peace & Love!")     
        
        Gumps.AddLabel(gd, 0, 440, 2037, "Script V:" + str(round(scriptVersion * 100, 2)))
        
        offsetDinoDNAX = 380
        offsetDinoDNAY = 250
        Gumps.AddBackground(gd,offsetDinoDNAX+10,offsetDinoDNAY,50,140,430)
        Gumps.AddLabel(gd,175,63,1152,"Meesa")
        Gumps.AddLabel(gd,215,63,1152,"JarJar")
        
        for loc in dinodnaimage:
            Gumps.AddImage(gd,int(loc[0] + offsetDinoDNAX),int(loc[1]+ offsetDinoDNAY),6000, loc[2])
            
        Gumps.AddButton(gd,185,217,5608,5609,48,1,0)
        
        Gumps.AddLabel(gd,390,365,1152,"DinoDNA")
        if minimized:
            try:
                Gumps.SendGump(int(gumpid), Player.Serial, littleX, littleY, gd.gumpDefinition, gd.gumpStrings)
            except:
                print("****** FAILED SENDGUMP");
        else:
            try:
                Gumps.SendGump(int(gumpid), Player.Serial, bigX, bigY, gd.gumpDefinition, gd.gumpStrings)
            except:
                print("****** FAILED SENDGUMP"); 

def extractChargesAndMaxCharges(mystring):
    pattern = r'Charges: (\d+)/(\d+)'
    match = re.search(pattern, mystring)
    if match:
        charger = int(match.group(1))
        maxCharges = int(match.group(2))
        return charger, maxCharges
    else:
        return None, None


def extractBookLocationNames(runebookSerial):
        
    Misc.Pause(200)
    runebook = Items.FindBySerial(runebookSerial)
    Items.UseItem(runebook)
    Misc.Pause(100)
    sixteenLocations = None
    charges = None
    maxCharges = None

    propstringlist = Items.GetPropStringList(runebook)
    for listItem in propstringlist:
        if 'charges:' in str(listItem).lower():
            charges, maxCharges = extractChargesAndMaxCharges(listItem)
            break
            
    startBookNames = 0
    items = Gumps.LastGumpGetLineList()
    for z in range(0, len(items)):

        if str(items[z]) == str(charges) and str(items[z+1]) == str(maxCharges):
            startBookNames = z + 2
            break
            
    sixteenLocations = items[startBookNames:startBookNames + 16]
    return sixteenLocations      
    
def getRunebookHomeIndex(runeBookSerial):
    runebook = Items.FindBySerial(runeBookSerial)
    Misc.Pause(200)
    Items.UseItem(runebook)
    Misc.Pause(100)
    gd = Gumps.GetGumpRawText(1431013363)
    sublist = extractBookLocationNames(runebook.Serial)
    count = 0
    homeRune = None
    
    for rune in sublist:
        if 'home' in str(rune).lower():
            homeRune = count
        count = count + 1
    return homeRune
   
def clean_string(s):
    cleaned_s = s.encode('ascii', 'ignore').decode('ascii')
    cleaned_s = ''.join(c if c.isalnum() else ' ' for c in cleaned_s)
    cleaned_s = cleaned_s.upper()
    return cleaned_s  
    
def save_atlas(atlas, filename):
    """Serialize and save the Atlas object to a file."""
    with open(filename, 'wb') as f:
        pickle.dump(atlas, f)
    print(f"Atlas saved to {filename}")


if gumpid in Gumps.AllGumpIDs():
    print("Found the gump open, closing it!")
    Gumps.CloseGump(gumpid)
    
  
bookDict ={}
minimized = True
minimizedGumpPosX = 0
minimizedGumpPosY = 0
maximizedGumpPosX = 0
maximizedGumpPosY = 0

lmrloc = [1396,1974,0]
lmrsafeloc = [1396,1964,7]


atlas = Atlas()

atlas = load_atlas("./RazorEnhanced/Scripts/MeesaJarJar_RunebookAtlas.pkl")


if atlas is not None:
    print("Atlas object loaded successfully.")
    atlas.findLMRunebook()
    atlas.sort_books_by_name()
    atlas.useRecallScrolls = False
else:
    print("Failed to load the Atlas object.")
    atlas = Atlas()
    atlas.findLMRunebook()  
    atlas.useRecallScrolls = False
   

bookCount, runeCount = atlas.libraryStats()    
print("Total Books in Library:", bookCount)
print("Total Runes in Library:", runeCount)
atlas.sort_books_by_name()

bigX = 500
bigY = 500
littleX = 500
littleY = 500
updateGump()
if 1431013363 in Gumps.AllGumpIDs():
        Misc.Pause(650)
        Gumps.SendAction(1431013363, 0)

while True:
    Misc.Pause(150)
    atlas.atlas_check_for_map_command()
    
    gd = Gumps.GetGumpData(gumpid)
    if gd:

        if gd.buttonid == 0:
            gd.buttonid = -1
            toggle_gump_state()
            updateGump()   
            
        if gd.buttonid > 999999: 
            selected_serial = gd.buttonid
            atlas.select_book_by_serial(selected_serial)
            gd.buttonid = -1
            updateGump()
            
        if gd.buttonid < 10000 and gd.buttonid >= 9000:
            button_index = gd.buttonid - 9000  
            atlas.select_book(atlas.rune_history[button_index][0])
           
            atlas.recallOrGate(atlas.rune_history[button_index][0], atlas.rune_history[button_index][1])
            toggle_gump_state()
            gd.buttonid = -1
            updateGump()                
            
        if gd.buttonid < 6000 and gd.buttonid > 4999:
            button_index = gd.buttonid - 4999  
            atlas.recallOrGate(atlas.selected_book, button_index-1)
            toggle_gump_state()
            gd.buttonid = -1
            updateGump()    
           

        if gd.buttonid > 7999 and gd.buttonid < 9000:
            
            Journal.Clear()
            ind = gd.buttonid - 8000
            if ind == 0:
                atlas.recallMeesaLMRunebook(2)
                
            if ind == 1:
                atlas.recallMeesaLMRunebook(3)
            
            if ind == 2:
                atlas.recallMeesaLMRunebook(3)
            
            if ind == 3:
                atlas.recallMeesaLMRunebook(4)
            
            if ind == 4:
                atlas.recallMeesaLMRunebook(8)
            
            if ind == 5:
                atlas.recallMeesaLMRunebook(5)
            
            if ind == 6:
                atlas.recallMeesaLMRunebook(7)
            
            if ind == 7:
                atlas.recallMeesaLMRunebook(6)
                        
            gd.buttonid = -1
            updateGump()   
            
        if gd.buttonid == 44:
            gd.buttonid = -1
            atlas.selectedFilter = 'book'
            atlas.titleSearchText = Gumps.GetTextByID(gd,33)
            atlas.Page = 1;
            updateGump()

        if gd.buttonid == 45:
            gd.buttonid = -1
            atlas.selectedFilter = 'rune'
            atlas.runeSearchText = Gumps.GetTextByID(gd,34)
            atlas.Page = 1;
            updateGump()
            
        if gd.buttonid == 93:
            gd.buttonid = -1
            atlas.firstPage()
            updateGump()

        if gd.buttonid == 94:
            gd.buttonid = -1
            atlas.lastPage()
            updateGump()

        if gd.buttonid == 96:
            gd.buttonid = -1
            atlas.decrease_page()
            updateGump()
                         
        if gd.buttonid == 97:
            gd.buttonid = -1
            atlas.increase_page()
            updateGump()
            
        if gd.buttonid == 98:
            gd.buttonid = -1
            atlas.selectedRecall = False
            updateGump()
            
        if gd.buttonid == 99:
            gd.buttonid = -1
            atlas.selectedRecall = True
            updateGump() 
            
        if gd.buttonid == 301:
            gd.buttonid = -1
            Journal.Clear()
            atlas.recallMeesaLMRunebook(0)
            updateGump()   
            
        if gd.buttonid == 302:
            gd.buttonid = -1
            Journal.Clear()
            atlas.recallMeesaLMRunebook(1)
            updateGump()  
            
        if gd.buttonid == 303:
            gd.buttonid = -1
            Journal.Clear()
            atlas.recallMeesaLMRunebook(atlas.homeRune)
            
            updateGump()  
            
        if gd.buttonid == 304:
            gd.buttonid = -1
            Journal.Clear()
            if atlas.transparent == True:
                atlas.transparent = False
            else:
                atlas.transparent = True
                
            updateGump()  
            
        if gd.buttonid == 400:
            gd.buttonid = -1
            
            if atlas.useRecallScrolls == True:
                atlas.useRecallScrolls = False
            else:
                atlas.useRecallScrolls = True
                
            updateGump()      
    
        if gd.buttonid == 95:  
            toggle_gump_state()
            gd.buttonid = -1        
         
        if gd.buttonid == 48:  
            if Misc.ScriptStatus("MeesaJarJar_RuneBookAtlas_Map.py") == False:
                Misc.ScriptRun("MeesaJarJar_RuneBookAtlas_Map.py")
            print("Starting Runebook Atlas Map")
            gd.buttonid = -1   
            updateGump()  