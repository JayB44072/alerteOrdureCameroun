from django import forms
from .models import Signalement

class SignalementForm(forms.ModelForm):
    class Meta:
        model = Signalement
        fields = ['quartier', 'description', 'photo']
        widgets = {
            'quartier': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Décrivez le dépôt sauvage...'
            }),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }