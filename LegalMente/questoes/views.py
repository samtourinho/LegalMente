import random
from django.shortcuts import render, redirect, get_object_or_404
from .models import Questao, RespostaUsuario
import re
import random

def questao_aleatoria(request, materia_slug):
    materia_nome = materia_slug.replace("-", " ").title().strip()
    questoes = Questao.objects.filter(materia__iexact=materia_nome)

    if request.method == "POST":
        questao_id = request.POST.get("questao_id")
        resposta_dada = request.POST.get("resposta")

        questao = Questao.objects.get(id=questao_id)
        resposta_correta = questao.correta.strip().upper()
        acertou = resposta_dada == resposta_correta

        return render(request, "questoes/questao_resposta.html", {
            "questao": questao,
            "resposta_dada": resposta_dada,
            "resposta_correta": resposta_correta,
            "acertou": acertou,
            "materia_slug": materia_slug
        })

    # Se for GET
    if not questoes.exists():
        return render(request, "questoes/erro.html", {"mensagem": "Nenhuma questão encontrada."})

    questao = random.choice(list(questoes))
    alternativas = questao.alternativas.split(" | ")
    questao.alternativas_list = alternativas

    return render(request, "questoes/questao_aleatoria.html", {
        "questao": questao,
        "materia_slug": materia_slug
    })

def flashcard(request, materia_slug):
    import re

    materia_nome = materia_slug.replace('-', ' ').title()
    questoes = Questao.objects.filter(materia__iexact=materia_nome)

    if not questoes.exists():
        return render(request, 'questoes/questao_nao_encontrada.html', {'materia': materia_nome})

    questao = random.choice(list(questoes))

    letra_correta = questao.resposta_correta.strip().lower()
    alternativas_raw = questao.alternativas.strip()

    # Detectar o separador (por linha ou por pipe)
    if '\n' in alternativas_raw:
        alternativas = alternativas_raw.split('\n')
    elif '|' in alternativas_raw:
        alternativas = [alt.strip() for alt in alternativas_raw.split('|')]
    else:
        alternativas = [alternativas_raw.strip()]

    # Lógica para identificar a alternativa correta
    alternativa_correta = None

    if len(alternativas) == 2 and all(alt.lower() in ["certo", "errado"] for alt in alternativas):
        if letra_correta in ["c", "e"]:
            mapa = {"c": "Certo", "e": "Errado"}
            alternativa_correta = mapa.get(letra_correta, "[alternativa não encontrada]")
        else:
            alternativa_correta = letra_correta.capitalize()
    else:
        # Formato tipo "a) algo"
        padrao = re.compile(rf"^{letra_correta}[\)\.\:\-–]?\s*", re.IGNORECASE)
        alternativa_correta = next(
            (alt for alt in alternativas if padrao.match(alt.strip())),
            f"{letra_correta}) [alternativa não encontrada]"
        )

    return render(request, 'questoes/flashcard.html', {
        'questao': questao,
        'materia_slug': materia_slug,
        'alternativas': alternativas,
        'alternativa_correta': alternativa_correta
    })