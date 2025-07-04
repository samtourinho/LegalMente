from django.urls import path
from . import views

urlpatterns = [
    path('<str:materia_slug>/', views.questao_aleatoria, name='questao_aleatoria'),
    path('<str:materia_slug>/flashcard/', views.flashcard, name='flashcard'),
]