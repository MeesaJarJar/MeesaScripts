# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description: Counts how many of each spell you have in a 
# container as scrolls. 
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#


# END CONFIG --------------------------------------------------#

from collections import defaultdict

# List of all spell names in lower case
spell_names = [
    "clumsy", "create food", "feeblemind", "heal", "magic arrow", "night sight",
    "reactive armor", "weaken", "agility", "cunning", "cure", "harm", "magic trap",
    "magic untrap", "protection", "strength", "bless", "fireball", "magic lock",
    "poison", "telekinisis", "teleport", "unlock", "wall of stone", "arch cure",
    "arch protection", "curse", "fire field", "greater heal", "lightning", "manadrain",
    "recall", "blade spirits", "dispel field", "incognito", "magic reflection", "mind blast",
    "paralyze", "poison field", "summon creature", "dispel", "energy bolt", "explosion",
    "invisibility", "mark", "mass curse", "paralyze field", "reveal", "chain lightning",
    "energy field", "flamestrike", "gate travel", "mana vampire", "mass dispel", "meteor storm",
    "polymorph", "earthquake", "energy vortex", "resurrection", "summon air elemental",
    "summon daemon", "summon earth elemental", "summon fire elemental", "summon water elemental"
]

inventory = defaultdict(int, {spell_name: 0 for spell_name in spell_names})

def parse_item_name(item_name):
    parts = item_name.split(' ')
    if parts[0].isdigit():
        quantity = int(parts[0])
        name = ' '.join(parts[1:]).replace("scroll", "").strip().lower()
    else:
        quantity = 1  # default quantity if not specified
        name = item_name.replace("scroll", "").strip().lower()
    return quantity, name
# Find the container by serial
container = Items.FindBySerial(0x41D14FA9)

for item in container.Contains:

    quantity, scroll_name = parse_item_name(item.Name)
    
    if scroll_name not in spell_names:
        print(f"Unrecognized item: {scroll_name}")  # Debugging line
        print(item)
        Misc.Pause(650)
        Items.Move(item,0x407CB012,-1)
    else:
        inventory[scroll_name] += quantity

for spell_name in spell_names:
    print(f"{inventory[spell_name]} {spell_name} scroll(s)")
