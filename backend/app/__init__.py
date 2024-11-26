import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Inicializando a instância do SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Carregar configurações do arquivo de configuração
    app.config.from_object("app.config.Config")  # Certifique-se de que a configuração está correta
    
    # Ativar CORS para permitir comunicação com o frontend
    CORS(app)

    # Inicializando o banco de dados
    db.init_app(app)

    # Registrando rotas e modelos
    with app.app_context():
        from . import routes, models
        # Use migrations para gerenciar o banco de dados em vez de criar tabelas diretamente aqui
        # db.create_all()  # Comentado, use Flask-Migrate para gerenciar alterações no banco de dados

    return app
