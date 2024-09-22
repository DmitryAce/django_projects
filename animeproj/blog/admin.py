from django.contrib import admin
from .models import BlogPost, BlogContentBlock, BlogComment


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('title', 'cover_image', 'header_image')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    list_display = ('title', 'created_at', 'updated_at',)
    search_fields = ('title',)
    list_filter = ('created_at', 'updated_at',)
    ordering = ('-created_at',)


@admin.register(BlogContentBlock)
class BlogContentBlockAdmin(admin.ModelAdmin):
    list_display = ('blog_post', 'order', 'header', 'short_text', 'image',)
    search_fields = ('blog_post__title', 'text',)
    ordering = ('blog_post', 'order',)

    def short_text(self, obj):
        return obj.text[:30] + '...' if obj.text else 'No text'
    short_text.short_description = 'Content Snippet'


@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ('blog_title', 'user', 'short_body', 'created_at',)
    search_fields = ('blog__title', 'user__username',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)

    def blog_title(self, obj):
        return obj.blog.title
    blog_title.short_description = 'Blog Title'
