from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Post
from .serializers import PostBaseModelSerializer

class PostModelViewSet(ModelViewSet): #API
    queryset = Post.objects.all()
    serializer_class = PostBaseModelSerializer
    
    def get_serializer_class(self):
        print(self.action)
        if self.action == 'create':
            return PostBaseModelSerializer
        return super().get_serializer_class()