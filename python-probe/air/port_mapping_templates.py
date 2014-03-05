import simplejson

from air import tools, appliance_sets, appliances, dev_mode_property_sets


__author__ = 'paoolo'

PREFIX = '/port_mapping_templates'


def _create_req(method=tools.HTTP_GET, url='', body=None, headers=None):
    return tools.create_req(method, PREFIX + url, body, headers)


def get_all_port_map_temp_by_at(appliance_type_id):
    url = '?appliance_type_id=%s' % str(appliance_type_id)
    return _create_req(url=url)


def get_all_port_map_temp_by_dev(dev_mode_property_set_id, target_port=None):
    url = '?dev_mode_property_set_id=%s' % str(dev_mode_property_set_id)
    if target_port is not None:
        url += '&target_port=%s' % str(target_port)
    return _create_req(url=url)


def get_port_map_temp(_id):
    url = '/%s' % str(_id)
    return _create_req(url=url)


def create_port_map_temp_for_at(appliance_type_id,
                                transport_protocol, application_protocol, service_name, target_port):
    body = {'port_mapping_template': {'appliance_type_id': appliance_type_id,
                                      'transport_protocol': transport_protocol,
                                      'application_protocol': application_protocol,
                                      'service_name': service_name,
                                      'target_port': target_port}}
    body = simplejson.dumps(body)
    return _create_req(method=tools.HTTP_POST, body=body, headers={'Content-Length': len(body),
                                                                   'Content-Type': 'application/json'})


def create_port_map_temp_for_dev(dev_mode_property_set_id,
                                 transport_protocol, application_protocol, service_name, target_port):
    body = {'port_mapping_template': {'dev_mode_property_set_id': dev_mode_property_set_id,
                                      'transport_protocol': transport_protocol,
                                      'application_protocol': application_protocol,
                                      'service_name': service_name,
                                      'target_port': target_port}}
    body = simplejson.dumps(body)
    return _create_req(method=tools.HTTP_POST, body=body, headers={'Content-Length': len(body),
                                                                   'Content-Type': 'application/json'})


def update_port_map_temp(_id, appliance_type_id=None, dev_mode_property_set_id=None,
                         transport_protocol=None, application_protocol=None, service_name=None, target_port=None):
    url = '/%s' % str(_id)
    _data = {}
    if appliance_type_id is not None:
        _data['appliance_type_id'] = appliance_type_id
    if dev_mode_property_set_id is not None:
        _data['dev_mode_property_set_id'] = dev_mode_property_set_id
    if transport_protocol is not None:
        _data['transport_protocol'] = transport_protocol
    if application_protocol is not None:
        _data['application_protocol'] = application_protocol
    if service_name is not None:
        _data['service_name'] = service_name
    if target_port is not None:
        _data['target_port'] = target_port
    body = {'port_mapping_template': _data}
    body = simplejson.dumps(body)
    return _create_req(method=tools.HTTP_PUT, url=url, body=body, headers={'Content-Length': len(body),
                                                                           'Content-Type': 'application/json'})


def delete_port_map_temp(_id):
    url = '/%s' % str(_id)
    return _create_req(method=tools.HTTP_DELETE, url=url)


def get_dev_id_for_app(app_id, dev_sets):
    if 'dev_mode_property_sets' in dev_sets:
        for dev_set in dev_sets['dev_mode_property_sets']:
            if 'appliance_id' in dev_set and dev_set['appliance_id'] == app_id:
                return dev_set
    return None


if __name__ == '__main__':
    _app_set = appliance_sets.create_app_set(
        appliance_set_type=appliance_sets.APP_SET_TYPE_DEV)
    print _app_set
    print '----'

    _app = appliances.create_app(_app_set['appliance_set']['id'], 1)
    print _app
    print '----'

    _dev_sets = dev_mode_property_sets.get_all_dev_mode_property_set(_app['appliance']['id'])
    print _dev_sets
    print '----'

    try:
        print get_all_port_map_temp_by_dev(_dev_sets['dev_mode_property_sets'][0]['id'])
        print '----'

        _port_mapping = create_port_map_temp_for_dev(_dev_sets['dev_mode_property_sets'][0]['id'], 'tcp', 'none',
                                                     'telnet', 25)
        print _port_mapping
        print '----'

        print get_all_port_map_temp_by_dev(_dev_sets['dev_mode_property_sets'][0]['id'])
        print '----'

        print update_port_map_temp(_port_mapping['port_mapping_template']['id'], service_name='http', target_port=80)
        print '----'

        print get_all_port_map_temp_by_dev(_dev_sets['dev_mode_property_sets'][0]['id'])
        print '----'

        print delete_port_map_temp(_port_mapping['port_mapping_template']['id'])
        print '----'

    finally:
        print appliances.delete_app(_app['appliance']['id'])
        print appliance_sets.delete_app_set(_app_set['appliance_set']['id'])
