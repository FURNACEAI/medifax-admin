import os

_AWS = {
    'status': 'dev',
    'base' : 'https://3ts6m0h20j.execute-api.us-east-1.amazonaws.com/',
    'employees': {
        'list': '/employee/list',
        'add': '/employee/create',
        'delete': '/employee/delete/',
        'update': '/employee/update/',
        'get': '/employee/',
        'auth': '/employee/auth'
    },
    'customers': {
        'list': '/employee/list',
        'add': '/employee/create',
        'delete': '/employee/delete/',
        'update': '/employee/update/',
        'get': '/employee/',
        'auth': '/employee/auth'
    }
}

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ba62343d-31e4-4cbe-957c-cbc1f0e30a14'
