from django.urls import path
from . views import *


app_name = 'anime'


urlpatterns = [
    path("<int:pk>/", IndexView.as_view(), name='details'),
    path('<int:pk>/delete_comment/', IndexView.as_view(), name='delete_comment'),
    path('<int:pk>/<int:rate>/', RateView.as_view(), name='rate'),
    path('<int:rateid>/delete_rate', RateView.as_view(), name='delete_rate'),
    path('toggle_favorite/<int:pk>', FavoriteView.as_view(), name='toggle_favorite'),
    path("<int:pk>/watch/<int:current>", WatchView.as_view(), name='watch'),
    path('<int:pk>/watch/<int:current>/delete_comment/', WatchView.as_view(), name='watch/delete_comment'),
]
