from flask import Blueprint, redirect, url_for, flash, render_template, request
from flask_login import current_user, login_user, logout_user, login_required

from mypyblog import bcrypt, db
from mypyblog.korisnici.forms import RegistrationaForma, LoginForma, AzurirajProfilForma, ZahtevajResetFormu, \
    ResetPasswordForma
from mypyblog.korisnici.utils import sacuvaj_sliku, posalji_reset_email
from mypyblog.models import Korisnik, Post

korisnici = Blueprint('korisnici', __name__)

@korisnici.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationaForma()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        korisnik = Korisnik(korisnicko_ime=form.korisnicko_ime.data, email=form.email.data, password=hashed_password)
        db.session.add(korisnik)
        db.session.commit()
        flash(f'Nalog je uspesno napravljen za korisnico ime: {form.korisnicko_ime.data}! Mozete se ulogovati!', 'success')
        return redirect(url_for('korisnici.login'))
    return render_template('register.html', title='Registracija', form=form)

@korisnici.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForma()
    if form.validate_on_submit():
        korisnik = Korisnik.query.filter_by(email=form.email.data).first()
        if korisnik and bcrypt.check_password_hash(korisnik.password, form.password.data):
            login_user(korisnik, remember=form.zapamti_me.data)
            sledeca_strana = request.args.get('next')
            if sledeca_strana:
                return redirect(sledeca_strana)
            else:
                return redirect(url_for('main.home'))
        else:
            flash('Neuspesno logovanje. Molim vas da proverite unete podatke.', 'danger')
    return render_template('login.html', title='Login', form=form)

@korisnici.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@korisnici.route("/profil", methods=['GET', 'POST'])
@login_required
def profil():
    form = AzurirajProfilForma()
    if form.validate_on_submit():

        if form.slika.data:
            slika_fajl = sacuvaj_sliku(form.slika.data)
            current_user.slika_fajl = slika_fajl

        current_user.korisnicko_ime = form.korisnicko_ime.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Vas profil je uspesno azuriran', 'success')
        return redirect(url_for('korisnici.profil'))

    elif request.method == 'GET':
        form.korisnicko_ime.data = current_user.korisnicko_ime
        form.email.data = current_user.email
    slika_fajl = url_for('static', filename='profilne_slike/' + current_user.slika_fajl)
    return render_template("profil.html", title='Profil', slika_fajl=slika_fajl, form=form)


@korisnici.route("/korisnik/<string:korisnicko_ime>")
def postovi_korisnika(korisnicko_ime):
    page = request.args.get('page', 1, type=int)
    korisnik = Korisnik.query.filter_by(korisnicko_ime=korisnicko_ime).first_or_404()
    posts = Post.query.filter_by(author=korisnik).order_by(Post.datum_posta.desc()).paginate(page=page, per_page=5)
    return render_template('korisnicki_post.html', posts=posts, korisnik=korisnik)



@korisnici.route("/restart_passworda", methods=['GET', 'POST'])
def zahtev_za_restart():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = ZahtevajResetFormu()
    if form.validate_on_submit():
        korisnik = Korisnik.query.filter_by(email=form.email.data).first()
        posalji_reset_email(korisnik)
        flash('E-mail sa instrukcijama za restartovanje passworda je poslat.', 'success')
        return redirect(url_for('korisnici.login'))

    return render_template('password_restart_zahtev.html', title='Restart Passworda', form=form)


@korisnici.route("/restart_passworda/<token>", methods=['GET', 'POST'])
def restart_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    korisnik = Korisnik.proveri_rest_token(token)
    if korisnik is None:
        flash('Token nije validan ili je istekao', 'warning')
        return redirect(url_for('korisnici.zahtev_za_restart'))
    form = ResetPasswordForma()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        korisnik.password = hashed_password
        db.session.commit()
        flash(f'Password je uspesno azuriran, mozete se ulogovati!', 'success')
        return redirect(url_for('korisnici.login'))
    return render_template('restart_token.html', title='Restart Passworda', form=form)
