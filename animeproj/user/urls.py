from django.urls import path, include
from .views import *


app_name = 'user'


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),

    
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/<int:user_id>/', ProfileDetailView.as_view(), name='profile_view'),
    
    path('', include('django.contrib.auth.urls')),
]
