import re
import random
import clr
import os
import System
import pickle
import math
os.chdir("C:/Program Files (x86)/UOForever/UO/Forever")
clr.AddReference('System')
from System.Diagnostics import Process, ProcessStartInfo
from subprocess import Popen, CREATE_NEW_CONSOLE
clr.AddReference("System.Drawing")
from System.Collections.Generic import List
from System import Int32 as int

def updateAllScripts():
    # Print the current working directory
    print("Current working directory:", os.getcwd())

    # Path to your .bat file
    bat_file_path = "./RazorEnhanced/Scripts/YousaPlaceThisFileInYourScriptsFolderAndDoubleClickItForMeesaScripts.bat"

    # Ensure the path is correct
    bat_file_path = os.path.abspath(bat_file_path)
    print("Absolute path to .bat file:", bat_file_path)

    # Start the process with a new console window
    process = Popen(bat_file_path, shell=True, creationflags=CREATE_NEW_CONSOLE)
    process.wait()
    print("Finished Updating Files, restarting Runebook Atlas now.")
    
def stopScript(script):
        
    if Misc.ScriptStatus(script) == True:
        Misc.ScriptStop(script)
        
        
def startScript(script):
        
    if Misc.ScriptStatus(script) == False:
        print("STARTING SCRIPT: ", script)
        Misc.ScriptRun(script)
        
print("STOPPING ALL MEESA SCRIPTS FOR UPDATE")

scripts = [
"MeesaJarJar_RunebookAtlas.py",
"MeesaJarJar_RuneBookAtlas_Map.py", 
"MeesaJarJar_RuneBookAtlas_Sextant.py"]

for script in scripts:
    stopScript(script)
    
updateAllScripts()

Misc.Pause(1000)
startScript(scripts[0])
print("YOUSA FINISHED DA UPDATING!")
Player.HeadMessage(0,"YOUSA FINISHED DA UPDATING! STARTING DA ATLAS AGAIN!")
    