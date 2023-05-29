from django.shortcuts import render
from django.shortcuts import get_object_or_404

from blog.models import Post, Category


def index(request):
    template = 'blog/index.html'
    # posts = get_full_public_posts_info().order_by('-pub_date')[:5]
    posts = Post.public_objects.all().order_by('-pub_date')[:5]
    context = {'post_list': posts}
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
    context = {'category': category,
               'post_list': post_list}
    return render(request, template, context)
