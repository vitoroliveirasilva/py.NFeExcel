import pdfplumber
import re

def extrai_dados_nf(pdf_path):
    try:
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

    except Exception as e:
        return None  # Retorna None para indicar erro na extração
