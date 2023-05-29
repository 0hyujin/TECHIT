from rest_framework import serializers
from .models import Post

class PostBaseModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        # fields = ['image', 'content',]