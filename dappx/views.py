from django.shortcuts import render

# Create your views here.
from dappx.forms import UserForm,UserProfileInfoForm,UploadFileForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from dappx.models import LogFile 
from django.contrib.auth.models import User

import os.path as op
import os
import time

@login_required
def index(request):
    if request.method == 'GET':
        # current_user = request.user
        username = User.objects.get(username=request.user)
        logs = LogFile.objects.filter(PostedBy = username)
        context = {
                "logs": logs
                 }
        return render(request,'dappx/index.html', context)

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            saved_path = handle_uploaded_file(request.user, request.FILES['file'])
        else:
            return HttpResponse(status=500)

        username = User.objects.get(username=request.user)
        logObj = LogFile.objects.create(
                            LogPath = saved_path,
                            FileName = request.FILES['file'].name,
                            PostedBy = username)
        logObj.save()
        return render(request,'dappx/index.html')


def handle_uploaded_file(user, f):
    file_center = "/home/haihuam/Projects/dprojx/uploadfiles/"
    user_file_dir = op.join(file_center, str(user))
    if not op.exists(user_file_dir):
        try: 
            os.makedirs(user_file_dir)
        except:
            # Directories created failed.
            return 

    file_name = "_".join([str(int(time.time())), f.name])
    file_save_path = op.join(user_file_dir, file_name)

    with open(file_save_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    return file_save_path

@login_required
def special(request):
    return HttpResponse("You are logged in !")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        # profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() :
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            # print(user_form.errors,profile_form.errors)
            print(user_form.errors)
    else:
        user_form = UserForm()
        # profile_form = UserProfileInfoForm()
    return render(request,'dappx/registration.html',
                          {'user_form':user_form,
                           'registered':registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # print(username, password)
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'dappx/login.html', {})
