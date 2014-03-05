import simplejson

from air import tools


__author__ = 'paoolo'

PREFIX = '/dev_mode_property_sets'


def _create_req(method=tools.HTTP_GET, url='', body=None, headers=None):
    return tools.create_req(method, PREFIX + url, body, headers)


def get_all_dev_mode_property_set(app_id=None):
    url = ''
    if app_id is not None:
        url += 'appliance_id=%s' % str(app_id)
    if len(url) > 0:
        url = '?' + url
    return _create_req(url=url)


def get_dev_mode_property_set(_id):
    url = '/%s' % str(_id)
    return _create_req(url=url)


def update_dev_mode_property_set(_id, name=None, description=None,
                                 shared=None, scalable=None,
                                 preference_cpu=1, preference_memory=1024, preference_disk=10240,
                                 security_proxy_id=1):
    url = '/%s' % str(_id)
    _data = {'id': str(_id)}
    if name is not None:
        _data['name'] = name
    if description is not None:
        _data['description'] = description
    if shared is not None:
        _data['shared'] = shared
    if scalable is not None:
        _data['scalable'] = scalable
    if preference_cpu is not None:
        _data['preference_cpu'] = preference_cpu
    if preference_memory is not None:
        _data['preference_memory'] = preference_memory
    if preference_disk is not None:
        _data['preference_disk'] = preference_disk
    if security_proxy_id is not None:
        _data['security_proxy_id'] = security_proxy_id
    body = {'dev_mode_property_set': _data}
    body = simplejson.dumps(body)
    return _create_req(method=tools.HTTP_PUT, url=url, body=body, headers={'Content-Length': len(body),
                                                                           'Content-Type': 'application/json'})


if __name__ == '__main__':
    print get_all_dev_mode_property_set()
    print '----'

    print get_dev_mode_property_set(0)
    print '----'

    print update_dev_mode_property_set(0)
