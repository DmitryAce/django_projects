from django.contrib import admin
from .models import Author, Category, Tag, Article

# Регистрация модели Author
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'affiliation', 'email')  # Поля в списке
    search_fields = ('name', 'email')  # Поля для поиска

# Регистрация модели Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Поля в списке
    search_fields = ('name',)  # Поля для поиска

# Регистрация модели Tag
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Поля в списке
    search_fields = ('name',)  # Поля для поиска

# Регистрация модели Article
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'published', 'created_at', 'updated_at')  # Поля в списке
    list_filter = ('published', 'category', 'tags')  # Фильтры
    search_fields = ('title', 'abstract', 'content')  # Поля для поиска
    filter_horizontal = ('authors', 'tags')  # Удобный выбор для ManyToMany-полей
    fieldsets = (  # Группировка полей при редактировании
        (None, {
            'fields': ('title', 'abstract', 'content', 'pdf_file')
        }),
        ('Метаданные', {
            'fields': ('authors', 'category', 'tags', 'published', 'published_by')
        }),
    )
    readonly_fields = ('created_at', 'updated_at')  # Поля только для чтения

    # Логика автоматического заполнения поля published_by
    def save_model(self, request, obj, form, change):
        if obj.published and not obj.published_by:
            obj.published_by = request.user
        super().save_model(request, obj, form, change)