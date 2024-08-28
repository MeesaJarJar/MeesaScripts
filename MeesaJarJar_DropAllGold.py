# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description: Drop All Meesa Gold Stacks
# - Loops through all gold stacks in the players main backpack
# - Tries to drop the gold at a random 1 tile away position
# This is because several servers do not allow placing objects 
# on a tile that a mobile is on top of. 
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#

# END CONFIG --------------------------------------------------#

import random

dropLocations = [
    [Player.Position.X - 1, Player.Position.Y + 1, Player.Position.Z],
    [Player.Position.X + 1, Player.Position.Y + 1, Player.Position.Z],
    [Player.Position.X - 1, Player.Position.Y - 1, Player.Position.Z],
    [Player.Position.X + 1, Player.Position.Y - 1, Player.Position.Z]
]

goldStacks = Items.FindAllByID(0x0EED, 0x0000,Player.Backpack.Serial, 1, False);
if goldStacks:
    Player.HeadMessage(2180,"Meesa Droppin All da Gold.");
    for goldStack in goldStacks:
        keepDroppingGold = True
        while keepDroppingGold:
            dropLoc = random.choice(dropLocations)
                
            prevWeight = Player.Weight
            Items.MoveOnGround(goldStack,-1,dropLoc[0],dropLoc[1], dropLoc[2])
            Misc.Pause(650);
            if Player.Weight < prevWeight:
                keepDroppingGold = False;

                