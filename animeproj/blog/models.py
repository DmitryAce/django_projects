from django.db import models
from django.contrib.auth.models import User

class BlogPost(models.Model):
    title = models.CharField(max_length=255, help_text='Enter the title of the blog post.')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cover_image = models.ImageField(upload_to='blog/blog_cover', blank=False, null=False)
    header_image = models.ImageField(upload_to='blog/blog_headers', blank=True, null=True)

    def __str__(self):
        return self.title
    
    def summary(self):
        return self.content_blocks.first().text[:50] + '...' if self.content_blocks.exists() else 'No content'


class BlogContentBlock(models.Model):
    blog_post = models.ForeignKey(BlogPost, related_name='content_blocks', on_delete=models.CASCADE)
    header = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']


class BlogComment(models.Model):
    blog = models.ForeignKey('BlogPost', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'Comment for {self.blog.title} from {self.user.username}'
    
    
    def short_body(self):
        return self.body[:30] + '...' if len(self.body) > 30 else self.body
    
    
    class Meta:
        unique_together = ('blog', 'user')
        ordering = ('blog',)
        verbose_name_plural = 'Blog Comments'
