'''
sensee login module

'''

import sys
import ConfigParser
import urllib
import hashlib

sys.path.append('../../')

import lib.utils as utils
import lib.auth as auth
import lib.logger as logger
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

    authLevel = NO_ACCESS
    key = ''

    cookieCnt = COOKIENAME + ( COOKIESTRING % 'None' )

    returnStatus = HTTP_STATUS_STRING % utils.httpStatus( 301 )

    if 'username' in postData:
        if 'password' in postData:
            users = utils.getUsers()
            for user in users:
                if ( user ==  postData['username'][0] and users[user] == hashlib.sha224(postData['password'][0]).hexdigest()):
                    logger.debug("  found user/pw in user list")
                    key = auth.openSession( user, RW_ACCESS )
                    authLevel = RW_ACCESS
                    cookieCnt = COOKIENAME + COOKIESTRING % ( user + ":" + key )                    
                    break

    if authLevel == NO_ACCESS:
        responseHeaders = [ ( 'Location', '/sensee?status=invalid_credentials' ),
                            ( 'Set-Cookie', cookieCnt), ]
        return responseHeaders, returnStatus, ''
    else:
        # save authentication session
        logger.debug("  cookieCnt: %s" % cookieCnt)
        responseHeaders = [ ( 'Location', '/sensee/_sample'+ '?' + urllib.unquote(urllib.urlencode(queryString, True))),
                            ( 'Set-Cookie', cookieCnt), ]
        return responseHeaders, returnStatus, ''

