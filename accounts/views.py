from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import InscriptionForm, ConnexionForm

def register(request):
    if request.user.is_authenticated:
        return redirect_by_role(request.user)
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'citoyen'
            user.save()
            login(request, user)
            messages.success(request, f'Bienvenue {user.username} !')
            return redirect_by_role(user)
        else:
            messages.error(request, 'Veuillez corriger les erreurs.')
    else:
        form = InscriptionForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.user.is_authenticated:
        return redirect_by_role(request.user)
    if request.method == 'POST':
        form = ConnexionForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Bienvenue {user.username} !')
            return redirect_by_role(user)
        else:
            messages.error(request, 'Identifiants incorrects.')
    else:
        form = ConnexionForm(request)  # ← correction ici
    return render(request, 'accounts/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.info(request, 'Vous avez été déconnecté.')
    return redirect('login')

def redirect_by_role(user):
    if user.role == 'agent':
        return redirect('hysacam_dashboard')
    return redirect('citoyen_accueil')