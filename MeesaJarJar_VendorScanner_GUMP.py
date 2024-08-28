# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! ------------#
# -------------------------------------------------------------#
# Description: 
# This script works in conjunction with MeesaJarJar Vendor Scanner
# Only this script needs to be run. You may set your Razor 
# Enhanced for this script to AutoStart at Login. The GUMP
# starts minimized. Click the green arrow next to Vendor Search 
# to open it. 
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#
gumpNumber = 786786786 #Can be any number not already used by other GUMPs. 
#file_path = r"C:\Program Files (x86)\UOForever\UO\Forever\RazorEnhanced\vendorsaleitemdata.csv"
file_path = r"C:\xampp\htdocs\vendorsaleitemdata.csv"
# END CONFIG --------------------------------------------------#

from System.Collections.Generic import List
from System import String
from System import Int32 as int
from System.Threading import Thread, ThreadStart
import csv
import random
import os
import time
import re

pageItems           = [];

currentPage         = 0;
totalItems          = 0;
filteredItems       = 0;
vendorSaleData      = None;
selectedItemID      = None;
selectedIndexNumber = None;
showMap             = False;
minimized           = False;
bgON                = True;


def extract_price(text):
    match = re.search(r'Price: ([\d,]+)', text)
    if match:
        return int(match.group(1).replace(',', ''))
    else:
        return None 

def resizeSmaller(larger_x, larger_y):
    
    larger_x = int(larger_x)
    larger_y = int(larger_y)
    larger_map_width = 5119
    larger_map_height = 4096
    smaller_map_size = 383

    smaller_x = int(larger_x * smaller_map_size / larger_map_width)
    smaller_y = int(larger_y * smaller_map_size / larger_map_height)

    return smaller_x, smaller_y
               
def applyFilter():
    global filteredItems, totalItems, vendorSaleData, pageItems, itemFilterPriceMin, itemFilterPriceMax, itemFilterName, itemFilterProperties

    pageItems = []
    currentPage = 0
    
    vendorSaleData = None
    selectedItemID = None
    selectedIndexNumber = None

    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            pass

    with open(file_path, 'r') as file:
        vendorSaleData = [line.strip() for line in file]
    totalItems = len(vendorSaleData)
    
    count = 0 

    filtered_data = [] 

    if itemFilterPriceMin == '':
        itemFilterPriceMin = 0;

    for item in vendorSaleData:
        rowData = item.split('|')
        try:
            price = extract_price(rowData[2])
            
        except:
            #print("Failed Getting Price from 2. Here is Row Data:");
            Misc.Pause(10)
            
        shouldWrite = True
        
        if 'free' in str(price).lower():
            price = 0

        if price is None:
           shouldWrite = False
           
        elif int(price) > int(itemFilterPriceMax) or int(price) < int(itemFilterPriceMin):
            shouldWrite = False
            
        if itemFilterName is not None:   
            if itemFilterName.lower() not in str(rowData[1]).lower():
                shouldWrite = False
                
        if itemFilterProperties is not None:   

            if itemFilterProperties.lower() not in str(rowData[2]).lower():
                shouldWrite = False
                 
        if shouldWrite:                
            pageItems.append(count)
            count = count + 1
            filtered_data.append(item)
            
    vendorSaleData = filtered_data  
    filteredItems = len(filtered_data)
 
