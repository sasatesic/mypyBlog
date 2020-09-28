from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError

from mypyblog.models import Korisnik


class RegistrationaForma(FlaskForm):
    korisnicko_ime = StringField('Korisnicko Ime', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('E-mail Adresa', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=20)])
    confirm_password = PasswordField('Potvrdi Password',
                                     validators=[DataRequired(), EqualTo('password'), Length(min=4, max=20)])
    submit = SubmitField('Potvrdi Registraciju')

    def validate_korisnicko_ime(self, korisnicko_ime):
        korisnik = Korisnik.query.filter_by(korisnicko_ime=korisnicko_ime.data).first()
        if korisnik:
            raise ValidationError('Izabrano korisnicko ime je zauzeto. Molim vas izaberite neko drugo.')

    def validate_email(self, email):
        korisnik = Korisnik.query.filter_by(email=email.data).first()
        if korisnik:
            raise ValidationError('Izabrana email adresa je zauzeta. Molim vas izaberite neku drugu.')


class LoginForma(FlaskForm):
    email = StringField('E-mail Adresa', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=20)])
    zapamti_me = BooleanField('Zapamti Me')
    submit = SubmitField('Uloguj Se')


class AzurirajProfilForma(FlaskForm):
    korisnicko_ime = StringField('Korisnicko Ime', validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('E-mail Adresa', validators=[DataRequired(), Email()])
    slika = FileField('Azuriraj Profilnu Sliku',
                      validators=[FileAllowed(['jpg', 'png'], message="Molim vas izaberite sliku u odgovarajucem formatu!")])
    submit = SubmitField('Azuriraj')

    def validate_korisnicko_ime(self, korisnicko_ime):
        if korisnicko_ime.data != current_user.korisnicko_ime:
            korisnik = Korisnik.query.filter_by(korisnicko_ime=korisnicko_ime.data).first()
            if korisnik:
                raise ValidationError('Izabrano korisnicko ime je zauzeto. Molim vas izaberite neko drugo.')

    def validate_email(self, email):
        if email.data != current_user.email:
            korisnik = Korisnik.query.filter_by(email=email.data).first()
            if korisnik:
                raise ValidationError('Izabrana email adresa je zauzeta. Molim vas izaberite neku drugu.')

            class ZahtevajResetFormu(FlaskForm):
                email = StringField('E-mail Adresa', validators=[DataRequired(), Email()])
                submit = SubmitField('Zahtevaj restartovanje passworda')

                def validate_email(self, email):
                    korisnik = Korisnik.query.filter_by(email=email.data).first()
                    if korisnik is None:
                        raise ValidationError('Uneta email adresa ne postoji.')

            class ResetPasswordForma(FlaskForm):
                password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=20)])
                confirm_password = PasswordField('Potvrdi Password',
                                                 validators=[DataRequired(), EqualTo('password'),
                                                             Length(min=4, max=20)])
                submit = SubmitField('Restartuj Password')


class ZahtevajResetFormu(FlaskForm):
    email = StringField('E-mail Adresa', validators=[DataRequired(), Email()])
    submit = SubmitField('Zahtevaj restartovanje passworda')

    def validate_email(self, email):
        korisnik = Korisnik.query.filter_by(email=email.data).first()
        if korisnik is None:
            raise ValidationError('Uneta email adresa ne postoji.')


class ResetPasswordForma(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=20)])
    confirm_password = PasswordField('Potvrdi Password',
                                     validators=[DataRequired(), EqualTo('password'), Length(min=4, max=20)])
    submit = SubmitField('Restartuj Password')