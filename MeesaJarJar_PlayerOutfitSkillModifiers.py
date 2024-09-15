# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description: This script prints out your current + properties
# of the items you currently have equipped for the typical UO
# skills. 
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#

# END CONFIG --------------------------------------------------#

attributes = [
    "Alchemy", "Anatomy", "Animal Lore", "Item ID", "Arms Lore", "Parry", "Begging", "Blacksmith", "Fletching", "Peacemaking", 
    "Camping", "Carpentry", "Cartography", "Cooking", "Detect Hidden", "Discordance", "EvalInt", "Healing", "Fishing", "Forensics", 
    "Herding", "Hiding", "Provocation", "Inscribe", "Lockpicking", "Magery", "Magic Resist", "Mysticism", "Tactics", "Snooping", 
    "Musicianship", "Poisoning", "Archery", "Spirit Speak", "Stealing", "Tailoring", "Animal Taming", "Taste ID", "Tinkering", 
    "Tracking", "Veterinary", "Swords", "Macing", "Fencing", "Wrestling", "Lumberjacking", "Mining", "Meditation", "Stealth", 
    "Remove Trap", "Necromancy", "Focus", "Chivalry", "Bushido", "Ninjitsu", "Spell Weaving", "Imbuing"
]

for attribute in attributes:
    value = Player.SumAttribute(attribute)
    if value > 0:
        print(f"{attribute}: {value}")
