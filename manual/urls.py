"""
URL configuration for manual project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include 
from django.conf import settings 
from django.conf.urls.static import static

from guide import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index),
    path('admin/', admin.site.urls),
    path('index/', views.index, name='index'),
    #path('contact/', views.contact, name='contact'),
    path('lecture/', views.lecture, name='lecture'),
    path('i18n/', include('django.conf.urls.i18n')),

    path('category/index/', views.category_index, name='category_index'),
    path('category/create/', views.category_create, name='category_create'),
    path('category/edit/<int:id>/', views.category_edit, name='category_edit'),
    path('category/delete/<int:id>/', views.category_delete, name='category_delete'),
    path('category/read/<int:id>/', views.category_read, name='category_read'),

    path('teststask/index/', views.teststask_index, name='teststask_index'),
    path('teststask/create/', views.teststask_create, name='teststask_create'),
    path('teststask/edit/<int:id>/', views.teststask_edit, name='teststask_edit'),
    path('teststask/delete/<int:id>/', views.teststask_delete, name='teststask_delete'),
    path('teststask/read/<int:id>/', views.teststask_read, name='teststask_read'),
    path('teststask/list/', views.teststask_list, name='teststask_list'),
    path('teststask/run/<int:id>/', views.teststask_run, name='teststask_run'),

    path('question/index/<int:id>/', views.question_index, name='question_index'),
    path('question/create/<int:teststask_id>/', views.question_create, name='question_create'),
    path('question/edit/<int:id>/', views.question_edit, name='question_edit'),
    path('question/delete/<int:id>/', views.question_delete, name='question_delete'),
    path('question/read/<int:id>/', views.question_read, name='question_read'),

    path('protocol/index/', views.protocol_index, name='protocol_index'),
    path('protocol/list/', views.protocol_list, name='protocol_list'),
    path('protocol/edit/<int:id>/', views.protocol_edit, name='protocol_edit'),

    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('logout/', views.logoutUser, name="logout"),
    path('settings/account/', views.UserUpdateView.as_view(), name='my_account'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
