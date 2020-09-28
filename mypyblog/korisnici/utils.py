import os
import secrets

from PIL import Image
from flask_mail import Message

from mypyblog import app, mail


def sacuvaj_sliku(slika):
    nasumicni_hex = secrets.token_hex(8)
    _, f_ekstenzija = os.path.splitext(slika.filename)
    ime_fajla_slike = nasumicni_hex + f_ekstenzija
    put_do_slike = os.path.join(app.root_path, 'static/profilne_slike', ime_fajla_slike)

    velicina_slike = (125, 125)
    s = Image.open(slika)
    s.thumbnail(velicina_slike)
    s.save(put_do_slike)

    return ime_fajla_slike


def url_for(param, token, _external):
    pass


def posalji_reset_email(korisnik):
    token = korisnik.dodaj_reset_token()
    poruka = Message('Zahtev Za Resetovanje Passworda', sender='mojpyblogrs@gmail.com', recipients=[korisnik.email])
    poruka.body = f''' Da bi ste resetovali vas password, posetite sledeci link:
    {url_for('korisnici.restart_token', token=token, _external=True)}    
    '''
    mail.send(poruka)