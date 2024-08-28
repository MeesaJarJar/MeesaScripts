# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! ------------#
# -------------------------------------------------------------#
# Description: This script is a Player Vendor Scanning script
# made to be used with the Vendor Scanner GUMP ingame. 
# This script is called automatically, you do not need to start
# it, only add it to RE Scripts tab. If you set up XAMPP on your
# pc in the location I show in config, then you can also
# make use of the internet page I created that displays the 
# items in a searchable, easy to use format.
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#

#folder = r"C:\\Program Files (x86)\\UOForever\\UO\\Forever\\RazorEnhanced\\"
folder = r"C:\\xampp\\htdocs\\"
# END CONFIG --------------------------------------------------#

from System.Collections.Generic import List
from System import Byte
import re
import os
import random
import struct
import clr
clr.AddReference("System.Drawing")
from System.Drawing import Image
from System.Drawing.Imaging import ImageFormat

vendorMasterList = []
scannedContainers = set()
itemMasterList = []
delay = 300

def remove_html_tags(input_string):
    # Pattern to match anything within < > style tags
    pattern = r'<[^>]+>'
    return re.sub(pattern, '', input_string)
    
def remove_property_objects(s):
    # Remove all the unwanted patterns
    pattern = r'<RazorEnhanced\.Property object at 0x[0-9a-fA-F]+'
    cleaned_string = re.sub(pattern, '', s)
    
    # Extract all properties within square brackets
    properties = re.findall(r'\[.*?\]', cleaned_string)
    
    # Concatenate properties with a comma separator
    properties_str = ','.join(properties)
    
    # Extract the trailing characters after ')'
    trailing_characters = re.findall(r'\)\|.*', cleaned_string)[0][1:]
    
    # Combine the properties string with the trailing characters
    final_string = properties_str + trailing_characters
    
    return (remove_html_tags(final_string)).replace('[Property],[ ', '')


def scan_container(container_serial, vendor_position, vendor_name):
    #print("In Scan Container");
    container = Items.FindBySerial(container_serial)
    if container and container.Serial not in scannedContainers:
        scannedContainers.add(container.Serial)  # Keep track of scanned containers
        
        Items.UseItem(container)
        Misc.Pause(delay)
        if '0 Items' not in (cont.Properties):
            for item in container.Contains:
                if item.IsContainer:
                    # Recursive call for nested containers
                    #print("Found Container in Container. Scanning new container");

                    scan_container(item.Serial, vendor_position, vendor_name)
                else:
                    # Process item
                    #print("Item:", item.Name);
                    itemMasterList.append([item.Serial, vendor_position[0], vendor_position[1], vendor_name.replace(',', '')])


Journal.Clear()
Misc.ClearIgnore()
Misc.SetSharedValue('PlayerLastX', Player.Position.X)
Misc.SetSharedValue('PlayerLastY', Player.Position.Y)

def checkMoving():
    PlayerLastX = Misc.ReadSharedValue('PlayerLastX')
    PlayerLastY = Misc.ReadSharedValue('PlayerLastY')

    # Check if the players current position is different from the last known position
    if PlayerLastX != Player.Position.X or PlayerLastY != Player.Position.Y:
        # Player has moved
        Misc.SetSharedValue('PlayerIsMoving', True)
        #Player.HeadMessage(0,"MOVING")
    else:
        # Player has not moved
        Misc.SetSharedValue('PlayerIsMoving', False)
        #Player.HeadMessage(9,"STOPPED")

    # Update the last known position to the current position
    Misc.SetSharedValue('PlayerLastX', Player.Position.X)
    Misc.SetSharedValue('PlayerLastY', Player.Position.Y)
    
def append_unique_line(file_path, line):
    # Read all existing lines in the file
    with open(file_path, 'r', encoding='utf-8') as file:
        existing_lines = file.readlines()

    # Check if the line already exists in the file
    if line + '\n' not in existing_lines:
        # If the line doesnt exist, append it to the file
        with open(file_path, 'a', encoding='utf-8') as file:
            encoded_line = line.encode('utf-8')  # Encode the line
            file.write(encoded_line.decode('utf-8') + '\n')  # Decode and write the line
            #print(f"Line appended to {file_path}: {line}")
    #else:
        #print(f"The line already exists in {file_path}: {line}")


        
