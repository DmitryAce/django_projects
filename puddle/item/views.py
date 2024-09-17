from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Item, Category
from .forms import NewItemForm, EditItemForm


PAGINATION = 2


item_list_response = openapi.Response(
    description="List of items",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'items': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'name': openapi.Schema(type=openapi.TYPE_STRING),
                        'description': openapi.Schema(type=openapi.TYPE_STRING),
                        'price': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT),
                        'image': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI),
                        'is_sold': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'created_by': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'created_at': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
                    }
                ),
            ),
            'categories': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'name': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                ),
            ),
        }
    )
)


@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('query', openapi.IN_QUERY, description="Search query", type=openapi.TYPE_STRING),
        openapi.Parameter('category', openapi.IN_QUERY, description="Category ID", type=openapi.TYPE_INTEGER),
    ],
    responses={
        200: item_list_response,
        400: openapi.Response(description="Invalid input"),
    },
    operation_summary="Get a list of items",
    operation_description="Retrieve a list of items that match the search query and category ID. Returns a list of items with their details.",
    tags=['Items']
)
@api_view(['GET'])
@permission_classes([AllowAny])
def items(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False)
    
    if category_id:
        items = items.filter(category_id=category_id)
    
    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    paginator = Paginator(items, PAGINATION)
    page = request.GET.get('page')

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('item/items_list.html', {
            'items': items,
            'paginator': paginator,
            'categories': categories,
            'category_id': int(category_id),
        })
        return JsonResponse({'html': html})

    return render(request, 'item/items.html', {
        'items': items,
        'query': query,
        'categories': categories,
        'category_id': int(category_id),
        'paginator': paginator,
    })


@swagger_auto_schema(
    method='get', 
    responses={200: 'Success'}
)
@api_view(['GET'])
@permission_classes([AllowAny])
def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]
    
    
    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_items,
        'category': item.category.name.lower()
    })


@swagger_auto_schema(
    methods=['GET', 'POST'],
    responses={200: 'Success', 201: 'Created'},
    operation_description="Получить форму для нового элемента или создать новый элемент"
)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            return redirect('item:detail', pk=item.id)
    else:
        form = NewItemForm()
    
    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Новый товар',
    })


@swagger_auto_schema(
    methods=['GET', 'POST'],
    responses={200: 'Success', 201: 'Created'},
    operation_description="Получить форму для изменения или изменить элемент"
)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)

    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)
        
        if form.is_valid():
            form.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = EditItemForm(instance=item)
    
    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Edit Item',
    })


@swagger_auto_schema(
    methods=['GET'], 
    responses={200: 'Success', 'ХАХХА':'ПОДПИСЫВАЙТЕСЬ НА БУСТИ'}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def delete(request, pk, creator):
    item = get_object_or_404(Item, pk=pk, created_by=creator)
    item.delete()
    
    return redirect('dashboard:index')


@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('query', openapi.IN_QUERY, description="Search query", type=openapi.TYPE_STRING),
        openapi.Parameter('category', openapi.IN_QUERY, description="Category ID", type=openapi.TYPE_INTEGER),
    ],
    responses={
        200: item_list_response,
        400: openapi.Response(description="Invalid input"),
    },
    operation_summary="Get a list of items of category",
    operation_description="Retrieve a list of items that match category ID. Returns a list of items with their details.",
    tags=['Items']
)
@api_view(['GET'])
@permission_classes([AllowAny])
def category(request, pk):
    categoryName = Category.objects.get(pk=pk)
    categoryname = "Товары в категории "+str(Category.objects.get(pk=pk)).lower()
    items = Item.objects.filter(is_sold=False, category=pk)
    
    paginator = Paginator(items, PAGINATION)
    page = request.GET.get('page')

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('item/items_list.html', {
            'items': items,
            'paginator': paginator,
        })
        return JsonResponse({'html': html})

    return render(request, 'item/category.html', {
        'items': items,
        'categoryName': categoryName,
        'categoryname': categoryname,
        'paginator': paginator,
    })