from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView, DetailView, UpdateView, DeleteView, CreateView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django.utils import timezone

from blog.models import Post, Category, Comment
from .forms import CommentForm, PostForm
from core.constants import QUANTITY_ON_PAGE

User = get_user_model()


# ===== Миксины =====
class PublishedPostsMixin:
    """Миксин для получения только опубликованных постов."""

    def get_published_queryset(self, manager):
        return manager.filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True,
        ).annotate(comment_count=Count('comments')).order_by('-pub_date')


class OwnerOrPublishedMixin(PublishedPostsMixin):
    """Миксин для проверки авторства или получения опубликованных постов."""

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(
            Q(author_id=self.request.user.id) | Q(
                is_published=True,
                category__is_published=True,
                pub_date__lte=timezone.now()
            )
        )


class OwnerRequiredMixin:
    """Миксин для проверки, что пользователь является автором объекта."""

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not request.user.is_authenticated or obj.author != request.user:
            return redirect(
                'blog:post_detail',
                post_id=obj.post_id if hasattr(obj, 'post_id') else obj.id
            )
        return super().dispatch(request, *args, **kwargs)


class CommentObjectMixin:
    """Миксин для получения комментария и формирования success_url."""

    model = Comment
    pk_url_kwarg = 'comment_id'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Comment,
            id=self.kwargs['comment_id'],
            post_id=self.kwargs['post_id']
        )

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={
            'post_id': self.object.post_id})


# ===== Главная страница =====
class IndexListView(PublishedPostsMixin, ListView):
    model = Post
    template_name = 'blog/index.html'
    paginate_by = QUANTITY_ON_PAGE

    def get_queryset(self):
        return self.get_published_queryset(Post.objects)


# ===== Просмотр поста =====
class PostDetailView(OwnerOrPublishedMixin, DetailView):
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.all().order_by('created_at')
        return context


# ===== Создание поста =====
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:profile', kwargs={
            'username': self.request.user.username
        })


# ===== Редактирование поста =====
class PostUpdateView(OwnerRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={
            'post_id': self.object.id
        })


# ===== Удаление поста =====
class PostDeleteView(OwnerRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'
    success_url = reverse_lazy('blog:index')


# ===== Страница категории =====
class CategoryPostsListView(PublishedPostsMixin, ListView):
    model = Post
    template_name = 'blog/category.html'
    paginate_by = QUANTITY_ON_PAGE

    def get_queryset(self):
        category = self.get_category()
        return self.get_published_queryset(category.posts)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.get_category()
        return context

    def get_category(self):
        return get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )


# ===== Профиль пользователя =====
class ProfileListView(PublishedPostsMixin, ListView):
    """Страница профиля пользователя со списком его постов."""

    model = Post
    template_name = 'blog/profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    paginate_by = QUANTITY_ON_PAGE

    def get_profile_user(self):
        return get_object_or_404(
            User,
            username=self.kwargs['username']
        )

    def get_queryset(self):
        profile_user = self.get_profile_user()
        queryset = (
            Post.objects.filter(author=profile_user)
            .annotate(comment_count=Count('comments'))
            .order_by('-pub_date')
        )
        return queryset

    def get_context_data(self, **kwargs):
        """Добавляем в контекст объект пользователя профиля."""
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_profile_user()
        return context


# ===== Редактирование профиля =====
class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'blog/user.html'
    fields = ['first_name', 'last_name', 'username', 'email']
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('blog:profile', kwargs={
            'username': self.request.user.username
        })


# ===== Добавление комментария =====
@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        return redirect('blog:post_detail', post_id=post_id)
    return render(request, 'blog/detail.html', {
        'post': post,
        'form': form,
        'comments': post.comments.all().order_by('created_at')
    })


# ===== Редактирование комментария =====
class CommentUpdateView(CommentObjectMixin, OwnerRequiredMixin, UpdateView):
    form_class = CommentForm
    template_name = 'blog/comment.html'


# ===== Удаление комментария =====
class CommentDeleteView(OwnerRequiredMixin, CommentObjectMixin, DeleteView):
    template_name = 'blog/comment.html'
