# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description: This script simply looks for NON LOCKED DOWN
# items that are within a range of 12 of the player. This helps
# find items that you forgot to lock down! Some items that
# are like floor tiles, rugs, or mini houses, appear as though
# they are not locked down so you will have to ignore those.
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#

# END CONFIG --------------------------------------------------#

while Player.Connected == True:
    
    itemFilter = Items.Filter()
    itemFilter.RangeMin = 0 
    itemFilter.RangeMax = 12

    itemList = Items.ApplyFilter(itemFilter)

    for item in itemList:
        if 'locked down' not in str(item.Properties).lower():
            print(item, item.Position.X, item.Position.Y, item.Position.Z)
            Items.Message(item,1150,'THIS ITEM IS NOT LOCKED DOWN:            ' +  item.Name)
            #Items.Message(item,1150,item.Name)
    Misc.Pause(10000)