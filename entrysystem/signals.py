from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import NewUser, SecurityProfile, Security, Resident, ResidentProfile


@receiver(post_save, sender=Resident)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.usertype == "Resident":
        ResidentProfile.objects.create(user=instance)


@receiver(post_save, sender=Security)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.usertype == "Security":
        SecurityProfile.objects.create(user=instance)


@receiver(post_save, sender=NewUser)
def mark_created_user_as_active(sender, instance, created, **kwargs):
    if created:
        instance.is_active = True
        instance.save()
