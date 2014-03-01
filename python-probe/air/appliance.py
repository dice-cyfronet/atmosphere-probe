import simplejson

from air import tools
from air import appliance_sets


__author__ = 'paoolo'

PREFIX = '/appliances'


def _create_req(method=tools.HTTP_GET, url='', body=None):
    return tools.create_req(method, PREFIX + url, body)


@tools.catch_exception
def get_all_app(_all=False):
    url = '?all=true' if _all else ''
    return _create_req(url=url)


@tools.catch_exception
def get_app(_id):
    url = '/%s' % str(_id)
    return _create_req(url=url)


@tools.catch_exception
def get_app_endpoints(_id):
    url = '/%s/endpoints' % str(_id)
    return _create_req(url=url)


@tools.catch_exception
def create_app(app_set_id, config_temp_id=1):
    body = {'appliance': {'appliance_set_id': app_set_id, 'configuration_template_id': config_temp_id}}
    return _create_req(method=tools.HTTP_POST, body=simplejson.dumps(body))


@tools.catch_exception
def update_app(_id, name=''):
    body = {'appliance': {'name': name}}
    url = '/%s' % str(_id)
    return _create_req(method=tools.HTTP_PUT, url=url, body=simplejson.dumps(body))


@tools.catch_exception
def delete_app(_id):
    url = '/%s' % int(_id)
    return _create_req(method=tools.HTTP_DELETE, url=url)


if __name__ == '__main__':
    _app_set = appliance_sets.create_app_set(
        appliance_set_type=appliance_sets.APP_SET_TYPE_DEV)
    print _app_set
    print '----'

    try:
        print get_all_app()
        print '----'

        app = create_app(_app_set['appliance_set']['id'])
        print app
        __id = app['appliance']['id']
        print '----'

        print get_all_app()
        print '----'

        print get_app(__id)
        print '----'

        print get_app_endpoints(__id)
        print '----'

        print update_app(__id, 'name')
        print '----'

        print delete_app(__id)

    finally:
        print appliance_sets.delete_app_set(_app_set['appliance_set']['id'])
