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
import re
import errno

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
    
    print "Building app: %s" % ' '.join(arguments)
    subprocess.call(arguments, stdout=open('/dev/null', 'w'))
    os.chdir(previous_dir)

def quit_simulator():
    subprocess.call(['killall', 'Simulator'])

def reset_simulator():
    shutil.rmtree(os.path.expanduser('~/Library/Application Support/iPhone Simulator'), ignore_errors=True)

def start_simulator(device, app_path):
    subprocess.call(['xcrun', 'instruments', '-w', "%s" % (device)])
    subprocess.call(['xcrun', 'simctl', 'install', device, app_path])
    print "Installed app %s on device %s" % (app_path, device)

def is_running(pid):
    try:
        os.kill(pid, 0)
    except OSError as err:
        if err.errno == errno.ESRCH:
            return False
    return True

def get_simulators():
    output = subprocess.check_output(['xcrun', 'instruments', '-s', 'devices'], close_fds=True)
    simulators = []

    for line in output.split('\n'):
        #result = re.match('([\w ]+) \(([\d.]+)\) \[([A-Z0-9-])\]', line)
        result = re.match('(.+) \(([\d.]+)\) \[([A-Z0-9-]+)\]', line)

        if result:
            simulators.append((result.group(1), result.group(2), result.group(3)))

    return simulators

def simctl(device, app, args, output_path):
    subprocess_args = ['xcrun', 'simctl', 'launch', device, app]
    subprocess_args += args
    subprocess_args += [output_path]

    print "Launching app in simulator: %s" % ' '.join(subprocess_args)

    launch_output = subprocess.check_output(subprocess_args)
    launch_pid = int(re.search(': (\d+)$', launch_output).group(1))

    while is_running(launch_pid):
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

    compile_app()
    
    # create destination directory
    if not os.path.exists(options['destination_path']):
        os.makedirs(options['destination_path'])

    # sort simulators by version (this ensures we take the latest iOS version if ios_version isn't specified)
    simulators = sorted(get_simulators(), key=lambda x: x[1], reverse=True)

    for device in options['device_names']:
        # find the simulator UUID for the specified device
        for next_simulator in simulators:
            if next_simulator[0] == device and ('ios_version' not in options or ('ios_version' in options and next_simulator[1] == options['ios_version'])):
                device_uuid = next_simulator[2]
                break

        start_simulator(device_uuid, app_path)
        
        for language in options['languages']:
            language_path = os.path.join(options['destination_path'], language)
            if not os.path.exists(language_path):
                os.makedirs(language_path)
            
            print 'Creating screenshots for {} using {}...'.format(language, device)
            
            if 'reset_between_runs' in options and options['reset_between_runs']:
                quit_simulator()
                reset_simulator()

            simctl(device, options['bundle_id'], ['-AppleLanguages', '({})'.format(language), '-AppleLocale', language], language_path)

    quit_simulator()
