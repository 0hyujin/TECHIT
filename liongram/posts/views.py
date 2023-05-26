from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required

import accounts


from .forms import PostBaseForm, PostCreateForm, PostDetailForm
from .models import Post


def index(request):
    post_list = Post.objects.all()
    context ={
        'post_list': post_list
    }
    return render(request, 'index.html', context)

def post_list_view(request):
    #post_list = Post.objects.all()
    post_list = Post.objects.filter(writer = request.user)
    context = {
        'post_list': post_list
    }
    return render(request, 'posts/post_list.html', context)


def post_detail_view(request,id):
    if request.method == 'GET':
        if request.user.is_authenticated: # 사용자가 인증되어있으면 = 로그인 되있으면
            try:
                post = Post.objects.get(id=id) #id에 해당하는 게시물 검색
            except Post.DoesNotExist: #예외발생
                return redirect('index')
            context = {
                'post':post
            }
            return render(request, 'posts/post_detail.html',context)
        else: #사용자 인증이 되어있지 않으면 = 로그인 안되어있으면
            return redirect('/accounts/login')
    ###########################
    # post = Post.objects.get(id=id)
    # context = {
    #     'post' :post
    # }
    # return render(request, 'posts/post_detail.html', context)
        
@login_required
def post_create_view(request):
    if request.method == 'GET':
        return render(request, 'posts/post_form.html', {'form': PostBaseForm()})
    else:
        image = request.FILES.get('image')
        content = request.POST.get('content')
        Post.objects.create(
            image = image,
            content = content,
            writer = request.user
        )
        return redirect('index')

def post_create_form_view(request):
    if request.method == 'GET':
        form = PostBaseForm()
        context = {'form': form}
        return render(request, 'posts/post_form2.html', context)
    else:
        form = PostBaseForm(request.POST, request.FILES)

        if form.is_valid():
            Post.objects.create(
                image=form.cleaned_data['image'],
                content=form.cleaned_data['content'],
                writer=request.user
            )
        else:
            return redirect('posts:post-create')
        return redirect('index')
        #image = request.FILES.get('image')
        #content = request.POST.get('content')
        # Post.objects.create(
        #     image = image,
        #     content = content,
        #     writer = request.user
        # )
        # return redirect('index')

def post_update_view(request, id):
    post = Post.objects.get(id=id)
    if request.method == 'GET':
        context = {
            'post' : post
        }
        return render(request, 'posts/post_form.html', context)
    elif request.method =='POST':
        new_image = request.FILES.get('image')
        content = request.POST.get('content')
        if new_image :
            post.image.delete()
            post.image = new_image
        post.content = content
        post.save()
        return redirect('post_detail', post.id)

def post_delete_view(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'GET':
        context = {
            #'post':post
            'accounts':accounts
        }
        return render(request, 'posts/post_confirm_delete.html', context)
    else:
        post.delete()
        return redirect('index')

def url_view(request):
    print('url_view()')
    data = {'code': '001', 'msg':'OK'}
    return HttpResponse('<h1>url_view</h1>')
    #return JsonResponse(data)

def url_parameter_view(request, username):
    print('url_parameter_view()')
    print(f'username: {username}')
    print(f'request.GET: {request.GET}')
    return HttpResponse(username)

def function_view(request):
    print(f'request.method: {request.method}')
    if request.method == 'GET':
        print(f'request.GET: {request.GET}')
    elif request.method == 'POST':
        print(f'request.POST: {request.POST}')
    return render(request, 'view.html')

class class_view(ListView):
    model = Post
    template_name = 'cbv_view.html'

def function_list_view(request):
    object_list = Post.objects.all().order_by('-id')
    return render(request, 'cbv_view.html', {'object_list':object_list})