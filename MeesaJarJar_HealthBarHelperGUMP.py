# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! ------------#
# -------------------------------------------------------------#
# Description: Displays GUMP with the Health Bars, and Poison / 
# Death / Hurt / Out of Range of players around the user. 
# Heal, Cure, Rez players. Displays guildmates as well as others.
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#


# END CONFIG --------------------------------------------------#

from System.Collections.Generic import List
from System import Byte
import os

gumpNumber = 163167436
if Gumps.HasGump(gumpNumber):
    Gumps.CloseGump(gumpNumber)

GID = 0

GHOST = 1152
POISONED = 69
FULLHEALTH = 4
NOTFULLHEALTH = 34
mobSerialList = []
triToggle = 1
maxMobiles = 20

def addHealthBar(gd, index, mobile, offsetX, widthOffset, healthBarOffsetY, healthUnitHeight, color):
    for z in range(mobile.Hits * 3):
        Gumps.AddImage(gd, 10 + offsetX + (index * widthOffset), -15 + healthBarOffsetY + z * healthUnitHeight, 30074, color)

def addButton(gd, index, offsetX, widthOffset, buttonOffsetY, buttonBaseID, inRange):
    buttonID = 1000 + index  # Start button IDs from 1000 to avoid any default or negative values
    Gumps.AddButton(gd, offsetX + (index * widthOffset), buttonOffsetY + 75, buttonBaseID, buttonBaseID, buttonID, 1, 0)
    if not inRange:
        Gumps.AddImage(gd, offsetX + (index * widthOffset), 5 + buttonOffsetY + 75, 28)

def addTriToggleImage(gd, index, offsetX, widthOffset, buttonOffsetY, triToggle):
    images = [10720, 10721, 10722]
    Gumps.AddImage(gd, offsetX + (index * widthOffset) + 17, -45 + buttonOffsetY + 85, images[triToggle - 1])

def addNameLabel(gd, index, mobile, offsetX, widthOffset, labelOffsetY):
    charH = 0
    for char in str(mobile.Name)[:7]:
        Gumps.AddLabel(gd, offsetX + 16 + (index * widthOffset), labelOffsetY + charH, 1152, char)
        charH += 12

def updateGump():
    global GID, mobSerialList, triToggle, widthOffset

    offsetX = 50
    widthOffset = 40

    gd = Gumps.CreateGump(True, True, False, False)
    Gumps.AddPage(gd, 0)

    Gumps.AddImage(gd, 20, 110, 31)

    #if len(filteredMobiles) >= 1:
        #Gumps.AddBackground(gd, len(filteredMobiles) * widthOffset + 50, 110, 34, 30, 31)

    healthUnitHeight = 1
    buttonOffsetY = 50
    labelOffsetY = 165
    healthBarOffsetY = 160

    for index, mobile in enumerate(filteredMobiles):
        if mobile is None:
            continue

        Journal.Clear()

        inRange = Player.DistanceTo(mobile) <= 11

        Gumps.AddBackground(gd, offsetX + (index * widthOffset) + 5, buttonOffsetY + 85, 36, 120, 420)

        if mobile.Poisoned:
            addHealthBar(gd, index, mobile, offsetX, widthOffset, healthBarOffsetY, healthUnitHeight, POISONED)
            addButton(gd, index, offsetX, widthOffset, buttonOffsetY, 2250, inRange)  # Cure icon
            addTriToggleImage(gd, index, offsetX, widthOffset, buttonOffsetY, triToggle)
            triToggle = triToggle % 3 + 1
        elif mobile.Hits < mobile.HitsMax - 2:
            addHealthBar(gd, index, mobile, offsetX, widthOffset, healthBarOffsetY, healthUnitHeight, NOTFULLHEALTH)
            addButton(gd, index, offsetX, widthOffset, buttonOffsetY, 2268, inRange)  # Heal icon
            addTriToggleImage(gd, index, offsetX, widthOffset, buttonOffsetY, triToggle)
            triToggle = triToggle % 3 + 1
        elif mobile.Hits == mobile.HitsMax:
            addHealthBar(gd, index, mobile, offsetX, widthOffset, healthBarOffsetY, healthUnitHeight, FULLHEALTH)
            addButton(gd, index, offsetX, widthOffset, buttonOffsetY, 2283, inRange)  # Invisibility icon
        elif mobile.IsGhost == True:
            addHealthBar(gd, index, mobile, offsetX, widthOffset, healthBarOffsetY, healthUnitHeight, FULLHEALTH)
            addButton(gd, index, offsetX, widthOffset, buttonOffsetY, 2298, inRange)  # rez icon

        if mobile.Notoriety == 2:
            Gumps.AddImage(gd, offsetX + (index * widthOffset) - 7, -10 + 5 + buttonOffsetY + 75, 494, 277)

        if Journal.Search("cannot see") or Journal.Search("too far away"):
            print(f"FAILED TO TARGET {mobile.Name}")
            Target.Cancel()

        addNameLabel(gd, index, mobile, offsetX, widthOffset, labelOffsetY)
    Gumps.CloseGump(gumpNumber)
    Gumps.SendGump(gumpNumber, Player.Serial, 400, 300, gd.gumpDefinition, gd.gumpStrings)

