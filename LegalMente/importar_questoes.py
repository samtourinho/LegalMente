import csv
import os
from questoes.models import Questao

# Caminho para a pasta onde estão os arquivos CSV
PASTA = "csv"

# Mapeia os nomes dos arquivos para matéria e banca
def extrair_info(nome_arquivo):
    nome = nome_arquivo.lower()
    if "administrativo" in nome:
        materia = "Direito Administrativo"
    elif "constitucional" in nome:
        materia = "Direito Constitucional"
    elif "civil" in nome and "processual" not in nome:
        materia = "Direito Civil"
    elif "penal" in nome and "processual" not in nome:
        materia = "Direito Penal"
    elif "processualpenal" in nome or "processual_penal" in nome:
        materia = "Processo Penal"
    elif "processualcivil" in nome or "processual_civil" in nome:
        materia = "Processo Civil"
    elif "portugues" in nome:
        materia = "Língua Portuguesa"
    else:
        materia = "Outros"

    if "cespe" in nome:
        banca = "CESPE"
    elif "fcc" in nome:
        banca = "FCC"
    else:
        banca = "Desconhecida"

    return materia, banca

# Caminhar pelos arquivos CSV na pasta
for nome_arquivo in os.listdir(PASTA):
    caminho = os.path.join(PASTA, nome_arquivo)
    materia, banca = extrair_info(nome_arquivo)

    with open(caminho, encoding='utf-8') as f:
        leitor = csv.DictReader(f)
        for linha in leitor:
            enunciado = linha['Perguntas'].strip()
            alternativas = linha['Alternativas'].strip()
            resposta = linha['Resposta'].strip().lower()
            ano = int(linha['Ano'])

            # Evita duplicação por enunciado
            if not Questao.objects.filter(enunciado=enunciado, materia=materia, banca=banca).exists():
                Questao.objects.create(
                    materia=materia,
                    banca=banca,
                    enunciado=enunciado,
                    alternativas=alternativas,
                    resposta_correta=resposta,
                    ano=ano
                )

print("Importação concluída com sucesso.")
