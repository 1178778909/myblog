from django.shortcuts import render, redirect
from django.core.cache import cache
from django.contrib.contenttypes.models import ContentType
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import JsonResponse

from read_statistics import utils
from blog.models import Blog
from .forms import LoginForm, RegForm

def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = utils.get_seven_days_read_data(blog_content_type)

    # 获取七天热门博客的缓存数据
    hot_data_7days = cache.get('get_7days_hot_data')
    if hot_data_7days is None:
        hot_data_7days = utils.get_7days_hot_data(blog_content_type)
        cache.set('get_7days_hot_data', hot_data_7days, 3600)

    context = {}
    context['today_hot_data'] = utils.get_today_hot_data(blog_content_type)
    context['yesterday_hot_data'] = utils.get_yesterday_hot_data(blog_content_type)
    context['hot_data_7days'] = hot_data_7days
    context['dates'] = dates
    context['read_nums'] = read_nums
    return render(request, 'home.html', context)

def login(request):   
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from'), reverse('home'))                  
    else:
        login_form = LoginForm()

    context = {}
    context['login_form'] = login_form
    return render(request, 'login.html', context)

def login_for_modal(request):
    login_form = LoginForm(request.POST)
    data = {}
    if login_form.is_valid():
        user = login_form.cleaned_data['user']
        auth.login(request, user)
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data) 

def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST)    
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']      
            password = reg_form.cleaned_data['password'] 
            email = reg_form.cleaned_data['email']
            # 创建用户
            user = User.objects.create_user(username, email, password)    
            user.save()
            # 登录用户
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        reg_form = RegForm()

    context = {}
    context['reg_form'] = reg_form
    return render(request, 'register.html', context)

    