from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

from blog.models import Post, Category

 

def index(request):
    template = 'blog/index.html'
    posts = Post.public_objects.all().order_by('-pub_date')[:5]
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, template, context)


def post_detail(request, id):
    template = 'blog/detail.html'
    post = get_object_or_404(Post.public_objects.all(), pk=id)
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category.objects.values(
            'title', 'description'
        ).filter(is_published=True),
        slug=category_slug
    )
    post_list = Post.public_objects.all().filter(
        category__slug__exact=category_slug,
    )
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'category': category,
               'page_obj': page_obj}
    return render(request, template, context)
