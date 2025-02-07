from flask import Blueprint, render_template, send_file, request, redirect, url_for, flash
import pandas as pd
import os
from werkzeug.utils import secure_filename
from EXTRACAONFS.utils import extrai_dados_nf
from app_config import Config

extracao_bp = Blueprint("extracao", __name__)

@extracao_bp.route('/')
def upload_form():
    return render_template('upload.html')

@extracao_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash("Nenhum arquivo enviado.", "error")
        return redirect(url_for('extracao.upload_form'))

    file = request.files['file']
    if file.filename == '':
        flash("Nenhum arquivo selecionado.", "error")
        return redirect(url_for('extracao.upload_form'))

    try:
        filename = secure_filename(file.filename)
        file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(file_path)

        # Extrai os dados
        dados_extraidos = extrai_dados_nf(file_path)
        if not dados_extraidos:
            flash("Erro ao processar o arquivo PDF. Verifique se o formato está correto.", "error")
            return redirect(url_for('extracao.upload_form'))

        output_path = os.path.join(Config.OUTPUT_FOLDER, "Resultado_Extração_NFs.xlsx")
        df = pd.DataFrame(dados_extraidos, columns=["Chave de Acesso", "CFOP", "Descrição do Produto", "Classificação"])
        df.to_excel(output_path, index=False)

        return send_file(output_path, as_attachment=True)

    except Exception as e:
        flash(f"Erro ao processar o arquivo: {str(e)}", "error")
        return redirect(url_for('extracao.upload_form'))
