from air import tools

__author__ = 'paoolo'

PREFIX = '/virtual_machines'


def _create_req(method=tools.HTTP_GET, url='', body=None, headers=None):
    return tools.create_req(method, PREFIX + url, body, headers)


def get_all_virtual_machines(app_id=None):
    url = ''
    if app_id is None:
        url += 'appliance_id=%s' % str(app_id)
    if len(url) > 0:
        url = '?' + url
    return _create_req(url=url)


def get_virtual_machines(_id):
    url = '/%s' % str(_id)
    return _create_req(url=url)


if __name__ == '__main__':
    print get_all_virtual_machines()
    print '----'

    print get_virtual_machines(0)
    print '----'
