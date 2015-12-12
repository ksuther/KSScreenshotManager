#!/usr/bin/env python
# Usage: python make_screenshots.py /path/to/screenshot/output
# This script will create the output directory if necessary.

import os
import sys
import time
import subprocess
import glob
import argparse
import json
import shutil

def compile_app():
    previous_dir = os.getcwd()
    os.chdir(project_path)
    
    # This is specifying -destination instead of -sdk iphonesimulator to ensure that this works with apps that have Watch apps
    # By default this script uses an iPhone 4s as the destination so that the 32-bit version gets built (which will run on all devices)
    # The destination can be configured in the options json
    if 'scheme_name' in options:
        arguments = ['xcrun', 'xcodebuild', '-scheme', options['scheme_name'], '-configuration', options['build_config'], '-destination', options['build_destination'], '-derivedDataPath', 'build', 'clean', 'build']
    else:
        arguments = ['xcrun', 'xcodebuild', '-target', options['target_name'], '-configuration', options['build_config'], '-destination', options['build_destination'], 'clean', 'build', 'SYMROOT=build']
    
    if 'skip_clean' in options and options['skip_clean']:
        # Don't clean the build before building and running
        arguments.remove('clean')
    
    print "Recompiling app: %s" % arguments
    subprocess.call(arguments, stdout=open('/dev/null', 'w'))
    os.chdir(previous_dir)

def quit_simulator():
    subprocess.call(['killall', 'Simulator'])

def reset_simulator():
    shutil.rmtree(os.path.expanduser('~/Library/Application Support/iPhone Simulator'), ignore_errors=True)

def start_simulator(device, app_path):
    subprocess.call(['xcrun', 'instruments', '-w', "%s (%s)" % (device, options['ios_version'])])
    subprocess.call(['xcrun', 'simctl', 'install', device, app_path])
    print "Installed app %s on device %s" % (app_path, device)

def simctl(device, app, args, output_path):
    subprocess_args = ['xcrun', 'simctl', 'launch', device, app]
    subprocess_args += args
    subprocess_args += [output_path]

    status = output_path + "/.screenshots.tmp"
    if os.path.isfile(status):
        os.remove(status) # Start from clean slate
    
    print "Launching app in simulator: %s" % subprocess_args
    subprocess.call(subprocess_args)
    print "Simulator launched, waiting for app to start..."
    # Wait for .screenshots.tmp file to appear
    while not os.path.isfile(status):
        time.sleep(1)
    print "Got it, now waiting for app to complete."
    while os.path.isfile(status):
        time.sleep(1)
    print "Complete!"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Build iOS screenshots.')
    parser.add_argument('--skip-clean', '-s', action='store_true', help='skip clean when calling xcodebuild')
    parser.add_argument('--path', '-p', dest='destination', help='destination path for screenshots (overrides config)')
    parser.add_argument('--device', '-d', dest='device_name', help='Run on a single device, ignoring config')
    parser.add_argument('--lang', '-l', dest='language', help='Run for a specific locale, ignoring config')
    parser.add_argument('config', help='path to JSON config file', default='config.json', nargs='?')

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

    if args.skip_clean:
        options['skip_clean'] = True

    if args.device_name:
        options['device_names'] = [args.device_name]

    if args.language:
        options['languages'] = [args.language]

    ###
    
    if os.path.isabs(options['project_path']):
        project_path = options['project_path']
    else:
        # project_path is relative to the parent directory of config_path
        project_path = os.path.realpath(os.path.join(os.path.dirname(config_path), options['project_path']))

    print 'Project path is ' + project_path

    if 'scheme_name' in options:
        app_path = os.path.join(project_path, 'build', 'Build', 'Products', options['build_config'] + '-iphonesimulator', options['app_name'])
    else:
        app_path = os.path.join(project_path, 'build', options['build_config'] + '-iphonesimulator', options['app_name'])

    if 'build_destination' not in options:
        # no destination was specified, assume we're building for an iPhone 4s so that we end up with a 32-bit binary that will run everywhere
        options['build_destination'] = 'name=iPhone 4s'

    print 'Building with ' + options['build_config'] + ' configuration...'
    compile_app()
    
    # create destination directory
    if not os.path.exists(options['destination_path']):
        os.makedirs(options['destination_path'])
        
    for device in options['device_names']:
        start_simulator(device, app_path)
        
        for language in options['languages']:
            language_path = os.path.join(options['destination_path'], language)
            if not os.path.exists(language_path):
                os.makedirs(language_path)
            
            print 'Creating screenshots for {} using {}...'.format(language, device)
            
            if 'reset_between_runs' in options and options['reset_between_runs']:
                quit_simulator()
                reset_simulator()

            simctl(device, options['app_id'], ['-AppleLanguages', '({})'.format(language), '-AppleLocale', language], language_path)

    quit_simulator()
