from .models import Question
from .forms import RegistrationForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Post
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout


def index(request):
    myname = "Ngoc Tuan do day ta ba"
    taisan1 = ["Dien thoai", "May Tinh", "May Bay", "Nhieu tien"]
    myname2 = "Ngoc Tuan do day ta ba 2"
    taisan2 = ["Dien thoai2", "May Tinh2", "May Bay2", "Nhieu tien2"]
    context1 = {"name": myname, "taisan": taisan1}
    context2 = {'first_name': myname2, "cotaisan": taisan2, 'age': 20}
    lagodo = {'last_name': 'Largo do'}

    # Merge all dictionaries into one
    context = {**context1, **context2, **lagodo}

    return render(request, "polls/index.html", context)


def viewlist(request):
    list_question = Question.objects.all()
    context = {"dsquest": list_question}
    return render(request, "polls/question_list.html", context)


def detailView(request, question_id):
    q = Question.objects.get(pk=question_id)
    return render(request, "polls/detail_question.html", {"qs": q})


def vote(request, question_id):
    q = Question.objects.get(pk=question_id)
    try:
        dulieu = request.POST["choice"]
        c = q.choice_set.get(pk=dulieu)
        c.vote += 1
        c.save()
    except:
        return HttpResponse("Loi khong co choice")
    return render(request, "polls/result.html", {"q": q})  #q de hien thi url, vd polls/5


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')  # Assuming the form has a password1 field for the password
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))  # Redirect to a named URL; adjust as needed
    else:
        form = RegistrationForm()
    return render(request, 'polls/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect(reverse('index'))  # Assuming 'index' is the name of your home page view
        else:
            # Return an 'invalid login' error message.
            return render(request, 'polls/login.html', {'error_message': 'Invalid login'})
    else:
        return render(request, 'polls/login.html')


def logout_view(request):
    """
    Log out the user and redirect to the home page.
    """
    logout(request)
    return redirect('/')  # Redirect to home page


def post(request, post_id):
    postg = get_object_or_404(Post, pk=post_id)
    return render(request, "polls/post.html", {"post": postg})


def post_detail(request, post_id):
    postg = get_object_or_404(Post, pk=post_id)
    return render(request, 'polls/post.html', {'post': postg})


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'polls/post_list.html', {'posts': posts})


from django.shortcuts import render, redirect
from .forms import PostForm
from django.contrib.auth.decorators import login_required


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  # Set the post's user to the current user
            post.save()
            return redirect('polls:post_list')  # Redirect to the post list after saving
    else:
        form = PostForm()
    return render(request, 'polls/post_create.html', {'form': form})
