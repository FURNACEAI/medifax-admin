import requests
import json
from app import login
from flask_login import UserMixin
from flask import session
from app import config as cfg
from uuid import uuid4
import boto
import os.path
from werkzeug.utils import secure_filename

class Customer():
    headers = {'user-agent': 'medifax/0.0.1', "Content-Type":"application/json" }
    user_id = ''
    first_name = ''

    def edit(self, form, rform):
        """"""
        #for x in form:
        #   print(x.name)
        payload = {
            "first_name": form.first_name.data,
            "middle_initial": form.middle_initial.data,
            "last_name": form.last_name.data,
            "password": "",
            "email": form.email.data,
            "home_phone": form.home_phone.data,
            "mobile_phone": form.mobile_phone.data,
            "street_address": form.street_address.data,
            "street_address_2": form.street_address_2.data,
            "city": form.city.data,
            "state": form.state.data,
            "zipcode": form.zipcode.data,
            "dob": form.dob.data,
            "blood_pressure_systolic": form.blood_pressure_systolic.data,
            "blood_pressure_diastolic": form.blood_pressure_diastolic.data,
            "blood_type": form.blood_type.data,
            "heart_rate": form.heart_rate.data,
            "height": form.height.data,
            "weight": form.weight.data,
            "active": form.active.data,
            "status": form.status.data,
            "gender": form.gender.data,
            "patient_preferences": form.patient_preferences.data,
            "family_history": form.family_history.data,
            "allergies": form.allergies.data,
            "patient_consents": form.patient_consents.data,
            "referrals": form.referrals.data,
            "lab_results": form.lab_results.data,
            "care_plan": form.care_plan.data,
            "lifestyle_history": form.lifestyle_history.data,
            "social_history": form.social_history.data,
            "current_problems_0": form['current_problems_0'].data,
            "current_problems_1": form['current_problems_1'].data,
            "current_problems_2": form['current_problems_2'].data,
            "current_problems_3": form['current_problems_3'].data,
            "current_problems_4": form['current_problems_4'].data,
            "current_problems_5": form['current_problems_5'].data,
            "current_problems_6": form['current_problems_6'].data,
            "current_problems_7": form['current_problems_7'].data,
            "current_problems_8": form['current_problems_8'].data,
            "current_problems_9": form['current_problems_9'].data,
            "medication_name_0": form['medication_name_0'].data,
            "medication_name_1": form['medication_name_1'].data,
            "medication_name_2": form['medication_name_2'].data,
            "medication_name_3": form['medication_name_3'].data,
            "medication_name_4": form['medication_name_4'].data,
            "medication_name_5": form['medication_name_5'].data,
            "medication_name_6": form['medication_name_6'].data,
            "medication_name_7": form['medication_name_7'].data,
            "medication_name_8": form['medication_name_8'].data,
            "medication_name_9": form['medication_name_9'].data,
            "medication_dose_0": form['medication_dose_0'].data,
            "medication_dose_1": form['medication_dose_1'].data,
            "medication_dose_2": form['medication_dose_2'].data,
            "medication_dose_3": form['medication_dose_3'].data,
            "medication_dose_4": form['medication_dose_4'].data,
            "medication_dose_5": form['medication_dose_5'].data,
            "medication_dose_6": form['medication_dose_6'].data,
            "medication_dose_7": form['medication_dose_7'].data,
            "medication_dose_8": form['medication_dose_8'].data,
            "medication_dose_9": form['medication_dose_9'].data,
            "medication_freq_0": form['medication_freq_0'].data,
            "medication_freq_1": form['medication_freq_1'].data,
            "medication_freq_2": form['medication_freq_2'].data,
            "medication_freq_3": form['medication_freq_3'].data,
            "medication_freq_4": form['medication_freq_4'].data,
            "medication_freq_5": form['medication_freq_5'].data,
            "medication_freq_6": form['medication_freq_6'].data,
            "medication_freq_7": form['medication_freq_7'].data,
            "medication_freq_8": form['medication_freq_8'].data,
            "medication_freq_9": form['medication_freq_9'].data,
            "dental_condition": form['dental_condition'].data,
            "dentist_name": form['dentist_name'].data,
            "dentist_email": form['dentist_email'].data,
            "dentist_phone": form['dentist_phone'].data,
            "ins_planid_dental": form['ins_planid_dental'].data,
            "ins_provider_dental": form['ins_provider_dental'].data,
            "ins_street_addr_dental": form['ins_street_addr_dental'].data,
            "ins_city_dental": form['ins_city_dental'].data,
            "ins_state_dental": form['ins_state_dental'].data,
            "ins_zipcode_dental": form['ins_zipcode_dental'].data,
            "ins_phone_dental": form['ins_phone_dental'].data,
            "ins_email_dental": form['ins_email_dental'].data,
            "ins_planid_med": form['ins_planid_med'].data,
            "ins_provider_med": form['ins_provider_med'].data,
            "ins_street_addr_med": form['ins_street_addr_med'].data,
            "ins_city_med": form['ins_city_med'].data,
            "ins_state_med": form['ins_state_med'].data,
            "ins_zipcode_med": form['ins_zipcode_med'].data,
            "ins_phone_med": form['ins_phone_med'].data,
            "ins_email_med": form['ins_email_med'].data,
            "bmi": form.bmi.data
        }
        print(payload)
        url = "%s%s%s%s" % (cfg._AWS['customers']['base'],cfg._AWS['status'],cfg._AWS['customers']['update'],form.user_id.data)
        payload = json.dumps(payload)
        r = requests.post(url, headers=self.headers, data=payload)
        print(r)
        req = r.json()
        print(req)
        # print("MSG: %s")  % req['message']
        if req['message'] == 'Success':
            self.id = req['id']
            return True
        else:
            return False




        #for x in form:
        #    print(x.name)
        #print("MED: %s " % form.medication_name.data)
        #print("Blood Pressure: %s " % form.blood_pressure_systolic.data)

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

    def s3_upload(source_file, upload_dir=None, acl='public-read'):
        """ Uploads WTForm File Object to Amazon S3
            Expects following app.config attributes to be set:
                S3_KEY              :   S3 API Key
                S3_SECRET           :   S3 Secret Key
                S3_BUCKET           :   What bucket to upload to
                S3_UPLOAD_DIRECTORY :   Which S3 Directory.
            The default sets the access rights on the uploaded file to
            public-read.  It also generates a unique filename via
            the uuid4 function combined with the file extension from
            the source file.
        """

        if upload_dir is None:
            upload_dir = app.config["S3_UPLOAD_DIRECTORY"]

        source_filename = secure_filename(source_file.data.filename)
        source_extension = os.path.splitext(source_filename)[1]

        destination_filename = uuid4().hex + source_extension

        # Connect to S3 and upload file.
        conn = boto.connect_s3(app.config["S3_KEY"], app.config["S3_SECRET"])
        b = conn.get_bucket(app.config["S3_BUCKET"])

        sml = b.new_key("/".join([upload_dir, destination_filename]))
        sml.set_contents_from_string(source_file.data.read())
        sml.set_acl(acl)

        return destination_filename


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

        r = requests.post('https://5y96pktw7j.execute-api.us-east-1.amazonaws.com/prod/employee/create', headers=self.headers, data=payload)
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
        url = "%s%s%s" % (cfg._AWS['employees']['base'],cfg._AWS['status'],cfg._AWS['employees']['auth'])
        print(url)
        r = requests.post(url, headers=self.headers, data=payload)
        req = r.json()
        if req['message'] == 'Success':
            self.id = req['id']
            return True
        else:
            return False

    def load(self, id):
        url = "https://5y96pktw7j.execute-api.us-east-1.amazonaws.com/prod/employee/%s" % id
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
    u = user.load(id)
    session['user_first_name'] = u.first_name
    session['user_id'] = u.user_id
    return u
