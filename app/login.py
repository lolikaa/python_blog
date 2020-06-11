from flask_login import LoginManager, UserMixin

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

