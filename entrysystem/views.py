from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from .forms import UserRegisterForm
from .models import Visitor, NewUser
from .forms import generate_visit_code


# Create your views here


def home(request):
    return render(request, "home.html")


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hi {username}, your account has been created successfully')
            return redirect('home')
    else:
        form = UserRegisterForm()

    return render(request, "register.html", {'form': form})


def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('base')
        else:
            messages.info(request, "Invalid Login")
            return redirect('login')

    else:
        if request.user.is_authenticated:
            return redirect('base')
        return render(request, 'login.html')


@login_required
def base(request):
    if request.method == 'POST':
        name = request.POST['name']
        valid_from = request.POST['from']
        valid_to = request.POST['to']
        code = generate_visit_code()
        creator = request.user
        print(request.user)

        visit = Visitor(name=name, valid_from=valid_from, valid_to=valid_to, code=code, creator=creator)
        visit.save()

        messages.success(request, f'Visitor should use the code: {code} ')
        return redirect('base')
    else:
        if request.user.usertype == NewUser.security:
            code = request.GET.get("code")
            visit = None
            if code:
                try:
                    visit = Visitor.objects.get(code=code)
                except Visitor.DoesNotExist:
                    visit = None
            return render(request, 'visit.html', {"visit": visit})
        else:
            return render(request, 'base.html')


def get_visit(request, code):
    if request.method == "GET":
        visit = Visitor.objects.get(code=code)
        return render(request, "", {"visit": visit})


def user_logout(request):
    if request.method == "POST":
        logout(request)
        messages.info(request, "You have been logged out successfully.")
        return redirect("login")
