from django.shortcuts import render,HttpResponse,get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from comment.models import Comment
from comment.form import CommentForm
from read_num.utils import read_num_method,get_seven_day_read_method
from read_num.models import ReadDetail
from .models import BlogType,Blog

# Create your views here.

def get_blog_list_comman_data(request,blog_all_list):
    paginator = Paginator(blog_all_list,5)
    page_num = request.GET.get('page', 1)
    # 获取所有页码
    page_of_blogs = paginator.get_page(page_num)
    #获取当前页
    current_page_num = page_of_blogs.number
    #获取前后两页的页码范围
    page_range = list(range(max(current_page_num-2,1),current_page_num))+\
                 list(range(current_page_num,min(current_page_num+2,paginator.num_pages+1)))
    #加上省略标记
    if page_range[0]-1>=2:
        page_range.insert(0,'...')
    if paginator.num_pages - page_range[-1] >=2:
        page_range.append('...')
    #加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0,1)
    if page_range[-1] !=paginator.num_pages :
        page_range.append(paginator.num_pages)
    blogtypes = BlogType.objects.all()
    context = {
        'blogs':page_of_blogs.object_list,
        'page_of_blogs':page_of_blogs,
        'page_range':page_range,
        "blogtypes" : blogtypes,
        # 'blog_types':BlogType.objects.annotate(blog_)

    }
    return context
def home(request):
    week,read_nums=get_seven_day_read_method(Blog)
    context={
        'week':week,
        'read_nums':read_nums
    }
    return render(request, 'home.html', context=context)

def blog_list(request):
    blogs=Blog.objects.all()
    context = get_blog_list_comman_data(request,blogs)
    return render(request, 'blog/blog_list.html', context=context)

def blog_type(request,blog_type_pk):
    blogtypes = BlogType.objects.all()
    blogs=Blog.objects.filter(blog_type_id=blog_type_pk)
    context = get_blog_list_comman_data(request,blogs)
    return render(request, 'blog/blog-type.html',context=context)


def blog_detail(request,pk):
    # 获取Blog对象
    blog=get_object_or_404(Blog,id=pk)
    #blog所有分类
    blogtypes = BlogType.objects.all()

    # 阅读计数cookie
    read_cookie_key = read_num_method(request,blog)
    # 评论对象
    blog_content_type = ContentType.objects.get_for_model(blog)
    comments =Comment.objects.filter(content_type=blog_content_type,object_id=blog.pk,parent=None)
    context={
        'blog':blog,
        'comments':comments,
        'comment_form':CommentForm(initial={'content_type':'Blog','object_id':blog.pk,
                                       'reply_to':0}),
        'blogtypes':blogtypes
    }
    response=render(request,'blog/blog_content.html',context=context)
    response.set_cookie(read_cookie_key,'true',expires=60*60*24)

    return  response

