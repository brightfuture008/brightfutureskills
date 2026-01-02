from django import forms
from .models import CourseComment, ChatMessage

class CommentForm(forms.ModelForm):
    class Meta:
        model = CourseComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Add a comment...'}),
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['message']
        widgets = {
            'message': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type a message...'}),
        }