def getFilteredMobiles():
    global filteredMobiles, mobSerialList

    mobileFilter = Mobiles.Filter()
    mobileFilter.Enabled = True
    mobileFilter.RangeMin = -1
    mobileFilter.RangeMax = 12
    mobileFilter.CheckLineOfSight = True
    mobileFilter.Notorieties = List[Byte](bytes([1, 2]))

    foundMobiles = Mobiles.ApplyFilter(mobileFilter)

    newFilteredMobiles = [None] * maxMobiles
    mobSerialList = [None] * maxMobiles  # Reset mobSerialList to match maxMobiles

    for mobile in foundMobiles:
        if mobile.Body in [400, 401, 402, 403]:  # mobile.CanRename or 
            for i in range(maxMobiles):
                if newFilteredMobiles[i] is None:
                    newFilteredMobiles[i] = mobile
                    mobSerialList[i] = mobile.Serial  # Populate mobSerialList with the corresponding serial
                    break
                elif newFilteredMobiles[i] and newFilteredMobiles[i].Serial == mobile.Serial:
                    newFilteredMobiles[i] = mobile
                    mobSerialList[i] = mobile.Serial  # Update mobSerialList with the corresponding serial
                    break

    filteredMobiles = newFilteredMobiles

def handleButtonPresses(gd):
    buttonID = gd.buttonid
    #print(f"Button pressed: {buttonID}")  # Debug: Print the button ID

    if buttonID == -1:
        return

    idx = buttonID - 1000  # Adjust the buttonID to get the correct index
    print(f"Target index: {idx}")  # Debug: Print the target index

    if idx < 0 or idx >= len(mobSerialList):
        print(f"Invalid index for mobSerialList: {idx}")
        return

    # Use the actual button ID to determine which spell to cast
    if buttonID in range(1000, 1020):  # Assuming a max of 20 mobiles
        # Check the exact spell to cast based on the original buttonBaseID
        buttonBaseID = getButtonBaseID(gd, idx)  # Custom function to get the actual buttonBaseID
        print(f"Base ID: {buttonBaseID}")  # Debug: Print the base ID

        if buttonBaseID == 2283:  # Invisibility icon ID
            castSpellMagery("Invisibility", idx)
        elif buttonBaseID == 2298:  # REZ icon ID
            castSpell("Resurrection", idx)
        elif buttonBaseID == 2268:  # Heal icon ID
            castSpell("Greater Heal", idx)
        elif buttonBaseID == 2250:  # Cure icon ID
            castSpell("Cure", idx)
    elif buttonID >= 4000 and buttonID < 5000:
        castSpell("Resurrection", idx)

def getButtonBaseID(gd, idx):

    if idx < 0 or idx >= len(filteredMobiles) or mobSerialList[idx] is None:
        print(f"Invalid index for getButtonBaseID: {idx}")
        return None

    mobile = filteredMobiles[idx]
    if mobile is None:
        return None

    if mobile.Poisoned:
        return 2250  # Cure icon ID
    elif mobile.Hits < mobile.HitsMax - 2:
        return 2268  # Heal icon ID
    elif mobile.Hits == mobile.HitsMax:
        return 2283  # Invisibility icon ID
    
    return None  # Return None if no condition matches (shouldn't happen in normal cases)


def castSpell(spell, idx):
    try:
        if idx < 0 or idx >= len(mobSerialList) or mobSerialList[idx] is None:
            print(f"Invalid index for mobSerialList: {idx}")
            return

        mob = Mobiles.FindBySerial(mobSerialList[idx])
        if mob:
            print(f"Casting {spell} on {mob.Name}")
            Player.HeadMessage(0, f"Casting {spell} on: {mob.Name}")
            Player.ChatSay(1150,f"Casting {spell} on: {mob.Name}")
        Spells.Cast(spell, mobSerialList[idx], 1000)
        Misc.Pause(750)
        Target.TargetExecute(mobSerialList[idx])
        Gumps.CloseGump(gumpNumber)
        Gumps.SendGump(gumpNumber, Player.Serial, 400, 300, gd.gumpDefinition, gd.gumpStrings)
    except Exception as e:
        print(f"FAILED to cast {spell} on index {idx}: {e}")
    updateGump()

def castSpellMagery(spell, idx):
    try:
        if idx < 0 or idx >= len(mobSerialList) or mobSerialList[idx] is None:
            print(f"Invalid index for mobSerialList: {idx}")
            return

        mob = Mobiles.FindBySerial(mobSerialList[idx])
        if mob:
            print(f"Casting Magery spell {spell} on {mob.Name}")
            Player.HeadMessage(0, f"Casting {spell} on: {mob.Name}")
        Spells.CastMagery(spell)
        Misc.Pause(2000)
        Target.TargetExecute(mobSerialList[idx])
        Gumps.CloseGump(gumpNumber)
        Gumps.SendGump(gumpNumber, Player.Serial, 400, 300, gd.gumpDefinition, gd.gumpStrings)
    except Exception as e:
        print(f"FAILED to cast Magery spell {spell} on index {idx}: {e}")
    updateGump()

filteredMobiles = [None] * maxMobiles
updateGump()
mobSerialList = []
prevListMobiles = []
idx = 0

while True:
    Misc.Pause(250)
    idx += 1
    gd = Gumps.GetGumpData(gumpNumber)
    oldMobiles = filteredMobiles
    getFilteredMobiles()

    serialListA = [oldMobile.Serial if oldMobile else None for oldMobile in oldMobiles]
    serialListB = [filteredMobile.Serial if filteredMobile else None for filteredMobile in filteredMobiles]

    if serialListA != serialListB or idx % 3 == 0:
        updateGump()

    if gd:
        handleButtonPresses(gd)
