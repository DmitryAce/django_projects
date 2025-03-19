# users/views.py
from rest_framework import generics, permissions
from externalAPIs.authentication import ApiKeyAuthentication
from .serializers import UserSerializer, RegisterSerializer
from .models import User
from .permissions import IsAdminUser, IsModeratorUser, IsAdminOrModerator


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer


class UserView(generics.RetrieveAPIView):
    authentication_classes = [ApiKeyAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


# class AdminOnlyView(generics.ListAPIView):
#     queryset = User.objects.all()
#     authentication_classes = [ApiKeyAuthentication]
#     permission_classes = (IsAdminUser,)
#     serializer_class = UserSerializer


# class ModeratorOrAdminView(generics.ListAPIView):
#     queryset = User.objects.all()
#     authentication_classes = [ApiKeyAuthentication]
#     permission_classes = (IsAdminOrModerator,)
#     serializer_class = UserSerializer