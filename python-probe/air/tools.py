import httplib
import simplejson

import config


__author__ = 'paoolo'

HTTP_GET = 'GET'
HTTP_POST = 'POST'
HTTP_PUT = 'PUT'
HTTP_DELETE = 'DELETE'


def create_req(method, url, body=None, headers=None):
    if not headers:
        headers = {}
    connection = httplib.HTTPConnection(config.API_URL)
    headers['PRIVATE-TOKEN'] = config.API_PRIVATE_TOKEN
    connection.request(method, config.API_PREFIX + url, body, headers=headers)
    response = connection.getresponse()
    content = response.read()
    try:
        data = simplejson.loads(content)
    except simplejson.JSONDecodeError as e:
        data = {}
    response.close()
    connection.close()
    return data
