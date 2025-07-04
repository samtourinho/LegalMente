"""
URL configuration for LegalMente project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from . import views
from .views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('usuarios/', include('usuarios.urls')),  # tudo do app de login/backend
    path('civil/smartcards/', views.civil_smartcards, name='civil_smartcards'),
    path('civil/questoes/', views.civil_questoes, name='civil_questoes'),
    path('contencioso/smartcards/', views.contencioso_smartcards, name='contencioso_smartcards'),
    path('contencioso/questoes/', views.contencioso_questoes, name='contencioso_questoes'),
    path('penal/smartcards/', views.penal_smartcards, name='penal_smartcards'),
    path('penal/questoes/', views.penal_questoes, name='penal_questoes'),
    path('tributario/smartcards/', views.tributario_smartcards, name='tributario_smartcards'),
    path('tributario/questoes/', views.tributario_questoes, name='tributario_questoes'),
    path('questoes/', include('questoes.urls')),
]

