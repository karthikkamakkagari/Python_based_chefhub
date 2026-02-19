from django.core.management.base import BaseCommand
from accounts.models import CustomUser

class Command(BaseCommand):
    help = "Create default SUPREM user"

    def handle(self, *args, **kwargs):
        if not CustomUser.objects.filter(username='suprem_demo').exists():
            CustomUser.objects.create_user(
                username='suprem_demo',
                email='karthikraj21011992@gmail.com',
                password='Suprem@123',
                phone_number='8897497962',
                account_type='SUPREM',
                token=999999,
                preferred_language='en'
            )
            self.stdout.write(self.style.SUCCESS("SUPREM user created!"))
        else:
            self.stdout.write(self.style.WARNING("SUPREM user already exists."))
