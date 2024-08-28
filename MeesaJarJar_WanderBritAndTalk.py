# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! ------------#
# -------------------------------------------------------------#
# Description: Wander brit bank saying phrases, and randomly
# gating to a runebook location. 
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#
phrase = "Meesa be gating to Lincoln Mallmorial!"
locations = [
    [1419, 1669, 10],
    [1434, 1669, 10],
    [1446, 1681, 10],
    [1445, 1697, 10],
    [1419, 1697, 10],
]
runebook = 0x42CABCA5;
runebookButtonNumber = 18 # Look at the Gump Inspector in RE
# and see what number comes up on the location you want to travel to when you click it

phrases = [
    "Meesa got da best stuff in all of da realm!",
    "Meesa got da best inventory!",
    "Meesa got da rarest crystals in town!",
    "Wesa gonna make lots of gold today, meesa sure of it!",
    "Meesa got da magic touch when it comes to items!",
    "Meesa shop is da happiest place da world, eet is!",
    "Meesa shop, where da deals are out of this world!",
    "Gatherin meesa goodies to sell, mesa so excited!",
    "Meesa shop is da secret to successful adventures!",
    "Meesa shop is da talk of the server!",
    "Yousa looking for rare artifacts? Meesa got em!",
    "Meesa got da best loot this side of de world!",
    "Meesa got da best selection, hands down!",
    "Meesa got rare artifacts from all over the land!",
    "Meesa shop, where every visit is an adventure!",
    "Yousa be adventurers, meesa can see it in your eyes!",
    "Meesa shop is a treasure trove of surprises!",
    "Meesa got da best deals, just for yousa!",
    "Meesa got a special discount for yousa today!",
    "Meesa got the latest and greatest runebooks in stock!",
    "Meesa shop, where every day people be goin!",
    "Yousa adventurers bring excitement to meesa life!",
    "Yousa want to be a hero? Meesa can help!",
    "Yousa be buyin, meesa be sellin!",
    "Meesa been collecting these treasures for ages!",
    "Meesa shop, where friends become customers!",
    "Yousa adventurers are always welcome here!",
    "Yousa lookin for weapons, armor, or shiny trinkets?",
    "Meesa shop, where da prices are unbeatable!",
    "Yousa want to join da Shopping Club?",
    "Take a look at meesa collection!",
    "Yousa in luck, meesa just restocked the shelves!",
    "Yousa want to haggle? Yousa be losin!",
    "Yousa have good taste, meesa can tell!",
    "Looking for rares? Meesa got them too!",
    "Looking for something specific, meesa can help yousa find it!",
    "Meesa always looking for new items to sell!",
    "Yousa got gold coins burning a hole in your pocket?",
    "Meesa appreciate your business, thank yousa!",
    "Whoa, dis moongate is trippy! Meesa feelin dizzy."

]

# END CONFIG --------------------------------------------------#

import time
import random

def gate():
    random_number = random.random()
    phrase = random.choice(phrases)
    
    
    if Timer.Check('phraseTimer') == False:
    
        Player.ChatSay(690,phrase)
        Timer.Create('phraseTimer', 10000);
    
    if random_number < 0.10:
        if Timer.Check('gateTimer') == False:
            Misc.Pause(1000)
            Player.ChatSay(690, phrase)
            Misc.Pause(650);
            Items.UseItem(runebook)
            Misc.Pause(250);
            Gumps.SendAction(1431013363, runebookButtonNumber)
            Timer.Create('gateTimer', '30000');
    
while True:
    for location in locations:
        try:
            print("Pathfinding to :", location[0], location[1], location[2])
            PathFinding.PathFindTo(location[0], location[1], location[2])
            Misc.Pause(random.randint(1000, 4000));
            gate()
            print("Arrived at location.")
            
        except Exception as e:
            print("Error in pathfinding:", e)
