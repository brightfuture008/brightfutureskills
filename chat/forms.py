from django import forms
from .models import ChatMessage, CourseComment

class MessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['message']
        widgets = {
            'message': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Type a message...',
                'id': 'chat-message-input'
            })
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = CourseComment
        fields = ['content', 'rating']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write a comment...'
            }),
            'rating': forms.HiddenInput(attrs={
                'id': 'rating-input',
                'value': 5
            })
        }