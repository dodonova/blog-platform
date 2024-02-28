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


class PostsPublicListView(ListView):
    """
    View to display a list of public posts with pagination.
    """
    model = Post
    queryset = Post.public_objects.annotate(
        comment_count=Count("comments"))
    paginate_by = 10


class BlogListView(PostsPublicListView):
    """
    View to display a list of public posts on the blog's index page.
    """
    template_name = 'blog/index.html'


class ByCategoryListView(PostsPublicListView):
    """
    View to display a list of public posts filtered by category.
    """
    template_name = 'blog/category.html'

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
        return context


class ByProfileListView(PostsPublicListView):
    template_name = 'blog/profile.html'

    def get_queryset(self) -> QuerySet[Any]:
        """
        Get the queryset of posts filtered by category.
        """
        username = self.kwargs.get('username')
        post_list = Post.objects.all().filter(
            author__username=username
        ).order_by('-pub_date')
        return post_list

    def get_context_data(self, **kwargs):
        """
        Add category to the context data.
        """
        context = super().get_context_data(**kwargs)
        user = self.kwargs.get('username')
        profile = get_object_or_404(
            User.objects.filter(username__exact=user)
        )
        context["user"] = self.request.user
        context["profile"] = profile
        return context


class PostDetailView(DetailView):
    """
    View to display the details of a single post.
    """
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
    """
    View to create a new blog post.
    """
    model = Post
    template_name = 'blog/create.html'
    form_class = PostForm

    def form_valid(self, form):
        """
        Set the author of the post as the current user.
        """
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """
        Redirect to the profile page after successful post creation.
        """
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class PostUpdateView(LoginRequiredMixin, UpdateView):
    """
    View to update an existing blog post.
    """
    model = Post
    fields = '__all__'
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        """
        Check if the user is the author of the post before allowing update.
        """
        instance = get_object_or_404(Post, pk=kwargs['pk'])
        if instance.author != request.user:
            return redirect('blog:post_detail', pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})


class PostDeleteView(LoginRequiredMixin, DeleteView):
    """
    View to delete an existing blog post.
    """
    model = Post
    template_name = 'blog/create.html'

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        """
        Check if the user is the author of the post before allowing delete.
        """
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
    """
    View to update the user profile.
    """    
    model = User
    fields = (
        'username',
        'email',
        'first_name',
        'last_name'
    )
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        """
        Get the current user's profile.
        """
        return self.request.user

    def get_success_url(self):
        """
        Redirect to the user profile page after successful update.
        """
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.object.username}
        )


class CommentCreateView(LoginRequiredMixin, CreateView):
    """
    View to create a new comment on a post.
    """
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
    """
    View to update an existing comment on a post.
    """
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
