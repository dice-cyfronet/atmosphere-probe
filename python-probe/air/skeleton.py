from air import tools

__author__ = 'paoolo'

PREFIX = '/'


def _create_req(method=tools.HTTP_GET, url='', body=None):
    return tools.create_req(method, PREFIX + url, body)


@tools.catch_exception
def do_something():
    return _create_req()


if __name__ == '__main__':
    print do_something()
    print '----'
