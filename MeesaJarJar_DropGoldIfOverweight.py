# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description: If player is over weight, drops gold enough to
# bring players weight back into acceptable range.
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#


# END CONFIG --------------------------------------------------#
while True:
    Misc.Pause(500);
    dropLocations = [[Player.Position.X-1,Player.Position.Y+1,Player.Position.Z],[Player.Position.X+1,Player.Position.Y+1,Player.Position.Z],[Player.Position.X-1,Player.Position.Y-1,Player.Position.Z],[Player.Position.X+1,Player.Position.Y-1,Player.Position.Z]]

    if Player.Weight > Player.MaxWeight:
        goldToDrop = (Player.Weight - Player.MaxWeight + 3)*50
        Misc.SendMessage("Player is overweight. Dropping some gold.");
        Player.HeadMessage(33,"Player is Overweight. Dropping " + str(goldToDrop) + " Gold. ");

        Misc.SendMessage("Dropping " + str(goldToDrop) + " gold.");
        goldStacks = Items.FindAllByID(0x0EED, 0x0000,Player.Backpack.Serial, 1, False);
        keepDroppingGold = True;
        for goldStack in goldStacks:
            
                goldDroppedSuccessfully = False;
                for dropLoc in dropLocations:
                    
                    if goldDroppedSuccessfully:
                        break;
                    if goldToDrop and keepDroppingGold:
                    
                        prevWeight = Player.Weight;
                       
                        Items.MoveOnGround(goldStack,goldToDrop,dropLoc[0],dropLoc[1], dropLoc[2])
                        Misc.Pause(600);
                        aftWeight = Player.Weight;

                        if prevWeight == aftWeight:
                            goldDroppedSuccessfully = False;
                    
                            Misc.SendMessage("Failed to drop gold. Location blocked. Trying different location.");
                            
                        else:
                            goldDroppedSuccessfully = True;
                            goldToDrop = (Player.Weight - Player.MaxWeight + 3)*50
                            
                            break;
                    else:
                        keepDroppingGold = False;