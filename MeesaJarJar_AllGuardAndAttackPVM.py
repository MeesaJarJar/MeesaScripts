# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description: This script says "all guard me" until it detects that the pet is guarding you. 
# It then attacks a target from your 'enemies' Target List in Razor Enhaned.
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#
enemiesTargetListName = "enemies" # Set this to the name of the Target tab list you create yourself for enemies in RE.
# END CONFIG --------------------------------------------------#

Journal.Clear()
guarding = False
while guarding == False:
    if Journal.Search("is now guarding you"):
        guarding = True
    else:
        Player.ChatSay(690, "all guard me")
        Misc.Pause(250)
        
    
Misc.Pause(200)
Target.AttackTargetFromList(enemiesTargetListName)