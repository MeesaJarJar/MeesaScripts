# Made by Meesa Jar Jar(BabyBro on Discord) & DinoDNA - Peace and Love!
# Meesa Rune Atlas - Easy, automated traveling by recalling or gating used exclusively 
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

#CONFIG ----------------------------------
atlasVersion = 427
scriptVersion = 05152024.01

#END CONFIG ------------------------------

import re
import random
import clr
import os
import System
import pickle
import math

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

            if distance > 25:

                atlas.recallMeesaLMRunebook(0)
                Misc.Pause(1500)

                navigate_to(1396,1965)
            else:
                navigate_to(1396,1965)

            book = Items.FindBySerial(atlas.selected_book["serial"])
            if book:
                
                if book.Position.Z > 26: 
                    
                    zFloor = 27
                else:
                    zFloor = 7
                    
                if zFloor == 27:
                    atlas.goUpstairs()
                    Misc.Pause(650)

                navigate_to(book.Position.X,book.Position.Y)

                Misc.Pause(250)

                namesx = extractBookLocationNames(tarSerial)

                foundName = False
                count = 0
                for myName in namesx:
                    
                    pattern = re.compile(r'[\W_]+')

                   
                    if re.sub(pattern, '', str(myName)) == re.sub(pattern, '', str(tarName)):
                        foundName = True
                        atlas.recallOrGate(atlas.selected_book, count)
                        pass
                    count = count + 1  

    
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
                    if distance > 25:

                        atlas.recallMeesaLMRunebook(0)
                        Misc.Pause(1500)

                        navigate_to(1396,1965)
                    else:
                        navigate_to(1396,1965)

                    book = Items.FindBySerial(selected_book["serial"])
                    if book:
                        
                        if book.Position.Z > 26: 
                            
                            zFloor = 27
                        else:
                            zFloor = 7
                            
                        if zFloor == 27 and Player.Position.Z == 7:
                            atlas.goUpstairs()
                            Misc.Pause(650)

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


