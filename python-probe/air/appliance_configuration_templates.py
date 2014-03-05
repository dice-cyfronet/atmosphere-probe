from air import tools

__author__ = 'paoolo'

PREFIX = '/appliance_configuration_templates'


def _create_req(method=tools.HTTP_GET, url='', body=None, headers=None):
    return tools.create_req(method, PREFIX + url, body, headers)


def get_all_app_config_temp():
    return _create_req()


if __name__ == '__main__':
    print get_all_app_config_temp()
    print '----'
