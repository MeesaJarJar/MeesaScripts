# Made by MeesaJarJar- http://github.com/MeesaJarJar/  --------#
# Original By Matsamilla- http://github.com/Matsamilla/
# BabyBro / MeesaJarJar on Discord - Peace & Love! ------------#
# -------------------------------------------------------------#
# Description: 
# Meesa Dragon Armor Crafting Gump 
# ToolTips must be enabled and must have a beetle
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#

gumpNumber = 13581630
dragDelay = 650
scaleColor = 'red' #pick color of scales, red, yellow, black, green, white, blue or blue2

fillBags = True # if true: Fill a bag with as many 
                # bags as you want to fill with armor sets.
                # Make sure bag is on beetle, lot of weight.

smithHammer = 0x13E3
smithHammerHue = 0x0000
#smithHammerHue = 0x0482 # ANCIENT + 15

dragonLegs = 0x2647
dragonTunic = 0x2641
dragonSleeves = 0x2657
dragonGloves = 0x2643
dragonHelm = 0x2645
dragonGorget = 0x2B69

dragonSuit = [(205,dragonGloves),(212,dragonGorget),(219,dragonHelm),(233,dragonSleeves),(226,dragonLegs),(240,dragonTunic)]
# END CONFIG --------------------------------------------------#

Player.HeadMessage(0,"Before you start, you must be OFF your beetle, with your beetle pack open.")    
Misc.Pause(1000)            
Player.HeadMessage(0,"Target Beetle")
beetle = Target.PromptTarget('Target Beetle')
Player.HeadMessage(0,"Target Item in Beetle Pack")
itemInBeetlePack = Target.PromptTarget('Target Item in Beetle Pack')
beetlePackItem = Items.FindBySerial(itemInBeetlePack)
beetlePack = beetlePackItem.RootContainer 

from System.Collections.Generic import List
from System import Int32 as int
import sys

noColor = 0x0000
self_pack = Player.Backpack.Serial
self = Player.Serial
dragTime = 600
gmCheckDelay = 200
craftTime = 1000
gumpTimeout = 4000

scissors = 0x0F9F

dragonScales = 0x26B4

if scaleColor == 'red':
    scaleColorGumpAction = 6
elif scaleColor == 'golden yellows':
    scaleColorGumpAction = 13
elif scaleColor == 'evil mage':
    scaleColorGumpAction = 20
elif scaleColor == 'greens':
    scaleColorGumpAction = 27
elif scaleColor == 'eon':
    scaleColorGumpAction = 34
elif scaleColor == 'valorite':
    scaleColorGumpAction = 41
elif scaleColor == 'paralytic':
    scaleColorGumpAction = 48

player_bag = Items.FindBySerial(Player.Backpack.Serial)
scissorsItem = Items.FindByID(scissors,-1,Player.Backpack.Serial, 1, 0)
if not scissorsItem:
    Player.HeadMessage(0,"ERROR FAILED TO FIND SCISSORS")
    print("ERROR - FAILED TO FIND SCISSORS!")
   
if fillBags:
    Player.HeadMessage(0,"Target bag with bags to fill with sets of armor.")
    baseBag = Target.PromptTarget('Target bag with bags to fill')

bags = [ 0xe76, 0xe75 , 0xe74 , 0xe78 , 0xe77 , 0x0E79 ]

if Player.GetRealSkillValue('Tinkering') < 80:
    craftOwnTools = False
else:
    craftOwnTools = True
    
def restockScales():
    if Items.BackpackCount(dragonScales,-1) < 250:
        if Player.Mount:
            Mobiles.UseMobile(Player.Serial)
            Misc.WaitForContext(beetle, 1500)
            if Player.Visible:
                Misc.ContextReply(beetle, 10)
            else:
                Misc.ContextReply(beetle, 0)
            Misc.Pause(dragTime)
        beetleScales = Items.FindByID( dragonScales , -1  , beetlePack, True )
        if beetleScales:
            Items.Move( beetleScales , self_pack , 300 )
            Misc.Pause(dragTime)
        else:
            Misc.SendMessage('Out of scales',33)
            sys.exit()
        
def craftTools():
    if craftOwnTools:
        currentTink = Items.FindByID(0x1EB8, -1, Player.Backpack.Serial, True )
        
        if Items.BackpackCount(0x1BF2, noColor) < 10:
            Misc.SendMessage('Out of Ignots',33)
            sys.exit()
        
        if Items.BackpackCount(0x1EB8, noColor) < 2:
            Items.UseItem(currentTink.Serial)
            Gumps.WaitForGump(949095101, 1500)
            Gumps.SendAction(949095101, 8)
            Gumps.WaitForGump(949095101, 1500)
            Gumps.SendAction(949095101, 23)

        if Items.BackpackCount( smithHammer, noColor) < 1: 
            Items.UseItem(currentTink.Serial)
            Gumps.WaitForGump(949095101,1500)
            Gumps.SendAction(949095101, 8)
            Gumps.WaitForGump(949095101,1500)
            Gumps.SendAction(949095101, 93)
