# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! ------------#
# -------------------------------------------------------------#
# Description: Meesa Spellbook - Slayer Spellbook Selector Gump!
# Scans the users backpack for Slayer Spellbooks, displays a 
# simply clickable gump that shows the lesser and super slayer
# types along with what mobiles they are effective against. 
# Special Thanks to Silent Nox for teaching me something I used here. 
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#

minimized = True # Set True to start minimized.
# END CONFIG --------------------------------------------------#

gumpNumber = 315136

slayer_dict = {
    "Vacuum": "Air Elemental, Summoned Air Elemental",
    "Repond": "Arctic Ogre Lord, Ogre, Ogre Lord, Brigands, Non-Player Humans, Cyclops, Titan, Ettin, Evil Mage, Evil Mage Lord, Frost Troll, Troll, Meer Captain, Meer Eternal, Meer Mage, Meer Warrior, Orc, Orc Bomber, Orc Brute, Orc Captain, Orcish Lord, Orcish Mage, Orcish Mine Overseer, Orc Leader, Orc Mine Bomber, Orc Miner, Ratman, Ratman Archer, Ratman Mage, Savage Rider, Savage Shaman, Savage, Troglodyte, Lummox Mage (Portal), Lummox War Hero (Portal), Lummox Warrior (Portal), Minotaur War Hero (Portal), Minotaur Warrior (Portal)",
    "Ogre Thrashing": "Arctic Ogre Lord, Ogre, Ogre Lord",
    "Orc Slaying": "Orc, Orc Bomber, Orc Brute, Orc Captain, Orcish Lord, Orcish Mage, Orcish Mine Overseer, Orc Leader, Orc Mine Bomber, Orc Miner",
    "Troll Slaughter": "Frost Troll, Troll",
    "Silver": "Ancient Lich, Lich, Lich Lord, Bogle, Bone Knight, Bone Mage, Skeleton, Skeletal Knight, Skeletal Mage, Darknight Creeper, Flesh Golem, Ghoul, Rotting Corpse, Zombie, Gore Fiend, Hell Steed, Skeletal Mount, Lady Of The Snow, Mummy, Pestilent Bandage, Revenant, Revenant Lion, Shadow Knight, Shade, Spectre, Wraith, Werewolf, Dream Wraith (Portal), Maddening Horror (Portal), Undead War Dog (Portal)",
    "Fey Slayer": "Centaur, CuSidhe, Ethereal Warrior, Kirin, Lord Oaks, Pixie, Phoenix Matriarch, Silvani, Treefellow, Unicorn, Wisp, ML Dryad, Satyr",
    "Elemental Ban": "Acid Elemental, Toxic Elemental, Poison Elemental, Greater Poison Elemental, Agapite Elemental, Bronze Elemental, Copper Elemental, Dull Copper Elemental, Golden Elemental, Iron Elemental, Shadow Iron Elemental, Valorite Elemental, Verite Elemental, Magnetite Elemental, Air Elemental, Summoned Air Elemental, Blood Elemental, Greater Blood Elemental, Blood Vortex, Crystal Elemental, Crystal Vortex, Earth Elemental, Summoned Earth Elemental, Deep Earth Elemental, Efreet, Fire Elemental, Summoned Fire Elemental, Magma Elemental, Pyroclastic Elemental, Ice Elemental, Snow Elemental, Kaze Kemono, RaiJu, Sand Vortex, Water Elemental, Summoned Water Elemental, Deep Water Elemental",
    "Blood Drinking": "Blood Elemental, Greater Blood Elemental, Blood Vortex",
    "Earth Shatter": "Agapite Elemental, Bronze Elemental, Copper Elemental, Dull Copper Elemental, Golden Elemental, Iron Elemental, Shadow Iron Elemental, Valorite Elemental, Verite Elemental, Magnetite Elemental, Crystal Vortex, Earth Elemental, Summoned Earth Elemental, Deep Earth Elemental, Greater Blood Elemental",
    "Elemental Health": "Poison Elemental, Greater Poison Elemental",
    "Flame Dousing": "Fire Elemental, Summoned Fire Elemental, Magma Elemental, Pyroclastic Elemental",
    "Summer Wind": "Snow Elemental, Ice Elemental",
    "Water Dissipation": "Water Elemental, Summoned Water Elemental, Deep Water Elemental",
    "Exorcism": "Abysmal Horror, Balron, Bone Daemon, Chaos Daemon, Arcane Daemon, Daemon, Summoned Daemon, Ice Fiend, Demon Knight, Shadow Knights, Devourer, Gargoyle, Stone Gargoyle, Burning Gargoyle, Fire Gargoyle, Flaming Gargoyle, Enslaved Gargoyle, Gargoyle Destroyer, Gargoyle Enforcer, Scorching Gargoyle, Smoldering Gargoyle, Gibberling, Horde Minion, Imp, Nether Imp, Burning Imp, Impaler, Ravager, Succubus, Devourer (Portal), Abysmal Horror (Portal), Dark Father (Portal), Moloch",
    "Balron Damnation": "Balron",
    "Daemon Dismissal": "Abysmal Horror, Balron, Bone Daemon, Chaos Daemon, Arcane Daemon, Daemon, Summoned Daemon, Ice Fiend, Demon Knight, Devourer, Gibberling, Horde Minion, Imp, Impaler, Ravager, Moloch",
    "Gargoyles Foe": "Fire Gargoyle, Gargoyle, Stone Gargoyle, Enslaved Gargoyle, Gargoyle Destroyer, Gargoyle Enforcer",
    "Arachnid Doom": "Abnormal Dread Spider, Dread Spider, Frost Spider, Giant Black Widow, Giant Spider, Mephitis, Scorpion, Terathan Avenger, Terathan Drone, Terathan Matriarch, Terathan Warrior",
    "Scorpions Bane": "Scorpion",
    "Spiders Death": "Dread Spider, Frost Spider, Giant Black Widow, Giant Spider, Mephitis, Abnormal Dread Spider",
    "Terathan": "Terathan Avenger, Terathan Drone, Terathan Matriarch, Terathan Warrior",
    "Reptilian Death": "Ancient Wyrm, Shadow Wyrm, White Wyrm, Deep Sea Serpent, Sea Serpent, Greater Dragon, Elder Dragon, Dragon, Dragon (Portal), Ancient Wyrm (Portal), Shadow Wyrm (Portal), Bahamut, Drake, Pathaleo Drake, Giant Ice Worm, Ice Serpent, Giant Serpent, Lava Serpent, Silver Serpent, Hiryu, Lesser Hiryu, Ice Snake, Lava Snake, Snake, Juka Lord, Juka Mage, Juka Warrior, Lizardman, Ophidian Archmage, Ophidian Knight, Ophidian Mage, Ophidian Matriarch, Ophidian Warrior, Reptalon, Serado, Serpentine Dragon, Skeletal Dragon, Swamp Dragon, Wyvern, Yamandon",
    "Dragon Slaying": "Ancient Wyrm, Shadow Wyrm, White Wyrm, Dragon (Portal), Ancient Wyrm (Portal), Shadow Wyrm (Portal), Bahamut, Greater Dragon, Elder Dragon, Dragon, Drake, Pathaleo Drake, Hiryu, Lesser Hiryu, Reptalon, Serpentine Dragon, Skeletal Dragon, Swamp Dragon, Wyvern",
    "Lizardman Slaughter": "Lizardman",
    "Ophidian": "Ophidian Archmage, Ophidian Knight, Ophidian Mage, Ophidian Matriarch, Ophidian Warrior",
    "Snakes Bane": "Deep Sea Serpent, Sea Serpent, Giant Ice Worm, Giant Serpent, Ice Serpent, Lava Serpent, Silver Serpent, Ice Snake, Lava Snake, Snake, Serado, Yamandon",
    "Abyss": "Balron, Blood Elementals, Pyroclastic Elementals, Unicorns, Wisps"  
}
super_slayer_types = [
    "Repond",
    "Silver",
    "Fey Slayer",
    "Elemental Ban",
    "Exorcism",
    "Arachnid Doom",
    "Reptilian Death"
]

