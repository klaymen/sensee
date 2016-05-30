'''
authentication module
'''

import pickle
from time import time
from random import randint
from lib.conf import *
import lib.logger as logger

config = ConfigParser.ConfigParser()
config.read(CONFIG_FILE)

SESSION_FILE    = config.get( "authentication", "sessionFile" )
SESSION_TIMEOUT = config.get( "authentication", "sessionTimeout" )
COOKIE_NAME     = config.get( "authentication", "cookieName" )

def openSession( username, mode, key = None ):
    '''
    opens a session for a user
    '''
    logger.debug('   openSession with user: %s, mode: %d' % (username, mode) )
    try:
        sessionFp = open( SESSION_FILE, 'r' )
        sessions = pickle.load( sessionFp )
        sessionFp.close()
        logger.debug('   existing sessions loaded')
    except StandardError:
        sessions = {}
        logger.debug('   no existing sessions found')
    try:
        keyString = "%x" % randint( 2**32, 2**64 ) if not key else key
        logger.debug('   generating key: %s' % keyString )
        timeInt = int( time() )
        sessions[username] = {
                'mode'  :   mode,
                'time'  :   timeInt,
                'key'   :   keyString,
                }
        if not os.path.exists(os.path.dirname(SESSION_FILE)):
            try:
                os.makedirs(os.path.dirname(SESSION_FILE))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        sessionFp = open( SESSION_FILE, 'w' )
        pickle.dump( sessions, sessionFp )
        logger.debug('   new session stored')
        sessionFp.close()
    except None:
        pass
    logger.debug( "user session created for %s, with key: %s, and time: %d" % ( username, keyString, timeInt ) )
    return keyString

def querySession( username, key ):
    '''
    check if the user has a valid session
    '''
    logger.debug('   querySession for user: %s with key: %s' % (username, key) )
    try:
        sessionFp = open( SESSION_FILE, 'r' )
        sessions = pickle.load( sessionFp )
        sessionFp.close()
        if username in sessions:
            logger.debug('   username found in sessions file')
            if sessions[username]['key'] == key and ( time() - sessions[username]['time'] ) < SESSION_TIMEOUT:
                logger.debug('   user has valid session,extending it')
                openSession( username, sessions[username]['mode'], key )
                logger.debug('   session stored accessLevel: %d' % sessions[username]['mode'])
                return sessions[username]['mode']
            elif ( time() - sessions[username]['time'] ) > SESSION_TIMEOUT:
                logger.debug('   session expired, cleaning up')
                destroySession( username )
            else:
                logger.debug('   sessions data [ time: %d, key: %s, mode: %d ]' % (sessions[username]['time'], sessions[username]['key'], sessions[username]['mode']))
                logger.debug('   user data [ time: %d, key: %s ]' % ( int(time()), key))
    except StandardError:
        pass
    return NO_ACCESS

def destroySession( username ):
    '''
    destroy a session
    '''
    logger.debug("   destroy session for user: %s" % username)
    sessionFp = open( SESSION_FILE, 'r' )
    sessions = pickle.load( sessionFp )
    sessionFp.close()
    try:
        logger.debug("   removing user from sessions...")
        del sessions[username]
        logger.debug("   ...done")
        sessionFp = open( SESSION_FILE, 'w' )
        pickle.dump( sessions, sessionFp )
        sessionFp.close()
        logger.debug('   session dumped')
    except None:
        pass
    return 1

