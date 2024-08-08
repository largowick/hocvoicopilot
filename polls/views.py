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
    post = get_object_or_404(Post, pk=post_id)
    face_detection_success = post.has_faces_detected()
    return render(request, 'polls/post_detail.html', {'post': post, 'face_detection_success': face_detection_success})

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'polls/post_list.html', {'posts': posts})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'polls/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'polls/post_edit.html', {'form': form})



from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from .models import Post
from .face_detection import detect_faces

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  # Set the post's user to the current user
            post.save()
            form.save_m2m()  # Save the many-to-many data for the form

            try:
                # Call the face detection function and save the results
                face_results = detect_faces(post.image.path)
                post.face_detection_results = face_results
                post.save()
            except Exception as e:
                print(f"Error in face detection: {e}")

            return redirect('polls:post_list')  # Redirect to the post list after saving
    else:
        form = PostForm()
    return render(request, 'polls/post_create.html', {'form': form})

from .gemini_api import get_gemini_data

def some_view(request):
    api_url = "https://api.gemini.com/v1/pubticker/btcusd"
    params = {
        "param1": "value1",
        "param2": "value2",
        "api_key": "AIzaSyA68eAWIHHjXkAbCkB2yld_aiZ5PImnjsY"
    }
    gemini_data = get_gemini_data(api_url, params)

    if gemini_data:
        print("Gemini Data:", gemini_data)  # Kiểm tra dữ liệu trả về
    else:
        print("No data returned from Gemini API")  # Thông báo lỗi

    return render(request, 'polls/some_template.html', {'gemini_data': gemini_data})

from django.shortcuts import render
from .forms import GeminiQuestionForm
from .gemini_api import get_gemini_data

def gemini_question_view(request):
    answer = None
    if request.method == 'POST':
        form = GeminiQuestionForm(request.POST)
        if form.is_valid():
            question = form.cleaned_data['question']
            # Gọi API Gemini với câu hỏi
            api_url = "https://api.gemini.com/v1/pubticker/btcusd"
            params = {"question": question}
            answer = get_gemini_data(api_url, params)
    else:
        form = GeminiQuestionForm()
    return render(request, 'polls/gemini_question.html', {'form': form, 'answer': answer})