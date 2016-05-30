'''
sensee utils library for general functions

'''

import os
import re

import ConfigParser
from lib.conf import *

config = ConfigParser.ConfigParser()
config.read( CONFIG_FILE ) 

try:
    USERLIST = config.get( 'authentication' , 'UserList' )

except IOError as eIO:
    print( 'error during processing config file: \'%s\'' % eIO )
    sys.exit(1)

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

def tail(file, lines = 40):
    bufsize = 8192

    fsize = os.stat(file).st_size

    iter = 0
    
    content = []
    
    with open(file) as f:
        if bufsize > fsize:
            bufsize = fsize-1
        data = []
        while True:
            iter +=1
            try:
                f.seek(fsize-bufsize*iter)
            except IOError:
                f.seek(0)
                content = f.readlines()
                break
            data.extend(f.readlines())
            if len(data) >= lines or f.tell() == 0:
                content = data[-lines:]
                break
    return content
    
def getUsers( ):
    '''
    returns the list of the users from file
    '''

    UserListFile = open( USERLIST, 'r' )

    users = {}

    try:
        for i in UserListFile:
            users[i.strip().split()[0]] = i.strip().split()[1]
    except StandardError:
        UserListFile.close()
        return 0

    UserListFile.close()
    return users