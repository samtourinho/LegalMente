from django.db import models
from django.contrib.auth.models import User

class Questao(models.Model):
    materia = models.CharField(max_length=100)
    banca = models.CharField(max_length=100)
    enunciado = models.TextField()
    alternativas = models.TextField()  # Exemplo: "a) ... | b) ... | c) ..."
    resposta_correta = models.CharField(max_length=1)
    ano = models.IntegerField()

    def alternativas_list(self):
        return self.alternativas.split(" | ")

    def __str__(self):
        return f"{self.materia} - {self.ano} - {self.enunciado[:50]}..."


class RespostaUsuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE)
    resposta_dada = models.CharField(max_length=1)
    acertou = models.BooleanField()
    respondido_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'questao')

    def __str__(self):
        return f"{self.usuario.username} - {self.questao.id} - {'✔' if self.acertou else '✘'}"
