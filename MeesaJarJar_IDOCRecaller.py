# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description: 
# Meesa Jar Jar - PRIVATE SCRIPT - DO NOT SHARE
# If yousa have this, and Jar Jar didnt give it to you directly, yousa in BIG doo doo.
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#


# END CONFIG --------------------------------------------------#

import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

emailToSendAlertTo = "user@domain.com"

def sendEmailAlert():
    try:
    # Email details
        from_email = "meesajarjaruo@gmail.com"

        subject = "IDOC HOUSE ALERT"
        body = "The house you were looking at has gone IDOC FYI"

        # Create the email
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = emailToSendAlertTo
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # SMTP server configuration
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        password = "wscb kvfj cezq euan"  # Use the App Password if 2FA is enabled

        # Send the email
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, to_email, msg.as_string())
            server.quit()
            print("Email sent successfully!")
        except Exception as e:
            print(f"Failed to send email: {e}")
    except:
        print("GENERAL ERROR - TELL JAR JAR!")


def hide():
    if Player.Visible == True:
        Player.UseSkill('Hiding')
        
sign = Target.PromptTarget('Select House Sign to Track:',0)

while Player.Connected == True:
    Player.HeadMessage(0,"Going to Greatly 1.")
    Player.ChatSay('[recall greatly1')
    Misc.Pause(6000)
    signToCheck = Items.FindBySerial(sign)
    Items.WaitForProps(signToCheck,1000)
    idocFound = False
    if 'danger' in str(signToCheck.Properties).lower():
        idocFound = True
        Player.HeadMessage(0,"IT WENT IDOC OMG YAY!")
        sendEmailAlert()
        Misc.Pause(650)
        
    Player.HeadMessage(0,"Going Home.")
    Player.ChatSay('[recall home')
    Misc.Pause(3500)
    Player.PathFindTo(2132,3453,0)
    Misc.Pause(5000)
    Player.PathFindTo(2142,3450,0)
    Misc.Pause(5000)
    Player.PathFindTo(2143,3439,2)
    Misc.Pause(5000)    
    hide()
    if Player.Position.X == 2143 and Player.Position.Y == 3439:
        print("Reached Home Safe Inside Spot.")
        
        if idocFound == True:
            for z in range(0, 30):
                    
                print("IDOC DETECTED - WARNING")
                Misc.Beep()
                Misc.Pause(1000)
    else:
        print("ERROR - DID NOT REACH SAFE SPOT!")
        Misc.Beep()
        Misc.Pause(1000)
        Misc.Beep()
        Misc.Pause(1000)
        Misc.Beep()
        print("STOPPING SCRIPT!")
        sys.exit()
        
    for z in range(0,5):
        hide()
        Misc.Pause(1000 * 60)
    
    