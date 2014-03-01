from air import tools

__author__ = 'paoolo'

PREFIX = '/port_mapping_templates'


def _create_req(method=tools.HTTP_GET, url='', body=None):
    return tools.create_req(method, PREFIX + url, body)


@tools.catch_exception
def get_all_port_map_temp_by_at(appliance_type_id):
    url = '?appliance_type_id=%s' % str(appliance_type_id)
    return _create_req(url=url)


@tools.catch_exception
def get_all_port_map_temp_by_dev(dev_mode_property_set_id):
    url = '?dev_mode_property_set_id=%s' % str(dev_mode_property_set_id)
    return _create_req(url=url)


@tools.catch_exception
def get_port_map_temp(_id):
    url = '/%s' % str(_id)
    return _create_req(url=url)


@tools.catch_exception
def create_port_map_temp_for_at(appliance_type_id,
                                transport_protocol, application_protocol, service_name, target_port):
    url = '?appliance_type_id=%s&transport_protocol=%s&application_protocol=%s&service_name=%s&target_port=%s' % \
          (str(appliance_type_id),
           str(transport_protocol), str(application_protocol), str(service_name), str(target_port))
    return _create_req(method=tools.HTTP_POST, url=url)


@tools.catch_exception
def create_port_map_temp_for_dev(dev_mode_property_set_id,
                                 transport_protocol, application_protocol, service_name, target_port):
    url = '?dev_mode_property_set_id=%s&transport_protocol=%s&application_protocol=%s&service_name=%s&target_port=%s' % \
          (str(dev_mode_property_set_id),
           str(transport_protocol), str(application_protocol), str(service_name), str(target_port))
    return _create_req(method=tools.HTTP_POST, url=url)


@tools.catch_exception
def update_port_map_temp(_id, appliance_type_id='', dev_mode_property_set_id='',
                         transport_protocol='', application_protocol='', service_name='', target_port=''):
    url = '/%s?appliance_type_id=%s&dev_mode_property_set_id=%s' \
          '&transport_protocol=%s&application_protocol=%s&service_name=%s&target_port=%s' % \
          (str(_id), str(appliance_type_id), str(dev_mode_property_set_id),
           str(transport_protocol), str(application_protocol), str(service_name), str(target_port))
    return _create_req(method=tools.HTTP_PUT, url=url)


@tools.catch_exception
def delete_port_map_temp(_id):
    url = '/%s' % str(_id)
    return _create_req(method=tools.HTTP_DELETE, url=url)


if __name__ == '__main__':
    print get_all_port_map_temp_by_at(0)
    print '----'

    print get_all_port_map_temp_by_dev(0)
    print '----'

    print get_port_map_temp(0)
    print '----'
