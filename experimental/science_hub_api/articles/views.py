from rest_framework import viewsets, permissions
from .models import Article, Author, Category, Tag
from .serializers import ArticleSerializer, AuthorSerializer, CategorySerializer, TagSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from externalAPIs.authentication import ApiKeyAuthentication
from externalAPIs.permissions import CanAccessArticles

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    authentication_classes = [ApiKeyAuthentication]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser, CanAccessArticles]
        return [permission() for permission in permission_classes]