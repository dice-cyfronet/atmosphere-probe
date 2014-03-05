from air import tools

__author__ = 'paoolo'

PREFIX = '/appliance_types'


def _create_req(method=tools.HTTP_GET, url='', body=None, headers=None):
    return tools.create_req(method, PREFIX + url, body, headers)


def get_all_appliance_types(name=None):
    url = ''
    if name is not None:
        url += 'name=%s' % str(name)
    if len(url) > 0:
        url = '&' + url
    return _create_req(url=url)


if __name__ == '__main__':
    print get_all_appliance_types()
    print '----'
