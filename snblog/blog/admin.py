from django.contrib import admin

# Register your models here.

from .models import Category, Post, Location


admin.site.empty_value_display = 'Не задано'

admin.site.register(Category)
admin.site.register(Location)
admin.site.register(Post)