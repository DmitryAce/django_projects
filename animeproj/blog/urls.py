from django.urls import path, include

from blog.views import *


app_name = 'blog'


urlpatterns = [
    path('', IndexView.as_view(), name='blog'),
    path('details/<int:pk>/', BlogView.as_view(), name='blog_details'),
    path('details/<int:pk>/delete_comment/', BlogView.as_view(), name='delete_comment'),
]
