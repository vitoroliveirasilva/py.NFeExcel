import pdfplumber
import pandas as pd
import re

def extrair_dados_nota(pdf_path):
    cfop_validos = {"5667", "5656", "6929"}
    palavras_chave = {"etanol", "gasolina", "diesel"}  # Palavras para verificar na descrição
    dados = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            texto = page.extract_text()
            if not texto:
                continue

            # Extraindo a chave de acesso (44 dígitos)
            chave_match = re.search(r'\b\d{44}\b', texto)
            chave_acesso = chave_match.group() if chave_match else "Não encontrado"

            # Extraindo CFOP e Descrição do Produto corretamente da tabela
            cfop = "Não encontrado"
            descricao_produto = "Não encontrado"

            table = page.extract_table()
            if table:
                for row in table:
                    if row and len(row) > 4:  # Garantindo que a linha tenha informações
                        try:
                            descricao_produto = row[1].strip() if row[1] else "Não encontrado"  # Segunda coluna contém a descrição
                            cfop = row[4].strip() if row[4] else "Não encontrado"  # Quinta coluna contém o CFOP
                        except IndexError:
                            continue  # Se houver erro de índice, ignora a linha

            # Aplicando a lógica de classificação
            if cfop in cfop_validos:
                classificacao = "Pertence a frotas"
            elif any(palavra in descricao_produto.lower() for palavra in palavras_chave):
                classificacao = "Pertence a frotas"
            else:
                classificacao = "Não pertence a frotas"

            # Adiciona os dados extraídos à lista
            dados.append([chave_acesso, cfop, descricao_produto, classificacao])

    return dados

def salvar_para_excel(dados, output_path):
    df = pd.DataFrame(dados, columns=["Chave de Acesso", "CFOP", "Descrição do Produto", "Classificação"])
    df.to_excel(output_path, index=False)

# Caminho do PDF de entrada e do Excel de saída
pdf_path = "notas_fiscais.pdf"  # Substitua pelo caminho do seu arquivo PDF
output_path = "resultado.xlsx"

# Executando o processamento
dados_extraidos = extrair_dados_nota(pdf_path)
salvar_para_excel(dados_extraidos, output_path)

print(f"✅ Processamento concluído! Resultado salvo em {output_path}")
