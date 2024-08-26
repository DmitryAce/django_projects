from django.contrib import admin

from .models import Category, Scientist

# Register your models here.
admin.site.register(Scientist)
admin.site.register(Category)