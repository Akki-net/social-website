from django.db import models
from django.conf import settings
from django.utils import timezone
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
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
    class Category(models.TextChoices):
        MENTALHEALTH = 'MH', 'Mental Health'
        HEARTDISEASE = 'HD', 'Heart Disease'
        COVID19 = 'CV', 'Covid19'
        IMMUNIZATION = 'IM', 'Immunization'
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts')
    content = models.TextField()
    category = models.CharField(max_length=2, choices=Category.choices, default=Category.COVID19)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    image = models.ImageField(upload_to='posts/%Y/%m/%d/', blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]
    def __str__(self):
        return self.title