dinodnaimage = [[16,1,Black],
[17,1,Black],
[18,1,Black],
[19,1,Black],
[16,2,Black],
[17,2,Black],
[18,2,Black],
[19,2,Black],
[20,2,Black],
[6,3,Black],
[7,3,Black],
[17,3,Black],
[18,3,Black],
[19,3,Black],
[20,3,Black],
[21,3,Black],
[22,3,White],
[5,4,Black],
[6,4,Black],
[7,4,Black],
[8,4,Black],
[20,4,Black],
[21,4,Black],
[5,5,Black],
[6,5,Black],
[7,5,Black],
[21,5,Black],
[4,6,Black],
[5,6,Black],
[6,6,Black],
[7,6,Black],
[4,7,Black],
[5,7,Black],
[6,7,Black],
[22,7,White],
[4,8,Black],
[5,8,Black],
[4,9,Black],
[17,10,Black],
[20,10,Black],
[21,10,Black],
[22,10,Black],
[17,11,Black],
[18,11,White],
[19,11,White],
[20,11,White],
[22,11,Black],
[10,12,Black],
[11,12,Black],
[13,12,Black],
[16,12,Black],
[18,12,White],
[19,12,White],
[20,12,White],
[21,12,White],
[23,12,Black],
[9,13,Black],
[11,13,White],
[12,13,White],
[14,13,Black],
[15,13,Black],
[16,13,Black],
[17,13,White],
[18,13,White],
[19,13,White],
[20,13,White],
[21,13,White],
[22,13,White],
[23,13,Black],
[10,14,White],
[11,14,White],
[12,14,White],
[13,14,White],
[14,14,White],
[15,14,Black],
[16,14,Black],
[17,14,White],
[18,14,White],
[19,14,White],
[20,14,White],
[21,14,White],
[22,14,White],
[24,14,Black],
[8,15,Black],
[10,15,White],
[11,15,White],
[12,15,White],
[13,15,White],
[14,15,White],
[15,15,White],
[16,15,Black],
[18,15,White],
[19,15,White],
[20,15,White],
[21,15,White],
[22,15,White],
[23,15,White],
[24,15,Black],
[9,16,White],
[10,16,White],
[11,16,White],
[12,16,White],
[13,16,White],
[14,16,White],
[15,16,White],
[18,16,White],
[19,16,White],
[20,16,White],
[21,16,White],
[22,16,White],
[23,16,White],
[7,17,Black],
[9,17,White],
[10,17,White],
[11,17,White],
[12,17,White],
[13,17,White],
[14,17,White],
[15,17,White],
[16,17,White],
[17,17,Black],
[18,17,White],
[21,17,White],
[22,17,White],
[23,17,White],
[9,18,White],
[10,18,White],
[11,18,White],
[12,18,White],
[13,18,White],
[16,18,White],
[17,18,Black],
[19,18,Black],
[20,18,Black],
[22,18,White],
[23,18,White],
[25,18,Black],
[9,19,White],
[10,19,White],
[11,19,White],
[12,19,White],
[14,19,Black],
[15,19,Black],
[16,19,White],
[17,19,Black],
[20,19,Black],
[21,19,White],
[22,19,White],
[23,19,White],
[25,19,Black],
[9,20,White],
[10,20,White],
[11,20,White],
[12,20,White],
[14,20,Black],
[15,20,Black],
[16,20,White],
[19,20,White],
[20,20,White],
[21,20,White],
[22,20,White],
[23,20,White],
[9,21,White],
[10,21,White],
[11,21,White],
[12,21,White],
[13,21,White],
[16,21,White],
[17,21,Black],
[18,21,Black],
[19,21,White],
[20,21,White],
[21,21,White],
[22,21,White],
[23,21,White],
[24,21,Black],
[8,22,Black],
[9,22,White],
[10,22,White],
[11,22,White],
[12,22,White],
[13,22,White],
[14,22,White],
[15,22,White],
[16,22,White],
[17,22,Black],
[19,22,Black],
[23,22,Black],
[10,23,White],
[11,23,White],
[12,23,White],
[13,23,White],
[14,23,White],
[15,23,White],
[17,23,Black],
[20,23,Black],
[21,23,Black],
[22,23,Black],
[9,24,Black],
[11,24,White],
[12,24,White],
[13,24,White],
[14,24,White],
[16,24,Black],
[10,25,Black],
[15,25,Black],
[12,26,Black],
[13,26,Black],
[26,26,Black],
[26,27,Black],
[25,28,Black],
[26,28,Black],
[11,29,Black],
[24,29,Black],
[25,29,Black],
[22,30,Black],
[23,30,Black],
[24,30,Black],
[25,30,Black],
[11,31,White],
[15,31,Black],
[16,31,Black],
[17,31,Black],
[18,31,Black],
[19,31,Black],
[20,31,Black],
[21,31,Black],
[22,31,Black],
[23,31,Black],
[24,31,Black],
[16,32,Black],
[17,32,Black],
[18,32,Black],
[19,32,Black],
[20,32,Black],
[24,32,Black],
[17,33,Black],
[18,33,Black],
[19,33,Black],
[21,33,White],
[22,33,White],
[23,33,White],
[22,35,White],
[23,35,White],
[24,36,Black],
[34,36,Black],
[37,38,Black],
[32,39,Black],
[34,39,Yellow],
[35,39,Yellow],
[36,39,Yellow],
[22,40,Black],
[23,40,Black],
[34,40,Yellow],
[35,40,Yellow],
[36,40,Yellow],
[38,40,Black],
[21,41,Black],
[25,41,Black],
[32,41,White],
[33,41,Black],
[35,41,Yellow],
[36,41,Yellow],
[39,41,Yellow],
[40,41,Yellow],
[41,41,Yellow],
[42,41,Yellow],
[43,41,Yellow],
[44,41,Yellow],
[46,41,Black],
[20,42,Black],
[22,42,Red],
[23,42,Red],
[25,42,Black],
[34,42,Black],
[38,42,Yellow],
[39,42,Yellow],
[40,42,Yellow],
[41,42,Yellow],
[42,42,Yellow],
[43,42,Yellow],
[44,42,Yellow],
[45,42,Yellow],
[51,42,Black],
[52,42,Black],
[53,42,Black],
[54,42,Black],
[20,43,Black],
[22,43,Red],
[23,43,Red],
[25,43,Black],
[36,43,Black],
[38,43,Yellow],
[39,43,Yellow],
[40,43,Yellow],
[41,43,Yellow],
[42,43,Yellow],
[43,43,Yellow],
[44,43,Yellow],
[45,43,Yellow],
[46,43,Yellow],
[50,43,Black],
[55,43,Black],
[20,44,Black],
[25,44,Black],
[38,44,Yellow],
[39,44,Yellow],
[40,44,Yellow],
[41,44,Yellow],
[42,44,Yellow],
[43,44,Yellow],
[44,44,Yellow],
[45,44,Yellow],
[46,44,Yellow],
[49,44,Black],
[21,45,Black],
[24,45,Black],
[25,45,Black],
[38,45,Yellow],
[39,45,Yellow],
[40,45,Yellow],
[41,45,Yellow],
[42,45,Yellow],
[43,45,Yellow],
[44,45,Yellow],
[45,45,Yellow],
[46,45,Yellow],
[48,45,Black],
[56,45,Black],
[57,45,White],
[22,46,Black],
[26,46,Black],
[38,46,Yellow],
[39,46,Yellow],
[40,46,Yellow],
[41,46,Yellow],
[42,46,Yellow],
[43,46,Yellow],
[44,46,Yellow],
[45,46,Yellow],
[46,46,Yellow],
[48,46,Black],
[56,46,Black],
[57,46,White],
[21,47,Black],
[22,47,White],
[23,47,White],
[24,47,White],
[25,47,White],
[27,47,Black],
[36,47,Black],
[38,47,Yellow],
[39,47,Yellow],
[40,47,Yellow],
[41,47,Yellow],
[42,47,Yellow],
[43,47,Yellow],
[44,47,Yellow],
[45,47,Yellow],
[49,47,Black],
[22,48,White],
[23,48,White],
[24,48,White],
[25,48,White],
[26,48,White],
[39,48,Yellow],
[40,48,Yellow],
[41,48,Yellow],
[42,48,Yellow],
[43,48,Yellow],
[44,48,Yellow],
[45,48,Yellow],
[49,48,Black],
[55,48,Black],
[22,49,White],
[23,49,White],
[24,49,White],
[25,49,White],
[26,49,White],
[34,49,Black],
[35,49,Yellow],
[36,49,Yellow],
[37,49,Yellow],
[41,49,Yellow],
[42,49,Yellow],
[43,49,Yellow],
[50,49,Black],
[54,49,Black],
[55,49,Black],
[56,49,Black],
[57,49,Black],
[22,50,White],
[23,50,White],
[24,50,White],
[25,50,White],
[26,50,White],
[33,50,Black],
[35,50,Yellow],
[36,50,Yellow],
[37,50,Yellow],
[38,50,Yellow],
[45,50,Yellow],
[52,50,Black],
[53,50,Black],
[54,50,Black],
[59,50,Black],
[21,51,Black],
[23,51,White],
[24,51,White],
[25,51,White],
[31,51,White],
[32,51,Black],
[34,51,Yellow],
[35,51,Yellow],
[36,51,Yellow],
[37,51,Yellow],
[40,51,Yellow],
[41,51,Yellow],
[43,51,Black],
[45,51,Yellow],
[53,51,Black],
[54,51,White],
[55,51,White],
[56,51,White],
[57,51,White],
[58,51,White],
[22,52,Black],
[26,52,Black],
[33,52,Yellow],
[34,52,Yellow],
[35,52,Yellow],
[36,52,Yellow],
[38,52,Black],
[40,52,Yellow],
[42,52,Black],
[43,52,Black],
[54,52,White],
[55,52,White],
[56,52,White],
[57,52,White],
[58,52,White],
[24,53,Black],
[25,53,Black],
[26,53,Black],
[28,53,Black],
[33,53,Yellow],
[34,53,Yellow],
[35,53,Yellow],
[37,53,Black],
[39,53,Black],
[41,53,Black],
[51,53,Black],
[52,53,Black],
[53,53,White],
[54,53,White],
[55,53,White],
[56,53,White],
[57,53,White],
[58,53,White],
[59,53,White],
[60,53,Black],
[24,54,Black],
[29,54,Black],
[51,54,Black],
[52,54,Black],
[53,54,White],
[54,54,White],
[55,54,White],
[56,54,White],
[57,54,White],
[58,54,White],
[59,54,White],
[60,54,Black],
[23,55,Black],
[30,55,Black],
[33,55,Black],
[34,55,Black],
[38,55,White],
[43,55,White],
[54,55,White],
[55,55,White],
[56,55,White],
[57,55,White],
[58,55,White],
[25,56,Red],
[26,56,Red],
[27,56,Red],
[28,56,Red],
[29,56,Red],
[33,56,Black],
[53,56,Black],
[54,56,White],
[55,56,White],
[56,56,White],
[57,56,White],
[59,56,Black],
[22,57,Black],
[25,57,Red],
[26,57,Red],
[27,57,Red],
[28,57,Red],
[29,57,Red],
[31,57,Black],
[54,57,Black],
[25,58,Red],
[26,58,Red],
[27,58,Red],
[28,58,Red],
[57,58,Black],
[23,59,Black],
[26,59,Red],
[27,59,Red],
[30,59,Black],
[24,60,Black],
[29,60,Black],
[49,60,Black],
[50,60,Black],
[53,60,Black],
[54,60,Black],
[25,61,Black],
[26,61,Black],
[27,61,Black],
[28,61,Black],
[29,61,Black],
[32,61,Black],
[48,61,Black],
[51,61,Red],
[52,61,Red],
[54,61,Black],
[27,62,Black],
[29,62,White],
[30,62,White],
[31,62,White],
[33,62,Black],
[36,62,Black],
[48,62,Black],
[50,62,Red],
[51,62,Red],
[52,62,Red],
[55,62,Black],
[28,63,White],
[29,63,White],
[30,63,White],
[31,63,White],
[32,63,White],
[34,63,Black],
[37,63,White],
[38,63,White],
[47,63,Black],
[48,63,Black],
[50,63,Red],
[51,63,Red],
[55,63,Black],
[27,64,White],
[28,64,White],
[29,64,White],
[30,64,White],
[31,64,White],
[32,64,White],
[33,64,White],
[36,64,White],
[37,64,White],
[38,64,White],
[39,64,White],
[48,64,Black],
[50,64,Red],
[51,64,Red],
[56,64,White],
[25,65,Black],
[27,65,White],
[28,65,White],
[29,65,White],
[30,65,White],
[31,65,White],
[32,65,White],
[33,65,White],
[36,65,White],
[37,65,White],
[38,65,White],
[39,65,White],
[44,65,Yellow],
[45,65,Yellow],
[50,65,Red],
[51,65,Red],
[54,65,Black],
[27,66,White],
[28,66,White],
[29,66,White],
[30,66,White],
[31,66,White],
[32,66,White],
[33,66,White],
[34,66,Black],
[36,66,White],
[37,66,White],
[38,66,White],
[39,66,White],
[40,66,Black],
[44,66,Yellow],
[45,66,Yellow],
[49,66,Black],
[50,66,Black],
[52,66,Black],
[53,66,Black],
[21,67,Black],
[23,67,Black],
[24,67,Black],
[28,67,White],
[29,67,White],
[30,67,White],
[31,67,White],
[32,67,White],
[34,67,Black],
[35,67,Black],
[37,67,White],
[38,67,White],
[43,67,Black],
[20,68,Black],
[24,68,Black],
[27,68,Black],
[29,68,White],
[30,68,White],
[31,68,White],
[33,68,Black],
[34,68,Black],
[35,68,Black],
[36,68,Black],
[37,68,Black],
[19,69,Black],
[25,69,Black],
[31,69,Black],
[32,69,Black],
[37,69,Black],
[38,69,Black],
[18,70,Black],
[19,70,Black],
[25,70,Black],
[31,70,Black],
[34,70,Red],
[35,70,Red],
[36,70,Red],
[38,70,Black],
[40,70,White],
[17,71,Black],
[18,71,Black],
[19,71,Black],
[25,71,Black],
[26,71,White],
[30,71,Black],
[32,71,Red],
[33,71,Red],
[34,71,Red],
[35,71,Red],
[36,71,Red],
[37,71,Red],
[39,71,Black],
[16,72,Black],
[19,72,Black],
[20,72,Black],
[24,72,Black],
[30,72,Black],
[32,72,Red],
[33,72,Red],
[34,72,Red],
[35,72,Red],
[36,72,Red],
[37,72,Red],
[17,73,White],
[18,73,White],
[20,73,Black],
[21,73,Black],
[22,73,Black],
[23,73,Black],
[32,73,Red],
[33,73,Red],
[34,73,Red],
[35,73,Red],
[37,73,Red],
[38,73,Red],
[40,73,Black],
[17,74,White],
[18,74,White],
[22,74,Black],
[30,74,Black],
[32,74,Red],
[33,74,Red],
[34,74,Red],
[35,74,Red],
[37,74,Red],
[38,74,Red],
[40,74,Black],
[17,75,White],
[18,75,White],
[29,75,White],
[33,75,Red],
[34,75,Red],
[36,75,Red],
[37,75,Red],
[39,75,Black],
[16,76,Black],
[31,76,Black],
[40,76,Yellow],
[41,76,Yellow],
[44,76,Black],
[13,77,White],
[15,77,Black],
[16,77,Black],
[17,77,Black],
[18,77,Black],
[32,77,Black],
[39,77,Yellow],
[40,77,Yellow],
[41,77,Yellow],
[42,77,Yellow],
[43,77,Yellow],
[45,77,Black],
[14,78,Black],
[19,78,Black],
[34,78,Black],
[37,78,Yellow],
[38,78,Yellow],
[39,78,Yellow],
[40,78,Yellow],
[41,78,Yellow],
[42,78,Yellow],
[43,78,Yellow],
[44,78,Yellow],
[13,79,Black],
[15,79,Red],
[18,79,Red],
[20,79,Black],
[24,79,Black],
[26,79,Black],
[34,79,Black],
[36,79,Yellow],
[37,79,Yellow],
[38,79,Yellow],
[39,79,Yellow],
[40,79,Yellow],
[41,79,Yellow],
[42,79,Yellow],
[43,79,Yellow],
[44,79,Yellow],
[46,79,Black],
[14,80,Red],
[15,80,Red],
[18,80,Red],
[19,80,Red],
[25,80,White],
[29,80,Black],
[32,80,Yellow],
[36,80,Yellow],
[37,80,Yellow],
[38,80,Yellow],
[39,80,Yellow],
[40,80,Yellow],
[41,80,Yellow],
[42,80,Yellow],
[43,80,Yellow],
[44,80,Yellow],
[45,80,Yellow],
[14,81,Red],
[15,81,Red],
[16,81,Red],
[17,81,Red],
[18,81,Red],
[19,81,Red],
[21,81,Black],
[23,81,White],
[24,81,White],
[25,81,White],
[26,81,White],
[27,81,White],
[28,81,Black],
[30,81,Yellow],
[31,81,Yellow],
[32,81,Yellow],
[33,81,Yellow],
[34,81,Yellow],
[37,81,Yellow],
[38,81,Yellow],
[39,81,Yellow],
[40,81,Yellow],
[41,81,Yellow],
[42,81,Yellow],
[43,81,Yellow],
[44,81,Yellow],
[45,81,Yellow],
[13,82,Black],
[15,82,Red],
[16,82,Red],
[17,82,Red],
[18,82,Red],
[19,82,Red],
[21,82,Black],
[23,82,White],
[24,82,White],
[25,82,White],
[26,82,White],
[29,82,Yellow],
[30,82,Yellow],
[31,82,Yellow],
[32,82,Yellow],
[33,82,Yellow],
[34,82,Yellow],
[35,82,Yellow],
[38,82,Yellow],
[39,82,Yellow],
[40,82,Yellow],
[41,82,Yellow],
[42,82,Yellow],
[43,82,Yellow],
[44,82,Yellow],
[45,82,Yellow],
[46,82,Black],
[47,82,White],
[13,83,Black],
[15,83,Red],
[16,83,Red],
[17,83,Red],
[20,83,Black],
[21,83,Black],
[22,83,White],
[23,83,White],
[24,83,White],
[25,83,White],
[26,83,White],
[29,83,Yellow],
[30,83,Yellow],
[31,83,Yellow],
[32,83,Yellow],
[33,83,Yellow],
[34,83,Yellow],
[35,83,Yellow],
[38,83,Yellow],
[39,83,Yellow],
[40,83,Yellow],
[41,83,Yellow],
[42,83,Yellow],
[43,83,Yellow],
[44,83,Yellow],
[48,83,Black],
[49,83,Black],
[14,84,Black],
[19,84,Black],
[20,84,Black],
[21,84,Black],
[22,84,White],
[23,84,White],
[24,84,White],
[25,84,White],
[26,84,White],
[29,84,Yellow],
[30,84,Yellow],
[31,84,Yellow],
[32,84,Yellow],
[33,84,Yellow],
[34,84,Yellow],
[35,84,Yellow],
[36,84,Yellow],
[38,84,Yellow],
[39,84,Yellow],
[40,84,Yellow],
[41,84,Yellow],
[42,84,Yellow],
[43,84,Yellow],
[45,84,Black],
[48,84,Black],
[49,84,Black],
[50,84,Black],
[15,85,Black],
[16,85,Black],
[17,85,Black],
[18,85,Black],
[21,85,Black],
[23,85,White],
[24,85,White],
[25,85,White],
[26,85,White],
[29,85,Yellow],
[30,85,Yellow],
[31,85,Yellow],
[32,85,Yellow],
[33,85,Yellow],
[34,85,Yellow],
[35,85,Yellow],
[38,85,Yellow],
[39,85,Yellow],
[40,85,Yellow],
[41,85,Yellow],
[42,85,Yellow],
[45,85,Black],
[46,85,Black],
[51,85,Black],
[22,86,Black],
[23,86,White],
[24,86,White],
[25,86,White],
[27,86,Black],
[29,86,Yellow],
[30,86,Yellow],
[31,86,Yellow],
[32,86,Yellow],
[33,86,Yellow],
[34,86,Yellow],
[35,86,Yellow],
[37,86,Black],
[43,86,Black],
[45,86,Black],
[47,86,Red],
[48,86,Red],
[49,86,Red],
[52,86,Black],
[28,87,Black],
[30,87,Yellow],
[31,87,Yellow],
[32,87,Yellow],
[33,87,Yellow],
[36,87,Black],
[39,87,Black],
[40,87,Black],
[41,87,Black],
[47,87,Red],
[48,87,Red],
[49,87,Red],
[50,87,Red],
[24,88,Black],
[25,88,Black],
[43,88,White],
[44,88,Black],
[47,88,Red],
[48,88,Red],
[49,88,Red],
[50,88,Red],
[51,88,Red],
[53,88,Black],
[28,89,Yellow],
[29,89,Yellow],
[30,89,Yellow],
[31,89,Yellow],
[34,89,Yellow],
[35,89,Yellow],
[44,89,Black],
[46,89,Red],
[47,89,Red],
[48,89,Red],
[50,89,Red],
[51,89,Red],
[53,89,Black],
[30,90,Yellow],
[31,90,Yellow],
[34,90,Yellow],
[37,90,White],
[44,90,Black],
[46,90,Red],
[47,90,Red],
[48,90,Red],
[50,90,Red],
[51,90,Red],
[53,90,Black],
[28,91,Black],
[30,91,Yellow],
[31,91,Yellow],
[34,91,Yellow],
[47,91,Red],
[48,91,Red],
[49,91,Red],
[54,91,White],
[27,92,Black],
[30,92,Yellow],
[32,92,Black],
[35,92,Black],
[45,92,Black],
[52,92,Black],
[31,93,Black],
[46,93,Black],
[47,93,Black],
[50,93,Black],
[51,93,Black],
[52,93,Black],
[29,94,Black],
[30,94,Black],
[48,94,Black],
[49,94,Black],
[51,94,White],
[52,94,White],
[55,94,Black],
[48,95,Black],
[49,95,White],
[50,95,White],
[51,95,White],
[52,95,White],
[53,95,White],
[54,95,White],
[49,96,White],
[50,96,White],
[51,96,White],
[52,96,White],
[53,96,White],
[54,96,White],
[55,96,White],
[56,96,Black],
[57,96,Black],
[46,97,Black],
[47,97,Black],
[48,97,White],
[49,97,White],
[50,97,White],
[51,97,White],
[52,97,White],
[53,97,White],
[54,97,White],
[55,97,White],
[57,97,Black],
[46,98,Black],
[48,98,White],
[49,98,White],
[50,98,White],
[51,98,White],
[52,98,White],
[53,98,White],
[54,98,White],
[55,98,White],
[57,98,Black],
[46,99,Black],
[47,99,Black],
[48,99,White],
[49,99,White],
[50,99,White],
[51,99,White],
[52,99,White],
[53,99,White],
[54,99,White],
[55,99,White],
[56,99,Black],
[57,99,Black],
[49,100,White],
[50,100,White],
[51,100,White],
[52,100,White],
[53,100,White],
[54,100,White],
[48,101,Black],
[50,101,White],
[51,101,White],
[52,101,White],
[53,101,White],
[54,101,White],
[55,101,Black],
[49,102,Black],
[51,102,White],
[52,102,White],
[54,102,Black],
[50,103,Black],
[51,103,Black],
[52,103,Black],
[53,103,Black],
[54,103,Black],
[50,104,Black],
[54,104,Black],
[49,105,Black],
[52,105,Red],
[53,105,Red],
[55,105,Black],
[49,106,Black],
[51,106,Red],
[52,106,Red],
[53,106,Red],
[55,106,Black],
[49,107,Black],
[51,107,Red],
[52,107,Red],
[55,107,Black],
[49,108,Black],
[54,108,Black],
[50,109,Black],
[51,109,Black],
[52,109,Black],
[53,109,Black],
[50,110,Black],
[51,110,Black],
[52,110,Black],
[50,111,White],
[51,111,White],
[49,112,White],
[50,112,White],
[51,112,White],
[52,112,White],
[45,113,Black],
[49,113,White],
[50,113,White],
[51,113,White],
[52,113,White],
[47,114,Black],
[48,114,Black],
[49,114,White],
[50,114,White],
[51,114,White],
[52,114,White],
[53,114,Black],
[43,115,Black],
[45,115,Yellow],
[46,115,Yellow],
[49,115,Black],
[52,115,Black],
[41,116,White],
[42,116,Black],
[44,116,Yellow],
[45,116,Yellow],
[46,116,Yellow],
[47,116,Yellow],
[48,116,Yellow],
[50,116,Black],
[43,117,Yellow],
[44,117,Yellow],
[45,117,Yellow],
[46,117,Yellow],
[47,117,Yellow],
[48,117,Yellow],
[40,118,Black],
[43,118,Yellow],
[44,118,Yellow],
[45,118,Yellow],
[46,118,Yellow],
[47,118,Yellow],
[48,118,Yellow],
[50,118,Black],
[38,119,Black],
[41,119,Black],
[42,119,Black],
[43,119,Yellow],
[44,119,Yellow],
[45,119,Yellow],
[46,119,Yellow],
[47,119,Yellow],
[48,119,Yellow],
[37,120,Black],
[42,120,Black],
[44,120,Yellow],
[45,120,Yellow],
[46,120,Yellow],
[47,120,Yellow],
[49,120,Black],
[33,121,Black],
[37,121,Black],
[42,121,Black],
[43,121,Black],
[48,121,Black],
[31,122,Black],
[32,122,Black],
[34,122,Black],
[43,122,Black],
[45,122,Black],
[46,122,Black],
[47,122,Black],
[31,123,Black],
[35,123,Black],
[42,123,Black],
[33,124,Red],
[38,124,Black],
[41,124,Black],
[31,125,Black],
[35,125,Black],
[39,125,Black],
[40,125,Black],
[31,126,Black],
[32,126,Black],
[33,126,Black],
[34,126,Black],
[35,126,Black]]


