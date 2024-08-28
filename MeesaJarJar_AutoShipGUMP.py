# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description: This is a simple GUMP for ships. It has most if 
# not all of the basic functions as original Razor CE. Script star
# ts Minimized, and has all boat commands including an 
# `Auto Target and Fire` option to make naval warfare a bit easier 
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#

# END CONFIG --------------------------------------------------#

from System.Collections.Generic import List
from System import Int32 as int
from System import Byte

gumpNumber      = 852752;
cannonsDeployed = False;
minimized       = True;
def updateGump():

    global gumpNumber, cannonsDeployed, minimized

    if minimized:
        gd = Gumps.CreateGump();
        Gumps.AddPage(gd, 0);
        gumpHeight = 40
        gumpWidth = 210

        startPointX = 280;
        startPointY = -2;
        Gumps.AddBackground(gd,startPointX-15,startPointY,gumpWidth,gumpHeight,40000)

        Gumps.AddLabel(gd,startPointX,startPointY+12,1149,"Meesa Jar Jar`s - AutoShip")

        Gumps.AddButton(gd, 455 , 8, 252,252,1000 + 50,252,0)

        Gumps.SendGump(gumpNumber, Player.Serial, 120, 120, gd.gumpDefinition, gd.gumpStrings)
    else:
        gd = Gumps.CreateGump();
        Gumps.AddPage(gd, 0);
        gumpHeight = 500
        gumpWidth = 440
        controlOffsetX = 185;
        controlOffsetY = 110;
        buttonSpacing  = 75;
        Gumps.AddBackground(gd, 0, 0, gumpWidth, gumpHeight, 9200)   
        
        Gumps.AddImageTiled(gd, 20, 25, gumpWidth-40, gumpHeight-50, 306) 
        
        Gumps.AddImageTiled(gd, 5, 25, 16, 450, 305) 
        Gumps.AddImageTiled(gd, 415, 25, 16, 450, 307) 
        Gumps.AddImageTiled(gd, 15, 20, 405, 16, 312) 
        Gumps.AddImageTiled(gd, 15, 475, 405, 16, 309) 
        
        Gumps.AddBackground(gd,30,-15,210,35,40000)
        
        Gumps.AddLabel(gd,40,-5,1149,"Meesa Jar Jar`s - AutoShip")
        
        Gumps.AddImageTiled(gd, 105, 30, 232, 232, 424) 
        Gumps.AddImageTiled(gd, 105, 258, 232, 100, 434) 
        
        Gumps.AddButton(gd,controlOffsetX,controlOffsetY - buttonSpacing,131,131,1000 + 1,131,0) ; #forward
        Gumps.AddButton(gd,controlOffsetX,controlOffsetY + buttonSpacing,137,137,1000 + 2,137,0) ; #backward
        Gumps.AddButton(gd,controlOffsetX-buttonSpacing,controlOffsetY,133,133,1000 + 3,133,0) ; #left
        Gumps.AddButton(gd,controlOffsetX+buttonSpacing,controlOffsetY,135,135,1000 + 4,135,0) ; #right    
        Gumps.AddButton(gd,controlOffsetX,controlOffsetY,134,134,1000 + 0,134,0) ; #stop
        
        Gumps.AddButton(gd,controlOffsetX - buttonSpacing,controlOffsetY - buttonSpacing,130,130,1000 + 5,130,0) ; #forward-left
        Gumps.AddButton(gd,controlOffsetX + buttonSpacing,controlOffsetY - buttonSpacing,132,132,1000 + 6,132,0) ; #forward-right
        Gumps.AddButton(gd,controlOffsetX - buttonSpacing,controlOffsetY + buttonSpacing,136,136,1000 + 7,136,0) ; #backward-left
        Gumps.AddButton(gd,controlOffsetX + buttonSpacing,controlOffsetY + buttonSpacing,138,138,1000 + 8,138,0) ; #backward-right    
        
        Gumps.AddButton(gd,controlOffsetX - buttonSpacing - buttonSpacing,controlOffsetY+5 ,4500,4500,1000 + 9,4500,0) ; #raise-anchor
        Gumps.AddLabel(gd,controlOffsetX - buttonSpacing - buttonSpacing-9,controlOffsetY  +50 ,0,"Raise Anchor")
        Gumps.AddButton(gd,controlOffsetX - buttonSpacing - buttonSpacing,controlOffsetY + buttonSpacing,4504,4504,1000 + 10,4504,0) ; #lower-anchor    
        Gumps.AddLabel(gd,controlOffsetX - buttonSpacing - buttonSpacing-9,controlOffsetY + buttonSpacing +45,0,"Lower Anchor")
        
        Gumps.AddButton(gd,controlOffsetX - buttonSpacing - buttonSpacing,controlOffsetY + (buttonSpacing*2)-15 ,4502,4502,1000 + 12,4502,0) ; #embark    
        Gumps.AddLabel(gd,controlOffsetX - buttonSpacing - buttonSpacing,controlOffsetY + (buttonSpacing*3) -45 ,0,"Embark")
        
        Gumps.AddButton(gd,controlOffsetX - buttonSpacing - buttonSpacing,controlOffsetY + (buttonSpacing*2)+45 ,4506,4506,1000 + 13,4506,0) ; #disembark   
        Gumps.AddLabel(gd,controlOffsetX - buttonSpacing - buttonSpacing-5,controlOffsetY + (buttonSpacing*3) +10,0,"Disembark")
        
        Gumps.AddButton(gd,controlOffsetX + (buttonSpacing*2)+15,controlOffsetY+5, 236,236,1000 + 11,236,0) ; #come-about 
        Gumps.AddLabel(gd,controlOffsetX + buttonSpacing + buttonSpacing+5,controlOffsetY +65,0,"Come About")
        

        Gumps.AddButton(gd, controlOffsetX - buttonSpacing , controlOffsetY + 155, 1643,1643,1000 + 14,1643,0) #fire-left

        Gumps.AddHtml(gd, controlOffsetX - 60, controlOffsetY + 205,50,50, '<basefont color=#f0f0f0 size=7><b><h2>Fire  Left</h2></b></basefont>',0,0)
        
        Gumps.AddButton(gd, controlOffsetX + buttonSpacing+10, controlOffsetY + 149, 1642,1642,1000 + 15,1642,0) #fire-right

        Gumps.AddHtml(gd, controlOffsetX +90, controlOffsetY + 205,50,50, '<basefont color=#f0f0f0 size=7><b><h2>Fire  Right</h2></b></basefont>',0,0)
        
        if cannonsDeployed == False:
            Gumps.AddButton(gd, controlOffsetX , controlOffsetY + 149, 13142,13142,1000 + 16,13142,0) #deploy-cannons
            Gumps.AddHtml(gd, controlOffsetX +13, controlOffsetY + 223,60,60, '<basefont color=#f0f0f0 size=7><b><h2>Deploy</h2></b></basefont>',0,0)
        
        if cannonsDeployed == True:
            Gumps.AddButton(gd, controlOffsetX , controlOffsetY + 149, 13136,13136,1000 + 16,13136,0) #deploy-cannons
            Gumps.AddHtml(gd, controlOffsetX +10, controlOffsetY + 223,60,60, '<basefont color=#f0f0f0 size=7><b><h2>Retract</h2></b></basefont>',0,0)
        
        
        Gumps.AddButton(gd, controlOffsetX - buttonSpacing, controlOffsetY+(buttonSpacing*3 +15)+10, 13104,13104,1000 + 18,13104,0) #take-helm
        Gumps.AddLabel(gd, controlOffsetX - buttonSpacing+15, controlOffsetY+(buttonSpacing*4)+15+10,0,"Take")
        Gumps.AddLabel(gd, controlOffsetX - buttonSpacing, controlOffsetY+(buttonSpacing*4)+15+15+10,0,"the Helm")   
        
        Gumps.AddButton(gd, controlOffsetX + buttonSpacing, controlOffsetY+(buttonSpacing*3 +15)+10, 13077,13077,1000 + 19,13077,0) #leave-helm
        Gumps.AddLabel(gd, controlOffsetX + buttonSpacing+15, controlOffsetY+(buttonSpacing*4)+15+10,0,"Leave")
        Gumps.AddLabel(gd, controlOffsetX + buttonSpacing+2, controlOffsetY+(buttonSpacing*4)+15+15+10,0,"the Helm")  
        
        Gumps.AddButton(gd, controlOffsetX , controlOffsetY+(buttonSpacing*3 +15)+10, 13131,13131,1000 + 20,13131,0) #leave-helm
        Gumps.AddLabel(gd, controlOffsetX  +25, controlOffsetY+(buttonSpacing*4)+10+15,0,"Scan")
        Gumps.AddLabel(gd, controlOffsetX -5, controlOffsetY+(buttonSpacing*4)+10+30,0,"the Horizons")
        
        Gumps.AddButton(gd, 20 , 30, 1417,1417,1000 + 40,1417,0) #turn-left
        Gumps.AddHtml(gd, 40, 48,50,50, '<basefont color=#f0f0f0 size=7><b><h2>Turn  Left</h2></b></basefont>',0,0)
        
        Gumps.AddButton(gd, 340 , 30, 1417,1417,1000 + 41,1417,0) #turn-right
        Gumps.AddHtml(gd, 360, 48,50,50, '<basefont color=#f0f0f0 size=7><b><h2>Turn  Right</h2></b></basefont>',0,0)    
        
        Gumps.AddButton(gd, controlOffsetX - buttonSpacing - 75 , controlOffsetY + 275, 1643,1643,1000 + 90,1643,0) #fire-auto-direction
        
        Gumps.AddLabel(gd,35,435,0,"Auto Target")
        Gumps.AddLabel(gd,40,450,0,"And Fire")
        
        Gumps.AddButton(gd, 215 , -9, 250,250,1000 + 50,250,0)
        
        Gumps.SendGump(gumpNumber, Player.Serial, 120, 120, gd.gumpDefinition, gd.gumpStrings)

