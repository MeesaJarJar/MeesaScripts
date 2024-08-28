# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description: Trivia Manager for Trivia on UOForever 
# Made this as a Mini Game for the Auction on UOF
# Questions saved in the CSV file in the following format:
# Number,Question,Answer,Asked
# 1,What skill in Ultima Online Forever is used to craft potions?,Alchemy,0
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#
csv_file_path = r'C:\Program Files (x86)\UOForever\UO\Forever\RazorEnhanced\trivia.csv'
filterWords = ['the','of','in','on','a','and']
# END CONFIG --------------------------------------------------#

gumpNumber = 6644433

from System.Collections.Generic import List
from System import String
from System import Int32 as int
from System.Threading import Thread, ThreadStart
import csv
import random
import os
import time

current_directory = os.getcwd()
print(f"The script is running in: {current_directory}")


def load_data():
    data = []
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append(row)
    return data

def save_data(data):
    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)

def select_random_question(data):
    data = data[3:]
    random_question = random.choice(data)

    question = random_question[1]
    answer = random_question[2]

    count = int(random_question[3]) if random_question[3].strip() else 0

    return question, answer, count

def add_question(data, new_question, new_answer):

    for row in data[3:]:
        if row[1].lower() == new_question.lower():
            return "Question already exists."

    new_row = [len(data) - 3 + 1, new_question, new_answer, 0, '', '', '']
    data.append(new_row)
    save_data(data)
    return "Question added successfully."

def check_answer(question, user_answer):
    data = load_data()

    data = data[3:]

    for row in data:
        if row[1].lower() == question.lower():
            actual_answer = row[2].lower()
            user_answer = user_answer.lower().replace(" ", "")
            return actual_answer == user_answer

    return False

selectedQuestion = None;
selectedAnswer   = None;
selectedCount    = None;
selectedWinner   = None;
logChat          = True;
winnerSet        = False;
startLoggingTimestamp = int(time.time())
matches = []
unfilteredLog = []
winnerPosition = None;

def updateGump():
    global selectedWinner
    global winnerPosition
    rightPageOffsetX = 225
    rightPageOffsetY = 50
    leftPageOffsetX = 25
    leftPageOffsetY = 50
    gd = Gumps.CreateGump();
    Gumps.AddPage(gd, 0);
    
    Gumps.AddImage(gd,0,0,39923)
    Gumps.AddLabel(gd,leftPageOffsetX+40, leftPageOffsetY-40, 0, "Say Question & Start")
    Gumps.AddButton(gd, leftPageOffsetX, leftPageOffsetY-40, 4005, 4006, 2, 1, 0)
    
    journalList = Journal.GetTextByType('Regular',True)
    matches = []
    unfilteredLog =[]
    matchesLower = []
    for entry in journalList:
        
        unfilteredLog.append(entry)
        entry = entry.split(':');
        
        name = entry[0]
        message = entry[1]
                
        for answer in selectedAnswer.split():
            
            
            if str(answer.lower()) in str(message).lower() and str(answer.lower()) not in filterWords:
                
                if [name.lower(),message.lower()] not in matchesLower:
                    matchesLower.append([name.lower(),message.lower()]);
                    matches.append([name,message]);

                    
                    
    matchesStrings = ["\n".join(pair) for pair in matchesLower]

    count = 0
    lineHeight = 22
    for match in matches:
        if count < 9:

            Gumps.AddImage(gd,leftPageOffsetX-25 , 50 + (lineHeight * count),1803)
            Gumps.AddImage(gd,leftPageOffsetX - 100, 50 + (lineHeight * count),5031)
            Gumps.AddLabelCropped(gd,leftPageOffsetX - 90, 50 + (lineHeight * count),100,20,0,match[0])
            if count == winnerPosition:
                Gumps.AddImage(gd,leftPageOffsetX-125,45+ (lineHeight * count),1227)
            Gumps.AddButton(gd,leftPageOffsetX+160,50 + (lineHeight * count),4005,4006,1000 + count,1,0)

            Gumps.AddLabelCropped(gd,leftPageOffsetX + 15, 50  + (lineHeight * count),100,25,0,match[1])
            
            
        count+=1
    
    matchesStr = "\n".join(unfilteredLog);
    
    Gumps.AddButton(gd, 0, 380, 5018, 5018, 3, 1, 0)
    Gumps.AddHtml(gd,leftPageOffsetX+25 ,leftPageOffsetY + 330,383,150,str(matchesStr),9304,True)
    Gumps.AddLabel(gd,rightPageOffsetX+40, rightPageOffsetY-40, 0, "Random Question :")
    Gumps.AddButton(gd, rightPageOffsetX, rightPageOffsetY-40, 4005, 4006, 1, 1, 0)
    Gumps.AddLabel(gd,rightPageOffsetX+70, rightPageOffsetY+208, 0, "Answer:")
    Gumps.AddHtml(gd,rightPageOffsetX ,rightPageOffsetY,180,180,str(selectedQuestion),9304,False)
    Gumps.AddLabel(gd,rightPageOffsetX+20, rightPageOffsetY+190, 0, "Times Asked : " + str(selectedCount))
    Gumps.AddHtml(gd,rightPageOffsetX ,rightPageOffsetY+223,180,100,str(selectedAnswer),9304,False)
    
    if winnerPosition is not None:
        
        if matches != []:
            selectedWinner = matches[winnerPosition]

            Gumps.AddHtml(gd,leftPageOffsetX ,leftPageOffsetY+223,180,100,str(selectedWinner[0] + "\n" + selectedWinner[1]),9304,False)

            Gumps.AddLabel(gd,leftPageOffsetX,leftPageOffsetY+200,0,'Currently Selected Winner :')
            Gumps.AddLabel(gd,leftPageOffsetX + 125,leftPageOffsetY + 275,0,"Accept?")
            Gumps.AddButton(gd,leftPageOffsetX + 115,leftPageOffsetY + 295,1147,1148,4,1,0)

    Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)
       

