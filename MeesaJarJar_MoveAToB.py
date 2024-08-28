# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description: Move Items from one container to another. 
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#


# END CONFIG --------------------------------------------------#
tarA = Target.PromptTarget("Select A",0)
tarB = Target.PromptTarget("Select B",0)
conA = Items.FindBySerial(tarA)
conB = Items.FindBySerial(tarB)
Items.UseItem(conA)
Misc.Pause(650)

Items.UseItem(conB)
Misc.Pause(650)

for item in conA.Contains:
    print(item)
    Items.Move(item,tarB,-1)
    Misc.Pause(250)