'''
sensee templates library

'''

import os
import re

import ConfigParser

from lib.conf import *

config = ConfigParser.ConfigParser()

import lib.logger as logger

REGEXP = re.compile( r'<!--\s*RW_START\s*-->(.*?)<!--\s*RW_END\s*-->', flags=re.DOTALL )

def read( path, name, extension = 'html', access = RO_ACCESS ):
    '''
    read() tries to load the selected template and returns its content.
    '''
    fullPath = os.path.join( path, str(name) + ( '' if len( extension ) and extension[0] == '.' else '.' ) + extension )    
    if os.path.exists( fullPath ):
        logger.debug( '  loading template file at \'%s\'' % fullPath )
        cnt = ''
        try:
            fileObject = open( fullPath, 'r' )
            cnt = fileObject.read()
            fileObject.close()

            if access == RO_ACCESS:
                cnt = REGEXP.sub( '', cnt )

        except IOError:
            logger.error( '  can\'t access template file: \'%s\'' % fullPath )
        return cnt
    else:
        logger.error( '  template file doesn\'t exist: \'%s\'' % fullPath )
        return ''
