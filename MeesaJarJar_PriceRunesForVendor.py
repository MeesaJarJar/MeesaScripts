# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description: Auto Price and Place Runes on your vendor.
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#
runebag = 0x41843DC6
vendorBackpack = 0x405A97F9
runePrice = 50
# END CONFIG --------------------------------------------------#


coordinates_L = [(x + 1.0, y + 1.0) for x in range(0, 6) for y in range(20, 26)]
coordinates_L.extend([(5 + 1.0, y + 1.0) for y in range(0, 26)])

coordinates_M = [(x + 26.0, 25.0) for x in range(0, 10, 3)] 
coordinates_M.extend([(x + 26.0, y + 26.0) for x in range(1, 3) for y in range(0, 6)]) 
coordinates_M.extend([(x + 26.0, y + 26.0) for x in range(7, 9) for y in range(0, 6)])  

all_coordinates = coordinates_L + coordinates_M

while True:
        
    runes = Items.FindByID(0x1F14,0x0000,runebag,1,False)
    if runes:

        current_coordinate = all_coordinates.pop(0)

        print(int(current_coordinate[0]+50), int(current_coordinate[1]+65))
        Items.Move(runes, vendorBackpack, 10, int(current_coordinate[0]+50), int(current_coordinate[1]+65))
        Misc.Pause(250);
        
        Misc.ResponsePrompt(str(runePrice))
        Misc.Pause(650);
        