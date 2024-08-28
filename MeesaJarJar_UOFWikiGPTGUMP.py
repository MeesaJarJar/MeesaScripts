# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! ------------#
# -------------------------------------------------------------#
# Description: UOF Trained AI Chat Bot
# Trained off of WIKI Data 7/10/2024 for UOForever Server
# This was just a proof of concept. It will not work for you
# unless you replace the API key with your own OpenAI Pro Key. 
# This was only to demonstrate how GPT could be leveraged with
# trained data to provide user answers to questions, among
# other interesting concepts. This will not work unless you
# also have a simple web server to run a php script to call the
# custom GPT that was created. I believe I posted what is needed
# in the Razor Enhanced Discord server if you are interested.
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#

# END CONFIG --------------------------------------------------#

from System.Collections.Generic import List
from System import String
from System import Int32 as int
from System.Threading import Thread, ThreadStart
import os
import re
import urllib.request
import urllib.parse

gumpNumber = 53778 
searchText = "What does a silver slayer do damage against?"
searchResponse = ''
htmltext = ''
def extract_last_bracket_items(input_string):
    match = re.search(r'\[([^\[\]]*)\](?!.*\[)', input_string)
    
    if match:
        items = match.group(1).split(',')
        items = [item.strip() for item in items]
        return items
    else:
        return []

      
def updateGump(): 
    gd = Gumps.CreateGump(True,True,True,True)

    Gumps.AddBackground(gd,0,0,512,60,40000)
    Gumps.AddBackground(gd,-15,-5,100,20,420)
    Gumps.AddLabel(gd,3,-3,1152,"Question:")
    if searchResponse != '':
        Gumps.AddBackground(gd,0,100,512,400,39925)
        Gumps.AddHtml(gd,25,125,500,350,str(searchResponse),False,True)
       
        Gumps.AddBackground(gd,-15,95,100,20,420)
        Gumps.AddLabel(gd,3,95,1152,"Answer:")
        
        
    Gumps.AddTextEntry(gd, 25, 20, 450, 35, 1152, 8855, str(searchText))

    Gumps.AddImage(gd,220,45,516)
    Gumps.AddButton(gd,230,55,518,518,4,1,0)
    Gumps.AddImage(gd,225,55,494)
    Gumps.AddLabel(gd,175,70,1150,"- Ask           Question -")
    Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)

def create_anchor_tags(input_string):
    match = re.search(r'\[([^\[\]]*)\](?!.*\[)', input_string)
    if match:
        items = match.group(1).split(',')
        anchor_tags = [f"<a href='{item.strip()}'>{item.strip()}</a>" for item in items]
        return anchor_tags
    else:
        return []

def searchQuestion(query_param):
    base_url = "http://ec2-99-99-99-99.us-east-2.compute.amazonaws.com:3000/query"
    encoded_query = urllib.parse.urlencode({"content": query_param})

    full_url = f"{base_url}?{encoded_query}"

    response_data = '' 
    with urllib.request.urlopen(full_url) as response:
        response_data = response.read().decode('utf-8') 

    htmltext =  response_data 
    cleaned_string = htmltext.replace('assistant > file_search', '')

    htmltext = cleaned_string.replace('assistant >', '')
    
    tags = create_anchor_tags(htmltext)
    tags_string = ' '.join(tags)
    htmltext = "Meesa Jar Jar says: " + htmltext + ' ' + tags_string
    return htmltext.strip()
    
 
updateGump()    
while True:
    Misc.Pause(100)
    
    gd = Gumps.GetGumpData(gumpNumber)

    if gd:
        if gd.buttonid != -1:
            if gd.buttonid == 0:
                searchResponse =''
                searchText = ''
                gd.buttonid = -1
                updateGump() 

        
        if gd.buttonid == 4:
                print("Asking a question!")
                searchText = str(Gumps.GetTextByID(gd, 8855))
                gd.buttonid = -1
                if len(searchText.strip()) > 4:
                    try:
                        searchResponse = searchQuestion(searchText)
                    except:
                        print("GENERAL ERROR: TELL JAR JAR")
                else:
                    print("Error: Must type a question first!")
                    
                updateGump()
                Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)
                updateGump()
