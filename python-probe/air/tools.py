import httplib
import simplejson
import traceback

import config


__author__ = 'paoolo'

HTTP_GET = 'GET'
HTTP_POST = 'POST'
HTTP_PUT = 'PUT'
HTTP_DELETE = 'DELETE'


def catch_exception(func):
    def inner_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            traceback.print_exc()

    return inner_func


def create_req(method, url, body=None, headers=None):
    if not headers:
        headers = {}
    connection = httplib.HTTPConnection(config.URL)
    headers['PRIVATE-TOKEN'] = config.PRIVATE_TOKEN
    connection.request(method, config.PREFIX + url, body, headers=headers)
    response = connection.getresponse()
    content = response.read()
    data = simplejson.loads(content)
    response.close()
    connection.close()
    return data
