from django.shortcuts import render, get_object_or_404
from django.db.models.functions import Now
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView

from blog.models import Post, Category
from core.constants import QUANTITY_ON_MAIN


class IndexListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    paginate_by = QUANTITY_ON_MAIN

    def get_queryset(self):
        return published(Post.objects)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_queryset(self):
        return published(Post.objects)


class CategoryPostsListView(ListView):
    model = Category
    template_name = template = 'blog/category.html'
    paginate_by = QUANTITY_ON_MAIN

    def get_queryset(self):
        category = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )
        return published(category.posts)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )
        return context


def published(manager):
    """Возвращает только опубликованные"""
    return manager.filter(
        pub_date__lte=Now(),
        is_published=True,
        category__is_published=True,
    )
