from datetime import datetime

from flask import redirect, url_for, render_template, flash, request
from flask_login import login_required, logout_user, login_user, current_user

from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, PostForm

from app.models import User, Post, Category


@app.route("/")
@app.route('/home')
def home():
    return render_template('index.html', posty=posty)


@app.route("/about/")
def about_me():
    dane = {'tytul': "Strona o mnie", 'tresc': "Witaj na stronie o mnie."}
    return render_template("omnie.html", tytul=dane["tytul"], tresc=dane["tresc"])


@app.route("/info/")
def info():
    dane = {'tytul': "Informacje", 'tresc': "Bardzo istotne informacje."}
    return render_template("info.html", tytul=dane["tytul"], tresc=dane["tresc"])


@app.route("/posty/")
def posty():
    dane = {'tytul': "Wpisy", 'tresc': "Historia wpisów na blogu"}
    posty = [
        {
            'author': {'username': 'Krzysztof'},
            'tytul': 'Blog Post 1',
            'body': 'Najlepszy wpis na świecie!',
            'data_publikacji': 'Czerwiec 18, 2020'
        },
        {
            'author': {'username': 'Małgorzata'},
            'tytul': 'Blog Post 2',
            'body': 'Recenzja najnowszej książki Żulczyka.',
            'data_publikacji': 'Maj 22, 2020'
        }]
    return render_template("posty.html", tytul=dane["tytul"], tresc=dane["tresc"], posty=posty)


@app.route("/rejestracja", methods=['GET', 'POST'])
def register():
    tytul = 'Rejestracja użytkownika'
    if current_user.is_authenticated:
        return redirect(url_for(request.url))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Konto {form.username.data} zostało pomyślnie utworzone. Możesz się zalogować.', 'success')
        return redirect(url_for('login'))
    return render_template('rejestracja.html', tytul='Rejestracja', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for(request.url))
    form = LoginForm()
    tytul = 'Zaloguj się'
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Logowanie nie powiodło się. Niepoprawny login lub hasło.', 'danger')
            return redirect(request.url)
    return render_template('formularz_logowania.html', tytul=tytul, form=form)


# procedura obslugi blegu logowania
@app.errorhandler(401)
def page_not_found(e):
    tytul = "Coś poszło nie tak..."
    blad = "401"
    return render_template('blad.html', tytul=tytul, blad=blad)


@app.errorhandler(500)
def internal_server_error(e):
    tytul = "Internal Server Error"
    blad = "500"
    return render_template('blad.html', tytul=tytul, blad=blad)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    tytul = "Wylogowanie"
    return render_template('logout.html', tytul=tytul)


@app.route("/account")
@login_required
def account():
    tytul = 'Twoje konto'
    image_file = url_for('static', filename="profile_pics/" + current_user.image_file)
    return render_template('account.html', tytul=tytul, image_file=image_file)


@app.route("/admin", methods=['GET', 'POST'])
@login_required
def admin():
    tytul = 'Admin panel'
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Twój post został udostępniony', 'success')
        return redirect(url_for('posty'))
    return render_template('admin_panel.html', tytul=tytul, form=form)