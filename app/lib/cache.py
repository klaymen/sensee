'''
sensee cache handler library

'''

import sys
import os
import subprocess
import shlex

from   lib.conf import *
import lib.logger as logger
import ConfigParser

config = ConfigParser.ConfigParser()
config.read( CONFIG_FILE )

try:
    ENABLECACHING         = config.get( "cache", "ENABLECACHING" )
    CACHEDIR              = config.get( "cache", "CACHEDIR" )
except StandardError as e:
    print( "error during processing config file: \'%s\'" % e )
    sys.exit(1)


def findLatestDate( path ):
    '''
    Finds the latest date of modify of any file in a directory structure
    '''

    logger.debug( "finding latest file mtime in %s" % path )
    if not str(ENABLECACHING).lower() in [ 'true', '1', 'on', 'enabled' ]:
        logger.debug( "caching is disabled in the configuration file" )
        return -1
    if not os.path.exists( path ):
        logger.error( "failed to determinate last modified date; path \'%s\' does not exist" % path )
        return -1
    out = subprocess.Popen( shlex.split("find %s -type f -printf \"%%T@\n\"" % path ), stdout = subprocess.PIPE ).communicate()[0]
    maxd = -1
    for i in out.split('\n'):
        if i.strip() and float(i) > maxd:
            maxd = float(i)
    return maxd

def fileDate( filePath ):
    '''
    returns the mtime of the file
    '''
    if not os.path.exists( filePath ):
        logger.error( "failed to determinate last modified date; path \'%s\' does not exist" % filePath )
        return -1
    return float( os.path.getmtime( filePath ) )

def cacheFile( base, module ):
    '''
    returns the module's cache file name
    '''
    return os.path.join( CACHEDIR, base.strip('/').replace('/', '_') + '_' + module + '.dump' )

