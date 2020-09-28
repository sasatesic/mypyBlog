from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from mypyblog import db, login_manager, app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(id_korisnika):
    return Korisnik.query.get(int(id_korisnika))

class Korisnik(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    korisnicko_ime = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    slika_fajl = db.Column(db.String(20), nullable=False, default='defaultna.jpg')
    password = db.Column(db.String(70), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def dodaj_reset_token(self, istice_sek=1800):
        s = Serializer(app.config['SECRET_KEY'], istice_sek)
        return s.dumps({'id_korisnika': self.id}).decode('utf-8')


    @staticmethod
    def proveri_rest_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            id_korisnika = s.loads(token)['id_korisnika']
        except:
            return None
        return Korisnik.query.get(id_korisnika)


    def __repr__(self):
        return f"Korisnik('{self.korisnicko_ime}', '{self.email}', '{self.slika_fajl}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    naslov = db.Column(db.String(100), nullable=False)
    datum_posta = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    sadrzaj = db.Column(db.Text, nullable=False)
    id_korisnika = db.Column(db.Integer, db.ForeignKey('korisnik.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.naslov}', '{self.datum_posta}')"