'''
Created on 05/09/2011

@author: Robin Chow
'''

import os, logging
import argparse
import ConfigParser
import glob

# global variables
cfgFile = ''
config = {}

def initLogging(baseFilename, args):
    # setting up logging to file
    logFile = '%s.log' % baseFilename
    loglevelNumeric = getattr(logging, args.loglevel.upper(), None)
    if not isinstance(loglevelNumeric, int):
        loglevelNumeric = logging.WARNING
    logging.basicConfig(filename=logFile,level=loglevelNumeric,format='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S%p')

    # setting up logging to console
    logConsole = logging.StreamHandler()
    logConsole.setLevel(loglevelNumeric);
    logConsole.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%I:%M:%S%p'))
    logging.getLogger().addHandler(logConsole)

def getBaseFilename():
    (path, filename) = os.path.split(__file__)
    (baseFilename, _) = os.path.splitext(filename)
    return baseFilename

def parseConfig(filename):
    global config

    cfg = ConfigParser.RawConfigParser()
    cfg.read(filename)
    
    config['dirNum'] = cfg.getint('Directories', 'Number')
    
    config['directories'] = []
    for i in range(config['dirNum']):
        config['directories'].append(cfg.get('Directories', str(i)))

    logging.debug('config: %s' % config)

if __name__ == '__main__':
    global config

    baseFilename = getBaseFilename()
    cfgFile = '%s.cfg' % baseFilename

    parser = argparse.ArgumentParser(description="Auto File Processing Service")
    parser.add_argument('--loglevel', choices=['DEBUG','INFO','WARNING','ERROR','CRITICAL'], default='WARNING')
    args = parser.parse_args()
    
    initLogging(baseFilename, args)
    parseConfig(cfgFile)
    
    # get list of directories to scan
    metafile = 'aphistory.txt'
    for directory in config['directories']:
        os.path.join(directory, metafile)
        pass
    # in each directory, there should be a file that gives the previous list of files and update times
    # using that list, derive the list of files to process
    # from config, run the necessary script/exe/function on the list of files