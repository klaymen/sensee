'''
sensee logout module

'''

import sys
import ConfigParser

sys.path.append('../../')

import lib.auth     as auth
import lib.utils    as utils
from   lib.conf import *

config = ConfigParser.ConfigParser()
config.read( CONFIG_FILE )

COOKIENAME   = config.get( 'authentication', 'cookieName' )
COOKIESTRING = '=%s; path=/'

FILTERS = [ 'html', ]
DEFAULTFILTER = FILTERS[0]


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
    login module for user authentication
    '''

    if COOKIENAME in cookies:
        try:
            cookieData = cookies[COOKIENAME].strip().split(':')
            auth.destroySession( cookieData[0] )
        except StandardError:
            pass

    cookieCnt = COOKIENAME + ( COOKIESTRING % 'None' )

    returnStatus = HTTP_STATUS_STRING % utils.httpStatus( 301 )

    responseHeaders = [ ( 'Location', '/sensee' ),
                        ( 'Set-Cookie', cookieCnt), ]
    return responseHeaders, returnStatus, ''

