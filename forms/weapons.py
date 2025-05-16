from flask_wtf import FlaskForm
from sqlalchemy import String
from werkzeug.sansio.multipart import Field
from wtforms import PasswordField, SubmitField, EmailField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import BooleanField, StringField
from wtforms.validators import DataRequired



class AddJobForm(FlaskForm):

    submit = SubmitField('Войти')