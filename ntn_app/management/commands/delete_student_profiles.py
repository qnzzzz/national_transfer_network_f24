from django.core.management.base import BaseCommand
from ntn_app.models import StudentProfile

class Command(BaseCommand):
    help = 'Delete all StudentProfile data'

    def handle(self, *args, **kwargs):
        StudentProfile.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted all StudentProfile data'))