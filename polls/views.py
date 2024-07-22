from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Question
from .forms import RegistrationForm
from django.shortcuts import render, get_object_or_404


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
    #get_object_or_404(request)
    list_question = Question.objects.all()
    context = {"dsquest": list_question}
    return render(request, "polls/question_list.html", context)


def detailView(request, question_id):
    q = Question.objects.get(pk=question_id)
    return render(request, "polls/detail_question.html", {"qs": q})


from django.http import HttpResponse, HttpResponseRedirect


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
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    return render(request, 'polls/register.html', {'form': form})

from .models import Post

def post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, "polls/post.html", {"post": post})

# polls/views.py



def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'polls/post.html', {'post': post})

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
            return redirect('some_view')
    else:
        form = PostForm()
    return render(request, 'polls/post_create.html', {'form': form})