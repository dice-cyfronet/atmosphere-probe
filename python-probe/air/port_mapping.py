from air import tools

__author__ = 'paoolo'

PREFIX = '/port_mappings'


def _create_req(method=tools.HTTP_GET, url='', body=None):
    return tools.create_req(method, PREFIX + url, body)


@tools.catch_exception
def get_all_port_mappings():
    return _create_req()


@tools.catch_exception
def get_port_mapping(_id):
    url = '/%s' % str(_id)
    return _create_req(url=url)


if __name__ == '__main__':
    print get_all_port_mappings()
    print '----'

    print get_port_mapping(0)
