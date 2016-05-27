'''
sensee logger library

'''

import os
import datetime
import ConfigParser
import lib.utils as utils
from lib.conf import *

config = ConfigParser.ConfigParser()
config.read(CONFIG_FILE)
LOGFILE = config.get( "general", "LOGFILE" )

LOGLEVELS = [ "none", "error", "warning", "info", "debug" ]
LOGLEVEL = str( config.get( "general", "LOGLEVEL" ) ).lower()

LOGLEVEL = LOGLEVELS.index( LOGLEVEL ) if LOGLEVEL in LOGLEVELS else LOGLEVELS.index( "debug" )

def read(lines = 40):
    try:
        return utils.tail(LOGFILE, lines)
    except:
        return "The log file is empty."

def write( prefix, message ):
    '''
    Write message to the specified logfile
    '''

    if not os.path.isfile(LOGFILE):
        with open(LOGFILE, 'w') as logFileObject:
            os.chmod(LOGFILE, 0o666)
    try: 
        logFileObject = open( LOGFILE, "a" )
    except StandardError:
        return -1
    logFileObject.write( "%s |%s| %s\n" % (datetime.datetime.now().isoformat(), prefix, message) )
    logFileObject.flush()
    logFileObject.close()

    return 0

def warning( message ):
    '''
    If log level is appropriate write warning message to the specified logfile
    '''
    if LOGLEVEL >= LOGLEVELS.index( "warning" ):
        return write( 'WW', message )
    else:
        return 0

def error( message ):
    '''
    If log level is appropriate write error message to the specified logfile
    '''
    if LOGLEVEL >= LOGLEVELS.index( "error" ):
        return write( 'EE', message )
    else:
        return 0

def info( message ):
    '''
    If log level is appropriate write info message to the specified logfile
    '''
    if LOGLEVEL >= LOGLEVELS.index( "info" ):
        return write( 'II', message )
    else:
        return 0

def debug( message ):
    '''
    If log level is appropriate write debug message to the specified logfile
    '''
    if LOGLEVEL >= LOGLEVELS.index( "debug" ):
        return write( 'DD', message )
    else:
        return 0
