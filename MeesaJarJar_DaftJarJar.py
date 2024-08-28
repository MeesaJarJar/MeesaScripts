# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description: Work it. Make it. Do it. Makes us.
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#
delay = 1500
scale = 1
betweenDelay = 3000
color = 0
# END CONFIG --------------------------------------------------#

while True:
    color = color + 1
    Player.ChatSay(color, "Work it")
    Misc.Pause(int(delay * scale))
    Player.ChatSay(color, "Make it")
    color = color + 1
    Misc.Pause(int(delay * scale))
    Player.ChatSay(color, "Do it")
    color = color + 1
    Misc.Pause(int(delay * scale))
    Player.ChatSay(color, "Makes us")
    color = color + 1
    Misc.Pause(int(betweenDelay * scale))
    Player.ChatSay(color, "Harder")
    color = color + 1
    Misc.Pause(int(delay * scale))
    Player.ChatSay(color, "Better")
    color = color + 1
    Misc.Pause(int(delay * scale))
    Player.ChatSay(color, "Faster")
    color = color + 1
    Misc.Pause(int(delay * scale))
    Player.ChatSay(color, "Stronger")
    color = color + 1
    Misc.Pause(int(betweenDelay * scale))
    Player.ChatSay(color, "More than")
    color = color + 1
    Misc.Pause(int(delay * scale))
    Player.ChatSay(color, "Hour")
    color = color + 1
    Misc.Pause(int(delay * scale))
    Player.ChatSay(color, "Hour")
    color = color + 1
    Misc.Pause(int(delay * scale))
    Player.ChatSay(color, "Never")
    color = color + 1
    Misc.Pause(int(betweenDelay * scale))
    Player.ChatSay(color, "Ever")
    color = color + 1
    Misc.Pause(int(delay * scale))
    Player.ChatSay(color, "After")
    color = color + 1
    Misc.Pause(int(delay * scale))
    Player.ChatSay(color, "Work is")
    color = color + 1
    Misc.Pause(int(delay * scale))
    Player.ChatSay(color, "Over")
    color = color + 1
    Misc.Pause(int(betweenDelay * scale))
    for z in range(0, 4):
        Player.ChatSay(color, "Work it harder, make it better")
        color = color + 1
        Misc.Pause(int(delay * scale))
        Player.ChatSay(color, "Do it faster, makes us stronger")
        color = color + 1
        Misc.Pause(int(delay * scale))
        Player.ChatSay(color, "More than ever, hour after hour")
        color = color + 1
        Misc.Pause(int(delay * scale))
        Player.ChatSay(color, "Work is never over")
        color = color + 1

        scale = scale * 0.9