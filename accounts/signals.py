from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def set_token(sender, instance, created, **kwargs):
    if created:
        if instance.account_type == 'SUPREM':
            instance.token = 999999
        elif instance.token == 0:
            instance.token = 0  # default, needs SUPREM approval
        instance.save()