class BagManager:
    def __init__(self):
        self.positions = [
            (15, 50),     # Position 1 (row 1, column 1)
            (55, 50),     # Position 2 (row 1, column 2)
            (75, 50),     # Position 3 (row 1, column 3)
            (15, 100),    # Position 4 (row 2, column 1)
            (55, 100),    # Position 5 (row 2, column 2)
            (100, 100)    # Position 6 (row 2, column 3)
        ]
        self.num_positions = len(self.positions)
        self.next_position_index = 0

    def moveToBag(self, item, container):
        if self.next_position_index < self.num_positions:
            x, y = self.positions[self.next_position_index]
            Items.Move(item, container,1, x, y)
            print(f"Moving item {item} to ({x}, {y})")
            self.next_position_index += 1
        else:
            # Reset to the start position
            self.next_position_index = 0
            x, y = self.positions[self.next_position_index]
            Items.Move(item, container,1, x, y)
            print("Resetting to start position and continuing...")

# Initialize BagManager instance
bag_manager = BagManager()
    
def craftDragArmor(bag):
    Misc.Pause(dragTime)
    Items.UseItem(bag)
    Misc.Pause(dragTime)
    for i in dragonSuit:
        while True:
            Misc.Pause(dragTime)
            restockScales()
            
            craftTools()
            hammer = Items.FindByID(smithHammer,smithHammerHue,Player.Backpack.Serial,True)
            if Items.FindByID( i[1] , -1 , bag.Serial ):
                break
            if hammer:
                if Gumps.CurrentGump() != 949095101:
                
                
                    Items.UseItem(hammer)
                Gumps.WaitForGump(949095101, gumpTimeout)
                Gumps.SendAction(949095101, 15) #Platemail Menu
                Gumps.WaitForGump(949095101, gumpTimeout)
                Gumps.SendAction(949095101, i[0])
                Gumps.WaitForGump(949095101, gumpTimeout)
                Misc.Pause(gmCheckDelay)
                craftedArmor = Items.FindByID(i[1],-1,Player.Backpack.Serial)
                if craftedArmor:
                    Items.WaitForProps(craftedArmor,500)
                    if 'exceptional' in Items.GetPropStringByIndex(craftedArmor,0):
                        #moveToBag(craftedArmor,bag)
                        bag_manager.moveToBag(craftedArmor, bag)
                        break
                    else:
                        #trashItem(craftedArmor)
                        #smeltItem(craftedArmor)
                        cutItem(craftedArmor)
            else:
                Player.HeadMessage(33,'No Smith Hammers!')
                sys.exit()
        
def trashItem(item):
    Items.Move(item, trashcan, 0)
    Misc.Pause(dragTime)

def smeltItem(item):
    
    hammer = Items.FindByID(smithHammer,-1,Player.Backpack.Serial,True)
            
    if hammer:
        if Gumps.CurrentGump() != 949095101:
            Misc.Pause(dragDelay)
            Items.UseItem(hammer)
        Gumps.WaitForGump(949095101, gumpTimeout)
        Gumps.SendAction(949095101, 14)    
        Misc.Pause(dragDelay)
        Target.TargetExecute(item)

def cutItem(item):
        Misc.Pause(dragDelay)
        Items.UseItem(scissorsItem)
        Misc.Pause(dragDelay)
        Target.TargetExecute(item)
        Misc.Pause(dragDelay)
        
def moveToBag(item, container):
    global bag_manager
    if Player.Mount:
        Misc.Pause(dragDelay)
        Mobiles.UseMobile(Player.Serial)
        Misc.WaitForContext(beetle, 1500)
        if Player.Visible:
            Misc.ContextReply(beetle, 10)
        else:
            Misc.ContextReply(beetle, 0)
        Misc.Pause(dragTime)
    # Assuming you want to move the item to the first available position in the bag
    bag_manager.moveToBag(item, container)
    Misc.Pause(dragTime)
    
def setColor():
    Misc.Pause(dragDelay)
    Items.UseItemByID(smithHammer,-1)
    Gumps.WaitForGump(949095101, gumpTimeout)
    Gumps.SendAction(949095101, 56)
    Gumps.WaitForGump(949095101, gumpTimeout)
    Gumps.SendAction(949095101, scaleColorGumpAction)
    Misc.Pause(dragTime)

def startCrafting():
    Player.HeadMessage(0,"Starting to Craft Armor now!")
    Journal.Clear()


    fillBag = None
    fillBag = Items.FindBySerial(baseBag)
    
    if fillBag != None:
        Items.UseItem(fillBag)
        Misc.Pause(dragTime)

        for b in fillBag.Contains:
            currentBag = Items.FindBySerial(b.Serial)
            if currentBag.IsContainer:
                craftDragArmor(currentBag)
        if not Player.Mount:
            Mobiles.UseMobile(beetle)
        Player.HeadMessage(0,'All Done Crafting Dragon Armor')            
        Misc.SendMessage('All Done Crafting Dragon Armor')
    else:
        print("ERROR: FAILED TO FIND FILL BAG!")
