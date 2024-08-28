# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description:  Number Guessing Game - Fun! 
# A Random number between 0 and 100 is chosen (including 0 and 100)
# Whoever guesses the number first wins!
# Numbers can only be in the numerical format like `33` instead of `thirty three`
# Simple GUMP with buttons to help manage the game. Auto announces
# when a winner guesses the number first! 
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#

# END CONFIG --------------------------------------------------#

from System.Collections.Generic import List
from System import Byte 
from System.Threading import Timer
from System import String
from System import Int32 as int

import os
import random

gumpNumber = 465546546

RED = 32
GREEN = 68
WHITE = 1152
YELLOW = 2179
selectedNumber = ""
chatPause = 2000
haveWinner = False
winnerName = ''
winnerSerial = ''

def updateGump():
    global selectedNumber
    gd = Gumps.CreateGump()
    Gumps.AddPage(gd, 0)

    
    Gumps.AddBackground(gd,25,25,250,75,39925)
    Gumps.AddBackground(gd,0,65,250,85,40000)
    Gumps.AddBackground(gd,175,75,75,70,40000)
    
    Gumps.AddImage(gd,0,0,52)
    Gumps.AddLabel(gd, 193,88, WHITE,str("Number:"))
    
    
    Gumps.AddLabel(gd, 203,116, GREEN,str(selectedNumber))
    Gumps.AddLabel(gd, 45, 10, 1152, 'Meesa Jar Jar`s')
    Gumps.AddLabel(gd, 55, 38, 1152, 'Guess Meesa Number (0->100)')
    Gumps.AddLabel(gd, 65, 80, 2057, "Explain Rules")
    Gumps.AddButton(gd, 30, 80, 4005, 4006, 3, 1, 0) 
    Gumps.AddLabel(gd, 65, 113, 2057, "Pick & Start!")
    Gumps.AddButton(gd, 30, 111, 4005, 4006, 4, 1, 0)  
    
    if haveWinner:
        Gumps.AddImage(gd,150,145,40020)
        Gumps.AddLabel(gd,168,148,WHITE, winnerName)
    else:
        Gumps.AddImage(gd,150,145,40031)
        Gumps.AddLabel(gd,168,148,WHITE,"No Winner Yet")
        
    Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)

def pickAndStart():
    Player.ChatSay(40,"*▼****** 3 ******▼*")
    Misc.Pause(1000)
    Player.ChatSay(51,"**▼***** 2 *****▼**")
    Misc.Pause(1000)
    Player.ChatSay(53,"***▼**** 1 ****▼***")
    Misc.Pause(1000)
    Player.ChatSay(62,"====> GUESS! <====")
    playGame()

    
    
def explainRules():
    global selectedNumber
    colorSayNum = 1358
    Player.ChatSay(colorSayNum,"Meesa going to be choosing a number")
    Misc.Pause(chatPause)
    Player.ChatSay(colorSayNum,"Betweenin and includin` 0 and 100")
    Misc.Pause(chatPause)
    Player.ChatSay(colorSayNum,"When Meesa say GO, you be guessin!")
    Misc.Pause(chatPause)
    Player.ChatSay(colorSayNum,"Only be usin numbers 0,1,2,3,4,5,6,7,8,9")
    Misc.Pause(chatPause)
    Player.ChatSay(colorSayNum,"No other letters, no sayin `eleven`, only 11!")
    Misc.Pause(chatPause)

def playGame():
    global selectedNumber, haveWinner, winnerName, winnerSerial
    Journal.Clear() 
    haveWinner = False
    selectedNumber = random.randint(0, 100)
    while not haveWinner:
        updateGump()
        Misc.Pause(1000)
        lines = Journal.GetTextByType('Regular',True)
        
        for line in lines:
            split = line.split(': ')
            if split[1] == str(selectedNumber):
                haveWinner = True
                Player.ChatSay(GREEN,"We have a Winner!")
                Misc.Pause(1000)
                Player.ChatSay(51,str(split[0]))
                Misc.Pause(1000)
                Player.ChatSay(GREEN,"Yousa Won!")
                Misc.Pause(1000)
                winnerName = str(split[0])
                
                break
        
        Journal.Clear() 
        
updateGump()

while True:
    Misc.Pause(500)
    gd = Gumps.GetGumpData(gumpNumber)

    if gd:

        if gd.buttonid == 0:
            #print("User Tried to close GUMP")
            gd.buttonid = -1

            Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)
            updateGump()
            
        if gd.buttonid == 3:
            explainRules()
            updateGump() 
            gd.buttonid = -1
            
        if gd.buttonid == 4:
            pickAndStart()
            updateGump() 
            gd.buttonid = -1

            
