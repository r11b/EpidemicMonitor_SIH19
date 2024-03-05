from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo


class AdminLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class AdminCreateForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Password (again)', validators=[DataRequired(),
                              EqualTo('password')])
    submit = SubmitField('Create')


class DiseaseAddForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    desc = StringField('Description')
    type_ = StringField('Type')
    symptoms = TextAreaField('Symptoms')
    diagnosis = TextAreaField('Diagnosis')
    complications = TextAreaField('Complications')
    transmissions = TextAreaField('Transmissions')
    causes = TextAreaField('Causes')
    deaths = StringField('Deaths')
    onset = StringField('Onset')
    medications = TextAreaField('Medications')
    links = TextAreaField('Links')
    submit = SubmitField('Add')


class DiseaseEditForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    desc = StringField('Description')
    type_ = StringField('Type')
    symptoms = TextAreaField('Symptoms')
    diagnosis = TextAreaField('Diagnosis')
    complications = TextAreaField('Complications')
    transmissions = TextAreaField('Transmissions')
    causes = TextAreaField('Causes')
    deaths = StringField('Deaths')
    onset = StringField('Onset')
    medications = TextAreaField('Medications')
    links = TextAreaField('Links')
    submit = SubmitField('Edit')


class DiseaseSearchForm(FlaskForm):
    search = StringField('', validators=[DataRequired()])
    submit = SubmitField('Search')


class HospitalAddForm(FlaskForm):
    id = StringField('ID')
    name = StringField('Name', validators=[DataRequired()])
    address = StringField('Address')
    longitude = StringField('Longitude')
    latitude = StringField('Latitude')
    contact = TextAreaField('Contact')
    website = StringField('Website')
    submit = SubmitField('Add')


class HospitalEditForm(FlaskForm):
    id = StringField('ID')
    name = StringField('Name', validators=[DataRequired()])
    address = StringField('Address')
    longitude = StringField('Longitude')
    latitude = StringField('Latitude')
    contact = TextAreaField('Contact')
    website = StringField('Website')
    submit = SubmitField('Edit')


class HospitalSearchForm(FlaskForm):
    search = StringField('', validators=[DataRequired()])
    submit = SubmitField('Search')
