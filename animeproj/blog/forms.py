from django import forms
from .models import BlogComment

class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'placeholder': 'Оставить комментарий'})
        }
        labels = {
            'body': ''
        }
