from django import forms
from django.forms import ModelForm, TextInput, Textarea, DateInput, NumberInput, CheckboxInput
from .models import Category, Teststask, Question, Protocol
#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

# При разработке приложения, использующего базу данных, чаще всего необходимо работать с формами, которые аналогичны моделям.
# В этом случае явное определение полей формы будет дублировать код, так как все поля уже описаны в модели.
# По этой причине Django предоставляет вспомогательный класс, который позволит вам создать класс Form по имеющейся модели
# атрибут fields - указание списка используемых полей, при fields = '__all__' - все поля
# атрибут widgets для указания собственный виджет для поля. Его значением должен быть словарь, ключами которого являются имена полей, а значениями — классы или экземпляры виджетов.
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title',]
        widgets = {
            'title': TextInput(attrs={"size":"100"}),            
        }
        labels = {
            'title': _('category_title'),            
        }
    # Метод-валидатор для поля title
    def clean_title(self):
        data = self.cleaned_data['title']
        # Ошибка если начинается не с большой буквы
        #if data.istitle() == False:
        #    raise forms.ValidationError(_('Value must start with a capital letter'))
        # Ошибка минимальная длина
        if len(data) < 3:
            raise forms.ValidationError(_('Minimum length 3 characters'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data

class TeststaskForm(forms.ModelForm):
    class Meta:
        model = Teststask
        fields = ['category', 'title', 'details', 'minutes', 'limit']
        widgets = {
            'category': forms.Select(attrs={'class': 'chosen'}),
            'title': TextInput(attrs={"size":"100"}),
            'details': Textarea(attrs={'cols': 80, 'rows': 6}),            
            'minutes': NumberInput(attrs={"size":"10", "min":3}),
            'limit': NumberInput(attrs={"size":"10", "min":50, "max":100}),            
        }
        labels = {
            'category': _('category'),            
        }        
    # Метод-валидатор для поля title
    def clean_title(self):
        data = self.cleaned_data['title']
        if len(data) < 3:
            raise forms.ValidationError(_('Minimum length 3 characters'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data
    # Метод-валидатор для поля minutes
    def clean_minutes(self):
        data = self.cleaned_data['minutes']
        if data < 3:
            raise forms.ValidationError(_('Minimum time 3 minutes'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data
    # Метод-валидатор для поля limit
    def clean_limit(self):
        data = self.cleaned_data['limit']
        if data < 50:
            raise forms.ValidationError(_('Minimum value 50%'))
        if data > 100:
            raise forms.ValidationError(_('Maximum value 100%'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question', 'photo', 'reply1', 'ok1', 'reply2', 'ok2', 'reply3', 'ok3', 'reply4', 'ok4', 'reply5', 'ok5']
        widgets = {
            'question': Textarea(attrs={'cols': 80, 'rows': 6}),
            'reply1': Textarea(attrs={'cols': 80, 'rows': 4}),
            'ok1' : CheckboxInput(),
            'reply2': Textarea(attrs={'cols': 80, 'rows': 4}),
            'ok2' : CheckboxInput(),
            'reply3': Textarea(attrs={'cols': 80, 'rows': 4}),
            'ok3' : CheckboxInput(),
            'reply4': Textarea(attrs={'cols': 80, 'rows': 4}),
            'ok4' : CheckboxInput(),
            'reply5': Textarea(attrs={'cols': 80, 'rows': 4}),
            'ok5' : CheckboxInput(),
        }
        labels = {
            'teststask': _('teststask'),            
        }
    # Метод-валидатор для поля question
    def clean_question(self):
        data = self.cleaned_data['question']
        if len(data) < 7:
            raise forms.ValidationError(_('Minimum length 7 characters'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data
    # Метод-валидатор для поля reply1
    def clean_reply1(self):
        data = self.cleaned_data['reply1']
        if len(data) < 1:
            raise forms.ValidationError(_('Minimum length 1 characters'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data
    # Метод-валидатор для поля reply2
    def clean_reply2(self):
        data = self.cleaned_data['reply2']
        if len(data) < 1:
            raise forms.ValidationError(_('Minimum length 1 characters'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data
    # Метод-валидатор для полей reply... и ok...
    def clean(self):
        cleaned_data = super().clean()
        reply1 = cleaned_data.get("reply1")
        ok1 = cleaned_data.get("ok1")
        reply2 = cleaned_data.get("reply2")
        ok2 = cleaned_data.get("ok2")
        reply3 = cleaned_data.get("reply3")
        ok3 = cleaned_data.get("ok3")
        reply4 = cleaned_data.get("reply4")
        ok4 = cleaned_data.get("ok4")
        reply5 = cleaned_data.get("reply5")
        ok5 = cleaned_data.get("ok5")
        #print("reply1 ", reply1)
        #print("ok1 ", ok1)
        #print("reply2 ", reply2)
        #print("ok2 ", ok2)
        #print("reply3 ", reply3)
        #print("ok3 ", ok3)
        #print("reply4 ", reply4)
        #print("ok4 ", ok4)
        #print("reply5 ", reply5)
        #print("ok5 ", ok5)
        if ok1 == False and ok2 == False and ok3 == False and ok4 == False and ok5 == False:           
            raise ValidationError("There must be at least one correct answer")
        if (reply1 == "" and ok1 == True) or (reply2 == "" and ok2 == True) or (reply3 == "" and ok3 == True) or (reply4 == "" and ok4 == True) or (reply5 == "" and ok5 == True):           
            raise ValidationError("One of the empty answers is marked as correct")

class ProtocolForm(forms.ModelForm):
    class Meta:
        model = Protocol
        fields = ['comment',]
        widgets = {
            'comment': Textarea(attrs={'cols': 80, 'rows': 6}),          
        }
        labels = {
            'comment': _('protocol_comment'),            
        }
    # Метод-валидатор для поля title
    def clean_comment(self):
        data = self.cleaned_data['comment']
        # Ошибка минимальная длина
        if len(data) < 3:
            raise forms.ValidationError(_('Minimum length 3 characters'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data

# Форма регистрации
class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
