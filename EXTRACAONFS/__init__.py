# ========== IMPORTAÇÕES ==========
from flask import Flask  # Flask

# Configurações de ambiente
from app_config import Config


# ========== APP ==========
def criacao_app():
    # Configura a pasta static para importações como CSS e JS
    app = Flask(__name__, static_folder='./static')
    # Configuração do app
    app.config.from_object(Config)

    # Registrar blueprints
    from EXTRACAONFS.routes import register_blueprint
    register_blueprint(app)

    return app


# Criação do objeto app
app = criacao_app()
