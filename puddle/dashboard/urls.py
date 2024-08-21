from django.urls import path

from . import views 

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<int:pk>/', views.category, name='category'),
]
