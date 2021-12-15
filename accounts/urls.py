from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.signup, name="signup"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('forgotPassword', views.forgotPassword, name="forgotPassword"),
    path('forgotPasswordLink/<uidb64>/<token>/', views.forgotPasswordLink, name='forgotPasswordLink'),
    path('resetPassword', views.resetPassword, name='resetPassword'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('application_history/', views.application_history, name='application_history'),
]
