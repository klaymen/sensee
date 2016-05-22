'''
sensee utils library for general functions

'''

import os
import re

import ConfigParser
from lib.conf import *

config = ConfigParser.ConfigParser()
config.read( CONFIG_FILE ) 

def getFolders(path):
    '''
    return a list if direct non-hidden subdirectories of a path
    '''
    if os.path.lexists(path):
        return [name for name in os.listdir( path )
            if os.path.isdir( os.path.join( path, name ) ) and name[0] != '.' ]
    else:
        return 0

def getFiles(path):
    '''
    return a list if direct non-hidden subdirectories of a path
    '''
    if os.path.lexists(path):
        return [name for name in os.listdir( path )
            if os.path.isfile( os.path.join( path, name ) ) and name[0] != '.' ]
    else:
        return 0

def httpStatus(code):
    '''
    return status dictionary
    '''
    #200 - ok
    #400 - error parsing post data

    return { 'code' : code,
             'description' : CODE[code]
           }

