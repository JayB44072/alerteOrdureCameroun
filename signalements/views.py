from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Signalement, Quartier, Confirmation
from .forms import SignalementForm

@login_required
def citoyen_accueil(request):
    # Rediriger l'agent vers son dashboard
    if request.user.role == 'agent':
        return redirect('hysacam_dashboard')
    
    tous_signalements = Signalement.objects.all()
    
    # Stats réelles
    total = tous_signalements.count()
    nouveaux = tous_signalements.filter(statut__in=['nouveau', 'confirme']).count()
    en_traitement = tous_signalements.filter(statut='en_traitement').count()
    nettoyes = tous_signalements.filter(statut='nettoye').count()
    
    # Filtrage
    signalements = tous_signalements.order_by('-date_creation')
    quartiers = Quartier.objects.all()
    quartier_filtre = request.GET.get('quartier')
    if quartier_filtre:
        signalements = signalements.filter(quartier__id=quartier_filtre)
    
    return render(request, 'citoyen/accueil.html', {
        'signalements': signalements,
        'quartiers': quartiers,
        'quartier_filtre': quartier_filtre,
        'total': total,
        'nouveaux': nouveaux,
        'en_traitement': en_traitement,
        'nettoyes': nettoyes,
    })


@login_required
def signaler(request):
    # Rediriger l'agent
    if request.user.role == 'agent':
        return redirect('hysacam_dashboard')
    
    if request.method == 'POST':
        form = SignalementForm(request.POST, request.FILES)
        if form.is_valid():
            signalement = form.save(commit=False)
            signalement.auteur = request.user
            signalement.save()
            messages.success(request, 'Votre signalement a été enregistré !')
            return redirect('citoyen_accueil')
        else:
            messages.error(request, 'Veuillez corriger les erreurs.')
    else:
        form = SignalementForm()
    return render(request, 'citoyen/signaler.html', {'form': form})


@login_required
def mes_signalements(request):
    # Rediriger l'agent
    if request.user.role == 'agent':
        return redirect('hysacam_dashboard')
    
    signalements = Signalement.objects.filter(
        auteur=request.user
    ).order_by('-date_creation')
    return render(request, 'citoyen/mes_signalements.html', {
        'signalements': signalements
    })


@login_required
def confirmer(request, pk):
    # Rediriger l'agent
    if request.user.role == 'agent':
        return redirect('hysacam_dashboard')
    
    signalement = get_object_or_404(Signalement, pk=pk)
    if signalement.auteur == request.user:
        messages.warning(request, 'Vous ne pouvez pas confirmer votre propre signalement.')
        return redirect('citoyen_accueil')
    confirmation, created = Confirmation.objects.get_or_create(
        signalement=signalement,
        utilisateur=request.user
    )
    if created:
        if signalement.nombre_confirmations() >= 3:
            signalement.statut = 'confirme'
            signalement.save()
        messages.success(request, 'Confirmation enregistrée !')
    else:
        messages.info(request, 'Vous avez déjà confirmé ce signalement.')
    return redirect('citoyen_accueil')


@login_required
def hysacam_dashboard(request):
    if request.user.role != 'agent':
        messages.error(request, 'Accès réservé aux agents HYSACAM.')
        return redirect('citoyen_accueil')
    
    tous = Signalement.objects.all()
    
    # Stats réelles
    total = tous.count()
    nouveaux = tous.filter(statut__in=['nouveau', 'confirme']).count()
    en_traitement = tous.filter(statut='en_traitement').count()
    nettoyes = tous.filter(statut='nettoye').count()
    
    # Filtrage
    signalements = tous.order_by('-date_creation')
    statut_filtre = request.GET.get('statut')
    if statut_filtre:
        signalements = signalements.filter(statut=statut_filtre)
    
    return render(request, 'hysacam/dashboard.html', {
        'signalements': signalements,
        'statut_filtre': statut_filtre,
        'total': total,
        'nouveaux': nouveaux,
        'en_traitement': en_traitement,
        'nettoyes': nettoyes,
    })


@login_required
def changer_statut(request, pk):
    if request.user.role != 'agent':
        return redirect('citoyen_accueil')
    signalement = get_object_or_404(Signalement, pk=pk)
    nouveau_statut = request.POST.get('statut')
    if nouveau_statut in ['en_traitement', 'nettoye']:
        signalement.statut = nouveau_statut
        signalement.save()
        messages.success(request, 'Statut mis à jour avec succès !')
    return redirect('hysacam_dashboard')