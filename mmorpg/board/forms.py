from django import forms
from django.core.exceptions import ValidationError
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Post, Reaction


class PostForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = [
            'category',
            'title',
            'text',
        ]


class ReactionForm(forms.ModelForm):

    class Meta:
        model = Reaction
        fields = [
            'text',
        ]