def getMobileSide(diffX, diffY, playerDirection):

    if playerDirection == "North":
        if diffX < 0:
            return "Left"
        elif diffX > 0:
            return "Right"
        elif diffY > 0:
            return "Behind"
        else:
            return "Front"
    elif playerDirection == "East":
        if diffY < 0:
            return "Left"
        elif diffY > 0:
            return "Right"
        elif diffX > 0:
            return "Behind"
        else:
            return "Front"
    elif playerDirection == "South":
        if diffX > 0:
            return "Left"
        elif diffX < 0:
            return "Right"
        elif diffY < 0:
            return "Behind"
        else:
            return "Front"
    elif playerDirection == "West":
        if diffY > 0:
            return "Left"
        elif diffY < 0:
            return "Right"
        elif diffX < 0:
            return "Behind"
        else:
            return "Front"
    elif playerDirection == "Up":
        if diffX < 0:
            return "Left"
        elif diffX > 0:
            return "Right"
        elif diffY < 0:
            return "Front"
        else:
            return "Behind"
    elif playerDirection == "Down":
        if diffX < 0:
            return "Right"
        elif diffX > 0:
            return "Left"
        elif diffY > 0:
            return "Front"
        else:
            return "Behind"
    elif playerDirection == "Right":
        if diffY < 0:
            return "Right"
        elif diffY > 0:
            return "Left"
        elif diffX < 0:
            return "Front"
        else:
            return "Behind"
    elif playerDirection == "Left":
        if diffY < 0:
            return "Left"
        elif diffY > 0:
            return "Right"
        elif diffX > 0:
            return "Front"
        else:
            return "Behind"

      
