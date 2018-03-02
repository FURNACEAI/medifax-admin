import requests
import json
from app import login
from flask_login import UserMixin

class User(UserMixin):
    headers = {'user-agent': 'medifax/0.0.1', "Content-Type":"application/json" }
    id = ''
    first_name = ''

    def add(self, first_name, last_name, password, email, role, active):
        payload = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password,
            "user_role": role,
            "active": active
        }
        payload = json.dumps(payload)
        r = requests.post('https://3ts6m0h20j.execute-api.us-east-1.amazonaws.com/dev/employee/create', headers=self.headers, data=payload)
        req = r.json()
        if req['message'] == 'Success':
            self.id = req['id']
            return True
        else:
            return False

    def auth(self, username, password):
        """
        Authenticates a user against an AWS Lambda function
        """
        payload = '{"email": "%s", "password": "%s"}' % (username, password)
        # payload = json.dumps(payload)
        r = requests.post('https://3ts6m0h20j.execute-api.us-east-1.amazonaws.com/dev/employee/auth', headers=self.headers, data=payload)
        req = r.json()
        if req['message'] == 'Success':
            self.id = req['id']
            return True
        else:
            return False

    def fetch(self, id):
        url = "https://3ts6m0h20j.execute-api.us-east-1.amazonaws.com/dev/employee/%s" % id
        r = requests.get(url).json()
        self.id = r['id']
        self.first_name = r['name']['first']
        return self

    def set_password(self, password):
        pass

    def check_password(self, password):
        pass

@login.user_loader
def load_user(id):
    user = User()
    # return User.get(id)
    return user.fetch(id)
