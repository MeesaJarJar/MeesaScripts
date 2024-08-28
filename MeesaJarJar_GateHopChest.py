# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description: Meesa Jar Jar`s Gate Hopping Chest Script
# Set a drop container to a SECURE chest that is accessible 
# outside of your house. The rune location you mark for drop off 
# must have a clear access TO THE RIGHT of it because it has to 
# set the chest down first before putting it into the 
# drop container
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#
dropContainer = 0x411B9010
# END CONFIG --------------------------------------------------#

from System.Collections.Generic import List
from System import String
from System import Int32 as int
chestx = Items.Filter()
chestx.Enabled = True
chestx.OnGround = True
chestx.Movable = True
chestx.RangeMax = 1
chestx.IsContainer = True
chesty = Items.ApplyFilter(chestx)
chest = None
if chesty:
    chest = Items.Select( chesty , 'Nearest' )


gate = Items.FindByID(0x0F6C,0x0000,-1,3,False) 
if gate:
    Player.HeadMessage(0,"Found Gate.")
    Player.HeadMessage(0,"Using Gate.")
    Items.UseItem(gate) 

    if chest!= None:
        Player.HeadMessage(35,"Lifting Item")
        Gumps.SendAction(3716879466, 1) 
        Misc.Pause(350)
        chestSerial = chest.Serial
        Items.Lift(chest,-1)
        Misc.Pause(1000)

        Items.MoveOnGround(Items.FindBySerial(Player.Backpack.Serial),-1,Player.Position.X+1,Player.Position.Y,Player.Position.Z)
        Misc.Pause(650)
        Items.Move(chestSerial,dropContainer,1)
        Player.HeadMessage(0,"Gate Hop DONE, returning into gate.")
        gate = Items.FindByID(0x0F6C,0x0000,-1,3,False) 
        if gate:
            Player.HeadMessage(0,"Found Gate.")
            Player.HeadMessage(0,"Using Gate.")
            Misc.Pause(350)
            Items.UseItem(gate) 
        Player.HeadMessage(0,"Gate Hop Finished!") 
else:
    Player.HeadMessage(0,"No Gate Found!")
    print("GATE NOT FOUND")
                    