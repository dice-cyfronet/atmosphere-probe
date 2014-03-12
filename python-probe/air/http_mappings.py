from air import tools

__author__ = 'paoolo'

PREFIX = '/http_mappings'


def _create_req(method=tools.HTTP_GET, url='', body=None, headers=None):
    return tools.create_req(method, PREFIX + url, body, headers)


def get_all_http_map(app_id=None, port_mapping_template_id=None):
    url = ''
    if app_id is not None:
        url += 'appliance_id=%s' % str(app_id)
    if port_mapping_template_id is not None:
        if len(url) > 0: url += '&'
        url += 'port_mapping_template_id=%s' % str(port_mapping_template_id)
    if len(url) > 0:
        url = '?' + url
    return _create_req(url=url)


def get_http_map(_id):
    url = '/%s' % str(_id)
    return _create_req(url=url)


if __name__ == '__main__':
    print get_all_http_map(123)
    print '----'

    print get_http_map(0)
    print '----'
