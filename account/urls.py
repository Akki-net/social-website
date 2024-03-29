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
    path('create-post/', views.create_post, name='create_post'),
    # post views
    path('post-list', views.post_list, name='post_list'),
    path('post-detail/<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    # change password urls
    path('password-change/', auth_views.PasswordChangeView.as_view(),
         name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(),
          name='password_change_done'),
    # reset password urls
    path('password-reset/', auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    # Appointment
    path('doctor-list/', views.DoctorList.as_view(), name='doctor_list'),
    path('make-appointment/<int:id>', views.make_appointment, name="make_appointment"),
    path('appointment-detail/<int:pk>', views.AppointmentDetail.as_view(), name="appointment_detail"),
]