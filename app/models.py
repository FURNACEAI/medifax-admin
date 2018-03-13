import requests
import json
from app import login
from flask_login import UserMixin
from flask import session
from app import config as cfg

class Customer():
    headers = {'user-agent': 'medifax/0.0.1', "Content-Type":"application/json" }
    user_id = ''
    first_name = ''

    def edit(self, form):
        return True


    def create(self, form):
        """ Creates a new customer record via an AWS Lambda function """
        payload = {
            "first_name": form.first_name.data,
            "middle_initial": form.middle_initial.data,
            "last_name": form.last_name.data,
            "email": form.email.data,
            "home_phone": form.home_phone.data,
            "mobile_phone": form.mobile_phone.data,
            "street_address": form.street_address.data,
            "street_address_2": form.street_address_2.data,
            "city": form.city.data,
            "state": form.state.data,
            "zipcode": form.zipcode.data,
            "dob": form.dob.data
        }
        url = "%s%s%s" % (cfg._AWS['customers']['base'],cfg._AWS['status'],cfg._AWS['customers']['add'])
        payload = json.dumps(payload)
        r = requests.post(url, headers=self.headers, data=payload)
        req = r.json()
        if req['message'] == 'Success':
            self.id = req['id']
            return True
        else:
            return False


class User(UserMixin):
    headers = {'user-agent': 'medifax/0.0.1', "Content-Type":"application/json" }
    user_id = ''
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

    def load(self, id):
        url = "https://3ts6m0h20j.execute-api.us-east-1.amazonaws.com/dev/employee/%s" % id
        r = requests.get(url).json()
        self.user_id = r['id']
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
    u = user.load(id)
    session['user_first_name'] = u.first_name
    session['user_id'] = u.user_id
    return u
