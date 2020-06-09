from flask import Flask, render_template, request, Response, redirect, url_for, session, abort
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from app import app




# config
app.config.update(
    DEBUG=True,
    SECRET_KEY='sekretny_klucz'
)









# ustawienie flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# model uzytkownika
class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.name = "user" + str(id)
        self.password = self.name + "_secret"

    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)


# generacja uzytkownikow
users = [User(id) for id in range(1, 10)]


@app.route("/login", methods=["GET", "POST"])
def login():
    tytul = 'Zaloguj się'
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if password == username + "_secret":
            id = username.split('user')[1]
            user = User(id)
            login_user(user)
            return redirect(url_for("main"))
        else:
            return abort(401)
    else:
        return render_template('formularz_logowania.html', tytul=tytul)


# procedura obslugo blegu logowania
@app.errorhandler(401)
def page_not_found(e):
    tytul = "Coś poszło nie tak..."
    blad = "401"
    return render_template('blad.html', tytul=tytul, blad=blad)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    tytul = "Wylogowanie"
    return render_template('logout.html', tytul=tytul)


# przeladowanie uzytkownika
@login_manager.user_loader
def load_user(userid):
    return User(userid)


@app.route("/")
@login_required  # wymaga logowania
def main():
    return render_template('index.html')


@app.route("/about/")
@login_required
def about_me():
    dane = {'tytul': "Strona o mnie", 'tresc': "Witaj na stronie o mnie."}
    return render_template("kontent.html", tytul=dane["tytul"], tresc=dane["tresc"])


@app.route("/info/")
def info():
    dane = {'tytul': "Informacje", 'tresc': "Bardzo istotne informacje."}
    return render_template("kontent.html", tytul=dane["tytul"], tresc=dane["tresc"])


@app.route("/posty/")
@login_required
def posty():
    dane = {'tytul': "Wpisy", 'tresc': "Historia wpisów na blogu"}
    posty = [
        {
            'author': {'username': 'Krzysztof'},
            'body': 'Najlepszy wpis na świecie!'
        },
        {
            'author': {'username': 'Małgorzata'},
            'body': 'Recenzja najnowszej książki Żulczyka.'
        }]
    return render_template("kontent.html", tytul=dane["tytul"], tresc=dane["tresc"], posty=posty)


if __name__ == "__main__":
    app.run(debug=True)
