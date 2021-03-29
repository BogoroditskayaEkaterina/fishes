from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count

from .models import Blog, Post
from .forms import LoginForm, RegistrationForm

def main(request):
    return render(request, 'main/index.html')

def log_out(request):
    logout(request)
    redirect_url = request.GET.get('next') or reverse('index')
    return redirect(redirect_url)

def log_in(request):
    if request.method == 'POST':
        logout(request)
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(request.GET['next'])
            else:
                form.add_error('username', 'Пользователя с такими данными нет')
    else: # GET
        form = LoginForm()
    return render(request, 'main/login.html', {'form': form})


def sign_up(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            logout(request)
            blog_title = form.cleaned_data['blog_title']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password_again = form.cleaned_data['password_again']
            if User.objects.filter(username=username).exists():
                form.add_error('username', 'Имя уже занято')
            elif password != password_again:
                form.add_error('password_again', 'Пароли не совпадают')
            else:
                user = User.objects.create_user(username, email, password)
                blog = Blog.objects.create(author=user, title=blog_title)
                login(request, user)
                context = {'blog': blog, 'posts': []}
                return render(request, 'main/posts.html', context)
    else: # GET
        form = RegistrationForm()
    return render(request, 'main/signup.html', {'form': form})


def get_blog_list(request):
    blogs = Blog.objects.annotate(post_count=Count('post')).order_by('created_at')
    context = {'blogs': blogs}
    return render(request, 'main/blog.html', context)


@login_required(login_url='/main/login')
def blog(request, blog_id):
    if request.method == 'POST':
        return create_post(request, blog_id)
    else:
        return render_blog(request, blog_id)


def render_blog(request, blog_id, additional_context={}):
    blog = get_object_or_404(Blog, id=blog_id)
    context = {
        'blog': blog,
        'posts': blog.post_set.order_by('-created_at'),
        **additional_context
    }
    return render(request, 'main/posts.html', context)


def create_post(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if blog.author_id != request.user.id:
        return HttpResponseForbidden('Тебе нельзя постить в этом блоге')

    subject = request.POST['subject']
    subject_error = None
    if not subject or subject.isspace():
        subject_error = 'Пожалуйста, дайте название вашему посту'

    text = request.POST['text']
    text_error = None
    if not text or text.isspace():
        text_error = 'Пожалуйста, напишите текст'

    #image = 'img/defaultUser.png'

    if subject_error or text_error:
        error_context = {
            'subject_error': subject_error,
            'text_error': text_error,
            'subject': subject,
            'text': text
        }
        return render_blog(request, blog_id, error_context)
    else:
        if request.FILES:
            image = request.FILES['image']
            Post(blog_id=blog.id, subject=subject, text=text, image=image).save()
        else:
            Post(blog_id=blog.id, subject=subject, text=text).save()
        return HttpResponseRedirect(reverse('blog_by_id', kwargs={'blog_id': blog_id}))

def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    blog = get_object_or_404(Blog, id=post.blog_id)
    if blog.author_id != request.user.id:
        #return HttpResponseForbidden('Ты не можешь удалять чужие посты')
        return render(request, 'main/sorry.html')
    post.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def get_info(request):
    blogs = Blog.objects.annotate(post_count=Count('post'))
    amount_posts = 0

    for blog in blogs:
        amount_posts += blog.post_count

    amount_blogs = Blog.objects.count()
    last_post = Post.objects.order_by('-created_at')[0]

    context = {
        'amount_posts': amount_posts,
        'amount_blogs': amount_blogs,
        'last_post': last_post
    }
    return render(request, 'main/news.html', context)