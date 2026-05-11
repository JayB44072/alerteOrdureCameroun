from django.db import models
from accounts.models import User

class Quartier(models.Model):
    nom = models.CharField(max_length=100)
    ville = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nom} - {self.ville}"

    class Meta:
        verbose_name = "Quartier"
        verbose_name_plural = "Quartiers"
        ordering = ['ville', 'nom']


class Signalement(models.Model):
    STATUT_CHOICES = (
        ('nouveau', '🔴 Nouveau'),
        ('confirme', '🟡 Confirmé'),
        ('en_traitement', '🔵 En traitement'),
        ('nettoye', '🟢 Nettoyé'),
    )

    auteur = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='signalements'
    )
    quartier = models.ForeignKey(
        Quartier,
        on_delete=models.CASCADE,
        related_name='signalements'
    )
    description = models.TextField()
    photo = models.ImageField(
        upload_to='signalements/',
        blank=True,
        null=True
    )
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='nouveau'
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def nombre_confirmations(self):
        return self.confirmations.count()

    def __str__(self):
        return f"Dépôt à {self.quartier} - {self.statut}"

    class Meta:
        verbose_name = "Signalement"
        verbose_name_plural = "Signalements"
        ordering = ['-date_creation']


class Confirmation(models.Model):
    signalement = models.ForeignKey(
        Signalement,
        on_delete=models.CASCADE,
        related_name='confirmations'
    )
    utilisateur = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='confirmations'
    )
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Confirmation"
        verbose_name_plural = "Confirmations"
        # Un utilisateur ne peut confirmer qu'une fois par signalement
        unique_together = ('signalement', 'utilisateur')

    def __str__(self):
        return f"{self.utilisateur} a confirmé {self.signalement}"