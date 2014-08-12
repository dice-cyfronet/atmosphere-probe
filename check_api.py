import httplib
import sys

import os
import air.config


pwd = os.path.dirname(os.path.abspath(__file__))
air.config.add_config_ini('%s/main.ini' % pwd)

__author__ = 'paoolo'

STATE_OK = 0
STATE_WARNING = 1
STATE_CRITICAL = 2
STATE_UNKNOWN = 3

if __name__ == '__main__':
    exit_code = STATE_UNKNOWN
    exit_output = ''

    if air.config.HTTPS == 'True':
        connection = httplib.HTTPSConnection(air.config.API_URL)
    else:
        connection = httplib.HTTPConnection(air.config.API_URL)

    connection.request('GET', '/users/sign_in')
    response = connection.getresponse()
    content = response.read()

    _status = int(response.status)
    _reason = str(response.reason)
    exit_output = 'code: %d, reason: %s' % (_status, _reason)
    if 100 <= _status < 300:
        exit_code = STATE_OK
    elif 300 <= _status < 400:
        exit_code = STATE_WARNING
    elif 400 <= _status < 600:
        exit_code = STATE_CRITICAL

    if exit_code == STATE_OK:
        exit_output = 'OK: ' + exit_output
    elif exit_code == STATE_WARNING:
        exit_output = 'WARNING: ' + exit_output
    elif exit_code == STATE_CRITICAL:
        exit_output = 'CRITICAL: ' + exit_output
    elif exit_code == STATE_UNKNOWN:
        exit_output = 'UNKNOWN: ' + exit_output

    print exit_output
    sys.exit(exit_code)
