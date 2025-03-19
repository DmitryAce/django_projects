from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Author(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя автора")
    affiliation = models.CharField(max_length=255, blank=True, verbose_name="Место работы")
    email = models.EmailField(blank=True, verbose_name="Email")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Название категории")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Название тега")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

class Article(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    abstract = models.TextField(verbose_name="Аннотация")
    content = models.TextField(verbose_name="Содержание")
    pdf_file = models.FileField(upload_to='articles/pdfs/', blank=True, null=True, verbose_name="PDF-файл")
    authors = models.ManyToManyField(Author, related_name='articles', verbose_name="Авторы")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name="Категория")
    tags = models.ManyToManyField(Tag, related_name='articles', verbose_name="Теги")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    published = models.BooleanField(default=False, verbose_name="Опубликовано")
    published_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Опубликовал")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"