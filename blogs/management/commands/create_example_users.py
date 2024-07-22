from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Create example users'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='bob').exists():
            User.objects.create_user(username='bob', password='squarepants')
            self.stdout.write(self.style.SUCCESS('Successfully created user bob'))

        if not User.objects.filter(username='alice').exists():
            User.objects.create_user(username='alice', password='redqueen')
            self.stdout.write(self.style.SUCCESS('Successfully created user alice'))
