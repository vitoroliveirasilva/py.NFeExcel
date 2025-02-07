from dotenv import load_dotenv
import os

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()


# Classe de configuração do app
class Config:
    
    # Diretório base do projeto
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # Chave secreta para segurança da aplicação
    SECRET_KEY = os.getenv('SECRET_KEY')

    # Diretórios de upload e output
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    OUTPUT_FOLDER = os.path.join(BASE_DIR, 'outputs')

    # Garante que os diretórios existam ao iniciar a aplicação
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    @staticmethod
    # Verifica a presença da variável de ambiente.
    def validacao_config():
        if not Config.SECRET_KEY:
            raise ValueError("A variável de ambiente 'SECRET_KEY' não está definida.")

Config.validacao_config()
