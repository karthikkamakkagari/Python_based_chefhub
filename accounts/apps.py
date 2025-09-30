from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        from .models import CustomUser
        from django.db.utils import OperationalError
        import accounts.signals
        try:
            if not CustomUser.objects.filter(username="supreme").exists():
                CustomUser.objects.create_superuser(
                    username="supreme",
                    password="password123",
                    account_type="supreme",
                    # token="infinite"
                )
        except OperationalError:
            # DB not ready (migrations not applied)
            pass
