# flask-backend/app.py
from flask import Flask
from flask_login import LoginManager
from models import User
from extensions import mysql
from flask_cors import CORS

# Importar blueprints
from login import auth_bp
from usuarios import usuarios_bp
from productos import productos_bp
from pedidos import pedidos_bp
from detalle_pedidos import detalle_pedidos_bp
from ingredientes import ingredientes_bp
from recetas import recetas_bp

app = Flask(__name__)
app.secret_key = "clave_secreta"

# Configuración MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Root'
app.config['MYSQL_DB'] = 'sweetland_by_anny'

mysql.init_app(app)

# CORS para React
CORS(app, origins=["http://localhost:5173"], supports_credentials=True)

# Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth_bp.login"

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

# Registrar blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(productos_bp)
app.register_blueprint(pedidos_bp)
app.register_blueprint(detalle_pedidos_bp)
app.register_blueprint(ingredientes_bp)
app.register_blueprint(recetas_bp)

@app.route("/")
def index():
    return {"mensaje": "Backend Sweetland funcionando"}

if __name__ == "__main__":
    app.run(debug=True, port=5000)