def updateGump(): 
    gd = Gumps.CreateGump(True,True,False,False)
    
    Gumps.AddImage(gd,0,-35,5170)  
    Gumps.AddImage(gd,20,-35,5171)
    Gumps.AddImage(gd,175,-35,5172)
    
    Gumps.AddBackground(gd, 0, 0, 218, 142, 2500)
    
    Gumps.AddBackground(gd, 25, 20, 175, 100, 302)

    Gumps.AddLabel(gd,80,32,0,"Scale Color")
    
    hue = 0
    hues = [1645, 2612, 2216, 2129, 2224, 1109, 2301]
    
    if scaleColor == 'red':
        hue = 1645
    elif scaleColor == 'paralytic':
        hue = 2612    
    elif scaleColor == 'golden yellows':
        hue = 2216   
    elif scaleColor == 'greens':
        hue = 2129
    elif scaleColor == 'valorite':
        hue = 2224
    elif scaleColor == 'evil mage':
        hue = 1109   
    elif scaleColor == 'eon':
        hue = 2301    
    else:
        print("FAILED TO FIND RIGHT COLOR FOR:", scaleColor)
        sys.exit()
 
    Gumps.AddHtml(gd,35,50,155,25,str("<CENTER> - " + str(scaleColor).upper() + ' - </CENTER>'),True,False)
    Gumps.AddImageTiled(gd,30,75,160,18,2621)    
    Gumps.AddImageTiled(gd,30,93,160,18,2627)     
    Gumps.AddItem(gd,35,32,dragonScales,hue)
    offsetX = 26
    hueIndex = 0
    
    for myHue in hues:

        if myHue == hue:
            
            Gumps.AddImage(gd,offsetX+4,68,2085)  
            
        offsetX = offsetX + 22
    
   
    offsetX = 26
    for myHue in hues:

        Gumps.AddItem(gd,offsetX-7,82,dragonScales,myHue)

        if myHue == hue:
            Gumps.AddButton(gd,offsetX,100,9723,9724,int(1000 + hueIndex),1,0)
        else:
            
            Gumps.AddButton(gd,offsetX,100,9720,9721,int(1000 + hueIndex),1,0)
        
        offsetX = offsetX + 22
        hueIndex = hueIndex + 1
        
      
    Gumps.AddLabel(gd,10,-15,2451,"   Dragon          Armor") 
    
    Gumps.AddButton(gd, 185, 95, 5556, 5555, 2, 1, 0) 
    Gumps.AddTooltip(gd,1061114,str("Start Crafting"))  
    Gumps.AddImage(gd,80,-25,494)
    Gumps.AddItem(gd,87,-25,8406)
    Gumps.AddLabel(gd,20,120,2033,"Created by Meesa Jar Jar")        
    Gumps.AddLabel(gd,50,130,2035,"Peace & Love!") 
    
    
    Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)
    
setColor()   
updateGump()

while True: 
    Misc.Pause(100)
    
    gd = Gumps.GetGumpData(gumpNumber)

    if gd:

        if gd.buttonid != -1:

            if gd.buttonid == 0:
               print("CLOSING SCRIPT")
               Player.HeadMessage(0,"Closing Script.")
               sys.exit()
               gd.buttonid = -1
               Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)    
               updateGump()
               
            if gd.buttonid == 2:

                startCrafting()
                
                gd.buttonid = -1
                Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)    
                updateGump()
                
            elif gd.buttonid >= 1000:

                if gd.buttonid == 1000:
                    scaleColor = 'red'    
                elif gd.buttonid == 1001:
                    scaleColor = 'paralytic' 
                elif gd.buttonid == 1002:
                    scaleColor = 'golden yellows' 
                elif gd.buttonid == 1003:
                    scaleColor = 'greens'                 
                elif gd.buttonid == 1004:
                    scaleColor = 'valorite'                 
                elif gd.buttonid == 1005:
                    scaleColor = 'evil mage' 
                elif gd.buttonid == 1006:
                    scaleColor = 'eon' 
                    
                if scaleColor == 'red':
                    scaleColorGumpAction = 6
                elif scaleColor == 'golden yellows':
                    scaleColorGumpAction = 13
                elif scaleColor == 'evil mage':
                    scaleColorGumpAction = 20
                elif scaleColor == 'greens':
                    scaleColorGumpAction = 27
                elif scaleColor == 'eon':
                    scaleColorGumpAction = 34
                elif scaleColor == 'valorite':
                    scaleColorGumpAction = 41
                elif scaleColor == 'paralytic':
                    scaleColorGumpAction = 48


    
                
                setColor()     
                gd.buttonid = -1
                
                Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings) 
                updateGump() 
