import simplejson

from air import tools
from air import appliance_sets
import config


__author__ = 'paoolo'

PREFIX = '/appliances'


def _create_req(method=tools.HTTP_GET, url='', body=None, headers=None):
    return tools.create_req(method, PREFIX + url, body, headers)


def get_all_app(_all=False):
    url = '?all=true' if _all else ''
    return _create_req(url=url)


def get_app(_id):
    url = '/%s' % str(_id)
    return _create_req(url=url)


def get_app_endpoints(_id):
    url = '/%s/endpoints' % str(_id)
    return _create_req(url=url)


def create_app(appliance_set_id, configuration_template_id,
               name=None, user_key_id=None, params=None):
    _data = {'appliance_set_id': appliance_set_id,
             'configuration_template_id': configuration_template_id}
    if name is not None:
        _data['name'] = name
    if user_key_id is not None:
        _data['user_key_id'] = user_key_id
    if params is not None:
        _data['params'] = params
    body = {'appliance': _data}
    body = simplejson.dumps(body)
    return _create_req(method=tools.HTTP_POST, body=body, headers={'Content-Length': len(body),
                                                                   'Content-Type': 'application/json'})


def update_app(_id, name=None):
    _data = {}
    if name is not None:
        _data['name'] = name
    body = {'appliance': _data}
    body = simplejson.dumps(body)
    url = '/%s' % str(_id)
    return _create_req(method=tools.HTTP_PUT, url=url, body=body, headers={'Content-Length': len(body),
                                                                           'Content-Type': 'application/json'})


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

        app = create_app(_app_set['appliance_set']['id'], 1)

        print app
        try:
            __id = app['appliance']['id']
        except:
            __id = 0

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
