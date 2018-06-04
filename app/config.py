import os

_AWS = {
    'headers': {'user-agent': 'medifax/0.0.1', "Content-Type":"application/json" },
    'status': 'prod',
    'employees': {
        'base' : 'https://5y96pktw7j.execute-api.us-east-1.amazonaws.com/',
        'list': '/employee/list',
        'add': '/employee/create',
        'delete': '/employee/delete/',
        'update': '/employee/update/',
        'get': '/employee/',
        'auth': '/employee/auth'
    },
    'customers': {
        'base' : 'https://u3tad4wx2c.execute-api.us-east-1.amazonaws.com/',
        'list': '/customers/list',
        'add': '/customers/create',
        'delete': '/customers/',
        'update': '/customers/update/',
        'onetimes3url': '/customers/onetimes3url',
        'get': '/customers/',
        'auth': '/customers/auth'
    }
}

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ba62343d-31e4-4cbe-957c-cbc1f0e30a14'
