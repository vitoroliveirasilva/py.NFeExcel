import pdfplumber
import re
import os

# Função para extrair dados de uma Nota Fiscal em formato PDF.
def extrai_dados_nf(pdf_path):
    try:
        # Definição de CFOPs válidos para classificação
        cfop_validos = {"5667", "5656", "6929"}
        # Definição de palavras-chave para a descrição da nota fiscal
        palavras_chave = {"etanol", "gasolina", "diesel"}
        # Lista para armazenar os dados extraídos
        dados = []

        # Abre o PDF utilizando pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                texto = page.extract_text()
                if not texto:
                    continue

                # Busca a chave de acesso da NF (44 dígitos numéricos)
                chave_match = re.search(r'\b\d{44}\b', texto)
                chave_acesso = chave_match.group() if chave_match else "Não encontrado"

                # Define valores padrão para caso não sejam encontrados
                cfop = "Não encontrado"
                descricao_produto = "Não encontrado"

                # Extrai as tabelas da página
                table = page.extract_table()
                if table:
                    for row in table:
                        # Verifica se a linha possui pelo menos 5 colunas (para evitar IndexError)
                        if row and len(row) > 4:
                            try:
                                # Obtém a descrição do produto (coluna 2)
                                descricao_produto = row[1].strip() if row[1] else "Não encontrado"
                                # Obtém o CFOP (coluna 5)
                                cfop = row[4].strip() if row[4] else "Não encontrado"
                            except IndexError:
                                continue  # Caso ocorra erro ao acessar colunas, ignora a linha
                
                # Verifica se o CFOP contém os valores válidos
                if cfop in cfop_validos:
                    classificacao = "Pertence a frotas"
                # Caso não tenha, verifica se a descrição contém as palavras-chave
                elif any(palavra in descricao_produto.lower() for palavra in palavras_chave):
                    classificacao = "Pertence a frotas"
                # Senão define como não pertencente a frotas
                else:
                    classificacao = "Não pertence a frotas"

                # Adiciona os dados extraídos à lista
                dados.append([chave_acesso, cfop, descricao_produto, classificacao])

        # Exclui o arquivo PDF após o processamento
        os.remove(pdf_path)

        return dados  # Retorna a lista contendo os dados extraídos da nota fiscal

    except Exception as e:
        print(f"Erro na extração: {e}")
        return None  # Retorna None em caso de erro na extração.