jarjarimage = [[    21, 6, Black    ],
[   22, 6, Black    ],
[   23, 6, Black    ],
[   24, 6, Black    ],
[   25, 6, Black    ],
[   26, 6, Black    ],
[   27, 6, Black    ],
[   19, 7, Black    ],
[   20, 7, Black    ],
[   21, 7, Black    ],
[   22, 7, Black    ],
[   23, 7, Black    ],
[   24, 7, Black    ],
[   25, 7, Black    ],
[   26, 7, Black    ],
[   27, 7, Black    ],
[   28, 7, Black    ],
[   19, 8, Black    ],
[   20, 8, Black    ],
[   21, 8, Black    ],
[   22, 8, Black    ],
[   23, 8, Black    ],
[   24, 8, Black    ],
[   25, 8, Black    ],
[   26, 8, Black    ],
[   27, 8, Black    ],
[   28, 8, Black    ],
[   18, 9, Black    ],
[   19, 9, Black    ],
[   20, 9, Black    ],
[   21, 9, Black    ],
[   22, 9, Black    ],
[   23, 9, Orange   ],
[   24, 9, Orange   ],
[   25, 9, Black    ],
[   26, 9, Black    ],
[   27, 9, Black    ],
[   28, 9, Black    ],
[   29, 9, Black    ],
[   38, 9, Black    ],
[   39, 9, Black    ],
[   40, 9, Black    ],
[   41, 9, Black    ],
[   42, 9, Black    ],
[   43, 9, Black    ],
[   17, 10, Black   ],
[   18, 10, Black   ],
[   19, 10, Black   ],
[   20, 10, Black   ],
[   21, 10, Black   ],
[   22, 10, Black   ],
[   23, 10, Orange  ],
[   24, 10, Orange  ],
[   25, 10, Orange  ],
[   26, 10, Black   ],
[   27, 10, Black   ],
[   28, 10, Black   ],
[   29, 10, Black   ],
[   37, 10, Black   ],
[   38, 10, Black   ],
[   39, 10, Black   ],
[   40, 10, Black   ],
[   41, 10, Black   ],
[   42, 10, Black   ],
[   43, 10, Black   ],
[   44, 10, Black   ],
[   45, 10, Black   ],
[   17, 11, Black   ],
[   18, 11, Black   ],
[   19, 11, Black   ],
[   20, 11, Black   ],
[   21, 11, Black   ],
[   22, 11, Orange  ],
[   23, 11, Orange  ],
[   24, 11, Orange  ],
[   25, 11, Orange  ],
[   26, 11, Black   ],
[   27, 11, Black   ],
[   28, 11, Black   ],
[   29, 11, Black   ],
[   30, 11, Black   ],
[   36, 11, Black   ],
[   37, 11, Black   ],
[   38, 11, Black   ],
[   39, 11, Black   ],
[   40, 11, Black   ],
[   41, 11, Black   ],
[   42, 11, Black   ],
[   43, 11, Black   ],
[   44, 11, Black   ],
[   45, 11, Black   ],
[   46, 11, Black   ],
[   17, 12, Black   ],
[   18, 12, Black   ],
[   19, 12, Black   ],
[   20, 12, Black   ],
[   21, 12, Black   ],
[   22, 12, Peach   ],
[   23, 12, Peach   ],
[   24, 12, Peach   ],
[   25, 12, Peach   ],
[   26, 12, Black   ],
[   27, 12, Black   ],
[   28, 12, Black   ],
[   29, 12, Black   ],
[   30, 12, Black   ],
[   31, 12, Black   ],
[   32, 12, Black   ],
[   33, 12, Black   ],
[   34, 12, Black   ],
[   35, 12, Black   ],
[   36, 12, Black   ],
[   37, 12, Black   ],
[   38, 12, Black   ],
[   39, 12, Black   ],
[   40, 12, Orange  ],
[   41, 12, Black   ],
[   42, 12, Black   ],
[   43, 12, Black   ],
[   44, 12, Black   ],
[   45, 12, Black   ],
[   46, 12, Black   ],
[   17, 13, Black   ],
[   18, 13, Black   ],
[   19, 13, Black   ],
[   20, 13, Black   ],
[   21, 13, Peach   ],
[   22, 13, Orange  ],
[   23, 13, Orange  ],
[   24, 13, Orange  ],
[   25, 13, Peach   ],
[   26, 13, Peach   ],
[   27, 13, Black   ],
[   28, 13, Black   ],
[   29, 13, Black   ],
[   30, 13, Black   ],
[   31, 13, Black   ],
[   32, 13, Black   ],
[   33, 13, Black   ],
[   34, 13, Black   ],
[   35, 13, Black   ],
[   36, 13, Black   ],
[   37, 13, Black   ],
[   38, 13, Orange  ],
[   39, 13, Orange  ],
[   40, 13, Orange  ],
[   41, 13, Orange  ],
[   42, 13, Black   ],
[   43, 13, Black   ],
[   44, 13, Black   ],
[   45, 13, Black   ],
[   46, 13, Black   ],
[   16, 14, Black   ],
[   17, 14, Black   ],
[   18, 14, Black   ],
[   19, 14, Black   ],
[   20, 14, Black   ],
[   21, 14, Black   ],
[   22, 14, Orange  ],
[   23, 14, Orange  ],
[   24, 14, Yellow  ],
[   25, 14, Black   ],
[   26, 14, Peach   ],
[   27, 14, Black   ],
[   28, 14, Black   ],
[   29, 14, Black   ],
[   30, 14, Black   ],
[   31, 14, Black   ],
[   32, 14, Black   ],
[   33, 14, Black   ],
[   34, 14, Black   ],
[   35, 14, Black   ],
[   36, 14, Black   ],
[   37, 14, Black   ],
[   38, 14, Peach   ],
[   39, 14, Peach   ],
[   40, 14, Peach   ],
[   41, 14, Orange  ],
[   42, 14, Black   ],
[   43, 14, Black   ],
[   44, 14, Black   ],
[   45, 14, Black   ],
[   46, 14, Black   ],
[   16, 15, Black   ],
[   17, 15, Black   ],
[   18, 15, Black   ],
[   19, 15, Black   ],
[   20, 15, Black   ],
[   21, 15, Orange  ],
[   22, 15, Yellow  ],
[   23, 15, Black   ],
[   24, 15, Orange  ],
[   25, 15, Yellow  ],
[   26, 15, Black   ],
[   27, 15, Black   ],
[   28, 15, Black   ],
[   29, 15, Black   ],
[   30, 15, Black   ],
[   31, 15, Black   ],
[   32, 15, Black   ],
[   33, 15, Black   ],
[   34, 15, Black   ],
[   35, 15, Black   ],
[   36, 15, Black   ],
[   37, 15, Peach   ],
[   38, 15, Peach   ],
[   39, 15, Orange  ],
[   40, 15, Peach   ],
[   41, 15, Peach   ],
[   42, 15, Black   ],
[   43, 15, Black   ],
[   44, 15, Black   ],
[   45, 15, Black   ],
[   46, 15, Black   ],
[   16, 16, Black   ],
[   17, 16, Black   ],
[   18, 16, Black   ],
[   19, 16, Black   ],
[   20, 16, Black   ],
[   21, 16, Orange  ],
[   22, 16, Yellow  ],
[   23, 16, Black   ],
[   24, 16, Yellow  ],
[   25, 16, Yellow  ],
[   26, 16, Black   ],
[   27, 16, Black   ],
[   28, 16, Black   ],
[   29, 16, Black   ],
[   30, 16, Orange  ],
[   31, 16, Peach   ],
[   32, 16, Black   ],
[   33, 16, Black   ],
[   34, 16, Black   ],
[   35, 16, Black   ],
[   36, 16, Black   ],
[   37, 16, Orange  ],
[   38, 16, Black   ],
[   39, 16, Orange  ],
[   40, 16, Orange  ],
[   41, 16, Black   ],
[   42, 16, Orange  ],
[   43, 16, Black   ],
[   44, 16, Black   ],
[   45, 16, Black   ],
[   46, 16, Black   ],
[   16, 17, Black   ],
[   17, 17, Black   ],
[   18, 17, Black   ],
[   19, 17, Black   ],
[   20, 17, Peach   ],
[   21, 17, Black   ],
[   22, 17, Orange  ],
[   23, 17, Orange  ],
[   24, 17, Yellow  ],
[   25, 17, Black   ],
[   26, 17, Orange  ],
[   27, 17, Black   ],
[   28, 17, Black   ],
[   29, 17, Peach   ],
[   30, 17, Peach   ],
[   31, 17, Peach   ],
[   32, 17, Peach   ],
[   33, 17, Orange  ],
[   34, 17, Black   ],
[   35, 17, Black   ],
[   36, 17, Orange  ],
[   37, 17, Black   ],
[   38, 17, Yellow  ],
[   39, 17, Black   ],
[   40, 17, Orange  ],
[   41, 17, Yellow  ],
[   42, 17, Orange  ],
[   43, 17, Black   ],
[   44, 17, Black   ],
[   45, 17, Black   ],
[   46, 17, Black   ],
[   16, 18, Black   ],
[   17, 18, Black   ],
[   18, 18, Black   ],
[   19, 18, Black   ],
[   20, 18, Orange  ],
[   21, 18, Peach   ],
[   22, 18, Black   ],
[   23, 18, Black   ],
[   24, 18, Black   ],
[   25, 18, Black   ],
[   26, 18, Black   ],
[   27, 18, Black   ],
[   28, 18, Peach   ],
[   29, 18, Peach   ],
[   30, 18, Peach   ],
[   31, 18, Peach   ],
[   32, 18, Peach   ],
[   33, 18, Peach   ],
[   34, 18, Black   ],
[   35, 18, Black   ],
[   36, 18, Orange  ],
[   37, 18, Orange  ],
[   38, 18, Yellow  ],
[   39, 18, Black   ],
[   40, 18, Orange  ],
[   41, 18, Yellow  ],
[   42, 18, Orange  ],
[   43, 18, Black   ],
[   44, 18, Black   ],
[   45, 18, Black   ],
[   46, 18, Black   ],
[   47, 18, Black   ],
[   15, 19, Black   ],
[   16, 19, Black   ],
[   17, 19, Black   ],
[   18, 19, Black   ],
[   19, 19, Black   ],
[   20, 19, Black   ],
[   21, 19, Peach   ],
[   22, 19, Peach   ],
[   23, 19, Peach   ],
[   24, 19, Peach   ],
[   25, 19, Orange  ],
[   26, 19, Black   ],
[   27, 19, Orange  ],
[   28, 19, Peach   ],
[   29, 19, Peach   ],
[   30, 19, Peach   ],
[   31, 19, Peach   ],
[   32, 19, Peach   ],
[   33, 19, Peach   ],
[   34, 19, Peach   ],
[   35, 19, Black   ],
[   36, 19, Peach   ],
[   37, 19, Black   ],
[   38, 19, Orange  ],
[   39, 19, Orange  ],
[   40, 19, Yellow  ],
[   41, 19, Orange  ],
[   42, 19, Black   ],
[   43, 19, Black   ],
[   44, 19, Black   ],
[   45, 19, Black   ],
[   46, 19, Black   ],
[   47, 19, Black   ],
[   15, 20, Black   ],
[   16, 20, Black   ],
[   17, 20, Black   ],
[   18, 20, Black   ],
[   19, 20, Black   ],
[   20, 20, Black   ],
[   21, 20, Orange  ],
[   22, 20, Peach   ],
[   23, 20, Peach   ],
[   24, 20, Orange  ],
[   25, 20, Black   ],
[   26, 20, Black   ],
[   27, 20, Orange  ],
[   28, 20, Peach   ],
[   29, 20, Peach   ],
[   30, 20, Peach   ],
[   31, 20, Peach   ],
[   32, 20, Peach   ],
[   33, 20, Peach   ],
[   34, 20, Peach   ],
[   35, 20, Orange  ],
[   36, 20, Orange  ],
[   37, 20, Peach   ],
[   38, 20, Orange  ],
[   39, 20, Orange  ],
[   40, 20, Orange  ],
[   41, 20, Peach   ],
[   42, 20, Black   ],
[   43, 20, Black   ],
[   44, 20, Black   ],
[   45, 20, Black   ],
[   46, 20, Black   ],
[   47, 20, Black   ],
[   15, 21, Black   ],
[   16, 21, Black   ],
[   17, 21, Black   ],
[   18, 21, Black   ],
[   19, 21, Black   ],
[   20, 21, Orange  ],
[   21, 21, Peach   ],
[   22, 21, Orange  ],
[   23, 21, Orange  ],
[   24, 21, Orange  ],
[   25, 21, Peach   ],
[   26, 21, Orange  ],
[   27, 21, Black   ],
[   28, 21, Peach   ],
[   29, 21, Peach   ],
[   30, 21, Peach   ],
[   31, 21, Peach   ],
[   32, 21, Peach   ],
[   33, 21, Peach   ],
[   34, 21, Peach   ],
[   35, 21, Black   ],
[   36, 21, Black   ],
[   37, 21, Peach   ],
[   38, 21, Peach   ],
[   39, 21, Peach   ],
[   40, 21, Peach   ],
[   41, 21, Peach   ],
[   42, 21, Black   ],
[   43, 21, Black   ],
[   44, 21, Black   ],
[   45, 21, Black   ],
[   46, 21, Black   ],
[   14, 22, Black   ],
[   15, 22, Black   ],
[   16, 22, Black   ],
[   17, 22, Black   ],
[   18, 22, Black   ],
[   19, 22, Black   ],
[   20, 22, Orange  ],
[   21, 22, Peach   ],
[   22, 22, Peach   ],
[   23, 22, Peach   ],
[   24, 22, Orange  ],
[   25, 22, Peach   ],
[   26, 22, Black   ],
[   27, 22, Orange  ],
[   28, 22, Peach   ],
[   29, 22, Peach   ],
[   30, 22, Peach   ],
[   31, 22, Peach   ],
[   32, 22, Peach   ],
[   33, 22, Peach   ],
[   34, 22, Peach   ],
[   35, 22, Orange  ],
[   36, 22, Black   ],
[   37, 22, Black   ],
[   38, 22, Orange  ],
[   39, 22, Orange  ],
[   40, 22, Peach   ],
[   41, 22, Black   ],
[   42, 22, Black   ],
[   43, 22, Black   ],
[   44, 22, Black   ],
[   45, 22, Black   ],
[   14, 23, Black   ],
[   15, 23, Black   ],
[   16, 23, Black   ],
[   17, 23, Black   ],
[   18, 23, Orange  ],
[   19, 23, Peach   ],
[   20, 23, Black   ],
[   21, 23, Orange  ],
[   22, 23, Orange  ],
[   23, 23, Black   ],
[   24, 23, Orange  ],
[   25, 23, Peach   ],
[   26, 23, Black   ],
[   27, 23, Peach   ],
[   28, 23, Peach   ],
[   29, 23, Peach   ],
[   30, 23, Peach   ],
[   31, 23, Peach   ],
[   32, 23, Peach   ],
[   33, 23, Peach   ],
[   34, 23, Peach   ],
[   35, 23, Orange  ],
[   36, 23, Black   ],
[   37, 23, Black   ],
[   38, 23, Black   ],
[   39, 23, Black   ],
[   40, 23, Black   ],
[   41, 23, Black   ],
[   42, 23, Black   ],
[   43, 23, Black   ],
[   44, 23, Black   ],
[   13, 24, Black   ],
[   14, 24, Black   ],
[   15, 24, Black   ],
[   16, 24, Black   ],
[   17, 24, Black   ],
[   18, 24, Peach   ],
[   19, 24, Peach   ],
[   20, 24, Orange  ],
[   21, 24, Peach   ],
[   22, 24, Peach   ],
[   23, 24, Peach   ],
[   24, 24, Peach   ],
[   25, 24, Orange  ],
[   26, 24, Orange  ],
[   27, 24, Peach   ],
[   28, 24, Peach   ],
[   29, 24, Peach   ],
[   30, 24, Peach   ],
[   31, 24, Peach   ],
[   32, 24, Peach   ],
[   33, 24, Peach   ],
[   34, 24, Peach   ],
[   35, 24, Peach   ],
[   36, 24, Orange  ],
[   37, 24, Orange  ],
[   38, 24, Black   ],
[   39, 24, Black   ],
[   40, 24, Orange  ],
[   41, 24, Black   ],
[   42, 24, Black   ],
[   43, 24, Black   ],
[   44, 24, Black   ],
[   45, 24, Black   ],
[   12, 25, Black   ],
[   13, 25, Black   ],
[   14, 25, Black   ],
[   15, 25, Black   ],
[   16, 25, Black   ],
[   17, 25, Orange  ],
[   18, 25, Peach   ],
[   19, 25, Peach   ],
[   20, 25, Peach   ],
[   21, 25, Peach   ],
[   22, 25, Peach   ],
[   23, 25, Peach   ],
[   24, 25, Peach   ],
[   25, 25, Orange  ],
[   26, 25, Peach   ],
[   27, 25, Peach   ],
[   28, 25, Peach   ],
[   29, 25, Peach   ],
[   30, 25, Peach   ],
[   31, 25, Peach   ],
[   32, 25, Peach   ],
[   33, 25, Peach   ],
[   34, 25, Peach   ],
[   35, 25, Peach   ],
[   36, 25, Peach   ],
[   37, 25, Peach   ],
[   38, 25, Orange  ],
[   39, 25, Orange  ],
[   40, 25, Peach   ],
[   41, 25, Black   ],
[   42, 25, Black   ],
[   43, 25, Black   ],
[   44, 25, Black   ],
[   45, 25, Black   ],
[   11, 26, Black   ],
[   12, 26, Black   ],
[   13, 26, Black   ],
[   14, 26, Black   ],
[   15, 26, Black   ],
[   16, 26, Black   ],
[   17, 26, Peach   ],
[   18, 26, Peach   ],
[   19, 26, Peach   ],
[   20, 26, Peach   ],
[   21, 26, Peach   ],
[   22, 26, Peach   ],
[   23, 26, Peach   ],
[   24, 26, Peach   ],
[   25, 26, Peach   ],
[   26, 26, Orange  ],
[   27, 26, Orange  ],
[   28, 26, Peach   ],
[   29, 26, Peach   ],
[   30, 26, Peach   ],
[   31, 26, Peach   ],
[   32, 26, Peach   ],
[   33, 26, Peach   ],
[   34, 26, Peach   ],
[   35, 26, Peach   ],
[   36, 26, Peach   ],
[   37, 26, Peach   ],
[   38, 26, Peach   ],
[   39, 26, Peach   ],
[   40, 26, Orange  ],
[   41, 26, Black   ],
[   42, 26, Black   ],
[   43, 26, Black   ],
[   44, 26, Black   ],
[   45, 26, Black   ],
[   10, 27, Black   ],
[   11, 27, Black   ],
[   12, 27, Black   ],
[   13, 27, Black   ],
[   14, 27, Black   ],
[   15, 27, Black   ],
[   16, 27, Black   ],
[   17, 27, Orange  ],
[   18, 27, Black   ],
[   19, 27, Orange  ],
[   20, 27, Peach   ],
[   21, 27, Peach   ],
[   22, 27, Peach   ],
[   23, 27, Peach   ],
[   24, 27, Orange  ],
[   25, 27, Black   ],
[   26, 27, Orange  ],
[   27, 27, Orange  ],
[   28, 27, Orange  ],
[   29, 27, Peach   ],
[   30, 27, Peach   ],
[   31, 27, Peach   ],
[   32, 27, Peach   ],
[   33, 27, Orange  ],
[   34, 27, Orange  ],
[   35, 27, Peach   ],
[   36, 27, Peach   ],
[   37, 27, Peach   ],
[   38, 27, Peach   ],
[   39, 27, Peach   ],
[   40, 27, Peach   ],
[   41, 27, Peach   ],
[   42, 27, Black   ],
[   43, 27, Black   ],
[   44, 27, Black   ],
[   45, 27, Black   ],
[   46, 27, Black   ],
[   9, 28, Black    ],
[   10, 28, Black   ],
[   11, 28, Black   ],
[   12, 28, Black   ],
[   13, 28, Black   ],
[   14, 28, Orange  ],
[   15, 28, Black   ],
[   16, 28, Black   ],
[   17, 28, Peach   ],
[   18, 28, Peach   ],
[   19, 28, Peach   ],
[   20, 28, Black   ],
[   21, 28, Peach   ],
[   22, 28, Peach   ],
[   23, 28, Peach   ],
[   24, 28, Black   ],
[   25, 28, Orange  ],
[   26, 28, Black   ],
[   27, 28, Orange  ],
[   28, 28, Peach   ],
[   29, 28, Peach   ],
[   30, 28, Peach   ],
[   31, 28, Peach   ],
[   32, 28, Peach   ],
[   33, 28, Orange  ],
[   34, 28, Orange  ],
[   35, 28, Black   ],
[   36, 28, Peach   ],
[   37, 28, Peach   ],
[   38, 28, Peach   ],
[   39, 28, Peach   ],
[   40, 28, Peach   ],
[   41, 28, Peach   ],
[   42, 28, Black   ],
[   43, 28, Black   ],
[   44, 28, Black   ],
[   45, 28, Black   ],
[   46, 28, Black   ],
[   8, 29, Black    ],
[   9, 29, Black    ],
[   10, 29, Black   ],
[   11, 29, Black   ],
[   12, 29, Black   ],
[   13, 29, Peach   ],
[   14, 29, Peach   ],
[   15, 29, Black   ],
[   16, 29, Peach   ],
[   17, 29, Peach   ],
[   18, 29, Peach   ],
[   19, 29, Peach   ],
[   20, 29, Peach   ],
[   21, 29, Orange  ],
[   22, 29, Peach   ],
[   23, 29, Peach   ],
[   24, 29, Orange  ],
[   25, 29, Black   ],
[   26, 29, Black   ],
[   27, 29, Black   ],
[   28, 29, Peach   ],
[   29, 29, Peach   ],
[   30, 29, Peach   ],
[   31, 29, Peach   ],
[   32, 29, Peach   ],
[   33, 29, Black   ],
[   34, 29, Orange  ],
[   35, 29, Black   ],
[   36, 29, Orange  ],
[   37, 29, Peach   ],
[   38, 29, Peach   ],
[   39, 29, Peach   ],
[   40, 29, Peach   ],
[   41, 29, Peach   ],
[   42, 29, Orange  ],
[   43, 29, Black   ],
[   44, 29, Black   ],
[   45, 29, Black   ],
[   46, 29, Black   ],
[   47, 29, Black   ],
[   7, 30, Black    ],
[   8, 30, Black    ],
[   9, 30, Black    ],
[   10, 30, Black   ],
[   11, 30, Black   ],
[   12, 30, Orange  ],
[   13, 30, Orange  ],
[   14, 30, Black   ],
[   15, 30, Orange  ],
[   16, 30, Peach   ],
[   17, 30, Peach   ],
[   18, 30, Peach   ],
[   19, 30, Peach   ],
[   20, 30, Peach   ],
[   21, 30, Peach   ],
[   22, 30, Peach   ],
[   23, 30, Orange  ],
[   24, 30, Orange  ],
[   25, 30, Orange  ],
[   26, 30, Peach   ],
[   27, 30, Peach   ],
[   28, 30, Peach   ],
[   29, 30, Peach   ],
[   30, 30, Peach   ],
[   31, 30, Peach   ],
[   32, 30, Peach   ],
[   33, 30, Black   ],
[   34, 30, Black   ],
[   35, 30, Black   ],
[   36, 30, Peach   ],
[   37, 30, Peach   ],
[   38, 30, Peach   ],
[   39, 30, Peach   ],
[   40, 30, Peach   ],
[   41, 30, Orange  ],
[   42, 30, Orange  ],
[   43, 30, Black   ],
[   44, 30, Black   ],
[   45, 30, Black   ],
[   46, 30, Black   ],
[   47, 30, Black   ],
[   7, 31, Black    ],
[   8, 31, Black    ],
[   9, 31, Black    ],
[   10, 31, Black   ],
[   11, 31, Black   ],
[   12, 31, Black   ],
[   13, 31, Black   ],
[   14, 31, Black   ],
[   15, 31, Peach   ],
[   16, 31, Peach   ],
[   17, 31, Black   ],
[   18, 31, Peach   ],
[   19, 31, Peach   ],
[   20, 31, Peach   ],
[   21, 31, Peach   ],
[   22, 31, Peach   ],
[   23, 31, Orange  ],
[   24, 31, Peach   ],
[   25, 31, Peach   ],
[   26, 31, Peach   ],
[   27, 31, Peach   ],
[   28, 31, Peach   ],
[   29, 31, Peach   ],
[   30, 31, Peach   ],
[   31, 31, Peach   ],
[   32, 31, Peach   ],
[   33, 31, Peach   ],
[   34, 31, Black   ],
[   35, 31, Black   ],
[   36, 31, Peach   ],
[   37, 31, Peach   ],
[   38, 31, Peach   ],
[   39, 31, Peach   ],
[   40, 31, Black   ],
[   41, 31, Orange  ],
[   42, 31, Black   ],
[   43, 31, Black   ],
[   44, 31, Black   ],
[   45, 31, Black   ],
[   46, 31, Black   ],
[   47, 31, Black   ],
[   48, 31, Black   ],
[   6, 32, Black    ],
[   7, 32, Black    ],
[   8, 32, Black    ],
[   9, 32, Black    ],
[   10, 32, Black   ],
[   11, 32, Orange  ],
[   12, 32, Orange  ],
[   13, 32, Orange  ],
[   14, 32, Black   ],
[   15, 32, Peach   ],
[   16, 32, Peach   ],
[   17, 32, Black   ],
[   18, 32, Black   ],
[   19, 32, Peach   ],
[   20, 32, Peach   ],
[   21, 32, Peach   ],
[   22, 32, Peach   ],
[   23, 32, Peach   ],
[   24, 32, Peach   ],
[   25, 32, Peach   ],
[   26, 32, Peach   ],
[   27, 32, Peach   ],
[   28, 32, Peach   ],
[   29, 32, Peach   ],
[   30, 32, Peach   ],
[   31, 32, Peach   ],
[   32, 32, Peach   ],
[   33, 32, Peach   ],
[   34, 32, Peach   ],
[   35, 32, Peach   ],
[   36, 32, Orange  ],
[   37, 32, Peach   ],
[   38, 32, Peach   ],
[   39, 32, Orange  ],
[   40, 32, Orange  ],
[   41, 32, Orange  ],
[   42, 32, Orange  ],
[   43, 32, Orange  ],
[   44, 32, Orange  ],
[   45, 32, Black   ],
[   46, 32, Black   ],
[   47, 32, Black   ],
[   48, 32, Black   ],
[   6, 33, Black    ],
[   7, 33, Black    ],
[   8, 33, Black    ],
[   9, 33, Black    ],
[   10, 33, Peach   ],
[   11, 33, Orange  ],
[   12, 33, Orange  ],
[   13, 33, Orange  ],
[   14, 33, Black   ],
[   15, 33, Peach   ],
[   16, 33, Peach   ],
[   17, 33, Peach   ],
[   18, 33, Black   ],
[   19, 33, Peach   ],
[   20, 33, Peach   ],
[   21, 33, Peach   ],
[   22, 33, Peach   ],
[   23, 33, Peach   ],
[   24, 33, Peach   ],
[   25, 33, Peach   ],
[   26, 33, Peach   ],
[   27, 33, Peach   ],
[   28, 33, Peach   ],
[   29, 33, Peach   ],
[   30, 33, Peach   ],
[   31, 33, Peach   ],
[   32, 33, Peach   ],
[   33, 33, Peach   ],
[   34, 33, Peach   ],
[   35, 33, Orange  ],
[   36, 33, Peach   ],
[   37, 33, Peach   ],
[   38, 33, Peach   ],
[   39, 33, Peach   ],
[   40, 33, Peach   ],
[   41, 33, Peach   ],
[   42, 33, Orange  ],
[   43, 33, Orange  ],
[   44, 33, Peach   ],
[   45, 33, Peach   ],
[   46, 33, Black   ],
[   47, 33, Black   ],
[   48, 33, Black   ],
[   49, 33, Black   ],
[   6, 34, Black    ],
[   7, 34, Black    ],
[   8, 34, Black    ],
[   9, 34, Black    ],
[   10, 34, Black   ],
[   11, 34, Peach   ],
[   12, 34, Orange  ],
[   13, 34, Orange  ],
[   14, 34, Black   ],
[   15, 34, Peach   ],
[   16, 34, Peach   ],
[   17, 34, Peach   ],
[   18, 34, Black   ],
[   19, 34, Orange  ],
[   20, 34, Peach   ],
[   21, 34, Peach   ],
[   22, 34, Peach   ],
[   23, 34, Peach   ],
[   24, 34, Peach   ],
[   25, 34, Peach   ],
[   26, 34, Peach   ],
[   27, 34, Peach   ],
[   28, 34, Peach   ],
[   29, 34, Peach   ],
[   30, 34, Peach   ],
[   31, 34, Peach   ],
[   32, 34, Peach   ],
[   33, 34, Peach   ],
[   34, 34, Peach   ],
[   35, 34, Peach   ],
[   36, 34, Peach   ],
[   37, 34, Peach   ],
[   38, 34, Peach   ],
[   39, 34, Peach   ],
[   40, 34, Peach   ],
[   41, 34, Black   ],
[   42, 34, Black   ],
[   43, 34, Black   ],
[   44, 34, Black   ],
[   45, 34, Orange  ],
[   46, 34, Black   ],
[   47, 34, Black   ],
[   48, 34, Black   ],
[   49, 34, Black   ],
[   50, 34, Black   ],
[   5, 35, Black    ],
[   6, 35, Black    ],
[   7, 35, Black    ],
[   8, 35, Black    ],
[   9, 35, Black    ],
[   10, 35, Black   ],
[   11, 35, Black   ],
[   12, 35, Orange  ],
[   13, 35, Orange  ],
[   14, 35, Black   ],
[   15, 35, Orange  ],
[   16, 35, Peach   ],
[   17, 35, Peach   ],
[   18, 35, Orange  ],
[   19, 35, Black   ],
[   20, 35, Peach   ],
[   21, 35, Peach   ],
[   22, 35, Orange  ],
[   23, 35, Orange  ],
[   24, 35, Orange  ],
[   25, 35, Orange  ],
[   26, 35, Orange  ],
[   27, 35, Orange  ],
[   28, 35, Orange  ],
[   29, 35, Peach   ],
[   30, 35, Peach   ],
[   31, 35, Peach   ],
[   32, 35, Peach   ],
[   33, 35, Peach   ],
[   34, 35, Peach   ],
[   35, 35, Peach   ],
[   36, 35, Peach   ],
[   37, 35, Peach   ],
[   38, 35, Peach   ],
[   39, 35, Peach   ],
[   40, 35, Black   ],
[   41, 35, Black   ],
[   42, 35, Orange  ],
[   43, 35, Orange  ],
[   44, 35, Black   ],
[   45, 35, Black   ],
[   46, 35, Black   ],
[   47, 35, Black   ],
[   48, 35, Black   ],
[   49, 35, Black   ],
[   50, 35, Black   ],
[   51, 35, Black   ],
[   5, 36, Black    ],
[   6, 36, Black    ],
[   7, 36, Black    ],
[   8, 36, Black    ],
[   9, 36, Peach    ],
[   10, 36, Orange  ],
[   11, 36, Orange  ],
[   12, 36, Black   ],
[   13, 36, Black   ],
[   14, 36, Black   ],
[   15, 36, Orange  ],
[   16, 36, Peach   ],
[   17, 36, Peach   ],
[   18, 36, Orange  ],
[   19, 36, Black   ],
[   20, 36, Black   ],
[   21, 36, Peach   ],
[   22, 36, Peach   ],
[   23, 36, Peach   ],
[   24, 36, Peach   ],
[   25, 36, Orange  ],
[   26, 36, Orange  ],
[   27, 36, Orange  ],
[   28, 36, Orange  ],
[   29, 36, Orange  ],
[   30, 36, Black   ],
[   31, 36, Black   ],
[   32, 36, Orange  ],
[   33, 36, Peach   ],
[   34, 36, Peach   ],
[   35, 36, Peach   ],
[   36, 36, Peach   ],
[   37, 36, Peach   ],
[   38, 36, Peach   ],
[   39, 36, Orange  ],
[   40, 36, Black   ],
[   41, 36, Orange  ],
[   42, 36, Orange  ],
[   43, 36, Black   ],
[   44, 36, Orange  ],
[   45, 36, Peach   ],
[   46, 36, Peach   ],
[   47, 36, Black   ],
[   48, 36, Black   ],
[   49, 36, Black   ],
[   50, 36, Black   ],
[   51, 36, Black   ],
[   5, 37, Black    ],
[   6, 37, Black    ],
[   7, 37, Black    ],
[   8, 37, Black    ],
[   9, 37, Orange   ],
[   10, 37, Orange  ],
[   11, 37, Orange  ],
[   12, 37, Black   ],
[   13, 37, Black   ],
[   14, 37, Orange  ],
[   15, 37, Black   ],
[   16, 37, Peach   ],
[   17, 37, Peach   ],
[   18, 37, Orange  ],
[   19, 37, Peach   ],
[   20, 37, Black   ],
[   21, 37, Black   ],
[   22, 37, Orange  ],
[   23, 37, Peach   ],
[   24, 37, Peach   ],
[   25, 37, Peach   ],
[   26, 37, Peach   ],
[   27, 37, Peach   ],
[   28, 37, Peach   ],
[   29, 37, Peach   ],
[   30, 37, Orange  ],
[   31, 37, Orange  ],
[   32, 37, Orange  ],
[   33, 37, Black   ],
[   34, 37, Orange  ],
[   35, 37, Peach   ],
[   36, 37, Peach   ],
[   37, 37, Peach   ],
[   38, 37, Peach   ],
[   39, 37, Black   ],
[   40, 37, Orange  ],
[   41, 37, Orange  ],
[   42, 37, Orange  ],
[   43, 37, Black   ],
[   44, 37, Orange  ],
[   45, 37, Black   ],
[   46, 37, Peach   ],
[   47, 37, Peach   ],
[   48, 37, Black   ],
[   49, 37, Black   ],
[   50, 37, Black   ],
[   51, 37, Black   ],
[   52, 37, Black   ],
[   5, 38, Black    ],
[   6, 38, Black    ],
[   7, 38, Black    ],
[   8, 38, Peach    ],
[   9, 38, Orange   ],
[   10, 38, Peach   ],
[   11, 38, Orange  ],
[   12, 38, Orange  ],
[   13, 38, Black   ],
[   14, 38, Orange  ],
[   15, 38, Black   ],
[   16, 38, Peach   ],
[   17, 38, Peach   ],
[   18, 38, Orange  ],
[   19, 38, Peach   ],
[   20, 38, Peach   ],
[   21, 38, Black   ],
[   22, 38, Black   ],
[   23, 38, Black   ],
[   24, 38, Black   ],
[   25, 38, Black   ],
[   26, 38, Orange  ],
[   27, 38, Orange  ],
[   28, 38, Peach   ],
[   29, 38, Peach   ],
[   30, 38, Peach   ],
[   31, 38, Orange  ],
[   32, 38, Orange  ],
[   33, 38, Orange  ],
[   34, 38, Orange  ],
[   35, 38, Orange  ],
[   36, 38, Orange  ],
[   37, 38, Orange  ],
[   38, 38, Black   ],
[   39, 38, Black   ],
[   40, 38, Orange  ],
[   41, 38, Orange  ],
[   42, 38, Black   ],
[   43, 38, Orange  ],
[   44, 38, Orange  ],
[   45, 38, Black   ],
[   46, 38, Black   ],
[   47, 38, Black   ],
[   48, 38, Black   ],
[   49, 38, Black   ],
[   50, 38, Black   ],
[   51, 38, Black   ],
[   52, 38, Black   ],
[   5, 39, Black    ],
[   6, 39, Black    ],
[   7, 39, Black    ],
[   8, 39, Black    ],
[   9, 39, Black    ],
[   10, 39, Peach   ],
[   11, 39, Orange  ],
[   12, 39, Orange  ],
[   13, 39, Black   ],
[   14, 39, Black   ],
[   15, 39, Black   ],
[   16, 39, Orange  ],
[   17, 39, Peach   ],
[   18, 39, Peach   ],
[   19, 39, Peach   ],
[   20, 39, Peach   ],
[   21, 39, Orange  ],
[   22, 39, White   ],
[   23, 39, White   ],
[   24, 39, Peach   ],
[   25, 39, Peach   ],
[   26, 39, Black   ],
[   27, 39, Peach   ],
[   28, 39, Black   ],
[   29, 39, Black   ],
[   30, 39, Black   ],
[   31, 39, Black   ],
[   32, 39, Black   ],
[   33, 39, Black   ],
[   34, 39, Black   ],
[   35, 39, Orange  ],
[   36, 39, Orange  ],
[   37, 39, Black   ],
[   38, 39, Orange  ],
[   39, 39, Orange  ],
[   40, 39, Orange  ],
[   41, 39, Orange  ],
[   42, 39, Black   ],
[   43, 39, Orange  ],
[   44, 39, Orange  ],
[   45, 39, Black   ],
[   46, 39, Black   ],
[   47, 39, Peach   ],
[   48, 39, Black   ],
[   49, 39, Black   ],
[   50, 39, Black   ],
[   51, 39, Black   ],
[   52, 39, Black   ],
[   53, 39, Black   ],
[   4, 40, Black    ],
[   5, 40, Black    ],
[   6, 40, Black    ],
[   7, 40, Black    ],
[   8, 40, Black    ],
[   9, 40, Black    ],
[   10, 40, Black   ],
[   11, 40, Orange  ],
[   12, 40, Black   ],
[   13, 40, Orange  ],
[   14, 40, Orange  ],
[   15, 40, Black   ],
[   16, 40, Black   ],
[   17, 40, Peach   ],
[   18, 40, Peach   ],
[   19, 40, Peach   ],
[   20, 40, Peach   ],
[   21, 40, Peach   ],
[   22, 40, Black   ],
[   23, 40, Black   ],
[   24, 40, Peach   ],
[   25, 40, Peach   ],
[   26, 40, Peach   ],
[   27, 40, White   ],
[   28, 40, Peach   ],
[   29, 40, White   ],
[   30, 40, White   ],
[   31, 40, Black   ],
[   32, 40, White   ],
[   33, 40, Black   ],
[   34, 40, Skin    ],
[   35, 40, Peach   ],
[   36, 40, Black   ],
[   37, 40, Peach   ],
[   38, 40, Peach   ],
[   39, 40, Orange  ],
[   40, 40, Orange  ],
[   41, 40, Black   ],
[   42, 40, Orange  ],
[   43, 40, Orange  ],
[   44, 40, Orange  ],
[   45, 40, Black   ],
[   46, 40, Black   ],
[   47, 40, Peach   ],
[   48, 40, Peach   ],
[   49, 40, Black   ],
[   50, 40, Black   ],
[   51, 40, Black   ],
[   52, 40, Black   ],
[   4, 41, Black    ],
[   5, 41, Black    ],
[   6, 41, Black    ],
[   7, 41, Black    ],
[   8, 41, Orange   ],
[   9, 41, Peach    ],
[   10, 41, Black   ],
[   11, 41, Black   ],
[   12, 41, Black   ],
[   13, 41, Orange  ],
[   14, 41, Orange  ],
[   15, 41, Orange  ],
[   16, 41, Black   ],
[   17, 41, Orange  ],
[   18, 41, Peach   ],
[   19, 41, Peach   ],
[   20, 41, Peach   ],
[   21, 41, Peach   ],
[   22, 41, Black   ],
[   23, 41, Black   ],
[   24, 41, Black   ],
[   25, 41, Black   ],
[   26, 41, Black   ],
[   27, 41, Peach   ],
[   28, 41, Black   ],
[   29, 41, Peach   ],
[   30, 41, Skin    ],
[   31, 41, Black   ],
[   32, 41, Peach   ],
[   33, 41, Black   ],
[   34, 41, Black   ],
[   35, 41, Black   ],
[   36, 41, Orange  ],
[   37, 41, Peach   ],
[   38, 41, Orange  ],
[   39, 41, Orange  ],
[   40, 41, Orange  ],
[   41, 41, Black   ],
[   42, 41, Orange  ],
[   43, 41, Orange  ],
[   44, 41, Black   ],
[   45, 41, Orange  ],
[   46, 41, Orange  ],
[   47, 41, Black   ],
[   48, 41, Orange  ],
[   49, 41, Orange  ],
[   50, 41, Black   ],
[   51, 41, Black   ],
[   52, 41, Black   ],
[   4, 42, Black    ],
[   5, 42, Black    ],
[   6, 42, Black    ],
[   7, 42, Black    ],
[   8, 42, Peach    ],
[   9, 42, Peach    ],
[   10, 42, Orange  ],
[   11, 42, Orange  ],
[   12, 42, Black   ],
[   13, 42, Black   ],
[   14, 42, Orange  ],
[   15, 42, Orange  ],
[   16, 42, Black   ],
[   17, 42, Black   ],
[   18, 42, Peach   ],
[   19, 42, Peach   ],
[   20, 42, Peach   ],
[   21, 42, Peach   ],
[   22, 42, Orange  ],
[   23, 42, Black   ],
[   24, 42, Peach   ],
[   25, 42, Black   ],
[   26, 42, Black   ],
[   27, 42, Black   ],
[   28, 42, Black   ],
[   29, 42, Black   ],
[   30, 42, Black   ],
[   31, 42, Black   ],
[   32, 42, Black   ],
[   33, 42, Black   ],
[   34, 42, Black   ],
[   35, 42, Black   ],
[   36, 42, Peach   ],
[   37, 42, Orange  ],
[   38, 42, Orange  ],
[   39, 42, Orange  ],
[   40, 42, Black   ],
[   41, 42, Black   ],
[   42, 42, Orange  ],
[   43, 42, Orange  ],
[   44, 42, Black   ],
[   45, 42, Orange  ],
[   46, 42, Orange  ],
[   47, 42, Black   ],
[   48, 42, Black   ],
[   49, 42, Black   ],
[   50, 42, Black   ],
[   51, 42, Black   ],
[   52, 42, Black   ],
[   53, 42, Black   ],
[   4, 43, Black    ],
[   5, 43, Black    ],
[   6, 43, Black    ],
[   7, 43, Black    ],
[   8, 43, Orange   ],
[   9, 43, Black    ],
[   10, 43, Orange  ],
[   11, 43, Orange  ],
[   12, 43, Black   ],
[   13, 43, Black   ],
[   14, 43, Black   ],
[   15, 43, Black   ],
[   16, 43, Black   ],
[   17, 43, Black   ],
[   18, 43, Black   ],
[   19, 43, Peach   ],
[   20, 43, Peach   ],
[   21, 43, Peach   ],
[   22, 43, Peach   ],
[   23, 43, Black   ],
[   24, 43, Skin    ],
[   25, 43, Peach   ],
[   26, 43, Peach   ],
[   27, 43, Peach   ],
[   28, 43, Black   ],
[   29, 43, Black   ],
[   30, 43, Black   ],
[   31, 43, Black   ],
[   32, 43, Peach   ],
[   33, 43, Peach   ],
[   34, 43, Black   ],
[   35, 43, Peach   ],
[   36, 43, Peach   ],
[   37, 43, Orange  ],
[   38, 43, Orange  ],
[   39, 43, Orange  ],
[   40, 43, Black   ],
[   41, 43, Black   ],
[   42, 43, Black   ],
[   43, 43, Black   ],
[   44, 43, Orange  ],
[   45, 43, Orange  ],
[   46, 43, Black   ],
[   47, 43, Black   ],
[   48, 43, Peach   ],
[   49, 43, Peach   ],
[   50, 43, Black   ],
[   51, 43, Black   ],
[   52, 43, Black   ],
[   53, 43, Black   ],
[   4, 44, Black    ],
[   5, 44, Black    ],
[   6, 44, Black    ],
[   7, 44, Black    ],
[   8, 44, Black    ],
[   9, 44, Black    ],
[   10, 44, Black   ],
[   11, 44, Black   ],
[   12, 44, Orange  ],
[   13, 44, Orange  ],
[   14, 44, Orange  ],
[   15, 44, Black   ],
[   16, 44, Black   ],
[   17, 44, Orange  ],
[   18, 44, Black   ],
[   19, 44, Black   ],
[   20, 44, Peach   ],
[   21, 44, Orange  ],
[   22, 44, Peach   ],
[   23, 44, Orange  ],
[   24, 44, Black   ],
[   25, 44, Peach   ],
[   26, 44, Peach   ],
[   27, 44, White   ],
[   28, 44, Skin    ],
[   29, 44, White   ],
[   30, 44, White   ],
[   31, 44, White   ],
[   32, 44, Peach   ],
[   33, 44, Black   ],
[   34, 44, Peach   ],
[   35, 44, Peach   ],
[   36, 44, Orange  ],
[   37, 44, Orange  ],
[   38, 44, Black   ],
[   39, 44, Black   ],
[   40, 44, Black   ],
[   41, 44, Black   ],
[   42, 44, Black   ],
[   43, 44, Orange  ],
[   44, 44, Orange  ],
[   45, 44, Orange  ],
[   46, 44, Black   ],
[   47, 44, Orange  ],
[   48, 44, Black   ],
[   49, 44, Peach   ],
[   50, 44, Black   ],
[   51, 44, Black   ],
[   52, 44, Black   ],
[   53, 44, Black   ],
[   4, 45, Black    ],
[   5, 45, Black    ],
[   6, 45, Black    ],
[   7, 45, Black    ],
[   8, 45, Peach    ],
[   9, 45, Peach    ],
[   10, 45, Black   ],
[   11, 45, Black   ],
[   12, 45, Orange  ],
[   13, 45, Orange  ],
[   14, 45, Orange  ],
[   15, 45, Orange  ],
[   16, 45, Black   ],
[   17, 45, Black   ],
[   18, 45, Peach   ],
[   19, 45, Black   ],
[   20, 45, Black   ],
[   21, 45, Black   ],
[   22, 45, Orange  ],
[   23, 45, Peach   ],
[   24, 45, Peach   ],
[   25, 45, Black   ],
[   26, 45, Black   ],
[   27, 45, Black   ],
[   28, 45, Black   ],
[   29, 45, Peach   ],
[   30, 45, Orange  ],
[   31, 45, Peach   ],
[   32, 45, Black   ],
[   33, 45, Peach   ],
[   34, 45, Peach   ],
[   35, 45, Black   ],
[   36, 45, Orange  ],
[   37, 45, Black   ],
[   38, 45, Orange  ],
[   39, 45, Black   ],
[   40, 45, Black   ],
[   41, 45, Black   ],
[   42, 45, Orange  ],
[   43, 45, Orange  ],
[   44, 45, Black   ],
[   45, 45, Black   ],
[   46, 45, Black   ],
[   47, 45, Orange  ],
[   48, 45, Black   ],
[   49, 45, Black   ],
[   50, 45, Black   ],
[   51, 45, Black   ],
[   52, 45, Black   ],
[   53, 45, Black   ],
[   4, 46, Black    ],
[   5, 46, Black    ],
[   6, 46, Black    ],
[   7, 46, Black    ],
[   8, 46, Peach    ],
[   9, 46, Orange   ],
[   10, 46, Orange  ],
[   11, 46, Black   ],
[   12, 46, Black   ],
[   13, 46, Black   ],
[   14, 46, Orange  ],
[   15, 46, Orange  ],
[   16, 46, Black   ],
[   17, 46, Black   ],
[   18, 46, Peach   ],
[   19, 46, Peach   ],
[   20, 46, Orange  ],
[   21, 46, Black   ],
[   22, 46, Black   ],
[   23, 46, Orange  ],
[   24, 46, Peach   ],
[   25, 46, Peach   ],
[   26, 46, Peach   ],
[   27, 46, Peach   ],
[   28, 46, Peach   ],
[   29, 46, Orange  ],
[   30, 46, Orange  ],
[   31, 46, Orange  ],
[   32, 46, Peach   ],
[   33, 46, Peach   ],
[   34, 46, Black   ],
[   35, 46, Black   ],
[   36, 46, Black   ],
[   37, 46, Orange  ],
[   38, 46, Orange  ],
[   39, 46, Black   ],
[   40, 46, Orange  ],
[   41, 46, Black   ],
[   42, 46, Orange  ],
[   43, 46, Black   ],
[   44, 46, Black   ],
[   45, 46, Orange  ],
[   46, 46, Orange  ],
[   47, 46, Black   ],
[   48, 46, Black   ],
[   49, 46, Orange  ],
[   50, 46, Black   ],
[   51, 46, Black   ],
[   52, 46, Black   ],
[   53, 46, Black   ],
[   54, 46, Black   ],
[   4, 47, Black    ],
[   5, 47, Black    ],
[   6, 47, Black    ],
[   7, 47, Black    ],
[   8, 47, Peach    ],
[   9, 47, Orange   ],
[   10, 47, Black   ],
[   11, 47, Orange  ],
[   12, 47, Orange  ],
[   13, 47, Black   ],
[   14, 47, Black   ],
[   15, 47, Black   ],
[   16, 47, Black   ],
[   17, 47, Black   ],
[   18, 47, Peach   ],
[   19, 47, Peach   ],
[   20, 47, Peach   ],
[   21, 47, Peach   ],
[   22, 47, Peach   ],
[   23, 47, Orange  ],
[   24, 47, Black   ],
[   25, 47, Black   ],
[   26, 47, Black   ],
[   27, 47, Orange  ],
[   28, 47, Orange  ],
[   29, 47, Peach   ],
[   30, 47, Peach   ],
[   31, 47, Peach   ],
[   32, 47, Peach   ],
[   33, 47, Black   ],
[   34, 47, Black   ],
[   35, 47, Orange  ],
[   36, 47, Orange  ],
[   37, 47, Orange  ],
[   38, 47, Black   ],
[   39, 47, Black   ],
[   40, 47, Black   ],
[   41, 47, Black   ],
[   42, 47, Black   ],
[   43, 47, Black   ],
[   44, 47, Black   ],
[   45, 47, Orange  ],
[   46, 47, Black   ],
[   47, 47, Black   ],
[   48, 47, Orange  ],
[   49, 47, Orange  ],
[   50, 47, Orange  ],
[   51, 47, Black   ],
[   52, 47, Black   ],
[   53, 47, Black   ],
[   54, 47, Black   ],
[   4, 48, Black    ],
[   5, 48, Black    ],
[   6, 48, Black    ],
[   7, 48, Black    ],
[   8, 48, Peach    ],
[   9, 48, Orange   ],
[   10, 48, Orange  ],
[   11, 48, Orange  ],
[   12, 48, Orange  ],
[   13, 48, Orange  ],
[   14, 48, Orange  ],
[   15, 48, Orange  ],
[   16, 48, Black   ],
[   17, 48, Black   ],
[   18, 48, Orange  ],
[   19, 48, Peach   ],
[   20, 48, Orange  ],
[   21, 48, Peach   ],
[   22, 48, Peach   ],
[   23, 48, Peach   ],
[   24, 48, Peach   ],
[   25, 48, Orange  ],
[   26, 48, Orange  ],
[   27, 48, Orange  ],
[   28, 48, Orange  ],
[   29, 48, Orange  ],
[   30, 48, Black   ],
[   31, 48, Black   ],
[   32, 48, Black   ],
[   33, 48, Black   ],
[   34, 48, Orange  ],
[   35, 48, Orange  ],
[   36, 48, Orange  ],
[   37, 48, Orange  ],
[   38, 48, Black   ],
[   39, 48, Black   ],
[   40, 48, Black   ],
[   41, 48, Black   ],
[   42, 48, Orange  ],
[   43, 48, Orange  ],
[   44, 48, Orange  ],
[   45, 48, Black   ],
[   46, 48, Black   ],
[   47, 48, Orange  ],
[   48, 48, Orange  ],
[   49, 48, Black   ],
[   50, 48, Orange  ],
[   51, 48, Black   ],
[   52, 48, Black   ],
[   53, 48, Black   ],
[   54, 48, Black   ],
[   55, 48, Black   ],
[   4, 49, Black    ],
[   5, 49, Black    ],
[   6, 49, Black    ],
[   7, 49, Black    ],
[   8, 49, Peach    ],
[   9, 49, Orange   ],
[   10, 49, Orange  ],
[   11, 49, Orange  ],
[   12, 49, Orange  ],
[   13, 49, Orange  ],
[   14, 49, Orange  ],
[   15, 49, Orange  ],
[   16, 49, Black   ],
[   17, 49, Orange  ],
[   18, 49, Black   ],
[   19, 49, Peach   ],
[   20, 49, Orange  ],
[   21, 49, Orange  ],
[   22, 49, Peach   ],
[   23, 49, Peach   ],
[   24, 49, Peach   ],
[   25, 49, Orange  ],
[   26, 49, Black   ],
[   27, 49, Orange  ],
[   28, 49, Orange  ],
[   29, 49, Black   ],
[   30, 49, Black   ],
[   31, 49, Orange  ],
[   32, 49, Orange  ],
[   33, 49, Orange  ],
[   34, 49, Orange  ],
[   35, 49, Orange  ],
[   36, 49, Orange  ],
[   37, 49, Orange  ],
[   38, 49, Black   ],
[   39, 49, Black   ],
[   40, 49, Orange  ],
[   41, 49, Orange  ],
[   42, 49, Black   ],
[   43, 49, Orange  ],
[   44, 49, Orange  ],
[   45, 49, Black   ],
[   46, 49, Orange  ],
[   47, 49, Black   ],
[   48, 49, Orange  ],
[   49, 49, Black   ],
[   50, 49, Black   ],
[   51, 49, Peach   ],
[   52, 49, Black   ],
[   53, 49, Black   ],
[   54, 49, Black   ],
[   55, 49, Black   ],
[   56, 49, Black   ],
[   4, 50, Black    ],
[   5, 50, Black    ],
[   6, 50, Black    ],
[   7, 50, Orange   ],
[   8, 50, Peach    ],
[   9, 50, Orange   ],
[   10, 50, Orange  ],
[   11, 50, Orange  ],
[   12, 50, Orange  ],
[   13, 50, Orange  ],
[   14, 50, Orange  ],
[   15, 50, Orange  ],
[   16, 50, Black   ],
[   17, 50, Orange  ],
[   18, 50, Black   ],
[   19, 50, Peach   ],
[   20, 50, Peach   ],
[   21, 50, Black   ],
[   22, 50, Peach   ],
[   23, 50, Peach   ],
[   24, 50, Peach   ],
[   25, 50, Peach   ],
[   26, 50, Peach   ],
[   27, 50, Orange  ],
[   28, 50, Orange  ],
[   29, 50, Orange  ],
[   30, 50, Peach   ],
[   31, 50, Peach   ],
[   32, 50, Orange  ],
[   33, 50, Orange  ],
[   34, 50, Orange  ],
[   35, 50, Orange  ],
[   36, 50, Orange  ],
[   37, 50, Black   ],
[   38, 50, Orange  ],
[   39, 50, Black   ],
[   40, 50, Orange  ],
[   41, 50, Orange  ],
[   42, 50, Black   ],
[   43, 50, Black   ],
[   44, 50, Black   ],
[   45, 50, Black   ],
[   46, 50, Orange  ],
[   47, 50, Black   ],
[   48, 50, Black   ],
[   49, 50, Orange  ],
[   50, 50, Orange  ],
[   51, 50, Orange  ],
[   52, 50, Black   ],
[   53, 50, Black   ],
[   54, 50, Black   ],
[   55, 50, Black   ],
[   56, 50, Black   ],
[   4, 51, Black    ],
[   5, 51, Black    ],
[   6, 51, Black    ],
[   7, 51, Orange   ],
[   8, 51, Peach    ],
[   9, 51, Orange   ],
[   10, 51, Orange  ],
[   11, 51, Orange  ],
[   12, 51, Black   ],
[   13, 51, Orange  ],
[   14, 51, Orange  ],
[   15, 51, Orange  ],
[   16, 51, Orange  ],
[   17, 51, Orange  ],
[   18, 51, Black   ],
[   19, 51, Orange  ],
[   20, 51, Peach   ],
[   21, 51, Black   ],
[   22, 51, Orange  ],
[   23, 51, Peach   ],
[   24, 51, Peach   ],
[   25, 51, Peach   ],
[   26, 51, Peach   ],
[   27, 51, Peach   ],
[   28, 51, Peach   ],
[   29, 51, Peach   ],
[   30, 51, Peach   ],
[   31, 51, Orange  ],
[   32, 51, Orange  ],
[   33, 51, Orange  ],
[   34, 51, Orange  ],
[   35, 51, Orange  ],
[   36, 51, Orange  ],
[   37, 51, Black   ],
[   38, 51, Orange  ],
[   39, 51, Black   ],
[   40, 51, Black   ],
[   41, 51, Black   ],
[   42, 51, Black   ],
[   43, 51, Black   ],
[   44, 51, Orange  ],
[   45, 51, Orange  ],
[   46, 51, Black   ],
[   47, 51, Orange  ],
[   48, 51, Black   ],
[   49, 51, Black   ],
[   50, 51, Black   ],
[   51, 51, Orange  ],
[   52, 51, Peach   ],
[   53, 51, Black   ],
[   54, 51, Black   ],
[   55, 51, Black   ],
[   56, 51, Black   ],
[   4, 52, Black    ],
[   5, 52, Black    ],
[   6, 52, Black    ],
[   7, 52, Black    ],
[   8, 52, Black    ],
[   9, 52, Orange   ],
[   10, 52, Orange  ],
[   11, 52, Orange  ],
[   12, 52, Orange  ],
[   13, 52, Black   ],
[   14, 52, Orange  ],
[   15, 52, Orange  ],
[   16, 52, Orange  ],
[   17, 52, Black   ],
[   18, 52, Orange  ],
[   19, 52, Black   ],
[   20, 52, Peach   ],
[   21, 52, Orange  ],
[   22, 52, Orange  ],
[   23, 52, Peach   ],
[   24, 52, Orange  ],
[   25, 52, Peach   ],
[   26, 52, Peach   ],
[   27, 52, Peach   ],
[   28, 52, Peach   ],
[   29, 52, Peach   ],
[   30, 52, Orange  ],
[   31, 52, Orange  ],
[   32, 52, Peach   ],
[   33, 52, Orange  ],
[   34, 52, Orange  ],
[   35, 52, Orange  ],
[   36, 52, Orange  ],
[   37, 52, Black   ],
[   38, 52, Orange  ],
[   39, 52, Black   ],
[   40, 52, Black   ],
[   41, 52, Orange  ],
[   42, 52, Orange  ],
[   43, 52, Black   ],
[   44, 52, Orange  ],
[   45, 52, Orange  ],
[   46, 52, Black   ],
[   47, 52, Orange  ],
[   48, 52, Orange  ],
[   49, 52, Black   ],
[   50, 52, Black   ],
[   51, 52, Orange  ],
[   52, 52, Black   ],
[   53, 52, Peach   ],
[   54, 52, Black   ],
[   55, 52, Black   ],
[   56, 52, Black   ],
[   5, 53, Black    ],
[   6, 53, Black    ],
[   7, 53, Black    ],
[   8, 53, Black    ],
[   9, 53, Black    ],
[   10, 53, Orange  ],
[   11, 53, Orange  ],
[   12, 53, Orange  ],
[   13, 53, Black   ],
[   14, 53, Orange  ],
[   15, 53, Orange  ],
[   16, 53, Orange  ],
[   17, 53, Black   ],
[   18, 53, Black   ],
[   19, 53, Black   ],
[   20, 53, Peach   ],
[   21, 53, Peach   ],
[   22, 53, Black   ],
[   23, 53, Peach   ],
[   24, 53, Orange  ],
[   25, 53, Peach   ],
[   26, 53, Peach   ],
[   27, 53, Orange  ],
[   28, 53, Orange  ],
[   29, 53, Orange  ],
[   30, 53, Orange  ],
[   31, 53, Peach   ],
[   32, 53, Peach   ],
[   33, 53, Orange  ],
[   34, 53, Orange  ],
[   35, 53, Orange  ],
[   36, 53, Black   ],
[   37, 53, Black   ],
[   38, 53, Orange  ],
[   39, 53, Black   ],
[   40, 53, Orange  ],
[   41, 53, Orange  ],
[   42, 53, Orange  ],
[   43, 53, Black   ],
[   44, 53, Orange  ],
[   45, 53, Orange  ],
[   46, 53, Orange  ],
[   47, 53, Black   ],
[   48, 53, Orange  ],
[   49, 53, Orange  ],
[   50, 53, Black   ],
[   51, 53, Black   ],
[   52, 53, Orange  ],
[   53, 53, Orange  ],
[   54, 53, Black   ],
[   55, 53, Black   ],
[   56, 53, Black   ],
[   6, 54, Black    ],
[   7, 54, Black    ],
[   8, 54, Black    ],
[   9, 54, Black    ],
[   10, 54, Black   ],
[   11, 54, Orange  ],
[   12, 54, Orange  ],
[   13, 54, Black   ],
[   14, 54, Orange  ],
[   15, 54, Orange  ],
[   16, 54, Orange  ],
[   17, 54, Orange  ],
[   18, 54, Black   ],
[   19, 54, Black   ],
[   20, 54, Orange  ],
[   21, 54, Peach   ],
[   22, 54, Black   ],
[   23, 54, Orange  ],
[   24, 54, Peach   ],
[   25, 54, Orange  ],
[   26, 54, Peach   ],
[   27, 54, Peach   ],
[   28, 54, Orange  ],
[   29, 54, Orange  ],
[   30, 54, Orange  ],
[   31, 54, Peach   ],
[   32, 54, Orange  ],
[   33, 54, Orange  ],
[   34, 54, Orange  ],
[   35, 54, Orange  ],
[   36, 54, Black   ],
[   37, 54, Orange  ],
[   38, 54, Orange  ],
[   39, 54, Black   ],
[   40, 54, Black   ],
[   41, 54, Orange  ],
[   42, 54, Orange  ],
[   43, 54, Orange  ],
[   44, 54, Black   ],
[   45, 54, Orange  ],
[   46, 54, Orange  ],
[   47, 54, Orange  ],
[   48, 54, Black   ],
[   49, 54, Orange  ],
[   50, 54, Orange  ],
[   51, 54, Black   ],
[   52, 54, Black   ],
[   53, 54, Black   ],
[   54, 54, Black   ],
[   55, 54, Black   ],
[   6, 55, Black    ],
[   7, 55, Black    ],
[   8, 55, Black    ],
[   9, 55, Black    ],
[   10, 55, Black   ],
[   11, 55, Black   ],
[   12, 55, Orange  ],
[   13, 55, Orange  ],
[   14, 55, Black   ],
[   15, 55, Orange  ],
[   16, 55, Orange  ],
[   17, 55, Orange  ],
[   18, 55, Black   ],
[   19, 55, Black   ],
[   20, 55, Black   ],
[   21, 55, Peach   ],
[   22, 55, Orange  ],
[   23, 55, Black   ],
[   24, 55, Peach   ],
[   25, 55, Orange  ],
[   26, 55, Orange  ],
[   27, 55, Peach   ],
[   28, 55, Peach   ],
[   29, 55, Peach   ],
[   30, 55, Peach   ],
[   31, 55, Peach   ],
[   32, 55, Orange  ],
[   33, 55, Orange  ],
[   34, 55, Orange  ],
[   35, 55, Orange  ],
[   36, 55, Black   ],
[   37, 55, Orange  ],
[   38, 55, Orange  ],
[   39, 55, Orange  ],
[   40, 55, Black   ],
[   41, 55, Orange  ],
[   42, 55, Orange  ],
[   43, 55, Orange  ],
[   44, 55, Black   ],
[   45, 55, Black   ],
[   46, 55, Orange  ],
[   47, 55, Orange  ],
[   48, 55, Black   ],
[   49, 55, Black   ],
[   50, 55, Orange  ],
[   51, 55, Orange  ],
[   52, 55, Black   ],
[   53, 55, Black   ],
[   54, 55, Black   ],
[   55, 55, Black   ],
[   8, 56, Black    ],
[   9, 56, Black    ],
[   10, 56, Black   ],
[   11, 56, Black   ],
[   12, 56, Black   ],
[   13, 56, Orange  ],
[   14, 56, Black   ],
[   15, 56, Orange  ],
[   16, 56, Orange  ],
[   17, 56, Orange  ],
[   18, 56, Orange  ],
[   19, 56, Black   ],
[   20, 56, Black   ],
[   21, 56, Peach   ],
[   22, 56, Peach   ],
[   23, 56, Black   ],
[   24, 56, Orange  ],
[   25, 56, Peach   ],
[   26, 56, Orange  ],
[   27, 56, Orange  ],
[   28, 56, Orange  ],
[   29, 56, Orange  ],
[   30, 56, Peach   ],
[   31, 56, Peach   ],
[   32, 56, Orange  ],
[   33, 56, Orange  ],
[   34, 56, Orange  ],
[   35, 56, Orange  ],
[   36, 56, Black   ],
[   37, 56, Orange  ],
[   38, 56, Orange  ],
[   39, 56, Orange  ],
[   40, 56, Black   ],
[   41, 56, Orange  ],
[   42, 56, Orange  ],
[   43, 56, Orange  ],
[   44, 56, Orange  ],
[   45, 56, Black   ],
[   46, 56, Black   ],
[   47, 56, Orange  ],
[   48, 56, Orange  ],
[   49, 56, Black   ],
[   50, 56, Black   ],
[   51, 56, Black   ],
[   52, 56, Black   ],
[   53, 56, Black   ],
[   54, 56, Black   ],
[   9, 57, Black    ],
[   10, 57, Black   ],
[   11, 57, Black   ],
[   12, 57, Black   ],
[   13, 57, Black   ],
[   14, 57, Black   ],
[   15, 57, Orange  ],
[   16, 57, Orange  ],
[   17, 57, Orange  ],
[   18, 57, Orange  ],
[   19, 57, Black   ],
[   20, 57, Black   ],
[   21, 57, Orange  ],
[   22, 57, Peach   ],
[   23, 57, Orange  ],
[   24, 57, Orange  ],
[   25, 57, Peach   ],
[   26, 57, Peach   ],
[   27, 57, Orange  ],
[   28, 57, Peach   ],
[   29, 57, Peach   ],
[   30, 57, Peach   ],
[   31, 57, Orange  ],
[   32, 57, Orange  ],
[   33, 57, Orange  ],
[   34, 57, Orange  ],
[   35, 57, Black   ],
[   36, 57, Black   ],
[   37, 57, Orange  ],
[   38, 57, Orange  ],
[   39, 57, Orange  ],
[   40, 57, Black   ],
[   41, 57, Black   ],
[   42, 57, Orange  ],
[   43, 57, Orange  ],
[   44, 57, Orange  ],
[   45, 57, Orange  ],
[   46, 57, Black   ],
[   47, 57, Black   ],
[   48, 57, Orange  ],
[   49, 57, Orange  ],
[   50, 57, Black   ],
[   51, 57, Black   ],
[   52, 57, Black   ],
[   53, 57, Black   ],
[   54, 57, Black   ],
[   10, 58, Black   ],
[   11, 58, Black   ],
[   12, 58, Black   ],
[   13, 58, Black   ],
[   14, 58, Black   ],
[   15, 58, Black   ],
[   16, 58, Orange  ],
[   17, 58, Orange  ],
[   18, 58, Orange  ],
[   19, 58, Black   ],
[   20, 58, Orange  ],
[   21, 58, Orange  ],
[   22, 58, Peach   ],
[   23, 58, Orange  ],
[   24, 58, Orange  ],
[   25, 58, Orange  ],
[   26, 58, Peach   ],
[   27, 58, Peach   ],
[   28, 58, Peach   ],
[   29, 58, Peach   ],
[   30, 58, Orange  ],
[   31, 58, Orange  ],
[   32, 58, Orange  ],
[   33, 58, Orange  ],
[   34, 58, Orange  ],
[   35, 58, Orange  ],
[   36, 58, Orange  ],
[   37, 58, Black   ],
[   38, 58, Orange  ],
[   39, 58, Orange  ],
[   40, 58, Orange  ],
[   41, 58, Black   ],
[   42, 58, Orange  ],
[   43, 58, Orange  ],
[   44, 58, Orange  ],
[   45, 58, Orange  ],
[   46, 58, Orange  ],
[   47, 58, Black   ],
[   48, 58, Black   ],
[   49, 58, Black   ],
[   50, 58, Black   ],
[   51, 58, Black   ],
[   52, 58, Black   ],
[   53, 58, Black   ],
[   12, 59, Black   ],
[   13, 59, Black   ],
[   14, 59, Black   ],
[   15, 59, Black   ],
[   16, 59, Black   ],
[   17, 59, Black   ],
[   18, 59, Orange  ],
[   19, 59, Black   ],
[   20, 59, Orange  ],
[   21, 59, Orange  ],
[   22, 59, Peach   ],
[   23, 59, Peach   ],
[   24, 59, Peach   ],
[   25, 59, Orange  ],
[   26, 59, Orange  ],
[   27, 59, Peach   ],
[   28, 59, Peach   ],
[   29, 59, Orange  ],
[   30, 59, Orange  ],
[   31, 59, Peach   ],
[   32, 59, Orange  ],
[   33, 59, Orange  ],
[   34, 59, Orange  ],
[   35, 59, Orange  ],
[   36, 59, Orange  ],
[   37, 59, Black   ],
[   38, 59, Orange  ],
[   39, 59, Orange  ],
[   40, 59, Orange  ],
[   41, 59, Black   ],
[   42, 59, Black   ],
[   43, 59, Orange  ],
[   44, 59, Orange  ],
[   45, 59, Orange  ],
[   46, 59, Black   ],
[   47, 59, Black   ],
[   48, 59, Black   ],
[   49, 59, Black   ],
[   50, 59, Black   ],
[   51, 59, Black   ],
[   52, 59, Black   ],
[   12, 60, Black   ],
[   13, 60, Black   ],
[   14, 60, Black   ],
[   15, 60, Black   ],
[   16, 60, Black   ],
[   17, 60, Black   ],
[   18, 60, Black   ],
[   19, 60, Black   ],
[   20, 60, Orange  ],
[   21, 60, Orange  ],
[   22, 60, Orange  ],
[   23, 60, Peach   ],
[   24, 60, Peach   ],
[   25, 60, Peach   ],
[   26, 60, Orange  ],
[   27, 60, Orange  ],
[   28, 60, Orange  ],
[   29, 60, Orange  ],
[   30, 60, Peach   ],
[   31, 60, Peach   ],
[   32, 60, Orange  ],
[   33, 60, Orange  ],
[   34, 60, Orange  ],
[   35, 60, Orange  ],
[   36, 60, Orange  ],
[   37, 60, Orange  ],
[   38, 60, Black   ],
[   39, 60, Black   ],
[   40, 60, Black   ],
[   41, 60, Orange  ],
[   42, 60, Black   ],
[   43, 60, Orange  ],
[   44, 60, Black   ],
[   45, 60, Black   ],
[   46, 60, Black   ],
[   47, 60, Black   ],
[   48, 60, Black   ],
[   49, 60, Black   ],
[   50, 60, Black   ],
[   14, 61, Black   ],
[   15, 61, Black   ],
[   16, 61, Black   ],
[   17, 61, Black   ],
[   18, 61, Black   ],
[   19, 61, Black   ],
[   20, 61, Black   ],
[   21, 61, Black   ],
[   22, 61, Black   ],
[   23, 61, Orange  ],
[   24, 61, Peach   ],
[   25, 61, Peach   ],
[   26, 61, Peach   ],
[   27, 61, Peach   ],
[   28, 61, Peach   ],
[   29, 61, Peach   ],
[   30, 61, Peach   ],
[   31, 61, Peach   ],
[   32, 61, Orange  ],
[   33, 61, Orange  ],
[   34, 61, Orange  ],
[   35, 61, Orange  ],
[   36, 61, Orange  ],
[   37, 61, Orange  ],
[   38, 61, Black   ],
[   39, 61, Black   ],
[   40, 61, Black   ],
[   41, 61, Black   ],
[   42, 61, Black   ],
[   43, 61, Black   ],
[   44, 61, Black   ],
[   45, 61, Black   ],
[   46, 61, Black   ],
[   47, 61, Black   ],
[   48, 61, Black   ],
[   16, 62, Black   ],
[   17, 62, Black   ],
[   18, 62, Black   ],
[   19, 62, Black   ],
[   20, 62, Black   ],
[   21, 62, Black   ],
[   22, 62, Black   ],
[   23, 62, Black   ],
[   24, 62, Black   ],
[   25, 62, Black   ],
[   26, 62, Orange  ],
[   27, 62, Orange  ],
[   28, 62, Peach   ],
[   29, 62, Peach   ],
[   30, 62, Peach   ],
[   31, 62, Peach   ],
[   32, 62, Orange  ],
[   33, 62, Orange  ],
[   34, 62, Orange  ],
[   35, 62, Orange  ],
[   36, 62, Orange  ],
[   37, 62, Orange  ],
[   38, 62, Black   ],
[   39, 62, Black   ],
[   40, 62, Black   ],
[   41, 62, Black   ],
[   42, 62, Black   ],
[   43, 62, Black   ],
[   44, 62, Black   ],
[   45, 62, Black   ],
[   46, 62, Black   ],
[   17, 63, Black   ],
[   18, 63, Black   ],
[   19, 63, Black   ],
[   20, 63, Black   ],
[   21, 63, Black   ],
[   22, 63, Black   ],
[   23, 63, Black   ],
[   24, 63, Black   ],
[   25, 63, Black   ],
[   26, 63, Black   ],
[   27, 63, Black   ],
[   28, 63, Black   ],
[   29, 63, Black   ],
[   30, 63, Black   ],
[   31, 63, Black   ],
[   32, 63, Black   ],
[   33, 63, Black   ],
[   34, 63, Black   ],
[   35, 63, Black   ],
[   36, 63, Black   ],
[   37, 63, Black   ],
[   38, 63, Black   ],
[   39, 63, Black   ],
[   40, 63, Black   ],
[   41, 63, Black   ],
[   42, 63, Black   ],
[   43, 63, Black   ],
[   44, 63, Black   ]]
    
    
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

atlas = load_atlas("./RazorEnhanced/Scripts/MeesaAtlas" + str(atlasVersion) + ".pkl")


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