from django import forms
from .models import AnimeComment

class AnimeCommentForm(forms.ModelForm):
    class Meta:
        model = AnimeComment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'placeholder': 'Оставить комментарий'})
        }
        labels = {
            'body': ''
        }
