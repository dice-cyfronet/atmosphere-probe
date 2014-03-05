import sys

from air import appliance_sets, appliances, dev_mode_property_sets, port_mappings, endpoint


__author__ = 'paoolo'

STATE_OK = 0
STATE_WARNING = 1
STATE_CRITICAL = 2
STATE_UNKNOWN = 3

if __name__ == '__main__':
    exit_code = STATE_OK
    exit_output = ''

    _all_app_set = appliance_sets.get_all_app_set()
    if 'message' in _all_app_set:
        exit_output += '%s, ' % _all_app_set['message']
        exit_code = STATE_WARNING

    _all_app = appliances.get_all_app()
    if 'message' in _all_app:
        exit_output += '%s, ' % _all_app['message']
        exit_code = STATE_WARNING

    _all_dev_prop = dev_mode_property_sets.get_all_dev_mode_property_set()
    if 'message' in _all_dev_prop:
        exit_output += '%s, ' % _all_dev_prop['message']
        exit_code = STATE_WARNING

    _all_end = endpoint.get_all_endpoints()
    if 'message' in _all_end:
        exit_output += '%s, ' % _all_end['message']
        exit_code = STATE_WARNING

    _all_port_map = port_mappings.get_all_port_mappings()
    if 'message' in _all_port_map:
        exit_output += '%s, ' % _all_port_map['message']
        exit_code = STATE_WARNING

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
