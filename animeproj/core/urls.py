from django.urls import path, include

from core.views import *


app_name = 'core'


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('category/<int:pk>/', CategoryView.as_view(), name='category'), 
    path('search/', SearchView.as_view(), name='search'),
    path('<str:order_by>', GeneralView.as_view(), name='general'),
    path('categories/', CategoriesView.as_view(), name='categories'),
]
