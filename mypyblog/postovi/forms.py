from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class PostForma(FlaskForm):
    naslov = StringField('Naslov', validators=[DataRequired()])
    sadrzaj = TextAreaField('Sadrzaj', validators=[DataRequired()])
    submit = SubmitField('Postavi')
