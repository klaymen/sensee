'''

default module

'''

import sys
import ConfigParser
import urllib

sys.path.append('../../')

import lib.utils     as utils
import lib.templates as template
from   lib.conf import *

config = ConfigParser.ConfigParser()
config.read( CONFIG_FILE )

try:
    LIBPATH         = config.get( 'general', 'LIBPATH' )
    ENABLECACHING   = config.get( 'cache', 'ENABLECACHING' )
except IOError as eIO:
    print( 'error during processing config file: \'%s\'' % eIO )
    sys.exit(1)

FILTERS = [ 'html', 'json', ]
DEFAULTFILTER = FILTERS[0]

#Get module's name from __file__
module = os.path.splitext(os.path.basename(__file__))[0]

MODULEPATH = os.path.join( LIBPATH, 'module', module )
TEMPLATEDIR = os.path.join( MODULEPATH, 'templates/html')

def buildHtml( status, queryString ):
    '''
    Build html page based on data if necessary
    '''

    errorString = "General error. I don't know how could that happen."
    errors = {
            'invalid_credentials'   :   'invalid login credentilas supplied',
            }
    if status.lower() in errors:
        errorString = errors[ status.lower() ]

    return template.read( TEMPLATEDIR, 'page') % {
            'url'       :   '?' + urllib.unquote(urllib.urlencode(queryString, True)),
            'status'    :   template.read( TEMPLATEDIR, 'status' ) % errorString if status else '',
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
    Display default page with login fields
    '''

    status = queryString['status'][0] if 'status' in queryString else ''
    cnt = buildHtml( status, queryString )

    returnStatus = HTTP_STATUS_STRING % utils.httpStatus( 200 )

    responseHeaders = [ ( "Content-Type", CONTENT_HTML ),
                        ( "Content-Length", str( len( cnt ) ) ) ]

    return responseHeaders, returnStatus, cnt
