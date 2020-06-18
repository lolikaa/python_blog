from os import abort

from flask import redirect, url_for, render_template, flash, request
from flask_login import login_required, logout_user, login_user, current_user

from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, PostForm, UpdateAccountForm

from app.models import User, Post, Category


@app.route("/")
@app.route('/home')
def home():
    tytul = "Witaj"
    return render_template('index.html', tytul=tytul, posty=posty)


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
    posty = Post.query.all()
    # [
    #     {
    #         'author': {'username': 'Krzysztof'},
    #         'tytul': 'Blog Post 1',
    #         'body': 'Najlepszy wpis na świecie!',
    #         'data_publikacji': 'Czerwiec 18, 2020'
    #     },
    #     {
    #         'author': {'username': 'Małgorzata'},
    #         'tytul': 'Blog Post 2',
    #         'body': 'Recenzja najnowszej książki Żulczyka.',
    #         'data_publikacji': 'Maj 22, 2020'
    #     }]
    return render_template("posty.html", tytul=dane["tytul"], tresc=dane["tresc"], posty=posty)


@app.route("/posty/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title=post.title, post=post)


@app.route("/posty/<int:post_id>/edit", methods=['GET', 'POST'])
@login_required
def post_edit(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        db.session.commit()
        flash('Twój post został pomyślnie edytowany', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.body.data = post.body
    return render_template("admin.html", title=post.title + "edit", post=post, form=form, legend='Edytuj post')


@app.route("/posty/<int:post_id>/delete", methods=['POST'])
@login_required
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Twój post został usunięty', 'success')
    return redirect(url_for('home'))


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
    return render_template('admin.html', tytul=tytul, form=form, legend='Tutaj tworzysz nowy post')


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
            return redirect(url_for('posty'))
        else:
            flash('Logowanie nie powiodło się. Niepoprawny login lub hasło.', 'danger')
            return redirect(request.url)
    return render_template('logform.html', tytul=tytul, form=form)


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


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    tytul = 'Twoje konto'
    image_file = url_for('static', filename="profile_pics/" + current_user.image_file)
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Twoje konto zostało zaktualizowane', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', tytul=tytul, image_file=image_file, form=form)
