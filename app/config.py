import os

_AWS = {
    'headers': {'user-agent': 'medifax/0.0.1', "Content-Type":"application/json" },
    'status': 'dev',
    'employees': {
        'base' : 'https://3ts6m0h20j.execute-api.us-east-1.amazonaws.com/',
        'list': '/employee/list',
        'add': '/employee/create',
        'delete': '/employee/delete/',
        'update': '/employee/update/',
        'get': '/employee/',
        'auth': '/employee/auth'
    },
    'customers': {
        'base' : 'https://7z6lcegucj.execute-api.us-east-1.amazonaws.com/',
        'list': '/customers/list',
        'add': '/customers/create',
        'delete': '/customers/',
        'update': '/customers/update/',
        'get': '/customers/',
        'auth': '/customers/auth'
    }
}

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ba62343d-31e4-4cbe-957c-cbc1f0e30a14'
