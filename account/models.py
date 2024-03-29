from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
import datetime

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
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
                     .filter(status=Post.Status.PUBLISHED, author__profile__type_of_user = 'DR')
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
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts')
    content = models.TextField()
    category = models.CharField(max_length=2, choices=Category.choices, default=Category.COVID19)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    image = models.ImageField(upload_to='posts/%Y/%m/%d/', blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.
    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])
class Appointment(models.Model):
    doctor_name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    required_speciality = models.CharField(max_length=2, choices=Post.Category.choices, default=Post.Category.COVID19)
    date_of_appointment = models.DateField(default=datetime.date.today, blank=True)
    start_time = models.TimeField(default=datetime.datetime.now().time(), blank=True)
    end_time = models.TimeField(blank=True)
    class Meta:
        ordering = ['-date_of_appointment', '-start_time']
        indexes = [
            models.Index(fields=['-date_of_appointment', '-start_time']),
        ]
    def get_absolute_url(self):
        return reverse('appointment_detail',
                       args=[self.id])