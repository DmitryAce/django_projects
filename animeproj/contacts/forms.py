from django import forms
from .models import ConversationMessage

class ConversationMessageForm(forms.ModelForm):
    class Meta:
        model = ConversationMessage
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control', 
                'style': 'resize: none;', 
                'placeholder': 'Введите ваше сообщение...'
            }),
        }
        labels = {
            'content': 'Сообщение',
        }
