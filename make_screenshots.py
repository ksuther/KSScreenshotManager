#!/usr/bin/python
# Usage: python make_screenshots.py /path/to/screenshot/output
# This script will create the output directory if necessary.

import os
import sys
import subprocess
import glob
import argparse
import json

def compile_iossim():
    previous_dir = os.getcwd()
    os.chdir(os.path.join(os.path.realpath(os.path.split(__file__)[0]), 'Contributed', 'ios-sim'))
    subprocess.call(['xcodebuild', '-scheme', 'ios-sim', '-configuration', 'Release', 'clean', 'build', 'SYMROOT=build'], stdout=open('/dev/null', 'w'))
    os.chdir(previous_dir)

def compile_app():
    previous_dir = os.getcwd()
    os.chdir(project_path)
    
    # Force the simulator build to use 32-bit, otherwise UIGetScreenImage doesn't exist
    subprocess.call(['xcodebuild', '-target', options['target_name'], '-configuration', options['build_config'], '-sdk', 'iphonesimulator', 'clean', 'build', 'SYMROOT=build', 'ARCHS=i386', 'ONLY_ACTIVE_ARCH=NO'], stdout=open('/dev/null', 'w'))
    os.chdir(previous_dir)

def quit_simulator():
    subprocess.call(['killall', 'iPhone Simulator'])

def iossim(app_path, args, device):
    iossim_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'Contributed', 'ios-sim', 'build', 'Release', 'ios-sim')
    subprocess_args = [iossim_path]

    subprocess_args += ['launch', app_path]

    # ios-sim does the default setting itself, so convert the device name into arguments that ios-sim expects
    if 'iPad' in device:
        subprocess_args += ['--family', 'ipad']
    if 'iPad Retina' in device:
        subprocess_args += ['--family', 'ipad', '--retina']
    elif 'iPhone Retina (3.5-inch)' in device:
        subprocess_args += ['--family', 'iphone', '--retina']
    elif 'iPhone Retina (4-inch)' in device:
        subprocess_args += ['--family', 'iphone', '--retina', '--tall']

    subprocess_args += ['--args']
    subprocess_args += args
    
    subprocess.call(subprocess_args)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Build iOS screenshots.')
    parser.add_argument('--path', '-p', dest='destination', help='destination path for screenshots (overrides config)')
    parser.add_argument('config', help='path to JSON config file')

    args = parser.parse_args()
    config_path = args.config

    ###
    # Read in configuration file
    ###

    try:
        options = json.load(open(config_path))
    except IOError:
        print 'Configuration file not found at ' + config_path
        exit()
    except ValueError:
        print "Syntax error in JSON file."
        exit()

    if args.destination:
        options['destination_path'] = args.destination

    ###
    
    if os.path.isabs(options['project_path']):
        project_path = options['project_path']
    else:
        # project_path is relative to the parent directory of config_path
        project_path = os.path.realpath(os.path.join(os.path.dirname(config_path), options['project_path']))
    
    app_path = os.path.join(project_path, 'build', options['build_config'] + '-iphonesimulator', options['app_name'])
    
    print 'Building with ' + options['build_config'] + ' configuration...'
    compile_app()
    
    
    print 'Building ios-sim...'
    compile_iossim()
    # create destination directory
    if not os.path.exists(options['destination_path']):
        os.makedirs(options['destination_path'])
        
    for device in options['devices']:
        quit_simulator()
        
        for language in options['languages']:
            language_path = os.path.join(options['destination_path'], language)
            if not os.path.exists(language_path):
                os.makedirs(language_path)
            
            print 'Creating screenshots for {} using {}...'.format(language, device)
            
            iossim(app_path, ['-AppleLanguages', '({})'.format(language), '-AppleLocale', language, language_path], device)

    quit_simulator()