def is_super_slayer(slayer_type):
    return slayer_type in super_slayer_types
    
def get_slayer_tooltip(slayer_type):
    return slayer_dict.get(slayer_type, "No data available for this slayer type.")
    
def getSlayerSpellbooks():
    slayerSpellbooks = []
    filterWords = ['spellbook', 'crafted', 'blessed', 'exceptional', 'spells', 'charges']

    for item in Player.Backpack.Contains:
        if item.Name.lower() == 'spellbook':
            charges = Items.GetPropValue(item, 'Charges')
            allProps = Items.GetProperties(item.Serial, 1000)
            slayer = None

            for prop in allProps:
                propLower = str(prop).strip().lower()

                if not any(word in propLower for word in filterWords):
                    slayer = str(prop)

            if slayer != None:
                slayerSpellbooks.append([int(charges) if charges else 0, slayer, item.Serial])

    return slayerSpellbooks

def getSlayerSpellbookSingle(item):
    filterWords = ['spellbook', 'crafted', 'blessed', 'exceptional', 'spells', 'charges']

    if item.Name.lower() == 'spellbook':
        charges = Items.GetPropValue(item, 'Charges')
        allProps = Items.GetProperties(item.Serial, 1000)
        slayer = None

        for prop in allProps:
            propLower = str(prop).strip().lower()

            if not any(word in propLower for word in filterWords):
                slayer = str(prop)

        if slayer != None:
            return [int(charges) if charges else 0, slayer, item.Serial]
    return False

