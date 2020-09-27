# model.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators


class PWDForm(FlaskForm):
    entity_name = StringField('Entity Name',[validators.DataRequired()])
    entity_username = StringField('Username',[validators.DataRequired()])
    password = StringField('Password', [validators.DataRequired()])
    ticket = StringField('Ticket', [validators.DataRequired()])
    submit = SubmitField('Submit')
