import datetime

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Category(models.Model):
    title = models.CharField(
        verbose_name="Заголовок",
        max_length=256,
        null=False
    )
    description = models.TextField(
        verbose_name="Описание",
        null=False
    )
    slug = models.SlugField(
        verbose_name="Идентификатор",
        unique=True,
        null=False,
        help_text="Идентификатор страницы для URL; разрешены символы латиницы, цифры, дефис и подчёркивание."
    )
    is_published = models.BooleanField(
        verbose_name="Опубликовано",
        default=True,
        null=False,
        help_text="Снимите галочку, чтобы скрыть публикацию."
    )
    created_at = models.DateTimeField(
        verbose_name="Добавлено",
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title 

class Location(models.Model):
    name = models.CharField(
        verbose_name="Название места",
        max_length=256,
        null=False
    )
    is_published = models.BooleanField(
        verbose_name="Опубликовано",
        default=True,
        null=False,
        help_text="Снимите галочку, чтобы скрыть публикацию."
    )
    created_at = models.DateTimeField(
        verbose_name="Добавлено",
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name 


class Post(models.Model):
    title = models.CharField(
        verbose_name="Заголовок",
        max_length=256,
        null=False
    )
    text = models.TextField(
        verbose_name="Текст",
        null=False
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата и время публикации",
        default=True,
        help_text="Если установить дату и время в будущем — можно делать отложенные публикации."
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="Автор публикации",
        null=False
    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        related_name="posts"
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Местоположение',
        related_name="posts"
    )
    is_published = models.BooleanField(
        verbose_name="Опубликовано",
        default=True,
        null=False,
        help_text="Снимите галочку, чтобы скрыть публикацию."
    )
    created_at = models.DateTimeField(
        verbose_name="Добавлено",
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации' 
        ordering = ('pub_date',)

    def __str__(self):
        return self.title 
