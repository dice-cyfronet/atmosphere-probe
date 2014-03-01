from air import tools

__author__ = 'paoolo'

PREFIX = '/http_mappings'


def _create_req(method=tools.HTTP_GET, url='', body=None):
    return tools.create_req(method, PREFIX + url, body)


@tools.catch_exception
def get_all_http_mappings():
    return _create_req()


@tools.catch_exception
def get_http_mappings(_id):
    url = '/%s' % str(_id)
    return _create_req(url=url)


if __name__ == '__main__':
    print get_all_http_mappings()
    print '----'

    print get_http_mappings(0)
    print '----'
