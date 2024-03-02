from django.db import models
from django.conf import settings
class Profile(models.Model):
    class User(models.TextChoices):
        PATIENT = 'PT', 'Patient'
        DOCTOR = 'DR', 'Doctor'
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type_of_user = models.CharField(max_length=2, choices=User.choices, default=User.PATIENT)
    address = models.TextField()
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    def _str_(self):
        return f'Profile of {self.user.username}'