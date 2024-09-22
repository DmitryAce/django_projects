from django.urls import path

from . views import *


app_name = 'contacts'


urlpatterns = [
    path('', IndexView.as_view(), name='contacts'),
    path('new/<int:pk>', NewView.as_view(), name="new"),
    path('conversation/<int:pk>', ConversationView.as_view(), name="conversation"),
]
