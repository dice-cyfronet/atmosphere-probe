#!/usr/bin/python
import httplib
import socket
import time
import traceback

from air import appliance_sets, appliances, port_mapping_templates, dev_mode_property_sets, port_mappings, \
    virtual_machines
import config


__author__ = 'paoolo'

SLEEP_TIME = 5
LIMIT_TIME = 300

STATE_OK = 0
STATE_WARNING = 1
STATE_CRITICAL = 2
STATE_UNKNOWN = 3


def vm_active(_app):
    _virtual_machines = virtual_machines.get_all_virtual_machines(_app['appliance']['id'])
    return len(_virtual_machines['virtual_machines']) > 0 and \
           'state' in _virtual_machines['virtual_machines'][0] and \
           _virtual_machines['virtual_machines'][0]['state'] == 'active'


def get_state(state):
    if state >= STATE_UNKNOWN:
        return 'UNKNOWN'
    elif state == STATE_CRITICAL:
        return 'CRITICAL'
    elif state == STATE_WARNING:
        return 'WARNING'
    else:
        return 'OK'


def check_point(_exit_output, _exit_status, _exit_now=False):
    check_point.exit_output += _exit_output
    check_point.exit_state = max(_exit_status, check_point.exit_status)

    if _exit_now:
        for hook in reversed(check_point.hooks):
            try:
                hook()
            except BaseException as _e:
                print 'hook error: %s' % str(_e)

        print '%s: %s' % (get_state(check_point.exit_state), check_point.exit_output)
        exit(check_point.exit_state)


check_point.exit_output = ''
check_point.exit_status = STATE_OK
check_point.hooks = []

if __name__ == '__main__':

    exit_output = 'UNKNOWN:'
    exit_status = STATE_OK
    exit_now = False

    delayed = False

    try:
        app_set = appliance_sets.create_app_set(appliance_set_type=appliance_sets.APP_SET_TYPE_DEV)
        if 'message' in app_set:
            check_point('cannot create appliance set: %s\n' % app_set['message'], STATE_CRITICAL, True)
        check_point.hooks.append(lambda: appliance_sets.delete_app_set(app_set['appliance_set']['id']))

        app = appliances.create_app(app_set['appliance_set']['id'], config.CONF_AT_ID)
        if 'message' in app:
            check_point('cannot create appliance: %s\n' % app['message'], STATE_CRITICAL, True)
        check_point.hooks.append(lambda: appliances.delete_app(app['appliance']['id']))

        sleep_time = 0
        while not vm_active(app) and sleep_time < (2 * LIMIT_TIME):
            time.sleep(SLEEP_TIME)
            sleep_time += SLEEP_TIME
            delayed = sleep_time > LIMIT_TIME
            exit_now = sleep_time > (2 * LIMIT_TIME)

        if not vm_active(app):
            check_point('cannot start vm', STATE_CRITICAL, True)

        if delayed:
            check_point('delay vm start', STATE_WARNING)

        dev_mode_prop_sets = dev_mode_property_sets.get_all_dev_mode_property_set(app['appliance']['id'])

        port_mapping_temp = port_mapping_templates.create_port_map_temp_for_dev(
            dev_mode_prop_sets['dev_mode_property_sets'][0]['id'], 'tcp', 'none', 'http', 80)
        if 'message' in port_mapping_temp:
            check_point('cannot create port mapping: %s\n' % str(port_mapping_temp['message']), STATE_CRITICAL, True)

        if 'port_mapping_templates' not in port_mapping_temp:
            port_mapping_temp = port_mapping_templates.get_all_port_map_temp_by_dev(
                dev_mode_prop_sets['dev_mode_property_sets'][0]['id'], 80)

        port_mapping = port_mappings.get_all_port_mappings(port_mapping_temp['port_mapping_templates'][0]['id'])

        connection = httplib.HTTPConnection(port_mapping['port_mappings'][0]['public_ip'],
                                            port_mapping['port_mappings'][0]['source_port'])
        try:
            connection.request('GET', '/')
            response = connection.getresponse()
            content = response.read()
            check_point('http: status: %d, reason: %s\n' % (int(response.status), str(response.reason)), STATE_OK)
        except socket.error as e:
            check_point('cannot connect to server: %s\n' % str(e), STATE_WARNING)

    except BaseException as e:
        traceback.print_exc()
        check_point('error during executing script: %s\n' % str(e), STATE_UNKNOWN, True)

    check_point('done\n', STATE_OK, True)
