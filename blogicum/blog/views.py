from typing import Any
from django.db.models import Count
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect
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

from .models import Post, Category, Comment
from .forms import PostForm, CommentForm

User = get_user_model()


class BlogListView(ListView):
    model = Post
    queryset = Post.public_objects.annotate(
        comment_count=Count("comments"))
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
        return Post.public_objects.all(
        ).filter(category__slug=category_slug).order_by('-pub_date')

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(
            Category.objects.all().filter(is_published=True),
            slug=self.kwargs.get('category_slug')
        )
        context['category'] = category
        for post in context['object_list']:
            post.comment_count = post.comments.count()
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
        for post in context['object_list']:
            post.comment_count = post.comments.count()
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comments.select_related('author')
        )
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/create.html'
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
            return redirect('blog:post_detail', pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        instance = get_object_or_404(Post, pk=kwargs['pk'])
        if instance.author != request.user:
            return redirect('blog:post_detail', pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class UserUpdateView(LoginRequiredMixin, UpdateView):
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


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'includes/comments.html'

    def form_valid(self, form):
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'pk': self.kwargs['pk']}
        )


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        instance = get_object_or_404(Comment, pk=self.kwargs['comment_pk'])
        if instance.author != request.user:
            return redirect('blog:post_detail', pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(Comment, pk=self.kwargs['comment_pk'])

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'pk': self.kwargs['pk']}
        )


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment.html'

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        instance = get_object_or_404(Comment, pk=self.kwargs['comment_pk'])
        if instance.author != request.user:
            return redirect('blog:post_detail', pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(Comment, pk=self.kwargs['comment_pk'])

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'pk': self.kwargs['pk']}
        )
