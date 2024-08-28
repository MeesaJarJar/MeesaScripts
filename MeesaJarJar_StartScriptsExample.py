# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! ------------#
# -------------------------------------------------------------#
# Description: Script Starter - Example Script
# Check if a list of scripts are running, if not start em!
# These scripts MUST BE ADDED manually to the Scripting tab of RE.
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#
scripts = ['mynameofscript.py', 'nameofotherscript.py']
# END CONFIG --------------------------------------------------#


for scriptFileName in scripts:
    if Misc.ScriptStatus(scriptFileName) == False:
        Misc.ScriptRun(scriptFileName)