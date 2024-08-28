# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! ------------#
# Others included: Matsamilla, Nox, sorry if I forgot anyone.
# --ALERT---WORK IN PROGRESS-----------------------------------#
# Description: MIB Sailer GUMP using A* Pathfinding for Sailing
# Work in progress script, runng into issues with custom islands
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#

# You cannot use this script yet - sorry. 
# END CONFIG --------------------------------------------------#
from heapq import heappop, heappush

import math
import random
import csv

def worldSave():
    if Journal.SearchByType('The world will save in 1 minute.', 'Regular' ):
        Misc.SendMessage('Pausing for world save', 33)
        while not Journal.SearchByType('World save complete.', 'Regular'):
            Misc.Pause(500)
        Misc.Pause(2500)
        Misc.SendMessage('Continuing run', 33)
        Journal.Clear()   
 
 
def splitToPieces(location):
    degree, secTemp= location.split('\xb0')
    seconds, direction = secTemp.split('\x27')
    return int(degree), int(seconds), direction
 
def convertDegreesToDecimal(degree, seconds, direction):
    result = 0
    if direction.lower() == 'w': 
        result = (LordBritishThrone[1]-(seconds/60.0)* TilesPerDegree[1]-degree*TilesPerDegree[1])%WorldSize[1]
    #    
    if direction.lower() == 'e': 
        result = (LordBritishThrone[1]+(seconds/60.0)* TilesPerDegree[1]+degree*TilesPerDegree[1])%WorldSize[1]
    #    
    if direction.lower() == 'n': 
        result = (LordBritishThrone[0]-(seconds/60.0)* TilesPerDegree[0]-degree*TilesPerDegree[0])%WorldSize[0]
    #    
    if direction.lower() == 's': 
        result = (LordBritishThrone[0]+(seconds/60.0)* TilesPerDegree[0]+degree*TilesPerDegree[0])%WorldSize[0]
    #    
    return int(result)+1
 
#def GetDecimalCoordinates(mib):
#    print(mib)
#    x = -1
#    y = -1
#    Items.UseItem(mib)
#    Gumps.WaitForGump(0, 3000)
#    if Gumps.HasGump():
#        texts = Gumps.LastGumpGetLineList()
#        location = texts[len(texts)-1]
#        z = location.split(',')
#        Player.HeadMessage(54, str(z[1]))
#        NSloc, EWloc = location.split(',')
#        deg1, sec1, dir1 = splitToPieces(NSloc) 
#        deg2, sec2, dir2 = splitToPieces(EWloc)
#        Gumps.CloseGump(0)
#        #
#        Misc.SendMessage("deg: {} sec: {} dir: {}".format(deg1, sec1, dir1))
#        Misc.SendMessage("deg: {} sec: {} dir: {}".format(deg2, sec2, dir2))
#        x = convertDegreesToDecimal(deg2, sec2, dir2)
#        y = convertDegreesToDecimal(deg1, sec1, dir1)
#        return x, y
#    else:
#        Misc.SendMessage("Gump did not Open for mib 0x{:x}".format(mib.Serial))
#    return x, y

def GetDecimalCoordinates(mib):
    print(mib)
    x = -1
    y = -1
    Items.UseItem(mib)
    Gumps.WaitForGump(0, 3000)
    if Gumps.HasGump():
        texts = Gumps.LastGumpGetLineList()
        location = texts[len(texts)-1]  # This line might cause issues if the gump is not formatted as expected
        print("Location string:", location)  # Debug output
        z = location.split(',')
        Player.HeadMessage(54, str(z[1]))
        NSloc, EWloc = location.split(',')
        deg1, sec1, dir1 = splitToPieces(NSloc) 
        deg2, sec2, dir2 = splitToPieces(EWloc)
        Gumps.CloseGump(0)
        #
        Misc.SendMessage("deg: {} sec: {} dir: {}".format(deg1, sec1, dir1))
        Misc.SendMessage("deg: {} sec: {} dir: {}".format(deg2, sec2, dir2))
        x = convertDegreesToDecimal(deg2, sec2, dir2)
        y = convertDegreesToDecimal(deg1, sec1, dir1)
        return x, y
    else:
        Misc.SendMessage("Gump did not Open for mib 0x{:x}".format(mib.Serial))
    return x, y
      
