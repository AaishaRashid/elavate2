
from django.urls import path

from main import views

urlpatterns = [

    path('', views.home, name='home'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('post', views.Post, name='posts'),
    path('profile setup', views.profile, name='profile'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('idea', views.idea, name='idea'),
    path('mentors', views.mentors, name='mentors'),
    path('general', views.general, name='generalprofile'),
]
