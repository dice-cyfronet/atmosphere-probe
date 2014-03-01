from air import tools

__author__ = 'paoolo'

PREFIX = '/port_mapping_properties'


def _create_req(method=tools.HTTP_GET, url='', body=None):
    return tools.create_req(method, PREFIX + url, body)


@tools.catch_exception
def get_all_port_map_prop(port_mapping_template_id):
    url = '?port_mapping_template_id=%s' % str(port_mapping_template_id)
    return _create_req(url=url)


@tools.catch_exception
def get_port_map_prop(_id):
    url = '/%s' % str(_id)
    return _create_req(url=url)


@tools.catch_exception
def create_port_mapping_prop(port_mapping_template_id, key, value=''):
    url = '?port_mapping_template_id=%s&key=%s&value=%s' % (str(port_mapping_template_id), str(key), str(value))
    return _create_req(method=tools.HTTP_POST, url=url)


@tools.catch_exception
def update_port_mapping_prop(_id, port_mapping_template_id='', key='', value=''):
    url = '/%s?port_mapping_template_id=%s&key=%s&value=%s' % \
          (str(_id), str(port_mapping_template_id), str(key), str(value))
    return _create_req(method=tools.HTTP_PUT, url=url)


@tools.catch_exception
def delete_port_mapping_prop(_id):
    url = '/%s' % str(_id)
    return _create_req(method=tools.HTTP_DELETE, url=url)


if __name__ == '__main__':
    print get_all_port_map_prop(0)
    print '----'

    print get_port_map_prop(0)
    print '----'

    _prop = create_port_mapping_prop(0, 'test')
    print _prop
    _id = _prop['port_mapping_properties']['id']
    print '----'

    print update_port_mapping_prop(_id)
    print '----'

    print delete_port_mapping_prop(_id)
