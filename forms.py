from flask_wtf import FlaskForm
from helpers import getters_mapping, napalm_actions, scheduler_choices
from wtforms import *
from wtforms.validators import DataRequired, EqualTo, Length, optional
from flask_wtf.file import FileAllowed
from netmiko.ssh_dispatcher import CLASS_MAPPER as netmiko_dispatcher

## Form for registering / logging in 

class RegisterForm(FlaskForm):
    length_validator = [DataRequired(), Length(min=6, max=25)]
    match_constraint = EqualTo('password', message='Passwords must match')
    match_validator = [DataRequired(), match_constraint]

    name = TextField('Username', length_validator)
    email = TextField('Email', length_validator)
    password = PasswordField('Password', length_validator)
    confirm = PasswordField('Repeat Password', match_validator)

class LoginForm(FlaskForm):
    name = TextField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])

class ForgotForm(FlaskForm):
    email = TextField('Email', validators=[DataRequired(), Length(min=6, max=40)])

class TestForm(FlaskForm):
    department = SelectField('', choices=())
    employee = SelectField('', choices=())
    
## Forms for managing devices
    
# devices can be added to the database either one by one via the AddDevice
# form, or all at once by importing an Excel or a CSV file.
class AddDevice(FlaskForm):
    hostname = TextField('Hostname', [optional()])
    ip_address = TextField('IP address', [optional()])
    os = TextField('Operating System', [optional()])
    
class AddDevices(FlaskForm):
    validators = [FileAllowed(['xls', 'xlsx', 'csv'], 'Excel or CSV file only')]
    file = FileField('', validators=validators)
    
class DeleteDevice(FlaskForm):
    devices = SelectMultipleField('Devices', choices=())
    
## Forms for Netmiko
    
class NetmikoForm(FlaskForm):
    username = TextField('Username', [optional()])
    password = PasswordField('Password', [optional()])
    secret = PasswordField('Secret password', [optional()])
    port = IntegerField('Port', [optional()], default=8022)
    
    # exclude base driver from Netmiko available drivers
    exclude_base_driver = lambda driver: 'telnet' in driver or 'ssh' in driver
    netmiko_drivers = sorted(tuple(filter(exclude_base_driver, netmiko_dispatcher)))
    drivers = [(driver, driver) for driver in netmiko_drivers]
    driver = SelectField('', [optional()], choices=drivers)
    
    global_delay_factor = FloatField('global_delay_factor', [optional()], default=1.)
    raw_script = TextAreaField('', [optional(), Length(max=200)])
    file = FileField('', validators=[FileAllowed(['yaml'], 'YAML only')])
    devices = SelectMultipleField('Devices', choices=())
    
## Forms for NAPALM

class NapalmGettersForm(FlaskForm):
    username = TextField('Username', [optional()])
    password = PasswordField('Password', [optional()])
    secret = PasswordField('Secret password', [optional()])
    port = IntegerField('Port', [optional()], default=8022)
    
    protocol_choices = (('Telnet',)*2, ('SSH',)*2, ('HTTP',)*2, ('HTTPS',)*2)
    protocol = RadioField('', [optional()], choices=protocol_choices)
    devices = SelectMultipleField('', [optional()], choices=())
    function_choices = [(function, function) for function in getters_mapping]
    functions = SelectMultipleField('Devices', choices=function_choices)
    scheduler_intervals = [(option, option) for option in scheduler_choices]
    scheduler = SelectField('', [optional()], choices=scheduler_intervals)
    output = TextAreaField('', [optional()])

class NapalmParametersForm(FlaskForm):
    username = TextField('Username', [optional()])
    password = PasswordField('Password', [optional()])
    secret = PasswordField('Secret password', [optional()])
    port = IntegerField('Port', [optional()], default=8022)
    
    protocol_choices = (('Telnet',)*2, ('SSH',)*2, ('HTTP',)*2, ('HTTPS',)*2)
    protocol = RadioField('', [optional()], choices=protocol_choices)
    action_choices = [(action, action) for action in napalm_actions]
    actions = SelectField('Actions', [optional()], choices=action_choices)
    raw_script = TextAreaField('', [optional(), Length(max=200)])
    file = FileField('', validators=[FileAllowed(['yaml'], 'YAML only')])
    devices = SelectMultipleField('Devices', choices=())
    format = 'Format: 2009-11-06 16:30:05'
    scheduler = TextField(format, [optional()])
    