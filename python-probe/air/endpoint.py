from air import tools

__author__ = 'paoolo'

PREFIX = '/endpoints'


def _create_req(method=tools.HTTP_GET, url='', body=None):
    return tools.create_req(method, PREFIX + url, body)


@tools.catch_exception
def get_all_endpoints():
    return _create_req()


@tools.catch_exception
def get_endpoint(_id):
    url = '/%s' % str(_id)
    return _create_req(url=url)


@tools.catch_exception
def create_endpoint(port_mapping_template_id, name, endpoint_type, invocation_path,
                    description='', descriptor=''):
    url = '?port_mapping_template_id=%s&name=%s&endpoint_type=%s&invocation_path=%s&description=%s&descriptor=%s' % \
          (str(port_mapping_template_id), str(name), str(endpoint_type), str(invocation_path),
           str(description), str(descriptor))
    return _create_req(method=tools.HTTP_POST, url=url)


@tools.catch_exception
def update_endpoint(_id, port_mapping_template_id='', name='', endpoint_type='', invocation_path='',
                    description='', descriptor=''):
    url = '/%s?port_mapping_template_id=%s&name=%s&endpoint_type=%s&invocation_path=%s&description=%s&descriptor=%s' % \
          (str(_id), str(port_mapping_template_id), str(name), str(endpoint_type), str(invocation_path),
           str(description), str(descriptor))
    return _create_req(method=tools.HTTP_POST, url=url)


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
