from django import forms
from django.contrib.auth.models import User
from .models import Profile, Post, Appointment
import datetime
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
    def clean_email(self):
        data = self.cleaned_data['email']
        qs = User.objects.exclude(id=self.instance.id)\
            .filter(email=data)
        if data != "" and qs.exists():
            raise forms.ValidationError('Email already in use')
        return data

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['type_of_user', 'address', 'photo']
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
    def clean_email(self):
        data = self.cleaned_data['email']
        if data != "" and User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email already in use')
        return data
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['category', 'title', 'content', 'image', 'status']
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['required_speciality', 'date_of_appointment', 'start_time']
    def clean_date_of_appointment(self):
        app_date = self.cleaned_data['date_of_appointment']
        if app_date < datetime.date.today():
            raise forms.ValidationError("Date must be equal or greater than today's!")
        return app_date
    def clean_start_time(self):
        data = dict(self.cleaned_data)
        try:
            qs = Appointment.objects.filter(date_of_appointment=self.clean_date_of_appointment(),\
                                    start_time__lte=data['start_time'], end_time__gte=data['start_time'])
            if qs.exists():
                raise forms.ValidationError('This time slot is already booked!')
            return data['start_time']
        except KeyError:
            return ""