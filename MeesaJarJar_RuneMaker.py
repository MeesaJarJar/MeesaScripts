# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description: Put empty, unmarked runes in your backpack main 
# container. Select the bag when prompted. It will keep making
# runes until none are left to mark.
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#
runeName = 'LM Rune Lib/Mall'

# END CONFIG --------------------------------------------------#

target = Target.PromptTarget("Select Bag to Put Marked Runes:",0)
while True and target:
    
    if Player.Mana < 20:
        
        while Player.Mana < Player.ManaMax:
            Player.UseSkill('Meditation')
            Misc.Pause(1000);
        Misc.Pause(1000);    
        
    emptyRune = Items.FindByID(0x1F14,0x0000,Player.Backpack.Serial,False,False)
    if emptyRune:
		Misc.Pause(650);
		Target.ClearLast()
		Spells.Cast('Mark')
		Misc.Pause(2500);

		Target.TargetExecute(emptyRune.Serial)

		Misc.Pause(650);
		Items.UseItem(emptyRune)
		Misc.Pause(200);
		Misc.ResponsePrompt(runeName) 
		Misc.Pause(650);
		Items.Move(emptyRune,target,1)

		Misc.Pause(650);
    else:
		break
