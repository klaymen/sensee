'''
sensee configuration
values used all over the code

'''

# config file
CONFIG_FILE = '/etc/sensee/sensee.conf'

NO_ACCESS = 0   # no access
RO_ACCESS = 1   # read only
RW_ACCESS = 2   # read/write access

# mime content types
CONTENT_TXT  = 'text/plain'
CONTENT_HTML = 'text/html'
CONTENT_CSV  = 'text/csv'
CONTENT_XLS  = 'application/vnd.ms-excel'
CONTENT_XLSX = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
CONTENT_PDF  = 'application/pdf'

# other related string constants
CONTENT_TYPE   = 'Content-Type'
CONTENT_LENGTH = 'Content-Lenght'

# CSS folder
CSS = '/sensee_styles'

# return values
CODE = {    200 : '200 OK', 
            400 : '400 INVALID COMMAND',
            301 : '301 MOVED PERMANENTLY',
            404 : '404 NOT FOUND',
            }

HTTP_STATUS_STRING = '%(code)d %(description)s'

import os
import ConfigParser

config = ConfigParser.ConfigParser()
config.read( CONFIG_FILE )
LIBPATH = config.get( 'general', 'LIBPATH' )
MODULEPATH = config.get( 'general', 'MODULEPATH' )

DEFAULT_PARAMS = {
        'type'      :   'module',
        'enabled'   :   'enabled',
        'access'    :   1,
        }

def getModuleParam(module, param):
    '''
    get module parameters (type)
    '''
    try:
        typeFile = os.path.join( MODULEPATH, module, param )
        fileObject = open( typeFile, 'r' )
        returnValue = fileObject.readline().strip()
        fileObject.close()
    except IOError: #StandardError:
        returnValue = DEFAULT_PARAMS[param]
    try:
        returnValue = int( returnValue )
    except ValueError:
        pass
    return returnValue

MODULES = {}
for directory in os.listdir(MODULEPATH):
    if directory[0] == '.':
        continue
    if os.path.exists(os.path.join( MODULEPATH, directory, '%s.py' % directory)):
        MODULES[directory] = {
                'dirname'   :   directory,
                'filename'  :   '%s.py' % directory,
                'type'      :   getModuleParam(directory, 'type'),
                'enabled'   :   getModuleParam(directory, 'enabled'),
                'access'    :   getModuleParam(directory, 'access'),
                }

# default module to load if no module is specified
DEFAULT_MODULE = 'default'