while True:
    mobileFilter = Mobiles.Filter()
    mobileFilter.Enabled = True
    mobileFilter.RangeMin = -1
    mobileFilter.RangeMax = 18
    mobileFilter.CheckLineOfSight = False
    mobileFilter.IsGhost = False
    mobileFilter.Notorieties = List[Byte](bytes([7]))  # Not 100% sure these are right notorieties
    mobileFilter.CheckIgnoreObject = True 
    foundMobiles = Mobiles.ApplyFilter(mobileFilter)
    
    checkMoving();
    
    Misc.Pause(250)
    count = 0
    for mobile in foundMobiles:
        count = count + 1
        if Journal.Search('wait to perform another'):
            Journal.Clear()
            delay += 25
            print("Opening Containers Too fast. Raising Delay to: " + str(delay))
        
        Timer.Create('PSTOP',99999)    
        while Misc.ReadSharedValue('PlayerIsMoving') == True:

            Player.HeadMessage(99,'STOP MOVING!')
            Misc.Pause(333);
            checkMoving();
            
            
        Player.HeadMessage(0,"Scraping Mob [" + str(count) + "|" + str(len(foundMobiles)) + "] : " +  str(mobile.Name))
        
        if mobile.Serial not in vendorMasterList:
            vendorMasterList.append(mobile.Serial)
            vendorMobile = Mobiles.FindBySerial(mobile.Serial)
            
            if vendorMobile is not None:
                Misc.IgnoreObject(vendorMobile)
                if vendorMobile.Backpack is not None:
                    mymobilepack = vendorMobile.Backpack.Serial
                    cont = Items.FindBySerial(mymobilepack)

                    if cont.Serial not in scannedContainers:
                        Items.WaitForProps(cont,250)
                        
                        if '0 items' not in str(cont.Properties).lower():
                            Items.UseItem(cont)
                            Misc.Pause(delay)      
                        
                            for item in cont.Contains:
                                Items.WaitForProps(item,250)
                                #print("*******", item.Properties)
                                if item.IsContainer and '0 items' not in str(item.Properties).lower():
                                    scan_container(item.Serial, [vendorMobile.Position.X, vendorMobile.Position.Y], vendorMobile.Name)
                                else:
                                    itemMasterList.append([item.Serial, vendorMobile.Position.X, vendorMobile.Position.Y, vendorMobile.Name.replace(',', '')])
                        else:
                            print("Found Empty Container.");
                        
    for item in itemMasterList:
        itemx = Items.FindBySerial(item[0])
        if itemx is not None:
            towrite = str(itemx.ItemID).strip() + '|' + remove_html_tags(str(itemx.Name)).strip() + '|' + remove_property_objects(str(itemx.Properties).strip() + "|" + str(item[1]).strip() + "|" + str(item[2]).strip()+ "|" + str(item[3]).strip() + "|" + str(itemx.Hue))
            if 'Price' in towrite and 'Price: Not for sale.' not in towrite:
            
                itemImage = Items.GetImage(itemx.ItemID, itemx.Hue);
                
                output_folder = "C:\\xampp\\htdocs\\UOItems\\"

                output_filename = output_folder + str(itemx.ItemID).strip() + '_' + str(itemx.Hue).strip() + ".png"

                itemImage.Save(output_filename, ImageFormat.Png);
                
                towrite = ' '.join(towrite.split())
                
                append_unique_line(folder + 'vendorsaleitemdata.csv', towrite)

                #Misc.AppendNotDupToFile(folder + 'vendorsaleitemdata.csv', towrite)

    itemMasterList.clear()
    Player.HeadMessage(256,'Keep Walking!')
    Timer.Create('PSTOP',1)