import os
import csv
from django.core.management.base import BaseCommand
from questoes.models import Questao


class Command(BaseCommand):
    help = 'Importa questões CSV para o banco de dados'

    def handle(self, *args, **kwargs):
        pasta = 'csv'  # Certifique-se de que essa pasta está no mesmo nível do manage.py

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

        total = 0

        # Carrega os enunciados existentes no banco para evitar consultas repetidas
        existentes = set(
            Questao.objects.values_list("enunciado", "materia", "banca")
        )

        for nome_arquivo in os.listdir(pasta):
            caminho = os.path.join(pasta, nome_arquivo)
            materia, banca = extrair_info(nome_arquivo)

            self.stdout.write(f"Importando arquivo: {nome_arquivo}")

            with open(caminho, encoding='utf-8') as f:
                leitor = csv.DictReader(f)
                for i, linha in enumerate(leitor, start=1):
                    try:
                        enunciado = linha['Perguntas'].strip()
                        alternativas = linha['Alternativas'].strip()
                        resposta = linha['Resposta'].strip().lower()
                        ano = int(linha['Ano'])
                    except KeyError as e:
                        self.stdout.write(self.style.WARNING(
                            f"  ⚠️ Coluna faltando no arquivo {nome_arquivo}: {e}"
                        ))
                        continue

                    chave = (enunciado, materia, banca)
                    if chave in existentes:
                        continue  # Já existe, pula

                    Questao.objects.create(
                        materia=materia,
                        banca=banca,
                        enunciado=enunciado,
                        alternativas=alternativas,
                        resposta_correta=resposta,
                        ano=ano
                    )
                    existentes.add(chave)
                    total += 1

                    if i % 100 == 0:
                        self.stdout.write(f"  {i} questões processadas...")

        self.stdout.write(self.style.SUCCESS(f"{total} novas questões importadas com sucesso."))
