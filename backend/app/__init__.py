from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")
    
    # Configuração CORS para permitir comunicação com o frontend
    CORS(app)

    # Inicializando o banco de dados
    db.init_app(app)

    # Registrando rotas
    with app.app_context():
        from . import routes, models
        db.create_all()  # Cria tabelas no banco de dados
        return app
