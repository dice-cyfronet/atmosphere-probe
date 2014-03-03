import simplejson

from air import tools


__author__ = 'paoolo'

PREFIX = '/endpoints'


def _create_req(method=tools.HTTP_GET, url='', body=None, headers=None):
    return tools.create_req(method, PREFIX + url, body, headers)


@tools.catch_exception
def get_all_endpoints():
    return _create_req()


@tools.catch_exception
def get_endpoint(_id):
    url = '/%s' % str(_id)
    return _create_req(url=url)


@tools.catch_exception
def create_endpoint(port_mapping_template_id, name=None,
                    description=None, descriptor=None,
                    endpoint_type=None, invocation_path=None):
    _data = {'port_mapping_template_id': port_mapping_template_id}
    if name is not None:
        _data['name'] = name
    if description is not None:
        _data['description'] = description
    if descriptor is not None:
        _data['descriptor'] = descriptor
    if endpoint_type is not None:
        _data['endpoint_type'] = endpoint_type
    if invocation_path is not None:
        _data['invocation_path'] = invocation_path
    body = {'endpoint': _data}
    body = simplejson.dumps(body)
    return _create_req(method=tools.HTTP_POST, body=body, headers={'Content-Length': len(body),
                                                                   'Content-Type': 'application/json'})


@tools.catch_exception
def update_endpoint(_id, port_mapping_template_id=None, name=None,
                    description=None, descriptor=None,
                    endpoint_type=None, invocation_path=None):
    url = '/%s' % str(_id)
    _data = {}
    if port_mapping_template_id is not None:
        _data['port_mapping_template_id'] = port_mapping_template_id
    if name is not None:
        _data['name'] = name
    if description is not None:
        _data['description'] = description
    if descriptor is not None:
        _data['descriptor'] = descriptor
    if endpoint_type is not None:
        _data['endpoint_type'] = endpoint_type
    if invocation_path is not None:
        _data['invocation_path'] = invocation_path
    body = {'endpoint': _data}
    body = simplejson.dumps(body)
    return _create_req(method=tools.HTTP_POST, url=url, body=body, headers={'Content-Length': len(body),
                                                                            'Content-Type': 'application/json'})


@tools.catch_exception
def delete_endpoint(_id):
    url = '/%s' % str(_id)
    return _create_req(method=tools.HTTP_DELETE, url=url)


@tools.catch_exception
def get_endpoint_descriptor(_id):
    url = '/%s/descriptor' % str(_id)
    return _create_req(method=tools.HTTP_GET, url=url)


if __name__ == '__main__':
    print get_all_endpoints()
    print '----'

    print get_endpoint(0)
    print '----'
