from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from routes.auth import auth
from routes.admin import admin_routes
from routes.standard_user import standard_user
from routes.doctor import docteur_routes
from models.models import db, create_tables , User
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_pyfile('config.py') 
login_manager = LoginManager(app)

login_manager.login_view = 'auth.login'

login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

db.init_app(app)
csrf = CSRFProtect(app)

#with app.app_context():
#    db.drop_all()
#    create_tables()

app.register_blueprint(auth)
app.register_blueprint(standard_user)
app.register_blueprint(docteur_routes)
app.register_blueprint(admin_routes)

if __name__ == "__main__":
    app.run(debug=True)
