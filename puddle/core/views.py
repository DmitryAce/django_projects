from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema

from item.models import Category, Item

from .forms import SignupForm

@swagger_auto_schema(method='get', responses={200: 'Success'})
@api_view(['GET'])
@permission_classes([AllowAny])
def index(request):
    items = Item.objects.filter(is_sold=False).order_by('-created_at')[0:6]
    categories = Category.objects.all()
    return render(request, 'core/index.html', {
        'categories': categories,
        'items': items,
    })

@swagger_auto_schema(method='get', responses={200: 'Success'})
@api_view(['GET'])
@permission_classes([AllowAny])
def contact(request):
    return render(request, 'core/contact.html')

@swagger_auto_schema(methods=['GET', 'POST'], responses={200: 'Success'})
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        
        if form.is_valid():
            form.save()
            
            return redirect('/login/')
    else:
        form = SignupForm()
    
    return render(request, 'core/signup.html', {
        'form': form 
    })