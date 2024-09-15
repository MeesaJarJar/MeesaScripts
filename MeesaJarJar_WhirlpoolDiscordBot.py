import re
import math
import os
import clr
from System import Int32 as int
import re
import math
import os
import clr
import mimetypes
import urllib.request
clr.AddReference("System.Drawing")  # Ensure we reference System.Drawing for image manipulation
from System.Drawing import Image, Graphics, Pen, Brush, Brushes, Font, FontStyle, Color

coordinates = []


def draw_red_circle_on_map(image_path, x, y, label):

    bmp = Image.FromFile(image_path)
    g = Graphics.FromImage(bmp)
    radius = 32 
    pen = Pen(Color.White, 5)  
    g.DrawEllipse(pen, x - radius, y - radius, 2 * radius, 2 * radius)
    
    radius = 128 
    pen = Pen(Color.Orange, 8)  
    g.DrawEllipse(pen, x - radius, y - radius, 2 * radius, 2 * radius)
        
    radius = 256 
    pen = Pen(Color.Red, 32)  
    g.DrawEllipse(pen, x - radius, y - radius, 2 * radius, 2 * radius)
        
    # Define the font for the label
    font = Font("Arial", 128, FontStyle.Bold)
    
    # Draw the text label with coordinates
    g.DrawString(label, font, Brushes.White, x + radius, y - radius)
    g.DrawString(label, font, Brushes.White, 0,0)
    # Save the updated image
    output_image_path = "marked_map.png"
    bmp.Save(output_image_path)
    
    # Clean up
    g.Dispose()
    bmp.Dispose()
    
    return output_image_path


def postDiscordMessageWithImage(message, image_path):
    webhook_url = "https://discord.com/api/webhooks/xxx"

    boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
    headers = {
        'Content-Type': f'multipart/form-data; boundary={boundary}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Prepare the message part
    message_data = f'--{boundary}\r\nContent-Disposition: form-data; name="content"\r\n\r\n{message}\r\n'

    # Prepare the file part
    mime_type, _ = mimetypes.guess_type(image_path)
    file_data = ''
    with open(image_path, 'rb') as f:
        file_content = f.read()
        file_data = (
            f'--{boundary}\r\n'
            f'Content-Disposition: form-data; name="file"; filename="{image_path}"\r\n'
            f'Content-Type: {mime_type}\r\n\r\n'
            f'{file_content.decode("latin1")}\r\n'
        )

    # End of the multipart request
    ending = f'--{boundary}--\r\n'

    # Combine all parts
    body = message_data + file_data + ending
    body = body.encode('latin1')

    req = urllib.request.Request(url=webhook_url, data=body, headers=headers, method='POST')

    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 204:
                print("Message with image sent successfully.")
            else:
                print(f"Failed to send the message. Status Code: {response.status}")
                print(f"Response: {response.read().decode('utf-8')}")
    except urllib.error.HTTPError as e:
        print(f"Failed to send the message. Status Code: {e.code}")
        print(f"Response: {e.read().decode('utf-8')}")
    except urllib.error.URLError as e:
        print(f"Failed to send the message. Reason: {e.reason}")


def sextantToCoords(degNS, minNS, dirNS, degWE, minWE, dirWE):
    degNS = int(degNS)
    minNS = int(minNS)
    degWE = int(degWE)
    minWE = int(minWE)

    off_x = 1319
    off_y = 1621

    max_x = 5120
    max_y = 4096

    tile_deg_x = max_x / 360.0
    tile_deg_y = max_y / 360.0

    tile_min_x = tile_deg_x / 60.0
    tile_min_y = tile_deg_y / 60.0

    # Calculate world coordinates
    x = (degWE * tile_deg_x) + (minWE * tile_min_x)
    y = (degNS * tile_deg_y) + (minNS * tile_min_y)

    # Adjust for direction
    x = off_x + (x if dirWE == 'E' else -x)
    y = off_y + (y if dirNS == 'S' else -y)

    # Handle wrap-around logic
    x = x % max_x
    y = y % max_y

    # Round coordinates to nearest integer
    x = int(round(x))
    y = int(round(y))

    return (x, y)


def extract_sextant_from_text(text):
    pattern = r"(\d+)[^\d]+(\d+)'([NS]),[^\d]+(\d+)[^\d]+(\d+)'([EW])"
    
    match = re.search(pattern, text)
    if match:
        degNS = match.group(1)
        minNS = match.group(2)
        dirNS = match.group(3)
        degWE = match.group(4)
        minWE = match.group(5)
        dirWE = match.group(6)
        return degNS, minNS, dirNS, degWE, minWE, dirWE
    else:
        raise ValueError("Sextant coordinates not found in the text")
        

while Player.Connected == True:
    Misc.Pause(3000)
    if Gumps.HasGump(3909731411):
        gump_line = Gumps.GetLine(3909731411, 2)

        degNS, minNS, dirNS, degWE, minWE, dirWE = extract_sextant_from_text(gump_line)

        x, y = sextantToCoords(degNS, minNS, dirNS, degWE, minWE, dirWE)
        if [x, y] not in coordinates:
            messageText = 'WHIRLPOOL ALERT - Location - X:' + str(x) + ' | Y:' + str(y)

            imagePath = draw_red_circle_on_map("./5120_4096_Map.png", x, y, f"{x},{y}")

            postDiscordMessageWithImage(messageText, imagePath)

            print("Sextant Coordinates:")
            print(f"NS: {degNS}° {minNS}' {dirNS}, WE: {degWE}° {minWE}' {dirWE}")
            print(f"World Coordinates: X = {x}, Y = {y}")
            coordinates.append([x, y])
