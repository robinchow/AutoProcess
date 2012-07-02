'''
Created on 05/09/2011

@author: Robin Chow
'''

import os, logging
import argparse
import ConfigParser
import glob
import json

# global variables
cfgFile = ''
config = {}
processingList = []
CONFIG_FILENAME = "directory_attributes.json"

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

def getValidFilesToProcess(basedir):
    fileList= []
    print "Listing directory contents"
    for filename in os.listdir(basedir):
        fullpath = os.path.join(basedir,filename)
        if os.path.isfile(fullpath):
            if filename != CONFIG_FILENAME:
                fileList.append(filename)
    return fileList


# Create an empty JSON file associated with this directory
def processFreshDir(basedir):
    print "Process fresh dir: %s" % basedir
    print "File did not exist"
    

    # List contents of directory
    fileList = getValidFilesToProcess(basedir)
    fileDictList = {}
    for s in fileList:
        element = {}
        element["filename"] = s;
        element["lastUpdated"] = 0
        fileDictList[s] = element

    s = json.dumps(fileDictList,ensure_ascii=False)
    FILE = open(fullfilepath,"w")
    FILE.write(s+"\n")
    FILE.close()
    



def processDir(basedir):
    print "Process dir: %s" % basedir

    jsonFile = os.path.join(basedir,CONFIG_FILENAME)
    FILE = open(jsonFile,"r")
    jsonString = FILE.read()

    print "JsonString: "
    print jsonString

    fileDictList = json.loads(jsonString)
    print "Parsed Json:"
    print fileDictList


    # List contents of directory
    fileList = getValidFilesToProcess(basedir)
    for f in fileList:
        # Get full path of file
        fullPath = os.path.join(basedir,f)
        modifiedTime = os.path.getmtime(fullPath)
        print "Modified time of %s is %d" % (f,modifiedTime)
        
        if f in fileDictList:
            element = fileDictList[f]
            print "This element was last updated at: %d" % element["lastUpdated"]
            lastUpdated = element["lastUpdated"]
            
            if modifiedTime > lastUpdated :
                print "We should process %s" % f
                processingList.append(fullPath)
                element["lastUpdated"] = modifiedTime
        else:
            # File was not already in list
            processingList.append(fullPath)
            element = {}
            element["filename"] = f;
            element["lastUpdated"] = 0
            fileDictList[f] = element
            

    print fileList
    print fileDictList
    print processingList

    s = json.dumps(fileDictList,ensure_ascii=False)
    FILE = open(fullfilepath,"w")
    FILE.write(s+"\n")
    FILE.close()

if __name__ == '__main__':
    global config
    print "Hello"
    baseFilename = getBaseFilename()
    cfgFile = '%s.cfg' % baseFilename

    parser = argparse.ArgumentParser(description="Auto File Processing Service")
    parser.add_argument('--loglevel', choices=['DEBUG','INFO','WARNING','ERROR','CRITICAL'], default='WARNING')
    args = parser.parse_args()
    
    initLogging(baseFilename, args)
    parseConfig(cfgFile)
    
    # get list of directories to scan
    metafile = CONFIG_FILENAME

    print "Directories:"
    print config['directories']
    
    for directory in config['directories']:
        fullfilepath = os.path.join(directory, metafile)
        if os.path.exists(fullfilepath):
            processDir(directory)
        else:
            processFreshDir(directory)
            
        pass
    # in each directory, there should be a file that gives the previous list of files and update times
    # using that list, derive the list of files to process
    # from config, run the necessary script/exe/function on the list of files
