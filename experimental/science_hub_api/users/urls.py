from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, UserView, AdminOnlyView, ModeratorOrAdminView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', UserView.as_view(), name='user'),
    path('admin/users/', AdminOnlyView.as_view(), name='admin_users'),
    path('moderator-or-admin/users/', ModeratorOrAdminView.as_view(), name='moderator_or_admin_users'),
]