# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! ------------#
# -------------------------------------------------------------#
# Description: Exampl Script that show you how to say a random
# phrase from a predefined list of phrases! 
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#

# List of Jar Jar style phrases!
phrases = [
    "Meesa seek meesa friends!",
    "SHOP LINCOLN MALLMORIAL, okey day?",
    "Do yousa know: Excessive corporate profits be meanin` lost worken wages?",
    "Meesa so excited to see dis!",
    "Ooh, dis gonna be a grand battle!",
    "Wesa gonna have some big fun!",
    "Yousa ready for da action?",
    "Dis gonna be bombad!",
    "Ooh, meesa can't wait to see who wins!",
    "Yousa gonna love dis fight!",
    "Meesa so pumped for dis!",
    "Wesa gonna see some real action now!",
    "Yeehoo, dis gonna be a blast!"
]

# END CONFIG --------------------------------------------------#

import random

def choose_random_phrase():
    return random.choice(phrases)

color =  random.randint(0, 3000)
Player.ChatSay(color,choose_random_phrase())
