# This script gates automatically for people when they request a gate via the GateCommand
# This helps save gold and resources on wasted gates that noone uses. 
# Brought to you by BabyBro of Lincoln Mallmorial Rune Library just east of Brit Gate on UOForever.

#Settings: Change these to fit your needs!
runebook = 0x42CABCA5 #Set to the runebook that you have the location you want to gate to selected as the default in the runebook.
GateCommand = "!LM" #When a player types !LM it will request a gate. Replace this with your own command!
minTimePerGateRequest = 60000 #This stops a player from requesting a gate over an over. It limits them to 1 per minute. 

line1 = "Need a gate to Lincoln Mallmorial Rune Library & Vendor Mall?"
line2 = "Kegs, High Charge Runebooks, Armor, Weapons, Recalls, Slayer / Full / Spellbooks, Rares!"
line3 = "Just say !LM and I will gate you! New On Demand gating!"
GateCommandResponse = "Gating now! Thank you for visiting us!"
LowManaResponse = "Sorry, low on Mana. Meditating and then I can gate!"

chatColor = 690 #Set the color of text for your lines. 53 is yellow, 62 is green, 37 red.
timeBetweenSpam = 20000 #Set the number in milliseconds (1000 = 1 second) of how long you want to wait before you spam your line1/2/3 again. 

#No need to change anything below here, unless you would like more lines of text added.

Journal.Clear()
totalGates = 0

def checkTimerExistsOrCreate(name,totalGates):
    
    if Timer.Check(name) == True:
        #Timer is not expired.
        Misc.SendMessage("Sorry, but " + str(name) + " has " + str(round(Timer.Remaining(name)/1000)) + " seconds remaining before they can ask for another gate.")
        Player.ChatSay(690,"Sorry, but " + str(name) + " has " + str(round(Timer.Remaining(name)/1000)) + " seconds remaining before they can ask for another gate.")
        Journal.Clear()
        
    else:
        #Timer is expired and users request for a gate is valid
        if Player.Mana < 40:
            Misc.Pause(750)
            Player.ChatSay(53, LowManaResponse) #53 is yellow, 62 is green, 37 red.
            Player.UseSkill("Meditation")
            while Player.Mana < 40:
                Misc.Pause(1000)
        Spells.CastMagery("Gate Travel")
        Player.ChatSay(13, GateCommandResponse)
        Target.WaitForTarget(60000, False)
        Target.TargetExecute(runebook)
        totalGates = totalGates + 1
        Timer.Create(name,60000,"Timer for " + str(name) + " is now expired. They may now ask for another gate.") 
    return totalGates
    
Timer.Create('spamTimer',1000)
        
while True:
    Misc.Pause(1000)
    
    #check the spam timer to see if it should say a message in chat
    if Timer.Check('spamTimer') == False:
        #SpamTimer is expired.
        Misc.SendMessage("Total Gates:" + str(totalGates)) #Display how many times weve gated so far this run.
        Player.ChatSay(chatColor,line1)#Say line 1
        Misc.Pause(2000)
        Player.ChatSay(chatColor,line2)#Say line 2
        Misc.Pause(2000)
        Player.ChatSay(chatColor,line3)#Say line 3     
        Timer.Create('spamTimer',timeBetweenSpam)

    lineAndName = Journal.GetLineText(GateCommand,True) # Searches Journal for the GateCommand
    
    if lineAndName:
        splitLine = lineAndName.split(':') # Seperates the players name from their line of text
        if splitLine[0] != Player.Name: # Makes sure the person running this script does not mistakenly trigger the Gatecommand
            totalGates = checkTimerExistsOrCreate(splitLine[0],totalGates) # Check if the player's spam timer is active. If its not, gate the player.
            
    Journal.Clear()