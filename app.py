from flask import Flask, render_template, request, send_file
import pdfplumber
import pandas as pd
import re
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def upload_form():
    return render_template('upload.html')

def extrair_dados_nota(pdf_path):
    cfop_validos = {"5667", "5656", "6929"}
    palavras_chave = {"etanol", "gasolina", "diesel"}
    dados = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            texto = page.extract_text()
            if not texto:
                continue

            chave_match = re.search(r'\b\d{44}\b', texto)
            chave_acesso = chave_match.group() if chave_match else "Não encontrado"

            cfop = "Não encontrado"
            descricao_produto = "Não encontrado"

            table = page.extract_table()
            if table:
                for row in table:
                    if row and len(row) > 4:
                        try:
                            descricao_produto = row[1].strip() if row[1] else "Não encontrado"
                            cfop = row[4].strip() if row[4] else "Não encontrado"
                        except IndexError:
                            continue

            if cfop in cfop_validos:
                classificacao = "Pertence a frotas"
            elif any(palavra in descricao_produto.lower() for palavra in palavras_chave):
                classificacao = "Pertence a frotas"
            else:
                classificacao = "Não pertence a frotas"

            dados.append([chave_acesso, cfop, descricao_produto, classificacao])
    
    return dados

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "Nenhum arquivo enviado"
    
    file = request.files['file']
    if file.filename == '':
        return "Nenhum arquivo selecionado"
    
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        
        dados_extraidos = extrair_dados_nota(file_path)
        if not dados_extraidos:
            return "Erro ao processar o arquivo PDF"
        
        output_path = os.path.join(OUTPUT_FOLDER, "Resultado_Extração_NFs.xlsx")
        df = pd.DataFrame(dados_extraidos, columns=["Chave de Acesso", "CFOP", "Descrição do Produto", "Classificação"])
        df.to_excel(output_path, index=False)
        
        return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
