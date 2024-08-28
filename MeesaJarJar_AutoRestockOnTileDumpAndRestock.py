# Made by MeesaJarJar - http://github.com/MeesaJarJar/ - BabyBro / MesaJarJar on Discord - Peace & Love!
# -------------------------------------------------------------#
# Description: Automatically Restock from Predetermined Box at Predetermined Tile Coordinate when Player Stands on Tile.  
# -------------------------------------------------------------#
# START CONFIG --------------------------------------------------#
restockBoxSerial = 0x428FD30F
dumpBoxSerial = 0x421AFD52

tileLocationX = 2674 # Tile that when stepped on triggers the 'reagentsnbandages' Organizer Agent you must create
tileLocationY = 577 # Tile that when stepped on triggers the 'reagentsnbandages' Organizer Agent you must create


tileLocationDumpX = 2673 # Tile that when stepped on triggers the 'dump_gems_and_loot','dump_hide_and_scales',and 'dump_tmap_and_runes' Organizer Agent you must create
tileLocationDumpY = 592 # Tile that when stepped on triggers the 'dump_gems_and_loot','dump_hide_and_scales',and 'dump_tmap_and_runes' Organizer Agent you must create
dragTime = 650

# END CONFIG --------------------------------------------------#

while True:
    Misc.Pause(2000);

    if Player.Position.X == tileLocationX and Player.Position.Y == tileLocationY:
                
        if Timer.Check('restockTimer') == False:
        
            Player.HeadMessage(0,"Restocking Player.")
            
            if Restock.Status() == False:
                Restock.RunOnce('reagentsnbandages',restockBoxSerial,Player.Backpack.Serial,dragTime)
            
            Timer.Create('restockTimer',10000)
            
            
            reagents = [0x0F8C,0x0F88,0x0F7B,0x0F85,0x0F86,0x0F8D,0x0F7A,0x0F84]
         
            for reg in reagents:
                restockResource = Items.FindByID(reg, -1, Player.Backpack.Serial)
                
                if restockResource:
                    Misc.Pause(100)     
                    Items.Move(restockResource, Player.Backpack.Serial, -1, 0, 300)
                    
                    
            while Player.Position.X == tileLocationX and Player.Position.Y == tileLocationY:
                
                Misc.Pause(1000); # Check every 1 second whether the player has left the restock position.
     
    if Player.Position.X == tileLocationDumpX and Player.Position.Y == tileLocationDumpY:
                
        if Timer.Check('restockTimer') == False:
        
            Player.HeadMessage(0,"Dumping from Player.")
            
            if Organizer.Status() == False:
                Organizer.RunOnce('dump_gems_and_loot',Player.Backpack.Serial,dumpBoxSerial,dragTime)
            
            while Organizer.Status() == True:
                Misc.Pause(100);
            if Organizer.Status() == False:
                Organizer.RunOnce('dump_hide_and_scales',Player.Backpack.Serial,dumpBoxSerial,dragTime)    
                
            while Organizer.Status() == True:
                Misc.Pause(100);
            if Organizer.Status() == False:
                Organizer.RunOnce('dump_tmap_and_runes',Player.Backpack.Serial,dumpBoxSerial,dragTime)        
            Timer.Create('dumpTimer',10000)
            
            while Player.Position.X == tileLocationDumpX and Player.Position.Y == tileLocationDumpY:
                
                Misc.Pause(1000); # Check every 1 second whether the player has left the restock position.
            