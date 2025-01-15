import datetime

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Category(models.Model):
    title = models.CharField(
        verbose_name="Название",
        max_length=256,
        null=False
    )
    description = models.TextField(
        verbose_name="Описание",
        null=False
    )
    slug = models.SlugField(
        verbose_name="Слаг",
        unique=True,
        null=False
    )
    is_published = models.BooleanField(
        default=True,
        null=False
    )
    created_at = models.DateTimeField(
        null=False,
        default=True
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title 

class Location(models.Model):
    name = models.CharField(
        verbose_name="Название",
        max_length=256,
        null=False
    )
    is_published = models.BooleanField(
        default=True,
        null=False
    )
    created_at = models.DateTimeField(
        null=False,
        default=True
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения' 

    def __str__(self):
        return self.name 


class Post(models.Model):
    title = models.CharField(
        verbose_name="Название",
        max_length=256,
        null=False
    )
    text = models.TextField(
        verbose_name="Текст",
        null=False
    )
    pub_date = models.DateTimeField(
        default=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="Автор",
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
        default=True,
        null=False
    )
    created_at = models.DateTimeField(
        null=False,
        default=True
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации' 

    def __str__(self):
        return self.title 
