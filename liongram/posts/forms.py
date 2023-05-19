from django import forms
from .models import Post

# class PostBaseForm(forms.Form):
#     image = forms.ImageField()
#     content = forms.CharField(widget=forms.Textarea)

class PostBaseForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = "__all__"

class PostCreateForm(PostBaseForm):
    class Meta(PostBaseForm.Meta):
        fields = ['image', 'content']