updateGump();    
while True:
    Misc.Pause(1000)
    
    gd = Gumps.GetGumpData(gumpNumber)
   
    if (gd.buttonid == 1000):
        Player.ChatSay(690, "Stop")
    if (gd.buttonid == 1001):
        Player.ChatSay(690, "Forward")
    if (gd.buttonid == 1002):
        Player.ChatSay(690, "Back")
    if (gd.buttonid == 1003):
        Player.ChatSay(690, "Left")
    if (gd.buttonid == 1004):
        Player.ChatSay(690, "Right")
    if (gd.buttonid == 1005):
        Player.ChatSay(690, "Forward Left")
    if (gd.buttonid == 1006):
        Player.ChatSay(690, "Forward Right")
    if (gd.buttonid == 1007):
        Player.ChatSay(690, "Back Left")
    if (gd.buttonid == 1008):    
        Player.ChatSay(690, "Back Right")
    if (gd.buttonid == 1009):    
        Player.ChatSay(690, "Raise Anchor")
    if (gd.buttonid == 1010):   
        Player.ChatSay(690, "Lower Anchor")
    if (gd.buttonid == 1011):            
        Player.ChatSay(690, "Come About")
    if (gd.buttonid == 1012):            
        Player.ChatSay(690, "Embark")
    if (gd.buttonid == 1013):            
        Player.ChatSay(690, "Disembark")          
    if (gd.buttonid == 1014):            
        Player.ChatSay(690, "Fire Left") 
    if (gd.buttonid == 1015):            
        Player.ChatSay(690, "Fire Right")  
    if (gd.buttonid == 1016):            
        
        if cannonsDeployed == False:
            Player.ChatSay(690, "Deploy the Cannons") 
            cannonsDeployed = True;
            updateGump()
        else:
            Player.ChatSay(690, "Retract the Cannons") 
            cannonsDeployed = False;
            updateGump()
      
    if (gd.buttonid == 1018):            
        Player.ChatSay(690, "Take the Helm")  
    if (gd.buttonid == 1019):            
        Player.ChatSay(690, "Leave the Helm") 
    if (gd.buttonid == 1040):            
        Player.ChatSay(690, "Turn Left") 
    if (gd.buttonid == 1041):            
        Player.ChatSay(690, "Turn Right")         
    if (gd.buttonid == 1020):            
        Player.ChatSay(690, "Scan the Horizons")     
   
    if (gd.buttonid == 1050):       
   
        if minimized ==  False:
            Player.ChatSay(690, "Minimizing")    
            minimized = True;
            updateGump() 
        else:
            Player.ChatSay(690, "Maximizing")   
            minimized = False;
            updateGump()
            
    if (gd.buttonid == 0):       
   
        if minimized ==  False:
            Player.ChatSay(690, "Minimizing")    
            minimized = True;
            updateGump() 
        else:
            Player.ChatSay(690, "Maximizing")   
            minimized = False;
            updateGump()     
            
    if (gd.buttonid == 1090): 
        
        mobile = Target.GetTargetFromList("shipautotarget")
        if mobile:


                mobileSerial = mobile.Serial
                mobileName = mobile.Name

                diffX = mobile.Position.X - Player.Position.X
                diffY = mobile.Position.Y - Player.Position.Y
                
                Player.HeadMessage(0,"*Firing Cannons!*")
                side = getMobileSide(diffX, diffY, Player.Direction)
                Player.HeadMessage(0,str(mobile.Name) +  " is on the " + side + " side of the player.")
                
                if side == 'Left':
                    Player.ChatSay(0,"Fire Left")
                    Misc.Pause(100)
                    Target.TargetExecute(mobile)
                elif side == 'Right':
                    Player.ChatSay(0,"Fire Right")
                    Misc.Pause(100)
                    Target.TargetExecute(mobile)
                break
        else:
            Player.HeadMessage(0,"No Found Targets to Fire Upon!")
            
        updateGump() 
        
    if (gd.buttonid != -1):

        updateGump()
        gd.buttonid = -1;
     