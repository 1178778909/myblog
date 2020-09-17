from django.shortcuts import render_to_response
from django.contrib.contenttypes.models import ContentType
from read_statistics import utils
from blog.models import Blog

def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = utils.get_seven_days_read_data(blog_content_type)

    context = {}
    context['today_hot_data'] = utils.get_today_hot_data(blog_content_type)
    context['yesterday_hot_data'] = utils.get_yesterday_hot_data(blog_content_type)
    context['hot_data_7days'] = utils.get_7days_hot_data()
    context['dates'] = dates
    context['read_nums'] = read_nums
    return render_to_response('home.html', context)