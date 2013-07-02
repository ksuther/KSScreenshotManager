#!/usr/bin/python
#Usage: python make_screenshots.py /path/to/screenshot/output
#This script will create the output directory if necessary.
#Set

import os
import sys
import subprocess
import glob
import json

def compile_waxsim():
    previous_dir = os.getcwd()
    os.chdir(os.path.join(os.path.realpath(os.path.split(__file__)[0]), 'Contributed', 'WaxSim'))
    subprocess.call(['xcodebuild', '-target', 'WaxSim', '-configuration', 'Release', 'SYMROOT=build'], stdout=open('/dev/null', 'w'))
    os.chdir(previous_dir)

def compile_app():
    previous_dir = os.getcwd()
    os.chdir(options['project_path'])
    subprocess.call(['xcodebuild', '-target', options['target_name'], '-configuration', options['build_config'], '-sdk', 'iphonesimulator', 'SYMROOT=build'], stdout=open('/dev/null', 'w'))
    os.chdir(previous_dir)

def quit_simulator():
    subprocess.call(['killall', 'iPhone Simulator'])

def set_device(device):
    subprocess.call(['defaults', 'write', 'com.apple.iphonesimulator', 'SimulateDevice', device])

def waxsim(app_path, args, device):
    waxsim_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'Contributed', 'WaxSim', 'build', 'Release', 'waxsim')
    subprocess_args = [waxsim_path]
    
    if 'iPad' in device:
        subprocess_args += ['-f', 'ipad']  
    
    subprocess_args += [app_path]    
    subprocess_args += args
    
    subprocess.call(subprocess_args)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: make_screenshots.py config-file-path'
        exit()

    ###
    # Read in configuration file
    ###

    try:
        options = json.load(open(sys.argv[1]))
    except IOError:
        print 'Configuration file not found at ' + sys.argv[1]
        exit()
    except ValueError:
        print "Syntax error in JSON file."
        exit()

    ###
    
    app_path = os.path.join(options['project_path'], 'build', options['build_config'] + '-iphonesimulator', options['app_name'])
    
    print 'Building with ' + options['build_config'] + ' configuration...'
    compile_app()
    
    print 'Building WaxSim...'
    compile_waxsim()
    
    #create destination directory
    if not os.path.exists(options['destination_path']):
        os.makedirs(options['destination_path'])
        
    for device in options['devices']:
        quit_simulator()
        set_device(device)
        
        for language in options['languages']:
            language_path = os.path.join(options['destination_path'], language)
            if not os.path.exists(language_path):
                os.makedirs(language_path)

            waxsim(app_path, ['-AppleLanguages', '({})'.format(language), '-AppleLocale', language, language_path], device)

    quit_simulator()