def updateGump(): 
    gd = Gumps.CreateGump(True, True, False, False)
    offsetx = 50
    offsety = 5
    
    Gumps.AddBackground(gd,offsetx-3, -3+offsety, 200, 20, 420) 
    
    Gumps.AddAlphaRegion(gd,offsetx+0,-3+offsety,1,1)
    Gumps.AddImage(gd,offsetx-3+190, -8+offsety,2088)
    Gumps.AddTooltip(gd,3012171,str("Click & Drag Here to Move"))
    Gumps.AddImage(gd,offsetx-3+190, -8+offsety,1609) 
    #Gumps.AddImage(gd,offsetx-3+200, -3+offsety,1606)
    equippedItem = Player.GetItemOnLayer('RightHand')

    if equippedItem and equippedItem.Name.lower() == 'spellbook':
        equippedSlayerDetails = getSlayerSpellbookSingle(equippedItem)
        if equippedSlayerDetails:
            if equippedSlayerDetails[1] == 'fey slayer':
                equippedSlayerDetails[1] = 'Fey Slayer'
                  
            Gumps.AddLabel(gd,offsetx+ 25, 0+offsety-2, 1152, f"{equippedSlayerDetails[1]}")
            Gumps.AddTooltip(gd,3012171,str(get_slayer_tooltip(equippedSlayerDetails[1])))
            Gumps.AddLabel(gd,offsetx+ 150, 0+offsety-2, 1152, f"{equippedSlayerDetails[0]}")
            Gumps.AddTooltip(gd,3012171,str(get_slayer_tooltip(equippedSlayerDetails[1])))
            Gumps.AddButton(gd,offsetx+ 0,0+offsety-2,40015,40014,2,True,0)
            Gumps.AddTooltip(gd,3012171,str(get_slayer_tooltip(equippedSlayerDetails[1])))
            Gumps.AddLabel(gd,offsetx+ 25, 0+offsety+12,5,"Currently Equipped")
            Gumps.AddAlphaRegion(gd,offsetx+ 25, 0+offsety+30,1,1)
            if minimized == False:
                Gumps.AddImage(gd,50,-20,2085)
    else:
        Gumps.AddLabel(gd,offsetx+ 25, 0+offsety-2, 1152, "No spellbook equipped")
        Gumps.AddImage(gd,50,8,2085)
        
    if minimized == False:
        
        Gumps.AddButton(gd,0,0,11047,11049,3,True,0) 
        Gumps.AddTooltip(gd,3012171,str("Meesa Jar Jar`s Slayer Spellbook - github.com/MeesaJarJar/"))
        index = 1 
        for slayer in getSlayerSpellbooks():
            if slayer[1] == 'fey slayer':
                slayer[1] = 'Fey Slayer'
                
            if is_super_slayer(slayer[1]):
                Gumps.AddImage(gd,offsetx-22, 4+index * 25+offsety,1802)
                Gumps.AddImage(gd,offsetx+8-22,4+ index * 25+offsety,1804)
                Gumps.AddLabel(gd,offsetx+8-27,3+ index * 25+offsety,1152,"S")
                Gumps.AddTooltip(gd,3012171,str("This Spellbook is a Super Slayer"))
                
            Gumps.AddLabel(gd,offsetx+ 25, index * 25+offsety, 1152, str(slayer[1]))  
            Gumps.AddTooltip(gd,3012171,str(get_slayer_tooltip(slayer[1])))
            Gumps.AddLabel(gd,offsetx+ 150, index * 25+offsety, 1152, f"{slayer[0]}") 
            Gumps.AddTooltip(gd,3012171,str(get_slayer_tooltip(slayer[1]))) 
            Gumps.AddButton(gd,offsetx+ 0,index * 25+offsety,40014,40017,slayer[2],True,0)
            Gumps.AddTooltip(gd,3012171,str(get_slayer_tooltip(slayer[1])))
            index += 1
    else:
        Gumps.AddButton(gd,0,0,11047,11049,3,True,0)
        Gumps.AddTooltip(gd,3012171,str("Meesa Jar Jar`s Slayer Spellbook - github.com/MeesaJarJar/"))
        Gumps.AddImage(gd,50,30,2084)
        
    Gumps.AddHtml(gd,-20,0,100,150,'<BASEFONT color=#fffccc size=7><b>M</b></BASEFONT>',False,False)  #  
    Gumps.AddHtml(gd,-10,10,100,150,'<BASEFONT color=#fffccc size=4><b>e</b></BASEFONT>',False,False)  #  
    Gumps.AddHtml(gd,-10,20,100,150,'<BASEFONT color=#fffccc size=4><b>e</b></BASEFONT>',False,False)  #  
    Gumps.AddHtml(gd,-10,30,100,150,'<BASEFONT color=#fffccc size=4><b>s</b></BASEFONT>',False,False)  #  
    Gumps.AddHtml(gd,-10,40,100,150,'<BASEFONT color=#fffccc size=4><b>a</b></BASEFONT>',False,False)  #  
    Gumps.AddHtml(gd,-22,52,100,150,'<BASEFONT color=#fffccc size=5>Spellbook</BASEFONT>',False,False)# 
    Gumps.CloseGump(gumpNumber)
    Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)

updateGump()

while True: 

    gd = Gumps.GetGumpData(gumpNumber)

    if gd and gd.buttonid != -1:
        if gd.buttonid == 2:
                #Misc.Pause(350)
                if Player.GetItemOnLayer("RightHand"):
                    try:
                        Player.UnEquipItemByLayer("RightHand",350)   
                        Misc.Pause(50)   
                    except:
                        Misc.NoOperation()
        if gd.buttonid == 3:
                if minimized == True:
                    minimized = False
                else:
                    minimized = True
                    
        else :
            try:
                Player.UnEquipItemByLayer("RightHand",350)
                Misc.Pause(50)
            except:
                Misc.NoOperation()
                
            it = Items.FindBySerial(gd.buttonid)
            if it:
                Misc.Pause(350)
                Player.EquipItem(it)
                Misc.Pause(250)
                minimized = True

        gd.buttonid = -1    
        Gumps.CloseGump(gumpNumber)
        Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)
        updateGump()            
    else:
        Misc.Pause(100)

    