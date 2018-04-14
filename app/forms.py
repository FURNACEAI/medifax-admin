from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, SelectField, TextAreaField, FieldList, HiddenField, FileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

STATE_ABBREV = [('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('FL', 'Florida'), ('GA', 'Georgia'),
                ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IO', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'),
                ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'),
                ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'),
                ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virgina'), ('WA', 'Washington'), ('WV', 'West Virgina'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')]

GENDER = [('', "Select a Gender"), ('Male', 'Male'), ('Female', 'Female')]
BLOOD_TYPE = [('', "Select a Blood Type"), ('O+', 'O+'), ('O-', 'O-'), ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-')]
IMG_TYPE = [('medical', 'Medical'), ('dental', 'Dental')]

SUB_STATUS = [('Awaiting HIPAA Consent', 'Awaiting HIPAA Consent'), ('HIPAA Consent Received', 'HIPAA Consent Received')]

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class AddEmployeeForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    user_role = SelectField('Role', choices=[('admin','Admin'),('manager','Manager'), ('staff','Staff')], validators=[DataRequired()])
    active = SelectField('Active Account', choices=[('true',' Yes '),('false',' No ')], validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Save')

class CreateCustomerForm(FlaskForm):
    """ """
    # Identity
    first_name = StringField('First Name', validators=[DataRequired()])
    middle_initial = StringField('Middle Initial')
    last_name = StringField('Last Name', validators=[DataRequired()])
    # Contact
    email = StringField('Email', validators=[DataRequired()])
    home_phone = StringField('Home Phone')
    mobile_phone = StringField('Mobile Phone', validators=[DataRequired()])
    # Address
    street_address = StringField('Street Address', validators=[DataRequired()])
    street_address_2 = StringField('Street Address 2')
    city = StringField('City', validators=[DataRequired()])
    state = SelectField('State', choices=STATE_ABBREV, validators=[DataRequired()])
    zipcode = StringField('ZIP', validators=[DataRequired()])
    # DOB
    dob = StringField('Date of Birth', validators=[DataRequired()])

    # Actions
    submit = SubmitField('Create Customer')

class EditCustomerForm(CreateCustomerForm):
    user_id = HiddenField('User ID')
    # Physical Exam
    blood_pressure_systolic = StringField('Blood Pressure Systolic')
    blood_pressure_diastolic = StringField('Blood Pressure Diastolic')
    heart_rate = StringField('Heart Rate')
    height = StringField('Height')
    weight = StringField('Weight')
    bmi = StringField('BMI')
    access_code = StringField('Access Code')

    # Medications
    medication_name_0 = StringField('Medication Name')
    medication_name_1 = StringField('Medication Name')
    medication_name_2 = StringField('Medication Name')
    medication_name_3 = StringField('Medication Name')
    medication_name_4 = StringField('Medication Name')
    medication_name_5 = StringField('Medication Name')
    medication_name_6 = StringField('Medication Name')
    medication_name_7 = StringField('Medication Name')
    medication_name_8 = StringField('Medication Name')
    medication_name_9 = StringField('Medication Name')

    medication_dose_0 = StringField('Medication Dosage')
    medication_dose_1 = StringField('Medication Dosage')
    medication_dose_2 = StringField('Medication Dosage')
    medication_dose_3 = StringField('Medication Dosage')
    medication_dose_4 = StringField('Medication Dosage')
    medication_dose_5 = StringField('Medication Dosage')
    medication_dose_6 = StringField('Medication Dosage')
    medication_dose_7 = StringField('Medication Dosage')
    medication_dose_8 = StringField('Medication Dosage')
    medication_dose_9 = StringField('Medication Dosage')

    medication_freq_0 = StringField('Medication Frequency')
    medication_freq_1 = StringField('Medication Frequency')
    medication_freq_2 = StringField('Medication Frequency')
    medication_freq_3 = StringField('Medication Frequency')
    medication_freq_4 = StringField('Medication Frequency')
    medication_freq_5 = StringField('Medication Frequency')
    medication_freq_6 = StringField('Medication Frequency')
    medication_freq_7 = StringField('Medication Frequency')
    medication_freq_8 = StringField('Medication Frequency')
    medication_freq_9 = StringField('Medication Frequency')

    # Medical / Lifestyle History
    current_problems_0 = StringField('Current Problems')
    current_problems_1 = StringField('Current Problems')
    current_problems_2 = StringField('Current Problems')
    current_problems_3 = StringField('Current Problems')
    current_problems_4 = StringField('Current Problems')
    current_problems_5 = StringField('Current Problems')
    current_problems_6 = StringField('Current Problems')
    current_problems_7 = StringField('Current Problems')
    current_problems_8 = StringField('Current Problems')
    current_problems_9 = StringField('Current Problems')

    gender = SelectField('Gender', choices=GENDER)
    blood_type = SelectField('Blood Type', choices=BLOOD_TYPE)
    patient_preferences = TextAreaField('Patient Preferences')
    patient_consents = TextAreaField('Emergency Contact')
    family_history = TextAreaField('Family History')
    lifestyle_history = TextAreaField('Lifestyle')
    social_history = TextAreaField('Social History')
    care_plan = TextAreaField('Care Plan')
    lab_results = TextAreaField('Recent Lab Results')
    referrals = TextAreaField('Referrals')
    allergies = TextAreaField('Precautions, Alergies, and Alerts')

    # Subscription Status
    active = SelectField('Account Active?', choices=[('true',' Yes '),('false',' No ')])
    status = SelectField('Account Status', choices=SUB_STATUS)

    # Dental History
    dentist_name = StringField('Dentist Name')
    dentist_phone = StringField('Dentist Phone')
    dentist_email = StringField('Dentist Email')

    dental_condition = TextAreaField('Current Dental Condition')

    # Dental Insurance
    ins_planid_dental = StringField('Insurance Plan ID')
    ins_provider_dental = StringField('Insurance Provider')
    ins_street_addr_dental = StringField('Dental Insurance Street Address')
    ins_city_dental = StringField('Dental Insurance City')
    ins_state_dental = StringField('Dental Insurance State')
    ins_zipcode_dental = StringField('Dental Insurance ZIP')
    ins_phone_dental = StringField('Dental Insurance Phone')
    ins_email_dental = StringField('Dental Insurance Email')

    # Medical Insurance
    ins_planid_med = StringField('Insurance Plan ID')
    ins_provider_med = StringField('Insurance Provider')
    ins_street_addr_med = StringField('Street Address')
    ins_city_med = StringField('City')
    ins_state_med = StringField('State')
    ins_zipcode_med = StringField('ZIP')
    ins_phone_med = StringField('Phone')
    ins_email_med = StringField('Email')

    img_name = StringField('Image Name')
    img_desc = TextAreaField('Image Description')
    img_type = SelectField('File Type', choices=IMG_TYPE)
    img_file = FileField('Image')
    img_submit = SubmitField('Upload')

    # Actions
    submit = SubmitField('Create Customer')
