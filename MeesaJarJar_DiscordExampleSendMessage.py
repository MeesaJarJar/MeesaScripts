# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description: Simple example of how to use URLLib using RE
# to send a message on a discord server via webhook. You must
# get a web hook url from your discord server and set it below.
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#
webhook_url = "https://discord.com/api/webhooks/527776638/rklOjnEC_Jv452379pDWqqmuKioi4xOvYhxB8K4BjAjq54c--csSWNSKdvT1GRkDc"
# END CONFIG --------------------------------------------------#

import json
import urllib.request

def postDiscordMessage(message):
    

    data = {
        "content": message
    }
    data = json.dumps(data).encode('utf-8')
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    req = urllib.request.Request(url=webhook_url, data=data, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 204:
                print("Message sent successfully.")
            else:
                print(f"Failed to send the message. Status Code: {response.status}")
                print(f"Response: {response.read().decode('utf-8')}")
    except urllib.error.HTTPError as e:
        print(f"Failed to send the message. Status Code: {e.code}")
        print(f"Response: {e.read().decode('utf-8')}")
    except urllib.error.URLError as e:
        print(f"Failed to send the message. Reason: {e.reason}")


postDiscordMessage("Meesa Testing, Okey day?")
