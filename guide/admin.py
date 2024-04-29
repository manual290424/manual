from django.contrib import admin

from .models import Category, Teststask, Question, Protocol

# Добавление модели на главную страницу интерфейса администратора
admin.site.register(Category)
admin.site.register(Teststask)
admin.site.register(Question)
admin.site.register(Protocol)
