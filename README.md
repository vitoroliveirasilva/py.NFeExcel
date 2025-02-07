# 📌 Extração de Dados de Notas Fiscais (NF-e) em PDF

## 📖 Sobre o Projeto
Este projeto é uma aplicação web desenvolvida com **Flask** para realizar a extração de dados de **Notas Fiscais Eletrônicas (NF-e) em PDF** e gerar um relatório em **Excel**. O sistema permite que os usuários façam o upload de arquivos PDF contendo notas fiscais e obtenham informações extraídas de forma automática.

## 🚀 Funcionalidades
- Upload de arquivos PDF contendo Notas Fiscais.
- Extração automática de **Chave de Acesso**, **CFOP**, **Descrição do Produto** e **Classificação**.
- Geração de um arquivo **Excel** com os dados extraídos.
- Interface amigável para facilitar o uso.
- Tratamento de erros para formatos inválidos.

## 📂 Estrutura do Projeto
```
📦 NFSRE
│── EXTRACAONFS/
│   ├── routes/
│   │   ├── __init__.py  # Inicialização do módulo
│   │   └── upload.py  # Rotas para upload de arquivos
│   ├── utils/
│   │   ├── __init__.py  # Inicialização do módulo
│   │   └── extracao_dados_utils.py  # Função para extração de dados
│── static/
│   ├── css/
│   │   └── style.css  # Arquivo de estilos
│   ├── img/
│   │   └── LogoBrasif.png  # Logotipo
│── templates/
│   └── upload.html  # Página de upload de arquivos
│── outputs/
│   └── Resultado_Extração_NFs.xlsx  # Arquivo gerado com os dados extraídos
│── uploads/
│   └── DANFES_29-01-2025_11.44.37.pdf  # Arquivo PDF enviado
│── venv/  # Ambiente virtual
│── .env  # Arquivo de configuração de variáveis de ambiente
│── .env.example  # Exemplo de configuração
│── .gitignore  # Arquivo para ignorar arquivos no Git
│── app_config.py  # Configurações do aplicativo
│── app.py  # Arquivo principal do Flask
│── LICENSE  # Licença do projeto
│── README.md  # Documentação do projeto
└── requirements.txt  # Lista de dependências
```

## 📦 Instalação e Configuração

### 1️⃣ Criar um ambiente virtual e ativá-lo
```sh
python -m venv venv  # Criar ambiente virtual
venv\Scripts\activate  # Windows
```

### 2️⃣ Instalar as dependências
```sh
pip install -r requirements.txt
```

### 3️⃣ Configurar diretórios de upload e saída
No arquivo `app_config.py`, defina os diretórios para upload e saída:
```python
import os

class Config:
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    OUTPUT_FOLDER = os.path.join(os.getcwd(), 'outputs')
```

Certifique-se de criar essas pastas no diretório do projeto:
```sh
mkdir uploads outputs
```

### 4️⃣ Executar a aplicação
```sh
python app.py
```

## 📄 Como Usar
1. Acesse a página inicial e faça o upload de um arquivo PDF contendo a nota fiscal.
2. O sistema processará o arquivo e extrairá os dados necessários.
3. Após o processamento, será gerado um arquivo Excel contendo os dados extraídos.
4. O download do relatório será iniciado automaticamente.

## 📜 Licença
Este projeto é distribuído sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais informações.

---
🚀 **Desenvolvido por [Vitor Oliveira Silva](https://github.com/vitoroliveirasilva)**
