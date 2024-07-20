from django.urls import path
from . import views
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
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('post/<int:post_id>/', views.post, name='post'),
    path('posts/', views.post_list, name='post_list'),
]
