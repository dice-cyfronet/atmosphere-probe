import simplejson

from air import tools, appliance_sets


__author__ = 'paoolo'


@tools.catch_exception
def create_app(_app_set_id):
    body = {'appliance': {'appliance_set_id': _app_set_id, 'configuration_template_id': 1}}
    data = tools.create_req(method=tools.HTTP_POST, url='/api/v1/appliances', body=simplejson.dumps(body))
    return data['appliance']['id']


@tools.catch_exception
def delete_app(_app_id):
    tools.create_req(method=tools.HTTP_DELETE, url='/api/v1/appliances/%s' % _app_id)


if __name__ == '__main__':
    app_set_id = appliance_sets.create_app_set()
    print app_set_id
    app_id = create_app(app_set_id)
    print app_id
    delete_app(app_id)
    appliance_sets.delete_app_set(app_set_id)
