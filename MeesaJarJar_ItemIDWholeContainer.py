# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description: Use ItemID to identify all objects in a selected
# container. Uses the Skill, not a wand.
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#


# END CONFIG --------------------------------------------------#
tar = Target.PromptTarget("Select Container with Unidentified Items",0)
cont = Items.FindBySerial(tar)
print(tar)
print(cont)
for item in cont.Contains:
    print(item.Name)
    Items.WaitForProps(item,3000)
    if 'unidentified' in str(item.Properties).lower():
        Player.UseSkill("Item ID")
        Misc.Pause(100)
        Target.TargetExecute(item)
        Misc.Pause(1000)