def processSOS():           
    Player.HeadMessage(1152,"Starting SOS Extraction.")
    #with open(MibFileName, 'a') as file:  # Open the file in append mode
    for mib in Player.Backpack.Contains:
        if mib.ItemID == 0x14EE:
            Items.UseItem(mib)
            Misc.Pause(800)  
            x, y = GetDecimalCoordinates(mib)
            Player.HeadMessage(54, str(x))
            Player.HeadMessage(54, str(y))
            Misc.SendMessage("X: {}".format(x))
            Misc.SendMessage("Y: {}".format(y))
            z = str(x) + ',' + str(y) + ',0,'+ str(mib) +',mib,' + 'blue' + '3' # Corrected the new line character
            Misc.Pause(100)
            print(z)
            
            Misc.AppendNotDupToFile(MibFileName,z)
            Misc.Pause(100)
            Gumps.SendAction(1426736667, 0)
            Misc.Pause(800)
    Player.HeadMessage(1152,"Finished SOS Extraction!")
    
def convert_to_rgb(binaryObstacleMap):
    rgb_map = [[[0, 0, 0] if pixel == 0 else [255, 255, 255] for pixel in row] for row in binaryObstacleMap]
    return rgb_map

def euclidean_distance(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

def calculate_total_distance(order, locations):
    total_distance = 0
    for i in range(len(order) - 1):
        total_distance += euclidean_distance(locations[order[i]], locations[order[i+1]])
    try:    
        total_distance += euclidean_distance(locations[order[-1]], locations[order[0]])
    except:
        print("Failed a calc.")
    return total_distance

def find_optimal_order(locations, num_iterations=100):
    num_locations = len(locations)
    optimal_order = None
    min_distance = float('inf')

    for _ in range(num_iterations):
        random_order = random.sample(range(num_locations), num_locations)
        distance = calculate_total_distance(random_order, locations)
        if distance < min_distance:
            min_distance = distance
            optimal_order = random_order
    
    return optimal_order, min_distance

def heuristic_euclidean(a, b):
    """Calculate the Euclidean distance between two points"""
    return ((a[0] - b[0])**2 + (a[1] - b[1])**2)**0.5

def heuristic_euclidean_wrapped(a, b, max_x, max_y):
    """Calculate the Euclidean distance between two points considering wrap-around."""
    dx = min(abs(a[0] - b[0]), max_x - abs(a[0] - b[0]))
    dy = min(abs(a[1] - b[1]), max_y - abs(a[1] - b[1]))
    return ((dx**2) + (dy**2))**0.5
  
def astar_wraparound(grid, start, goal):
    global explored_nodes
    # Initialize the open list (heap), closed list, and various scores and parents dictionaries
    open_list = []
    closed_list = set()
    start = (start[1], start[0])  # Adjusting start coordinate
    goal = (goal[1], goal[0])  # Adjusting goal coordinate
    g = {start: 0}
    h = {start: heuristic_euclidean_wrapped(start, goal, len(grid), len(grid[0]))}
    f = {start: h[start]}
    parents = {}

    heappush(open_list, (f[start], start))
    iteration = 0

    while open_list:
        iteration += 1
        
        if iteration >=10000:
            print(f"Iteration: {iteration}, Open List Size: {len(open_list)}")
            break
        _, current = heappop(open_list)
        #print(f"Processing Node: {current}, g: {g[current]}, h: {h[current]}, f: {f[current]}")
        closed_list.add(current)

        if current == goal:
            path = [current]
            while current in parents:
                current = parents[current]
                path.append(current)
            print("Path found!")
            
            return path[::-1]  # Returning the path in start-to-goal order

        for dx, dy in [(0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
            x, y = (current[0] + dx) % len(grid), (current[1] + dy) % len(grid[0])
            neighbor = (x, y)

            if grid[x][y] == 1 or neighbor in closed_list:
                continue

            tentative_g = g[current] + 1
            if neighbor not in g or tentative_g < g[neighbor]:
                parents[neighbor] = current
                g[neighbor] = tentative_g
                h[neighbor] = heuristic_euclidean_wrapped(neighbor, goal, len(grid), len(grid[0]))
                f[neighbor] = g[neighbor] + h[neighbor]

                if neighbor not in [i[1] for i in open_list]:
                    heappush(open_list, (f[neighbor], neighbor))
                    explored_nodes.append(neighbor)  # Track explored node
                    #print(f"Adding Neighbor: {neighbor}, g: {tentative_g}, h: {h[neighbor]}, f: {f[neighbor]}")
    

    #draw_explored_nodes(explored_nodes)  # This is a placeholder for your drawing logic

    print("No path found.")
    return []
    
def resizeSmaller(larger_x, larger_y):
    smaller_map_size = 1024
    larger_map_width = 5200
    larger_map_height = 4097
    
    smaller_x = (larger_x * smaller_map_size + larger_map_width // 2) // larger_map_width
    smaller_y = (larger_y * smaller_map_size + larger_map_height // 2) // larger_map_height

    return smaller_x, smaller_y
    
def resizeSmaller2(larger_x, larger_y):
    smaller_map_size = 383
    larger_map_width = 1024
    larger_map_height = 1024
    
    smaller_x = (larger_x * smaller_map_size + larger_map_width // 2) // larger_map_width
    smaller_y = (larger_y * smaller_map_size + larger_map_height // 2) // larger_map_height

    return smaller_x, smaller_y


def updateGump():
    global mibs, pathpoints, allPathPointsList, status, colors, currentPage, gumpNumber, explored_nodes
    
    gd = Gumps.CreateGump()
    Gumps.AddPage(gd, 0)
    gumpHeight = 383
    gumpWidth = 383
    
    #Gumps.AddBackground(gd, 0, 0, 383, 383, 5585) 
    
    # Larger map dimensions
    largerMapWidth = 5119
    largerMapHeight = 4096
    
    # Smaller map dimensions
    smallerMapWidth = 383
    smallerMapHeight = 383
    
    Gumps.AddBackground(gd, 0, 20, 383, 383, 5585) 

    for z in range(1,11):
        Gumps.AddImage(gd, -44 + (z*40), 3, 303)
        Gumps.AddImage(gd, -44 + (z*40), 383+21, 309)

    for h in range(0,10):    
        Gumps.AddImage(gd, -16, (h*40)+18, 305)
        Gumps.AddImage(gd, 383, (h*40)+18, 307)
        
    Gumps.AddImage(gd, -16, 3, 302)
    Gumps.AddImage(gd, 383, 3, 304)

    Gumps.AddImage(gd, -16, 383+20, 308)
    Gumps.AddImage(gd, 383, 383+20, 310)
    #Gumps.AddImage(gd, -2, 16,5599) 

    relativeX = int((Player.Position.X / largerMapWidth) * smallerMapWidth)
    relativeY = int((Player.Position.Y / largerMapHeight) * smallerMapHeight)

    
    Gumps.AddImage(gd,relativeX,relativeY,5602)
    Gumps.AddLabel(gd,relativeX+20,relativeY,920, "You")

    statusX = 400
    statusY = 20
    #Status
    for x in range(1,13):
        for y in range(1,24):
            Gumps.AddImage(gd, statusX -1 + (x * 16), statusY + (y * 16), 87)   
    for x in range(1,13):
        Gumps.AddImage(gd, statusX + ( x * 16), statusY, 84)    
        Gumps.AddImage(gd, statusX + ( x * 16), statusY + 373, 90)   

    for y in range(1,24):
        Gumps.AddImage(gd, statusX + 9 + ( x * 16), statusY + (y * 16), 88)
        Gumps.AddImage(gd, statusX-1 , statusY + (y * 16), 86)
            
    Gumps.AddImage(gd, statusX, statusY, 83)   
    Gumps.AddImage(gd, statusX, statusY + 373, 89)  

    Gumps.AddImage(gd, statusX + 200, statusY, 85)   
    Gumps.AddImage(gd, statusX + 200, statusY + 373, 91)  

    Gumps.AddImage(gd, statusX+50, statusY, 2480)

    Gumps.AddImage(gd, statusX+50, statusY +8, 2484)   
    if status == 0: #error enountered
        Gumps.AddImage(gd, statusX+55, statusY + 5, 40)
    elif status == 1: #not running
        Gumps.AddImage(gd, statusX+55, statusY + 5, 9750)
    elif status == 2: #RUNNING
        Gumps.AddImage(gd, statusX+55, statusY + 5, 9752) 
    else:
        # Default case if 'status' is not 0, 1, or 2
        print("Invalid status value")

    count      = 1
    countt = 0
    markerSize = 8
    pathpoints = list(set(pathpoints))       
    colors = []
    displayPerPage = 14
    while countt < 30:
        countt += 1   
        colors.append(countt*25)
        
    for pathpoint in pathpoints:
        Gumps.AddImage(gd, pathpoint[1], pathpoint[0]+20, 6001)
        
    for pathpointx in currentPath:
        # Adjust the coordinates if necessary based on your maps layout
        # Assuming pathpoint is in (x, y) format
        ex,ey = resizeSmaller2(pathpointx[1], pathpointx[0])
        Gumps.AddImage(gd, ex, ey , 6001, 132)
        
        
        
    #print("explored_nodes:", explored_nodes)
    for node in explored_nodes:
            
        Gumps.AddImage(gd, node[1], node[0]+20, 6008)   
        
    for mib in mibs:
        
        if count <= (displayPerPage * currentPage) and count >= (currentPage * count):
      
            # Calculate the relative x and y positions on the smaller map
            relativeX = int((int(mib[0]) / largerMapWidth) * smallerMapWidth)
            relativeY = int((int(mib[1]) / largerMapHeight) * smallerMapHeight)
            
            Gumps.AddImage(gd,round(relativeX-10),round(relativeY+5),5602)

            Gumps.AddImage(gd,round(relativeX-12),round(relativeY-14), 210)
            Gumps.AddLabel(gd,round(relativeX-6),round(relativeY-14), colors[count-1], str(count))
            
            if toggleCoords:
                if mib[0] > largerMapWidth /2:
                    Gumps.AddLabel(gd,relativeX-85, relativeY+3, colors[count-1], str(mib[0]) + "," + str(mib[1]))  
                if mib[0] <= largerMapWidth /2:
                    Gumps.AddLabel(gd,relativeX+5, relativeY+3,  colors[count-1], str(mib[0]) + "," + str(mib[1]))        

            Gumps.AddImage(gd,statusX + (15),statusY+(25* count),1042)
            Gumps.AddLabel(gd,statusX + (50),statusY+(25* count)+3, colors[count-1], str(mib[0]) + "," + str(mib[1]))
            
            Gumps.AddImage(gd,statusX + (25),statusY+(25* count),210)
            Gumps.AddLabel(gd,statusX + (29),statusY+(25* count)+2, colors[count-1], str(count))    
            
            Gumps.AddButton(gd,statusX + (125),statusY+(25* count)+2,4016,4014,1000 + count,1,1)
            
            count+=1
            
    Gumps.AddButton(gd,410,340,5608,5609,99,1,1)
    Gumps.SendGump(gumpNumber, Player.Serial, 40, 40, gd.gumpDefinition, gd.gumpStrings)


def generateAndDrawPoints():    
    pathpoints = []    
    for z in range(0, len(mibs)-1):
        print("MIB:", z)

        a,b = resizeSmaller(mibs[z][0], mibs[z][1])
        start_pos = (a, b)
        start_pos_large = mibs[z][0], mibs[z][1]

        try:
            c,d = resizeSmaller(mibs[z+1][0], mibs[z+1][1])
            goal_pos = (c, d)
            goal_pos_large = mibs[z+1][0], mibs[z+1][1]
            
        except IndexError:
            goal_pos_large = start_pos_large
            goal_pos = start_pos
        
        print("start:", start_pos,"goal:", goal_pos)
        print("startL:", start_pos_large,"goalL:", goal_pos_large)
        
        # Run the A* algorithm
        new_path = astar_wraparound(binaryObstacleMap, start_pos, goal_pos)
        
        print("Path LengthX:", len(new_path))
        nodeColor = [random.randint(0,254),random.randint(0,254),random.randint(0,254)]
        nodeColor2 = [random.randint(0,254),random.randint(0,254),random.randint(0,254)]

        #rgb_obstacle_map = rgb_obstacle_map_original
        for pos in new_path:
            resized_x, resized_y = resizeSmaller2(pos[0] , pos[1])  # Convert to smaller range
            pathpoints.append((resized_x, resized_y))  # Use parentheses to create a tuple
            
            for z in range(-2, 2):
                for t in range(-2, 2):
                    try:
                        #[pos[0] + t][pos[1] + z] = nodeColor

                        test = 1
                    except:
                        test = False
        
        print("Going Next MIB")
    
    pathpoints = list(set(pathpoints))  
    
    return pathpoints

def convert_packet_to_bytes(packet):
    byte_list = []
    for value in packet:
        try:
            byte_list.append(int(value, 16))
        except ValueError:
            print("Invalid hexadecimal value in packet:", value)
            print("Original packet:", packet)
            return None
    return byte_list

def createItemAtLocation(itemx,itemy,itemz,packet_list,hue):
    randidint = random.randrange(0,10000000)

    i_loc_x = hex(itemx) 
    i_loc_y = hex(itemy)
    i_loc_z = hex(itemz)

    if len(i_loc_x) < 6:
        i_loc_x = i_loc_x.replace("0x","0x0")
    if len(i_loc_y) < 6:
        i_loc_y = i_loc_y.replace("0x","0x0")    
    if len(i_loc_z) < 6:
        i_loc_z = i_loc_z.replace("0x","0x0") 

    x1 = i_loc_x[2:4]  
    x2 = i_loc_x[4:6]  
    y1 = i_loc_y[2:4]  
    y2 = i_loc_y[4:6]  
    z = i_loc_z 
    
    hues = hue.split(" ")

    packet_list[5] = hex(randidint)[2:].zfill(2)
    packet_list[15] = x1
    packet_list[16] = x2
    packet_list[17] = y1
    packet_list[18] = y2
    packet_list[19] = z
    packet_list[21] = hues[0]
    packet_list[22] = hues[1]
    
    byte_list = convert_packet_to_bytes(packet_list)
    
    PacketLogger.SendToClient(byte_list)
    
    return packet_list

def drawFakeItemAtSpot(X, Y):
    packet = "F3 00 01 00 48 FC BB 12 6E 7B 00 00 01 00 01 05 88 06 88 0A 00 04 15 20 00 00"  
    packet_list = packet.split(" ")  

    hue = "00 00"
    itemID = 0xB6D0
    X = int(X)
    Y = int(Y)
    Z = int(Player.Position.Z + 2)

    packet = createItemAtLocation(X,Y,Z,packet_list,hue)
    

def distance_between_points(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def sailToLocation(locationX, locationY):
    global optimal_order, binaryObstacleMap, stopSail, currentPath
#
#    startX = Player.Position.X 
#    startY = Player.Position.Y
    locationX -=3

    # Run the A* algorithm
    
    c,d = resizeSmaller(Player.Position.X - 3 , Player.Position.Y)
    player_pos = (c, d)    
    
    c,d = resizeSmaller(locationX, locationY)
    target_pos = (c, d)
    
    print("Player Pos:", player_pos)
    print("Target Pos:", target_pos)
    new_path = astar_wraparound(binaryObstacleMap, player_pos, target_pos)
    print("Path:", new_path)
    print("Path Length:", len(new_path))
    
    for pos in new_path:
        currentPath.append(pos)
          
            
    for pos in new_path:
        resized_x, resized_y = resizeSmaller2(pos[0] , pos[1])  # Convert to smaller range
        print("DEBUG:", resized_x, resized_y)

        try:
            print("DEBUGGGGG:", pos[0] + t,pos[1] + z)
            #rgb_obstacle_map[pos[0] + t][pos[1] + z] = [128,128,128]
        except:
            print("FAILED!!!!!!!!!")
        
                        
                        
    for pos in new_path:
        updateGump()
        print("Sailing to POS:", pos)
        prevCommand =  ''

        while Player.Position.X != locationX or Player.Position.Y != locationY:
            
            if stopSail == True:
                break
            #print("While", pos[0], pos[1])
            if Player.Position.X == locationX and Player.Position.Y == locationX:
                print("Player Reached Destination! Stopping navigation.")
                Player.ChatSay("Stop")
                break
                
            
            if distance_between_points(locationX, locationY, Player.Position.X, Player.Position.Y) > 4:
                one = ''
            else:
                one = ' One'
                
            if Player.Position.X < locationX and Player.Position.Y < locationY:
                if prevCommand != "Back Right" + str(one):
                    Player.ChatSay("Back Right" + str(one))
                    prevCommand = "Back Right" + str(one)
            elif Player.Position.X < locationX and Player.Position.Y > locationY:
                if prevCommand != "Forward Right" + str(one):
                    Player.ChatSay("Forward Right" + str(one))
                    prevCommand = "Forward Right" + str(one)
            elif Player.Position.X > locationX and Player.Position.Y > locationY:
                if prevCommand != "Forward Left" + str(one):
                    Player.ChatSay("Forward Left" + str(one))
                    prevCommand = "Forward Left" + str(one)
            elif Player.Position.X > locationX and Player.Position.Y < locationY:
                if prevCommand != "Back Left" + str(one):
                    Player.ChatSay("Back Left" + str(one))
                    prevCommand = "Back Left" + str(one)
            elif Player.Position.X < locationX and Player.Position.Y == locationY:
                if prevCommand != "Right" + str(one):
                    Player.ChatSay("Right" + str(one))
                    prevCommand = "Right" + str(one)
            elif Player.Position.X > locationX and Player.Position.Y == locationY:
                if prevCommand != "Left" + str(one):
                    Player.ChatSay("Left" + str(one))
                    prevCommand = "Left" + str(one)
            elif Player.Position.Y < locationY and Player.Position.X == locationX:
                if prevCommand != "Backward" + str(one):
                    Player.ChatSay("Backward" + str(one))
                    prevCommand = "Backward" + str(one)
            elif Player.Position.Y > locationY and Player.Position.X == locationX:
                if prevCommand != "Forward" + str(one):
                    Player.ChatSay("Forward" + str(one))
                    prevCommand = "Forward" + str(one)
                
            if distance_between_points(locationX, locationY, Player.Position.X, Player.Position.Y) < 16:
                drawFakeItemAtSpot(locationX+3, locationY)    
                
            Misc.Pause(650)
        
        
    print("Finished Sail To Location Function.")

# MIB Processor CONFIG
MibFileName = 'C:/Program Files (x86)/UOForever/UO/Forever/Data/Client/MIBCapture.csv'    

LordBritishThrone=[1624, 1323]    
WorldSize = [4096, 5120]
TilesPerDegree= [ WorldSize[0]/360.0, WorldSize[1]/360.0 ] 
# END MIB Processor CONFIG

processSOS()
    
status        = 0
currentPage   = 1
selectedPoint = [0,0]
currentPath = []

explored_nodes = []
toggleCoords  = True
print("Loading Binary Map for Pathfinding waterways.")
bin_file_path_png_padded = r'C:\Program Files (x86)\UOForever\UO\Forever\Data\Client\map_png_padded.bin' 

with open(bin_file_path_png_padded, 'rb') as f:
    img_array_from_bin_png_padded = []
    while True:
        byte = f.read(1)
        if not byte:
            break
        img_array_from_bin_png_padded.append(int.from_bytes(byte, 'little'))
        
binaryObstacleMap = [[1 if pixel >= 2 else 0 for pixel in img_array_from_bin_png_padded[i:i+1024]] for i in range(0, len(img_array_from_bin_png_padded), 1024)]

#_original = convert_to_rgb(binaryObstacleMap)

mibs = []
print("Loading MIB CSV File.")
with open(r'C:\Program Files (x86)\UOForever\UO\Forever\Data\Client\MIBCapture.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        if len(row) >= 2:  
            mibs.append([int(row[0]),int(row[1])])
            
for mib in mibs:
    print("RAWMIB:",mib)
    
num_locations = len(mibs)
print("Detected MIBs:",num_locations)

optimal_order, min_distance = find_optimal_order(mibs)
print("Optimal order:", optimal_order)
print("Minimum distance:", min_distance)

rearrangedList = [mibs[i] for i in optimal_order]
mibs = rearrangedList

pathpoints = generateAndDrawPoints()  
print("pathpoints:",pathpoints)

gumpNumber = 45347372
stopSail = False

print("STARTUP COMPLETE.")
updateGump()
while True:
    
    Misc.Pause(1000)

    gd = Gumps.GetGumpData(gumpNumber)

    if gd:

        if gd.buttonid == 0:
            gd.buttonid = -1
            Gumps.SendGump(gumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)
            updateGump()
            
        if gd.buttonid == 99:
            processSOS()
            gd.buttonid = -1
            updateGump()
            
        if gd.buttonid <= 2000 and gd.buttonid >= 999: # START
            print("PRESSED BUTTON:", gd.buttonid);  
            updateGump()
            
            print("Preparing to sail to:", mibs[gd.buttonid - 1001])
            
            sailToLocation(mibs[gd.buttonid - 1001][0], mibs[gd.buttonid - 1001][1])
            gd.buttonid = -1
            updateGump() 
            
        if Timer.Check('gumpUpdate') == False:
            #print("*** TIMER GUMP UPDATE **")
            Timer.Create('gumpUpdate',5000)
            updateGump()