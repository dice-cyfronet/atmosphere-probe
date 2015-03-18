import httplib
import socket
import time
import sys

import os
import re
import paramiko
import atmosphere.config


pwd = os.path.dirname(os.path.abspath(__file__))
atmosphere.config.add_config_ini('%s/../etc/main.ini' % pwd, '%s/../etc/secure.ini' % pwd)

from atmosphere.property import dev_mode_property_sets
from atmosphere.appliance import appliance_sets, appliances
from atmosphere.mapping import port_mapping_templates, port_mappings, http_mappings
from atmosphere.machine import virtual_machines


__author__ = 'paoolo'

SLEEP_TIME = 15
LIMIT_TIME = 600

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
    check_point.exit_status = max(_exit_status, check_point.exit_status)

    if _exit_now:
        for hook in reversed(check_point.hooks):
            try:
                hook()
            except BaseException as _e:
                print 'hook error: %s' % str(_e)

        print '%s: %s' % (get_state(check_point.exit_status), check_point.exit_output)
        sys.exit(check_point.exit_status)


check_point.exit_output = ''
check_point.exit_status = STATE_OK
check_point.hooks = []

if __name__ == '__main__':

    exit_output = ''
    exit_status = STATE_OK
    exit_now = False

    delayed = False

    try:
        app_set = appliance_sets.get_all_app_set()
        if 'message' in app_set:
            check_point('cannot get appliance set: %s; ' % app_set['message'], STATE_CRITICAL, True)
        if len(app_set['appliance_sets']) > 0:
            check_point('old appliance set exist, remove it; ', STATE_WARNING, False)
            appliance_sets.delete_app_set(app_set['appliance_sets'][0]['id'])

        # wait until old appliance set is remove
        time.sleep(SLEEP_TIME)

        app_set = appliance_sets.create_app_set(appliance_set_type=appliance_sets.APP_SET_TYPE_DEV)
        if 'message' in app_set:
            check_point('cannot create appliance set: %s; ' % app_set['message'], STATE_CRITICAL, True)
        check_point.hooks.append(lambda: appliance_sets.delete_app_set(app_set['appliance_set']['id']))

        # wait until new appliance set is created
        time.sleep(SLEEP_TIME)

        app = appliances.create_app(app_set['appliance_set']['id'], atmosphere.config.CONF_AT_ID)
        if 'message' in app:
            check_point('cannot create appliance: %s; ' % app['message'], STATE_CRITICAL, True)
        check_point.hooks.append(lambda: appliances.delete_app(app['appliance']['id']))

        sleep_time = 0
        while not vm_active(app) and sleep_time < (2 * LIMIT_TIME):
            time.sleep(SLEEP_TIME)
            sleep_time += SLEEP_TIME
            delayed = sleep_time > LIMIT_TIME
            exit_now = sleep_time > (2 * LIMIT_TIME)

        if not vm_active(app):
            check_point('cannot start vm; ', STATE_CRITICAL, True)

        if delayed:
            check_point('delay vm start; ', STATE_WARNING)

        dev_mode_prop_sets = dev_mode_property_sets.get_all_dev_mode_property_set(app['appliance']['id'])

        port_mapping_temp = port_mapping_templates.get_all_port_map_temp_by_dev(
            dev_mode_prop_sets['dev_mode_property_sets'][0]['id'], 22)
        port_mapping = port_mappings.get_all_port_mappings(
            port_mapping_template_id=port_mapping_temp['port_mapping_templates'][0]['id'])

        try:
            ssh = paramiko.SSHClient()

            ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            ssh.connect(port_mapping['port_mappings'][0]['public_ip'],
                        int(port_mapping['port_mappings'][0]['source_port']),
                        'root', 'password')

            (stdin, stdout, stderr) = ssh.exec_command('wget -q -O - http://169.254.169.254/openstack/latest/user_data')

            output = ''
            for line in stdout.readlines():
                output += line
                break

            if len(output) < 256:
                check_point('cannot get mi_ticket from user_data: %s; ' % str(output), STATE_WARNING, False)
            else:
                check_point('ssh: OK; user_data: %s...; ' % str(output[:64]), STATE_OK, False)

            ssh.close()
        except BaseException as e:
            check_point('cannot login ssh to server: %s; ' % str(e), STATE_WARNING, False)

        port_mapping_temp = port_mapping_templates.create_port_map_temp_for_dev(
            dev_mode_prop_sets['dev_mode_property_sets'][0]['id'], 'tcp', 'none', 'http', 80)

        time.sleep(SLEEP_TIME)

        if 'message' in port_mapping_temp:
            check_point('cannot create port mapping: %s; ' % str(port_mapping_temp['message']), STATE_CRITICAL, True)

        if 'port_mapping_templates' not in port_mapping_temp:
            port_mapping_temp = port_mapping_templates.get_all_port_map_temp_by_dev(
                dev_mode_prop_sets['dev_mode_property_sets'][0]['id'], 80)

        port_mapping = port_mappings.get_all_port_mappings(False, port_mapping_temp['port_mapping_templates'][0]['id'])

        connection = httplib.HTTPConnection(port_mapping['port_mappings'][0]['public_ip'],
                                            port_mapping['port_mappings'][0]['source_port'])
        try:
            connection.request('GET', '/')
            response = connection.getresponse()
            content = response.read()
            check_point('http: status: %d, reason: %s; ' % (int(response.status), str(response.reason)), STATE_OK)
        except socket.error as e:
            check_point('cannot connect to server: %s; ' % str(e), STATE_WARNING)

        port_mapping_temp = port_mapping_templates.create_port_map_temp_for_dev(
            dev_mode_prop_sets['dev_mode_property_sets'][0]['id'], 'tcp', 'http', 'http-2', 81)

        time.sleep(SLEEP_TIME)

        if 'message' in port_mapping_temp:
            check_point('cannot create port mapping: %s; ' % str(port_mapping_temp['message']), STATE_CRITICAL, True)

        port_mapping = http_mappings.get_all_http_map(app['appliance']['id'],
                                                      port_mapping_temp['port_mapping_template']['id'])

        url = re.sub('http://', '', port_mapping['http_mappings'][0]['url'])
        connection = httplib.HTTPConnection(url)
        try:
            connection.request('GET', '/')
            response = connection.getresponse()
            content = response.read()
            check_point('http-2: status: %d, reason: %s; ' % (int(response.status), str(response.reason)), STATE_OK)
        except socket.error as e:
            check_point('cannot connect to server: %s; ' % str(e), STATE_WARNING)

    except SystemExit as e:
        raise e

    except BaseException as e:
        check_point('error during executing script: %s; ' % str(e), STATE_CRITICAL, True)

    check_point('done; ', STATE_OK, True)
