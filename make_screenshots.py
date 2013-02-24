#!/usr/bin/python
#Usage: python make_screenshots.py /path/to/screenshot/output
#This script will create the output directory if necessary.
#Set

import os
import sys
import subprocess
import glob

###
# Customize these variables for your own project
###

#languages to create screenshots for
languages = ['en', 'de']

#devices to use - available device names are in the iOS Simulator under Hardware -> Device, such as iPad or iPad (Retina)
devices = ['"iPhone (Retina 3.5-inch)"', '"iPhone (Retina 4-inch)"']

project_path = os.path.join(os.path.realpath(os.path.split(__file__)[0]), 'Example') #Path to the Xcode project's enclosing directory
target_name = 'KSScreenshotManagerExample' #Xcode target name
app_name = 'KSScreenshotManagerExample.app' #Product name in build directory

destination_path = os.path.abspath(sys.argv[1]) #Path to save the screenshots, don't change this if you pass the path in through the arguments

###

def compile_waxsim():
    previous_dir = os.getcwd()
    os.chdir(os.path.join(os.path.realpath(os.path.split(__file__)[0]), 'Contributed', 'WaxSim'))
    subprocess.call(['xcodebuild', '-target', 'WaxSim', '-configuration', 'Release', 'SYMROOT=build'], stdout=open('/dev/null', 'w'))
    os.chdir(previous_dir)

def compile_app():
    previous_dir = os.getcwd()
    os.chdir(project_path)
    subprocess.call(['xcodebuild', '-target', target_name, '-configuration', 'Screenshots', '-sdk', 'iphonesimulator', 'SYMROOT=build'], stdout=open('/dev/null', 'w'))
    os.chdir(previous_dir)

def quit_simulator():
    subprocess.call(['killall', 'iPhone Simulator'])

def set_device(device):
    subprocess.call(['defaults', 'write', 'com.apple.iphonesimulator', 'SimulateDevice', device])

def waxsim(app_path, args):
    waxsim_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'Contributed', 'WaxSim', 'build', 'Release', 'waxsim')
    subprocess_args = [waxsim_path, app_path]
    subprocess_args += args
    
    subprocess.call(subprocess_args)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: make_screenshots.py screenshots-path'
        exit()
    
    app_path = os.path.join(project_path, 'build', 'Screenshots-iphonesimulator', app_name)
    
    print 'Building with Screenshots configuration...'
    compile_app()
    
    print 'Building WaxSim...'
    compile_waxsim()
    
    #create destination directory
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
        
    for device in devices:
        quit_simulator()
        set_device(device)
        
        for language in languages:
            waxsim(app_path, ['-AppleLanguages', '({})'.format(language), '-AppleLocale', language, destination_path])
    
    quit_simulator()