data = load_data()  

random_question, answer, count = select_random_question(data)
#print("Random Question:", random_question)
#print("Answer:", answer)
#print("Count:", count)
selectedQuestion = random_question
selectedAnswer = answer
selectedCount = count
  
updateGump() 

while True:
    
    Misc.Pause(1000)
    gd = Gumps.GetGumpData(gumpNumber)
    
    if gd:

        if gd.buttonid == 4:
            
            Player.ChatSay(295,"WE HAVE A WINNER!")
            Misc.Pause(500);
            Player.ChatSay(294,"Congrats, " + str(selectedWinner) +"!")
            Misc.Pause(500);
            Player.ChatSay(295,"You won!")
            
        if gd.buttonid == 3:
            Journal.Clear();
            winnerPosition = None;
            
        if gd.buttonid == 2:
            startLoggingTimestamp = int(time.time())
            Misc.Pause(500);
            Journal.Clear()
            Player.ChatSay(295,"Quiet Please...")
            Misc.Pause(1000);
            Player.ChatSay(295,"We are about to start the next Trivia Question...")
            Misc.Pause(1000);
            Player.ChatSay(295,"5...")
            Misc.Pause(1000);
            Player.ChatSay(295,"4...")
            Misc.Pause(1000);
            Player.ChatSay(295,"3...")
            Misc.Pause(1000);
            Player.ChatSay(295,"2...")
            Misc.Pause(1000);
            Player.ChatSay(295,"1...")
            Misc.Pause(1000);  
            Player.ChatSay(295,selectedQuestion)
            Journal.Clear()
            
        if gd.buttonid == 1:
            
            Player.HeadMessage(0, 'Selecting a Question at Random!')
            winnerPosition = None;
            random_question, answer, count = select_random_question(data)
            #print("Random Question:", random_question)
            #print("Answer:", answer)
            #print("Count:", count)
            selectedQuestion = random_question
            selectedAnswer = answer
            selectedCount = count

            gd.buttonid = -1
            updateGump()
            
        if gd.buttonid >= 1000:
            winnerPosition = gd.buttonid - 1000
            gd.buttonid = -1;

    updateGump()    
