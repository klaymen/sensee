'''
sensee errorlog module

'''
module = 'errorlog'

import sys
import pickle
import ConfigParser
from subprocess import check_output

sys.path.append('../../')

import lib.utils    as utils
import lib.logger   as logger
import lib.cache    as cache
from   lib.conf import *

config = ConfigParser.ConfigParser()
config.read( CONFIG_FILE )

try:
    LIBPATH         = config.get( 'general', 'LIBPATH' )
    ENABLECACHING   = config.get( 'cache', 'ENABLECACHING' )
    INSTALLPATH     = config.get( 'general', 'INSTALLPATH' )
except IOError as eIO:
    print( 'error during processing config file: \'%s\'' % eIO )
    sys.exit(1)


FILTERS = [ 'html']
DEFAULTFILTER = FILTERS[0]

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
            f.seek(fsize-bufsize*iter)
            data.extend(f.readlines())
            if len(data) >= lines or f.tell() == 0:
                content = data[-lines:]
                break
    return content

def buildData(data):
    '''
    build data to cache
    '''

    return tail('/var/log/apache2/error.log')    
    
def buildHtml(data):
    '''
    Build html page based on data if necessary
    '''

    return '<br />'.join(data)

def content(
        userName        = '',
        accessLevel     = '',
        newUrl          = '',
        command         = '',
        queryString     = '',
        postData        = '',
        cookies         = '',
        uploadFile      = ''
        ):
    '''
    What this module does?
    '''

    #==> extracting keys from queryString
    #==> key = utils.getKey( queryString )

    cacheFile = cache.cacheFile( '_____', module ) # ==> cache.cacheFile( key, module )


    # searching for cached data
    noCache = 0
    data    = ''

    if ENABLECACHING is 1:
        # valid cache found
        # loading data from cache

        try:
            cacheStream = open ( cacheFile, 'r')
            data = pickle.load( cacheStream )
            cacheStream.close ()
        except IOError:
            logger.error( 'failed to load cacheFile: \'%s\'' % cacheFile )
            noCache = 1 #Needs to load data
    else:
        noCache = 1 #Needs to load data

    if len(data) is 0:
        noCache = 1

    if noCache:
        # no or out-of date cache, building new one
        data = buildData(1)
        
        # creating cache
        if ENABLECACHING is 1:
            try:
                cacheStream = open ( cacheFile, 'w')
                pickle.dump( data, cacheStream )
                cacheStream.close()
            except IOError:
                logger.error( 'failed to save cacheFile: \'%s\'' % cacheFile )

    returnStatus = "200 OK"

    cnt = buildHtml(data)
    
    responseHeaders = [ ( "Content-Type", CONTENT_HTML ),
                        ( "Content-Length", str( len( cnt ) ) ) ]

    return responseHeaders, returnStatus, cnt
