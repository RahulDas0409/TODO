from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from todoapp.models import Todo

# Create your views here.
def index(request):
    todo = Todo.objects.all()
    context = {"todos":todo}
    return render(request, "index.html", context)

def addtodos(request):
    if request.method =="POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        complete = request.POST.get('complete')
        todo =Todo(title=title, description=description, complete=complete)
        todo.save()
    return render(request, "addtodos.html")

def signin(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, "Account was created for" + user)
            return redirect("Log In")
    context = {"form":form}
    return render(request, "signin.html", context)

def log_in(request):
    if request.user.is_authenticated:
        return redirect("Home")
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("Home")
            else:
                messages.info(request, "Username or password is incorrect")
        context={}
        return render(request, "login.html", context)

def log_out(request):
    logout(request)
    return redirect("Log In")