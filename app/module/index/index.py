'''
sensee index module

'''

import sys
import pickle
import ConfigParser


sys.path.append('../../')

import lib.utils    as utils
import lib.logger   as logger
import lib.templates as template
import lib.cache    as cache
from   lib.conf import *

config = ConfigParser.ConfigParser()
config.read( CONFIG_FILE )

try:
    LIBPATH         = config.get( 'general', 'LIBPATH' )
    ENABLECACHING   = config.get( 'cache', 'ENABLECACHING' )
except IOError as eIO:
    print( 'error during processing config file: \'%s\'' % eIO )
    sys.exit(1)

FILTERS = [ 'html', 'pdf', 'xls', 'csv', 'xlsx' ]
DEFAULTFILTER = FILTERS[0]

#Get module's name from __file__
module = os.path.splitext(os.path.basename(__file__))[0]

MODULEPATH = os.path.join( LIBPATH, 'module', module )
TEMPLATEDIR = os.path.join( MODULEPATH, 'templates/html')

def buildData(userName):
    '''
    build data to cache
    '''
    return userName

def buildHtml(data):
    '''
    Build html page based on data if necessary
    '''
    return template.read( TEMPLATEDIR, 'page') % {
            'content'       :   data
            }

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
        data = buildData(userName) #==> To be replaced with a specific call
        # creating cache
        if ENABLECACHING is 1:
            try:
                cacheStream = open ( cacheFile, 'w')
                pickle.dump( data, cacheStream )
                cacheStream.close()
            except IOError:
                logger.error( 'failed to save cacheFile: \'%s\'' % cacheFile )

    returnStatus = "200 OK"
    
    #==> build content using the selected filter
    cnt = buildHtml(data)
    
    responseHeaders = [ ( "Content-Type", CONTENT_HTML ),
                        ( "Content-Length", str( len( cnt ) ) ) ]

    return responseHeaders, returnStatus, cnt
