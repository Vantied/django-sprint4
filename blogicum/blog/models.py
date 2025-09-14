from django.db import models
from django.contrib.auth import get_user_model

from core.models import PublishedModel
from core.constants import MAX_LENGHT_TITLE, MAX_LENGHT_SLUG

User = get_user_model()


class Category(PublishedModel):
    title = models.CharField(
        max_length=MAX_LENGHT_TITLE,
        verbose_name='Заголовок',
        help_text='Максимальная длина строки — 256 символов'
    )
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        max_length=MAX_LENGHT_SLUG,
        unique=True,
        verbose_name='Идентификатор',
        help_text='Идентификатор страницы для URL; разрешены символы латиницы,'
        ' цифры, дефис и подчёркивание.'
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(PublishedModel):
    name = models.CharField(
        max_length=MAX_LENGHT_TITLE,
        verbose_name='Название места',
        help_text='Максимальная длина строки — 256 символов'
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Post(PublishedModel):
    title = models.CharField(
        max_length=MAX_LENGHT_TITLE,
        verbose_name='Заголовок',
        help_text='Максимальная длина строки — 256 символов'
    )
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text='Если установить дату и время в будущем'
        ' — можно делать отложенные публикации.'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author',
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        null=True,
        blank=False,
        verbose_name='Категория',
        related_name='posts'
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='blog_images',
        blank=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title


class Comment(PublishedModel):
    text = models.TextField(verbose_name='Комментарий')
    