def updateGump():
    if minimized == True:
        gd = Gumps.CreateGump();
        Gumps.AddPage(gd, 0);
        Gumps.AddImage(gd,580,0,40019)
        Gumps.AddLabel(gd,595,4,1152,"Vendor Search")
        Gumps.AddButton(gd,685,2,5540,5541,207,1,0)

    else:
        gd = Gumps.CreateGump();
        Gumps.AddPage(gd, 0);
        
        
        #if bgON:
        Gumps.AddImage(gd,0,0,40009)
            
        #Gumps.AddImage(gd,600,350,40010) #Item Preview
        
        if selectedIndexNumber is not None:
            
            Gumps.AddImage(gd,535,432,2524)
            Gumps.AddImage(gd,535,403,2521)
            Gumps.AddImage(gd,705,433,2525)
            Gumps.AddImage(gd,705,403,2522)
            
            Gumps.AddLabel(gd,643,417,2038,"Item Preview")
        
        Gumps.AddButton(gd,600,325,40135,40136,210,1,0)
        Gumps.AddLabel(gd,630,325,1997," Start Logging")
        Gumps.AddButton(gd,600,355,40135,40136,211,1,0)
        Gumps.AddLabel(gd,630,355,1997,"  Stop Logging")
        Gumps.AddButton(gd,600,385,40135,40136,212,1,0)
        Gumps.AddLabel(gd,630,385,1997,"  Clear Data")
        
        if showMap == False:
            
            if bgON:
                Gumps.AddImage(gd,510,145,299)

        if bgON:
            Gumps.AddImage(gd,30,65,1473) 

        Gumps.AddImage(gd,580,0,40019)
        Gumps.AddLabel(gd,595,4,1152,"Vendor Search")
        Gumps.AddButton(gd,685,2,5538,5539,207,1,0)
        
        
        
        for i in range(0,20):
            Gumps.AddImage(gd,30 + (35*i),79,40007)
        Gumps.AddImage(gd,30,79,40006)
        Gumps.AddImage(gd,695,79,40008)
        Gumps.AddImage(gd,30,30,1764)
        Gumps.AddButton(gd,240,82,40016,40026,101,1,0)
        

        if showMap == True:
            Gumps.AddImageTiled(gd,630,105,200,200,9003)
            Gumps.AddImage(gd,625,100,5528)
            Gumps.AddImage(gd,270,80,40019)
            Gumps.AddButton(gd,975,150,1231,1231,205,1,0)
        else:

            Gumps.AddButton(gd,690,100,1231,1231,205,1,0)
            
        if pageItems is None:
            Gumps.AddLabel(gd,287,83,1149,"Page: " + str(currentPage) + ' / ' + str(0))
        else:    
            Gumps.AddLabel(gd,287,83,1149,"Page: " + str(currentPage + 1) + ' / ' + str(round(len(pageItems)/10) +1))
        
        Gumps.AddLabel(gd,45,110,1149,'ItemID')
        
        Gumps.AddLabel(gd,123,110,1149,'Price')
        Gumps.AddLabel(gd,280,110,1149,'Name')
        Gumps.AddLabel(gd,425,110,1149,'Location')
        Gumps.AddLabel(gd,505,110,1149,'Vendor Name  TRACK')
        
        if filteredItems != 0 or totalItems != 0:
        
            Gumps.AddLabel(gd,50,80,1000,"Filtered Items: " + str(filteredItems) + " of "  + str(totalItems)  )
        
        Gumps.AddButton(gd,395,82,40017,40027,102,1,0)
        Gumps.AddImage(gd,10,100,2221)
        Gumps.AddImage(gd,10,250,2221)
        
        Gumps.AddButton(gd, 490, 76, 2472, 2474, 206, 1, 0)  
        Gumps.AddLabel(gd,520,80,1152,"Clear Tracker")
        
        
        
        lineOffsetX =75
        lineOffsetY = 135
        lineSpacingY = 35
        
        count = 0
        for z in range((currentPage * 10), (currentPage * 10) + 10):

            if vendorSaleData is not None and pageItems is not None:
                try:
                    rowData = vendorSaleData[pageItems[z]]
                    
                    rowData = rowData.split('|')
                  
                    price = extract_price(rowData[2]);

                    if 'free' in str(price).lower():
                        price = 0;
                 
                    if z == selectedIndexNumber:
                        
                        pinX,pinY = resizeSmaller(rowData[3],rowData[4])
                        pinX = pinX + 625
                        pinY = pinY + 100 
                        Gumps.AddImageTiled(gd,lineOffsetX-70,lineOffsetY  + (lineSpacingY * count),605,25,40004)
                        if showMap:

                            Gumps.AddImage(gd,lineOffsetX-100, lineOffsetY -4 + (lineSpacingY * count),1227)
                            Gumps.AddImage(gd,pinX,pinY,11410)

                    Gumps.AddLabel(gd,lineOffsetX-25,lineOffsetY + (lineSpacingY * count) ,int(rowData[6])-1,rowData[0])
                    Gumps.AddLabelCropped(gd,lineOffsetX + 125,lineOffsetY + (lineSpacingY * count),200,35,1149,rowData[1])
                    Gumps.AddLabel(gd,lineOffsetX + 332,lineOffsetY + (lineSpacingY * count),800,"X:" + str(rowData[3]) + ' Y:' + str(rowData[4]))
                    Gumps.AddLabelCropped(gd,lineOffsetX + 430,lineOffsetY + (lineSpacingY * count),100,35,1149,str(rowData[5]))
                    Gumps.AddLabel(gd,lineOffsetX + 50,lineOffsetY + (lineSpacingY * count),650,str(price))

                    Gumps.AddButton(gd, lineOffsetX + 530, lineOffsetY -2 + (lineSpacingY * count), 2151, 2153, (2000 + z), 1, 0)  
                    Gumps.AddButton(gd, lineOffsetX-70, lineOffsetY -2 + (lineSpacingY * count), 4005, 4006, (1000 + z), 1, 0)

                    count = count + 1;
                except:
                    pass
                    #print("FAILED TO LOAD A FULL PAGE OF ITEMS");
            
        Gumps.AddLabel(gd,50,35,1149,'  Min    Price    Max')  
        
        Gumps.AddTextEntry(gd,50,50,50,15,0,201,str(itemFilterPriceMin))
        
        Gumps.AddTextEntry(gd,165,50,50,15,0,202,str(itemFilterPriceMax))
        
        Gumps.AddImage(gd,235,30,1764)
        
        Gumps.AddLabel(gd,305,35,1149,'Item Name')
        
        if itemFilterName is None:
        
            Gumps.AddTextEntry(gd,260,50,150,15,0,203,str(''))
        else: 
            Gumps.AddTextEntry(gd,260,50,150,15,0,203,str(itemFilterName))
              
        Gumps.AddButton(gd,620,38,40021,40031,99,1,0)   
        Gumps.AddLabel(gd,650,40,2036,"Apply/Refresh")     
            
        if bgON:
            Gumps.AddButton(gd,620,78,2153,2154,217,1,0)   
        else:
            Gumps.AddButton(gd,620,78,9720,9721,217,1,0)   
            
        Gumps.AddLabel(gd,650,80,2036,"Toggle BG") 
        
        Gumps.AddImage(gd,440,30,1764)
        
        Gumps.AddLabel(gd,515,35,1149,'Properties')
        
        if itemFilterProperties is None:
            Gumps.AddTextEntry(gd,460,50,150,15,0,204,str(""))
        else:
            Gumps.AddTextEntry(gd,460,50,150,15,0,204,str(itemFilterProperties))
            
        if selectedIndexNumber is not None and vendorSaleData is not None :

            Gumps.AddHtml(gd,35,470,585,75,vendorSaleData[selectedIndexNumber],1,1)
        
        
        
        if selectedIndexNumber is not None:

            test = vendorSaleData[selectedIndexNumber].split('|')
            
            Gumps.AddItem(gd,660,470,int(test[0]), int(test[6]))
            
    Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)
       
