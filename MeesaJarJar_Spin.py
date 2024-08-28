# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description: Weesa do a big fast spin, okey day?
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#


# END CONFIG --------------------------------------------------#
while True:
    if   Player.Direction == "North": Player.Run("East")
    elif Player.Direction == "East":  Player.Run("South")
    elif Player.Direction == "South":  Player.Run("West")
    elif Player.Direction == "West": Player.Run("North")
    elif Player.Direction == "North": Player.Run("Up")
    elif Player.Direction == "Up":  Player.Run("Right")
    elif Player.Direction == "Right":  Player.Run("Down")
    elif Player.Direction == "Down": Player.Run("Left")
    elif Player.Direction == "Left": Player.Run("North")
    Misc.Pause(10)
    
