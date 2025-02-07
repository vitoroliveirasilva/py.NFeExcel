from flask import Blueprint, render_template, send_file, redirect, url_for, flash, request
import pandas as pd
import os
from werkzeug.utils import secure_filename
from EXTRACAONFS.utils import extrai_dados_nf
from app_config import Config

extracao_bp = Blueprint("extracao", __name__)


# Rota que exibe o formulário de upload de arquivos.
@extracao_bp.route('/')
def upload_form():
    return render_template('upload.html')


# Rota para upload de arquivos PDF contendo notas fiscais.
@extracao_bp.route('/upload', methods=['POST'])
def upload_file():

    # Verifica se um arquivo foi enviado na requisição
    if 'file' not in request.files:
        flash("Nenhum arquivo enviado.", "error")
        return redirect(url_for('extracao.upload_form'))

    file = request.files['file']  # Obtém o arquivo enviado
    if file.filename == '':  # Verifica se o nome do arquivo está vazio
        flash("Nenhum arquivo selecionado.", "error")
        return redirect(url_for('extracao.upload_form'))

    try:
        # Sanitiza o nome do arquivo para evitar problemas de segurança
        filename = secure_filename(file.filename)
        # Define o caminho para salvar o arquivo no servidor
        file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(file_path)  # Salva o arquivo no diretório de upload

        # Chama a função para extrair os dados da nota fiscal
        dados_extraidos = extrai_dados_nf(file_path)
        if not dados_extraidos:  # Se a extração falhar, exibe uma mensagem de erro
            flash("Erro ao processar o arquivo PDF. Verifique se o formato está correto.", "error")
            return redirect(url_for('extracao.upload_form'))

        # Define o caminho para salvar o arquivo Excel gerado
        output_path = os.path.join(Config.OUTPUT_FOLDER, "Resultado_Extração_NFs.xlsx")
        # Converte os dados extraídos em um DataFrame do pandas
        df = pd.DataFrame(dados_extraidos, columns=["Chave de Acesso", "CFOP", "Descrição do Produto", "Classificação"])
        df.to_excel(output_path, index=False)  # Salva os dados no formato Excel

        # Envia o arquivo Excel para download
        return send_file(output_path, as_attachment=True)

    except Exception as e:
        flash(f"Erro ao processar o arquivo: {str(e)}", "error")
        return redirect(url_for('extracao.upload_form'))
