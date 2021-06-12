import os
from flask import Flask
from flask_security import Security, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy

#Creamos una instancia de SQLAlchemy
db = SQLAlchemy()
#Creamos el objeto SQLalchemyUserDaaStore
from .models import User, Role
userDataStore = SQLAlchemyUserDatastore(db, User, Role)

def create_app():
    #Creamos una instancia del flask
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #Generar la clave de sessión para crear una cookie con la inf. de la sessión
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/flasksecurity'
    app.config['SECURITY_PASSWORD_SALT'] = 'thisissecretsalt'

    db.init_app(app)
    @app.before_first_request
    def create_all():
        db.create_all()

    #Conectando los modelos a flask-security.
    security = Security(app, userDataStore)

    #Configurando el login_manager
    #login_manager = LoginManager()
    #login_manager.login_view = 'auth.login'
    #login_manager.init_app(app)

    #Importamos la clase User.
    #from .models import User
    #@login_manager.user_loader
    #def load_user(user_id):
        #return User.query.get(int(user_id))

    #Registramos el blueprint para las rutas auth
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    #Registramos el blueprint para el resto de la aplicación
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
