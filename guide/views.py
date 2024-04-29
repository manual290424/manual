# Класс HttpResponse из пакета django.http, который позволяет отправить текстовое содержимое.
from django.http import HttpResponse, HttpResponseNotFound

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect

from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from django.urls import reverse

from django.contrib.auth import login as auth_login

import time

# Подключение моделей
from .models import Category, Teststask, Question, Protocol
# Подключение форм
from .forms import CategoryForm, TeststaskForm, QuestionForm, ProtocolForm, SignUpForm

# Create your views here.
# Групповые ограничения
def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups, login_url='403')

# Стартовая страница 
def index(request):
    return render(request, "index.html")

## Контакты
#def contact(request):
#    return render(request, "contact.html")

# Лекции
def lecture(request):
    return render(request, "lecture/index.html")

from django.contrib.auth import logout
def logoutUser(request):
    logout(request)
    return render(request, "index.html")
###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def category_index(request):
    try:
        category = Category.objects.all().order_by('title')
        return render(request, "category/index.html", {"category": category,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def category_create(request):
    try:
        if request.method == "POST":
            category = Category()
            category.title = request.POST.get("title")
            categoryform = CategoryForm(request.POST)
            if categoryform.is_valid():
                category.save()
                return HttpResponseRedirect(reverse('category_index'))
            else:
                return render(request, "category/create.html", {"form": categoryform})
        else:        
            categoryform = CategoryForm()
            return render(request, "category/create.html", {"form": categoryform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def category_edit(request, id):
    try:
        category = Category.objects.get(id=id)
        if request.method == "POST":
            category.title = request.POST.get("title")
            categoryform = CategoryForm(request.POST)
            if categoryform.is_valid():
                category.save()
                return HttpResponseRedirect(reverse('category_index'))
            else:
                return render(request, "category/edit.html", {"form": categoryform})
        else:
            # Загрузка начальных данных
            categoryform = CategoryForm(initial={'title': category.title, })
            return render(request, "category/edit.html", {"form": categoryform})
    except Category.DoesNotExist:
        return HttpResponseNotFound("<h2>Category not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def category_delete(request, id):
    try:
        category = Category.objects.get(id=id)
        category.delete()
        return HttpResponseRedirect(reverse('category_index'))
    except Category.DoesNotExist:
        return HttpResponseNotFound("<h2>Category not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
def category_read(request, id):
    try:
        category = Category.objects.get(id=id) 
        return render(request, "category/read.html", {"category": category})
    except Category.DoesNotExist:
        return HttpResponseNotFound("<h2>Category not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def teststask_index(request):
    try:
        teststask = Teststask.objects.all().order_by('id')
        return render(request, "teststask/index.html", {"teststask": teststask,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def teststask_create(request):
    try:
        if request.method == "POST":
            teststask = Teststask()
            teststask.title = request.POST.get("title")
            teststask.category = Category.objects.filter(id=request.POST.get("category")).first()
            teststask.details = request.POST.get("details")
            teststask.minutes = request.POST.get("minutes")
            teststask.limit = request.POST.get("limit")
            teststaskform = TeststaskForm(request.POST)
            if teststaskform.is_valid():
                teststask.save()
                return HttpResponseRedirect(reverse('teststask_index'))
            else:
                return render(request, "teststask/create.html", {"form": teststaskform})
        else:        
            teststaskform = TeststaskForm(request.FILES)
            return render(request, "teststask/create.html", {"form": teststaskform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def teststask_edit(request, id):
    try:
        teststask = Teststask.objects.get(id=id) 
        if request.method == "POST":
            teststask.title = request.POST.get("title")
            teststask.category = Category.objects.filter(id=request.POST.get("category")).first()
            teststask.details = request.POST.get("details")
            teststask.minutes = request.POST.get("minutes")
            teststask.limit = request.POST.get("limit")
            teststaskform = TeststaskForm(request.POST)
            if teststaskform.is_valid():
                teststask.save()
                return HttpResponseRedirect(reverse('teststask_index'))
            else:
                return render(request, "teststask/edit.html", {"form": teststaskform})
        else:
            # Загрузка начальных данных
            teststaskform = TeststaskForm(initial={'category': teststask.category, 'title': teststask.title,'details': teststask.details,'minutes': teststask.minutes,'limit': teststask.limit, })
            return render(request, "teststask/edit.html", {"form": teststaskform})
    except Teststask.DoesNotExist:
        return HttpResponseNotFound("<h2>Teststask not found</h2>")

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def teststask_delete(request, id):
    try:
        teststask = Teststask.objects.get(id=id)
        teststask.delete()
        return HttpResponseRedirect(reverse('teststask_index'))
    except Teststask.DoesNotExist:
        return HttpResponseNotFound("<h2>Teststask not found</h2>")

# Просмотр страницы read.html для просмотра объекта.
@login_required
@group_required("Managers")
def teststask_read(request, id):
    try:
        teststask = Teststask.objects.get(id=id) 
        return render(request, "teststask/read.html", {"teststask": teststask})
    except Teststask.DoesNotExist:
        return HttpResponseNotFound("<h2>Teststask not found</h2>")

# Список для выбора тестового задания
@login_required
def teststask_list(request):
    try:
        teststask = Teststask.objects.all().order_by('title')
        return render(request, "teststask/list.html", {"teststask": teststask,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Получить вопрос по id
def get_question_by_id(id):
    question = Question.objects.get(id=id)
    return question.question

@login_required
def teststask_run(request, id):
    try:
        # Вопросы и ответы к тестовому заданию
        question = Question.objects.filter(teststask_id=id).order_by('id')
        # Порог в % и время на выполнение тестового задания в мин.
        teststask = Teststask.objects.get(id=id)
        teststask_category = teststask.category
        teststask_title = teststask.title
        limit = teststask.limit
        print("limit: ", limit)
        minutes = teststask.minutes
        print("minutes: ", minutes)
        # Если нажата кнопка Accept (Принять)
        if ('accept_btn' in request.POST) or ('accept_timer_btn' in request.POST):
            # Считать со страницы ответы пользователя
            # {'radio6': 'on1', 'radio7': 'on2', 'cbox28': 'on2', 'cbox38': 'on3', 'radio9': 'on4', 'radio10': 'on5'}
            # 'radio7': 'on2' - для вопроса с id записи 7 выбрагн второй вариант ответа
            # 'cbox28': 'on2', 'cbox38': 'on3' - для вопроса с id записи 8 выбраны 2 и 3 варианты ответов
            dictionary_answer = {}
            for key, value in request.POST.items():
                if key != 'csrfmiddlewaretoken':
                    if key != 'accept_btn':
                        dictionary_answer.update({key:value})
                #print(f'Key: {key}')
                #print(f'Value: {value}')
            #for key in dictionary_answer:
                #print(key,dictionary_answer[key])
            print("dictionary_answer: ", dictionary_answer)
            # Сгруппировать многовариантые ответы и привести в более понятный вид
            # {'radio6': 'on1', 'radio7': 'on2', 'cbox28': 'on2', 'cbox38': 'on3', 'radio9': 'on4', 'radio10': 'on5'}
            # в
            # {'6': '1', '7': '2', '8': '23', '9': '4', '10': '5'}
            # Ответы пользователя answers:  пара 'id вопроса': 'выбранный номер(а) вопроса'  
            answers = {}
            for key in dictionary_answer:
                question_id = key[5:len(key)]           # выделить id вопроса                    
                if key[0:5]=='radio':                   # У вопроса только один вариант ответа
                    answers.update({ question_id : dictionary_answer[key][2:3]})
                if key[0:4]=='cbox':                    # У вопроса может быть несколько вариантов ответов
                    total = ''                          # Ответы на вопрос в виде 134 (выбраны первый, третий и четвертый варианты ответов)
                    temp = dictionary_answer            # Для перебора всех ответов на вопрос с данным question_id 
                    for key in temp:
                        if key[5:len(key)] == question_id:
                            total = total + dictionary_answer[key][2:3]
                    answers.update({question_id : total})
            print("answers: ", answers) # {'31': '1', '32': '2', '33': '3', '34': '4', '35': '5', '36': '1', '37': '2', '38': '3', '39': '4', '40': '5', '41': '1', '42': '2', '43': '3', '44': '4', '45': '5'}
            # Считать из базы данных в словарь dictionary_question id вопроса и выбор пользователя
            question2 = Question.objects.values('id', 'ok1', 'ok2', 'ok3', 'ok4', 'ok5').filter(teststask_id=id)
            dictionary_question = [entry for entry in question2]
            print("dictionary_question ", dictionary_question) #  [{'id': 16, 'ok1': False, 'ok2': False, 'ok3': False, 'ok4': True, 'ok5': False}, {'id': 17, 'ok1': False, 'ok2': True, 'ok3': False, 'ok4': False, 'ok5': False}, {'id': 18, 'ok1': False, 'ok2': False, 'ok3': False, 'ok4': True, 'ok5': False}, {'id': 19, 'ok1': False, 'ok2': False, 'ok3': False, 'ok4': False, 'ok5': True}, {'id': 20, 'ok1': False, 'ok2': False, 'ok3': False, 'ok4': True, 'ok5': False}, {'id': 21, 'ok1': False, 'ok2': False, 'ok3': False, 'ok4': False, 'ok5': True}, {'id': 22, 'ok1': False, 'ok2': True, 'ok3': False, 'ok4': False, 'ok5': False}, {'id': 23, 'ok1': False, 'ok2': False, 'ok3': False, 'ok4': False, 'ok5': True}, {'id': 24, 'ok1': True, 'ok2': False, 'ok3': False, 'ok4': False, 'ok5': False}, {'id': 25, 'ok1': False, 'ok2': False, 'ok3': True, 'ok4': False, 'ok5': False}, {'id': 26, 'ok1': False, 'ok2': False, 'ok3': False, 'ok4': False, 'ok5': False}, {'id': 27, 'ok1': False, 'ok2': False, 'ok3': False, 'ok4': False, 'ok5': True}, {'id': 28, 'ok1': False, 'ok2': True, 'ok3': False, 'ok4': False, 'ok5': False}, {'id': 29, 'ok1': False, 'ok2': False, 'ok3': False, 'ok4': True, 'ok5': False}, {'id': 30, 'ok1': False, 'ok2': False, 'ok3': False, 'ok4': True, 'ok5': False}]
            # Вопросы и правильные ответы пара 'id вопроса' : 'правильный ответ (ответы)' 
            questions = {}
            for d in dictionary_question:
                total = ''
                if d['ok1'] == True:
                    total = total + '1'
                if d['ok2'] == True:
                    total = total + '2'
                if d['ok3'] == True:
                    total = total + '3'
                if d['ok4'] == True:
                    total = total + '4'
                if d['ok5'] == True:
                    total = total + '5'
                questions.update({str(d['id']): total})
            print("questions ", questions)  #   {'16': '4', '17': '2', '18': '4', '19': '5', '20': '4', '21': '5', '22': '2', '23': '5', '24': '1', '25': '3', '26': '', '27': '5', '28': '2', '29': '4', '30': '4'}
            # Перебрать все вопросы (questions) и сравнить с тем что ответил пользователь (answers)
            total_questions = len(question)    # Всего вопросов
            print("total_questions ", total_questions)
            answered = {key: int(questions[key])-int(answers[key]) for key in questions if key in answers}
            print("answered ", answered) # 'id вопроса': 'результат проверки, если =0 то ответ правильный' {'31': 0, '32': 0, '33': 0, '34': -2, '35': -4, '36': 0, '37': 0, '38': 0, '39': 0, '40': 2, '41': 0, '42': 0, '43': 0, '44': 0, '45': -1}
            total_answered = len(answered)      # Всего отвечено
            print("total_answered ", total_answered)
            answered_correctly = 0              # Правильно отвечено
            wrong_answers = ""      # Неправильные ответы (список)
            for key, values in answered.items():
                if values == 0:
                    answered_correctly += 1     
                    print("Правильно отвечено: key (id вопроса) ", key)
                else:
                    print("Неправильно отвечено: key (id вопроса)", key)
                    wrong_answers = wrong_answers + get_question_by_id(key) + "\n"
            print("answered_correctly ", answered_correctly)
            print("wrong_answers ", wrong_answers)
            print("answered_correctly/total_questions ", answered_correctly/total_questions)            
            if (answered_correctly/total_questions)*100 >= limit:
                res = _('Test task completed')
            else:
                res = _('Test task failed')
            if (wrong_answers != ""):
                res = res + "\n" + _('Wrong answers') + ":\n" + wrong_answers
            # Записать результат и перейти на страницу с протоколом выполнения
            protocol = Protocol()
            protocol.teststask_id = id
            protocol.result = (answered_correctly/total_questions)*100
            protocol.details = _('Total Questions')+ ': ' + str(total_questions) + '. ' + _('Total replied') + ': ' + str(total_answered) + '. ' + _('Correctly answered') + ': ' + str(answered_correctly) + ', (' + str(round((answered_correctly/total_questions)*100,1)) + ' %). ' + res
            protocol.user_id = request.user.id
            protocol.save()
            return HttpResponseRedirect(reverse('protocol_list'))
        else:
            return render(request, "teststask/run.html", {"question": question, 'minutes': minutes, 'teststask_category': teststask_category, 'teststask_title': teststask_title})
    except Teststask.DoesNotExist:
        return HttpResponseNotFound("<h2>Teststask not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Протокол тестирования для менеджера (все записи)
@login_required
@group_required("Managers")
def protocol_index(request):
    try:
        protocol = Protocol.objects.all().order_by('-datep')
        return render(request, "protocol/index.html", {"protocol": protocol, })
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Протокол тестирования и решения задач для пользователя (только свои записи)
@login_required
def protocol_list(request):
    try:
        protocol = Protocol.objects.filter(user_id=request.user.id).order_by('-datep')
        return render(request, "protocol/list.html", {"protocol": protocol, })
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def protocol_edit(request, id):
    try:
        protocol = Protocol.objects.get(id=id)
        if request.method == "POST":
            protocol.comment = request.POST.get("comment")
            protocolform = ProtocolForm(request.POST)
            if protocolform.is_valid():
                protocol.save()
                return HttpResponseRedirect(reverse('protocol_index'))
            else:
                return render(request, "protocol/edit.html", {"form": protocolform, "protocol": protocol})
        else:
            # Загрузка начальных данных
            protocolform = ProtocolForm(initial={'comment': protocol.comment, })
            return render(request, "protocol/edit.html", {"form": protocolform, "protocol": protocol})
    except Protocol.DoesNotExist:
        return HttpResponseNotFound("<h2>Protocol not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)


###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def question_index(request, id):
    try:
        question = Question.objects.filter(teststask_id=id).order_by('id')
        teststask = Teststask.objects.get(id=id)
        return render(request, "question/index.html", {"question": question, "teststask": teststask})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def question_create(request, teststask_id):
    try:
        teststask = Teststask.objects.get(id=teststask_id)
        if request.method == "POST":
            question = Question()
            #question.teststask = Teststask.objects.filter(id=request.POST.get("teststask")).first()
            question.teststask_id = teststask_id       
            question.question = request.POST.get("question")
            if 'photo' in request.FILES:                
                question.photo = request.FILES['photo']    
            question.reply1 = request.POST.get("reply1")
            if (request.POST.get("ok1") == 'on'):
                question.ok1 = True
            else:
                question.ok1 = False
            question.reply2 = request.POST.get("reply2")
            if (request.POST.get("ok2") == 'on'):
                question.ok2 = True
            else:
                question.ok2 = False
            question.reply3 = request.POST.get("reply3")
            if (request.POST.get("ok3") == 'on'):
                question.ok3 = True
            else:
                question.ok3 = False
            question.reply4 = request.POST.get("reply4")
            if (request.POST.get("ok4") == 'on'):
                question.ok4 = True
            else:
                question.ok4 = False
            question.reply5 = request.POST.get("reply5")
            if (request.POST.get("ok5") == 'on'):
                question.ok5 = True
            else:
                question.ok5 = False
            questionform = QuestionForm(request.POST)
            if questionform.is_valid():
                question.save()
                return HttpResponseRedirect(reverse('question_index', args=(question.teststask_id,)))
            else:
                return render(request, "question/create.html", {"form": questionform, 'teststask_id': teststask_id, 'teststask': teststask,})
        else:        
            questionform = QuestionForm(request.POST)
            return render(request, "question/create.html", {"form": questionform, 'teststask_id': teststask_id, 'teststask': teststask,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
# И вначале по этому идентификатору мы пытаемся найти объект с помощью метода Question.objects.get(id=id).
# Поскольку в случае отсутствия объекта мы можем столкнуться с исключением Question.DoesNotExist,
# то соответственно нам надо обработать подобное исключение, если вдруг будет передан несуществующий идентификатор.
# И если объект не будет найден, то пользователю возващается ошибка 404 через вызов return HttpResponseNotFound().
# Если объект найден, то обработка делится на две ветви.
# Если запрос POST, то есть если пользователь отправил новые изменненые данные для объекта, то сохраняем эти данные в бд и выполняем переадресацию на корень веб-сайта.
# Если запрос GET, то отображаем пользователю страницу edit.html с формой для редактирования объекта.
@login_required
@group_required("Managers")
def question_edit(request, id):
    try:
        question = Question.objects.get(id=id)
        teststask = Teststask.objects.get(id=question.teststask_id)        
        if request.method == "POST":
            question.question = request.POST.get("question")
            if 'photo' in request.FILES:                
                question.photo = request.FILES['photo']    
            question.reply1 = request.POST.get("reply1")
            if (request.POST.get("ok1") == 'on'):
                question.ok1 = True
            else:
                question.ok1 = False
            question.reply2 = request.POST.get("reply2")
            if (request.POST.get("ok2") == 'on'):
                question.ok2 = True
            else:
                question.ok2 = False
            question.reply3 = request.POST.get("reply3")
            if (request.POST.get("ok3") == 'on'):
                question.ok3 = True
            else:
                question.ok3 = False
            question.reply4 = request.POST.get("reply4")
            if (request.POST.get("ok4") == 'on'):
                question.ok4 = True
            else:
                question.ok4 = False
            question.reply5 = request.POST.get("reply5")
            if (request.POST.get("ok5") == 'on'):
                question.ok5 = True
            else:
                question.ok5 = False        
            questionform = QuestionForm(request.POST)
            if questionform.is_valid():
                question.save()
                return HttpResponseRedirect(reverse('question_index', args=(question.teststask_id,))) 
            else:
                return render(request, "question/edit.html", {"form": questionform, 'teststask_id': question.teststask_id, 'teststask': teststask})            
        else:
            # Загрузка начальных данных
            questionform = QuestionForm(initial={'teststask': question.teststask, 'question': question.question, 'photo': question.photo,
                                                 'reply1': question.reply1,'ok1': question.ok1,'reply2': question.reply2,
                                                 'ok2': question.ok2,'reply3': question.reply3,'ok3': question.ok3,
                                                 'reply4': question.reply4,'ok4': question.ok4,'reply5': question.reply5,
                                                 'ok5': question.ok5,})
            return render(request, "question/edit.html", {"form": questionform, 'teststask_id': question.teststask_id, 'teststask': teststask})
    except Question.DoesNotExist:
        return HttpResponseNotFound("<h2>Question not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def question_delete(request, id):
    try:
        question = Question.objects.get(id=id)
        question.delete()
        return HttpResponseRedirect(reverse('question_index', args=(question.teststask_id,)))
    except Question.DoesNotExist:
        return HttpResponseNotFound("<h2>Question not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
@group_required("Managers")
def question_read(request, id):
    try:
        question = Question.objects.get(id=id) 
        return render(request, "question/read.html", {"question": question, "teststask_id": question.teststask_id})
    except Question.DoesNotExist:
        return HttpResponseNotFound("<h2>Question not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Регистрационная форма 
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return HttpResponseRedirect(reverse('index'))
            #return render(request, 'registration/register_done.html', {'new_user': user})
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

# Изменение данных пользователя
@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email',)
    template_name = 'registration/my_account.html'
    success_url = reverse_lazy('index')
    #success_url = reverse_lazy('my_account')
    def get_object(self):
        return self.request.user


