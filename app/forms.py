from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length

class AddUserForm(FlaskForm):
    nickname = StringField("Nickname", validators=[DataRequired(), Length(min=3, max=20)])
    submit = SubmitField("Add User")
