# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description: Sorts your Super and Lesser Slayer Spellbooks
# into two seperate containers, maintaining a grid style placement.
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#
cont1 = 0x44470C99 # Where we are placing lesser slayers
cont0 = 0x405E0275 # Where we are placing super slayers
# END CONFIG --------------------------------------------------#

import math

superslayers = ['Silver', 'Reptilian Death', 'Elemental Ban', 'Repond', 'Exorcism', 'Arachnid Doom', 'fey slayer']
lesserslayers = ["Ogre Thrashing", "Orc Slaying", "Troll Slaughter", "Blood Drinking", "Earth Shatter",
                 "Elemental Health", "Flame Dousing", "Summer Wind", "Vacuum", "Water Dissipation",  
                 "Balron Damnation", "Daemon Dismissal", "Gargoyles Foe", "Scorpions Bane", "Spiders Death",
                 "Terathan", "Dragon Slaying", "Lizardman Slaughter", "Ophidian", "Snakes Bane"]

superslayers.sort()
lesserslayers.sort()

superslayers_rows = [superslayers[i:i+5] for i in range(0, len(superslayers), 5)]
lesserslayers_rows = [lesserslayers[i:i+5] for i in range(0, len(lesserslayers), 5)]

for row in lesserslayers_rows:
  print(row)

min_x = 18 
min_y = 105
max_x = 130
max_y = 160

step_x = (max_x - min_x) / len(superslayers_rows[0])
step_y = (max_y - min_y) / len(superslayers_rows)

def get_position(slayer):
  return positions.get(slayer, (None, None))

positions = {}

for i, row in enumerate(superslayers_rows):
  for j, slayer in enumerate(row):
    x = j * step_x + min_x
    y = i * step_y + min_y
    positions[slayer] = (x, y)
      
for i, row in enumerate(lesserslayers_rows):
  for j, slayer in enumerate(row):
    x = j * step_x + min_x
    y = i * step_y + min_y
    positions[slayer] = (x, y)

container = Items.FindBySerial(cont2)
Items.UseItem(container)

container0 = Items.FindBySerial(cont0)
Items.UseItem(container0)

for item in container.Contains:
    print("Processing Item.")
    Misc.Pause(500)
    print(item.Name)
    props = Items.GetPropStringList(item)
    print(props)
    
    if props[3] in superslayers:
        #print("props3:" + str(props[3]))
        pos = get_position(props[3])
        
        print(props[3], cont0, 1, int(pos[0]), int(pos[1]))
        
        Items.Move(item.Serial, cont0, 1, int(pos[0]), int(pos[1]))
    else: 
        print("Didnt find in super slayer list") 
        print(props[3])
   
    if props[3] in lesserslayers:
        #print("props3:" + str(props[3]))
        pos = get_position(props[3])
        
        print(props[3], cont1, 1, int(pos[0]), int(pos[1]))
        
        Items.Move(item.Serial, cont1, 1, int(pos[0]), int(pos[1]))
    else: 
        print("Didn't find in supslayer list") 
        print(props[3])
