from django.shortcuts import render
from django.forms import model_to_dict
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination

from .models import Scientist, Category
from .serializers import ScientistSerializer
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly


class ScientitsAPIListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 10000

class ScientistAPIList(generics.ListCreateAPIView):
    """
    get:
    Возвращает список всех ученых.

    post:
    Создает нового ученого. Доступно только для авторизованных пользователей.
    """
    queryset = Scientist.objects.all()
    serializer_class = ScientistSerializer
    pagination_class = ScientitsAPIListPagination

class ScientistAPIUpdate(generics.RetrieveUpdateAPIView):
    """
    get:
    Возвращает информацию о конкретном ученом.

    put:
    Обновляет информацию о конкретном ученом. Доступно только для авторизованных пользователей.

    patch:
    Частично обновляет информацию о конкретном ученом.
    """
    queryset = Scientist.objects.all()
    serializer_class = ScientistSerializer
    permission_classes = (IsAuthenticated,)

class ScientistAPIDestroy(generics.RetrieveDestroyAPIView):
    """
    get:
    Возвращает информацию о конкретном ученом.

    delete:
    Удаляет информацию о конкретном ученом. Доступно только для администраторов.
    """
    queryset = Scientist.objects.all()
    serializer_class = ScientistSerializer
    permission_classes = (IsAuthenticated,)


# class ScientistViewSet(viewsets.ReadOnlyModelViewSet):
#     #queryset = Scientist.objects.all()
#     serializer_class = ScientistSerializer
    
#     def get_queryset(self):
#         pk = self.kwargs.get("pk")
    
#         if not pk:
#             return Scientist.objects.all()[:3]

#         return Scientist.objects.filter(pk=pk)
    
#     @action(methods=['get'], detail=True)
#     def category(self, request, pk=False):
#         category = Category.objects.get(pk=pk)
#         return Response({'categories': category.name})



# # GET
# class ScientistAPIView(generics.ListAPIView):
#     queryset = Scientist.objects.all()
#     serializer_class = ScientistSerializer


# # POST GET
# class ScientistAPIList(generics.ListCreateAPIView):
#     queryset = Scientist.objects.all()
#     serializer_class = ScientistSerializer


# # PUT PATCH
# class ScientistAPIUpdate(generics.UpdateAPIView):
#     queryset = Scientist.objects.all()
#     serializer_class = ScientistSerializer


# # CRUD
# class ScientistAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Scientist.objects.all()
#     serializer_class = ScientistSerializer




# ручная обработка любого типа запроса
# class ScientistAPIView(APIView):
#     def get(self, request):
#         w = Scientist.objects.all()
#         return Response({'posts': ScientistSerializer(w, many=True).data})
    

#     def post(self, request):
#         serializer = ScientistSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response({'post': serializer.data})
    

#     def put(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({'error': "Method PUT not allowed"})

#         try:
#             instance = Scientist.objects.get(pk=pk)
#         except:
#             return Response({'error': "Object does not exists"})
        
#         serializer = ScientistSerializer(data=request.data, instance=instance)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"post": serializer.data})
    
    
#     def delete(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({'error': "Method DELETE not allowed"})
        
#         instance = Scientist.objects.get(pk=pk)
#         instance.delete()

#         return Response({"post":"delete post " + str(pk)})