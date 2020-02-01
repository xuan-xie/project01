from django.shortcuts import render,reverse,redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegisterForm,LoginForm


# Create your views here.
def register(request):
    if request.method == 'POST':
        reg_form = RegisterForm(request.POST)
        if reg_form.is_valid():

            username = reg_form.cleaned_data['username']
            password = reg_form.cleaned_data['password']
            # 创建用户
            user = User.objects.create_user(username=username, password=password)
            user.save()

            # 登陆用户
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        reg_form = RegisterForm()
    context = {'reg_form':reg_form}
    return render(request, 'user/register.html', context=context)


def login(request):

    if request.method == 'POST':
        log_form = LoginForm(request.POST)
        if log_form.is_valid():

            username = log_form.cleaned_data['username']
            password = log_form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            auth.login(request,user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        log_form = LoginForm()
    context = {'log_form': log_form}
    return render(request, 'user/login.html', context=context)

@login_required
def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('home')))


