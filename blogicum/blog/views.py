from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView,
    UpdateView,
    DetailView,
    ListView,
    DeleteView
    )

from .models import Post, Category
from .forms import PostForm

User = get_user_model()

# class PostMixin:
#     model = Post
#     queryset = Post.objects.select_related('author'
#                     ).select_related('location'
#                     ).select_related('category')


class BlogListView(ListView):
    model = Post
    queryset = Post.public_objects.all()
    template_name = 'blog/index.html'
    ordering = ['-pub_date']
    paginate_by = 10


class ByCategoryListView(ListView):
    model = Post
    template_name = 'blog/category.html'
    # ordering = 'title'
    paginate_by = 10

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        return Post.public_objects.all().filter(
            category__slug=category_slug
            ).order_by('-pub_date')

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(
            Category.objects.all().filter(is_published=True),
            slug=self.kwargs.get('category_slug')
        )
        context['category'] = category
        return context


class ByProfileListView(ListView):
    model = Post
    template_name = 'blog/profile.html'
    ordering = 'title'
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        username = self.kwargs.get('username')
        post_list = Post.objects.all().filter(
            author__username=username
            ).order_by('-pub_date')
        return post_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.kwargs.get('username')
        profile = get_object_or_404(
            User.objects.filter(username__exact=user)
            )
        context["user"] = self.request.user
        context["profile"] = profile
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'


class PostCreateView(CreateView, LoginRequiredMixin):
    model = Post
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = '__all__'
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        instance = get_object_or_404(Post, pk=kwargs['pk'])
        if instance.author != request.user:
            raise HttpResponseForbidden
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})


class PostDeleteView(DeleteView, LoginRequiredMixin):
    model = Post
    template_name = 'blog/create.html'

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        instance = get_object_or_404(Post, pk=kwargs['pk'])
        if instance.author != request.user:
            raise HttpResponseForbidden
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class UserUpdateView(UpdateView, LoginRequiredMixin):
    model = User
    fields = (
        'username',
        'email',
        'first_name',
        'last_name'
    )
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.object.username}
        )
