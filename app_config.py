from dotenv import load_dotenv
import os

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

class Config:
    """Classe de configuração do aplicativo."""
    
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Diretório base do projeto

    # Chave secreta para segurança da aplicação
    SECRET_KEY = os.getenv('SECRET_KEY')

    # Diretórios de upload e saída
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    OUTPUT_FOLDER = os.path.join(BASE_DIR, 'outputs')

    # Garante que os diretórios existam ao iniciar a aplicação
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    @staticmethod
    def validacao_config():
        """Verifica a presença de variáveis críticas de ambiente."""
        if not Config.SECRET_KEY:
            raise ValueError("A variável de ambiente 'SECRET_KEY' não está definida.")

# Validação da configuração ao carregar
Config.validacao_config()