def track(number):
    if number == None:
        Player.TrackingArrow(0,0,False,False)  
    else:
        tracker = vendorSaleData[number].split('|')
        Player.TrackingArrow(int(tracker[3]),int(tracker[4]),True,False)
     
def run_logging_start():
    Player.HeadMessage(0,'STARTING VENDOR LOGGING')
    Misc.ScriptRun("MeesaJarJar_VendorScanner.py")

def run_logging_stop():
    Player.HeadMessage(0,'STOPPING VENDOR LOGGING')
    if Misc.ScriptStatus("MeesaJarJar_VendorScanner.py"):
        Misc.ScriptStop("MeesaJarJar_VendorScanner.py")
    
current_directory = os.getcwd()
print(f"The script is running in: {current_directory}")

itemFilterPriceMin   = 0;
itemFilterPriceMax   = 9999999;
itemFilterName       = None;
itemFilterProperties = None;

applyFilter()

updateGump() 

while True:
    
    Misc.Pause(250)
    gd = Gumps.GetGumpData(gumpNumber)
    
    if gd:
        
        if gd.buttonid == 0:
            minimized = True
            Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)
            updateGump()
            
        if gd.buttonid == 101:
            if currentPage > 0:
                currentPage = currentPage - 1
            gd.buttonid = -1
            updateGump()         
        
        if gd.buttonid == 102:
            if currentPage < len(pageItems)/10-1:
                currentPage = currentPage + 1
            gd.buttonid = -1
            updateGump()  
        if gd.buttonid == 205:
            if showMap == True:
                showMap = False;
            else:
                showMap = True;
            updateGump()    
                
        if gd.buttonid == 207:
            if minimized == True:
                minimized = False;
            else:
                minimized = True;
            updateGump()    
                           
        if gd.buttonid == 99:

            itemFilterPriceMin = Gumps.GetTextByID(gd,201)
            itemFilterPriceMax = Gumps.GetTextByID(gd,202)
            itemFilterName = Gumps.GetTextByID(gd,203)
            itemFilterProperties = Gumps.GetTextByID(gd,204)
            
            currentPage = 0
            selectedIndexNumber = None

            applyFilter()
            gd.buttonid = -1
            updateGump() 
            
        if gd.buttonid == 4:
            gd.buttonid = -1
            updateGump() 

        if gd.buttonid == 3:
            gd.buttonid = -1
            updateGump() 

        if gd.buttonid == 2:
            gd.buttonid = -1
            updateGump() 

        if gd.buttonid == 1:
            gd.buttonid = -1
            updateGump() 
        
        if gd.buttonid == 210:
            Player.HeadMessage(0, 'Starting Vendor Logging. ')
            script_thread = Thread(ThreadStart(run_logging_start))
            script_thread.Start()
            gd.buttonid = -1
            applyFilter()
            updateGump()
        
        if gd.buttonid == 211:
            Player.HeadMessage(0, 'Stopping Vendor Logging. ')
            script_thread = Thread(ThreadStart(run_logging_stop))
            script_thread.Start()
            gd.buttonid = -1
            applyFilter()
            updateGump()

        if gd.buttonid == 212:
            Player.HeadMessage(0, 'Clearing Vendor Log. ')
            print("Deleting:", file_path)
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"The file {file_path} has been deleted.")
                else:
                    print(f"The file {file_path} does not exist.")
                    
                #Misc.DeleteFile(file_path)
                
            except:
                print("FAILED TO DELETE VENDOR LOG FILE.")
            gd.buttonid = -1
            applyFilter()
            updateGump()
            
        if gd.buttonid == 217:
            Player.HeadMessage(0, 'Toggled BG. ')
        
            if bgON == True:
                bgON = False;
            else:
                bgON = True;
            
            gd.buttonid = -1
            updateGump()
            
        if gd.buttonid >= 1000 and gd.buttonid <= 1999:
            selectedIndexNumber =  (gd.buttonid - 1000)
            gd.buttonid = -1;
            updateGump() 
        if gd.buttonid == 206:
        
            track(None);
            updateGump()
        if gd.buttonid >= 2000 and gd.buttonid <= 3999:
            trackNumber =  (gd.buttonid - 2000)
            track(trackNumber);
            gd.buttonid = -1;
            updateGump()       
