from air import tools

__author__ = 'paoolo'

PREFIX = '/port_mappings'


def _create_req(method=tools.HTTP_GET, url='', body=None, headers=None):
    return tools.create_req(method, PREFIX + url, body, headers)


def get_all_port_mappings(port_mapping_template_id=None, virtual_machine_id=None):
    url = ''
    if port_mapping_template_id is not None:
        url += 'port_mapping_template_id=%s' % str(port_mapping_template_id)
    if virtual_machine_id is not None:
        if len(url) > 0: url += '&'
        url += 'virtual_machine_id=%s' % str(virtual_machine_id)
    if len(url) > 0:
        url = '?' + url
    return _create_req(url=url)


def get_port_mapping(_id):
    url = '/%s' % str(_id)
    return _create_req(url=url)


if __name__ == '__main__':
    print get_all_port_mappings()
    print '----'

    print get_port_mapping(0)
