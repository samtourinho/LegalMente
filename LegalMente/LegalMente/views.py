from django.shortcuts import render

def home_view(request):
    return render(request, 'LegalMente/home.html')

def civil_smartcards(request):
    return render(request, 'LegalMente/civil_smartcards.html')

def civil_questoes(request):
    return render(request, 'LegalMente/civil_questoes.html')

def contencioso_smartcards(request):
    return render(request, 'LegalMente/contencioso_smartcards.html')

def contencioso_questoes(request):
    return render(request, 'LegalMente/contencioso_questoes.html')

def penal_smartcards(request):
    return render(request, 'LegalMente/penal_smartcards.html')

def penal_questoes(request):
    return render(request, 'LegalMente/penal_questoes.html')

def tributario_smartcards(request):
    return render(request, 'LegalMente/tributario_smartcards.html')

def tributario_questoes(request):
    return render(request, 'LegalMente/tributario_questoes.html')