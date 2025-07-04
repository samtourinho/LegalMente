# usuarios/views.py
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Conta criada com sucesso! Faça login.")
            return redirect('login')
        else:
            messages.error(request, "Erro ao criar conta. Verifique os campos.")
    else:
        form = UserCreationForm()
    return render(request, 'usuarios/register.html', {'form': form})

def home(request):
    return render(request, 'home.html')