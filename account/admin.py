from django.contrib import admin
from .models import Profile, Post, Appointment
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'type_of_user', 'address', 'photo']
    raw_id_fields = ['user']
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['doctor_name', 'required_speciality', 'date_of_appointment', 'start_time', 'end_time']
    list_filter = ['doctor_name', 'required_speciality']
    raw_id_fields = ['doctor_name']
    date_hierarchy = 'date_of_appointment'
    ordering = ['-date_of_appointment', '-start_time']