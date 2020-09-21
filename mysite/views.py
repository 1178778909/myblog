from django.shortcuts import render, redirect
from django.core.cache import cache
from django.contrib.contenttypes.models import ContentType
from django.contrib import auth
from django.urls import reverse

from read_statistics import utils
from blog.models import Blog

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
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(request, username=username, password=password)
    referer = request.META.get('HTTP_REFERER', reverse('home'))
    if user is not None:
        auth.login(request, user)
        return redirect(referer)
    else:
        return render(request, 'error.html', {'msessage':'用户名或密码不正确'})
