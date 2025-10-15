# flask-backend/app.py
from flask import Flask
from flask_login import LoginManager
from models import User
from extensions import mysql
from flask_cors import CORS
from flask import Flask, jsonify, request


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

# CORS para React - CONFIGURACIÓN COMPLETA
CORS(app, 
     origins=["http://localhost:5173", "http://127.0.0.1:5173"],
     supports_credentials=True,
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
     allow_headers=["Content-Type", "Authorization", "X-Requested-With", "Accept"],
     expose_headers=["Content-Range", "X-Content-Range"],
     max_age=600
)

# Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth_bp.login"

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

# 🔧 SOLUCIÓN: Manejar OPTIONS globalmente antes de la autenticación
@app.before_request
def handle_options():
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

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