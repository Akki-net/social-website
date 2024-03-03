from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    # previous login url
    # path('login/', views.user_login, name="login")
    # login / logout urls
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    # dashboard urls
    path('', views.dashboard, name='dashboard'),
    path('edit/', views.edit, name='edit'),
    # change password urls
    path('password-change/', auth_views.PasswordChangeView.as_view(),
         name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(),
          name='password_change_done'),
]