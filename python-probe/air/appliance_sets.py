from air import tools

__author__ = 'paoolo'

PREFIX = '/appliance_sets'


def _create_req(method=tools.HTTP_GET, url='', body=None):
    return tools.create_req(method, PREFIX + url, body)


@tools.catch_exception
def get_all_app_set():
    return _create_req()


@tools.catch_exception
def get_app_set(_id):
    url = '/%s' % str(_id)
    return _create_req(url=url)


APP_SET_TYPE_DEV = 'development'
APP_SET_TYPE_PORTAL = 'portal'
APP_SET_TYPE_WORKFLOW = 'workflow'


@tools.catch_exception
def create_app_set(name='', priority='', appliance_set_type=''):
    url = '?name=%s&priority=%s&appliance_set_type=%s' % (name, priority, appliance_set_type)
    return _create_req(method=tools.HTTP_POST, url=url)


@tools.catch_exception
def update_app_set(_id, name='', priority=''):
    url = '?id=%s&name=%s&priority=%s' % (_id, name, priority)
    return _create_req(method=tools.HTTP_PUT, url=url)


@tools.catch_exception
def delete_app_set(_id):
    url = '/%s' % str(_id)
    return _create_req(method=tools.HTTP_DELETE, url=url)


if __name__ == '__main__':
    print get_all_app_set()
    print '----'

    app_set = create_app_set(appliance_set_type=APP_SET_TYPE_DEV)
    print app_set
    __id = app_set['appliance_set']['id']
    print '----'

    print get_all_app_set()
    print '----'

    print get_app_set(__id)
    print '----'

    print update_app_set(__id, name='name', priority='priority')
    print '----'

    print delete_app_set(__id)
