from django.db import models
#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _

from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

from django.contrib.auth.models import User

# Create your models here.

# Модели отображают информацию о данных, с которыми вы работаете.
# Они содержат поля и поведение ваших данных.
# Обычно одна модель представляет одну таблицу в базе данных.
# Каждая модель это класс унаследованный от django.db.models.Model.
# Атрибут модели представляет поле в базе данных.
# Django предоставляет автоматически созданное API для доступа к данным

# choices (список выбора). Итератор (например, список или кортеж) 2-х элементных кортежей,
# определяющих варианты значений для поля.
# При определении, виджет формы использует select вместо стандартного текстового поля
# и ограничит значение поля указанными значениями.

# Категория тестового задания
class Category(models.Model):
    # Читабельное имя поля (метка, label). Каждое поле, кроме ForeignKey, ManyToManyField и OneToOneField,
    # первым аргументом принимает необязательное читабельное название.
    # Если оно не указано, Django самостоятельно создаст его, используя название поля, заменяя подчеркивание на пробел.
    # null - Если True, Django сохранит пустое значение как NULL в базе данных. По умолчанию - False.
    # blank - Если True, поле не обязательно и может быть пустым. По умолчанию - False.
    # Это не то же что и null. null относится к базе данных, blank - к проверке данных.
    # Если поле содержит blank=True, форма позволит передать пустое значение.
    # При blank=False - поле обязательно.
    title = models.CharField(_('category_title'), max_length=128, unique=True)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'category'
    def __str__(self):
        # Вывод названияв тег SELECT 
        return "{}".format(self.title)

# Тестовое задание
class Teststask(models.Model):
    category = models.ForeignKey(Category, related_name='teststask_category', on_delete=models.CASCADE)
    title = models.CharField(_('teststask_title'), max_length=255)
    details = models.TextField(_('teststask_details'), blank=True, null=True)
    minutes = models.IntegerField(_('minutes'))
    limit = models.IntegerField(_('limit'))
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'teststask'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['title']),
        ]
        # Сортировка по умолчанию
        ordering = ['title']
    def __str__(self):
        # Вывод названияв тег SELECT 
        return "{} {}".format(self.title, self.category)
     
# Вопросы и ответы к тестовому заданию
class Question(models.Model):
    teststask = models.ForeignKey(Teststask, related_name='question_teststask', on_delete=models.CASCADE)
    question = models.TextField(_('question'))
    photo = models.ImageField(_('photo'), upload_to='images/', blank=True, null=True)
    reply1 = models.TextField(_('reply1'))
    ok1 = models.BooleanField(_('ok1'), default = False)
    reply2 = models.TextField(_('reply2'))
    ok2 = models.BooleanField(_('ok2'), default = False)
    reply3 = models.TextField(_('reply3'), blank=True, null=True)
    ok3 = models.BooleanField(_('ok3'), default = False)
    reply4 = models.TextField(_('reply4'), blank=True, null=True)
    ok4 = models.BooleanField(_('ok4'), default = False)
    reply5 = models.TextField(_('reply5'), blank=True, null=True)
    ok5 = models.BooleanField(_('ok5'), default = False)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'question'
    # Мультивариантный ответ (да или нет)
    def multi(self):
        i = 0
        if self.ok1 == True:
            i = i + 1
        if self.ok2 == True:
            i = i + 1
        if self.ok3 == True:
            i = i + 1
        if self.ok4 == True:
            i = i + 1
        if self.ok5 == True:
            i = i + 1
        if i > 1:
            return True
        else:
            return False
    # Правильный ответ (ответы). Например если второй ответ правильный то correctly='2', если третий и пятый то correctly='35'...
    def correctly(self):
        right = ''
        if self.ok1 == True:
            right = right + '1'
        if self.ok2 == True:
            right = right + '2'
        if self.ok3 == True:
            right = right + '3'
        if self.ok4 == True:
            right = right + '4'
        if self.ok5 == True:
            right = right + '5'
        return right
        
# Протокол выполнения тестового задания
class Protocol(models.Model):
    teststask = models.ForeignKey(Teststask, related_name='protocol_teststask', on_delete=models.CASCADE)
    datep = models.DateTimeField(_('datep'), auto_now_add=True)
    result = models.DecimalField(_('result'), max_digits=5, decimal_places=1)
    details = models.TextField(_('protocol_details'), blank=True, null=True)
    user = models.ForeignKey(User, related_name='protocol_user', on_delete=models.CASCADE)
    comment = models.TextField(_('protocol_comment'), blank=True, null=True)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'protocol'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['datep']),
        ]
        # Сортировка по умолчанию
        ordering = ['datep']
        
