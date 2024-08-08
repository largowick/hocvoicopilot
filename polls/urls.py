from django.urls import path
from . import views
from .views import create_post, logout_view
from django.contrib.auth import views as auth_views


app_name = 'polls'
urlpatterns = [
    path('detail/<int:question_id>/', views.detailView, name='detail'),
    path('list/', views.viewlist, name='view_list'),
    path('index/', views.index, name='index'),
    path('<int:question_id>', views.vote, name="vote"),
    path('register/', views.register, name='register'),
    #path('register/',views.register.as_view(template_name="polls/register.html"), name="register"),
    path('login/', auth_views.LoginView.as_view(template_name="polls/login.html"), name="login"),
    path('logout/', logout_view, name='logout'),
    #path('post/<int:post_id>/', views.post, name='post'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('posts/', views.post_list, name='post_list'),
    path('create-post/', views.create_post, name='create_post'),
    path('gemini/', views.some_view, name='gemini'),
    path('gemini/question/', views.gemini_question_view, name='gemini_question'),
]
