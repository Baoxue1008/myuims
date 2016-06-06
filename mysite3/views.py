#coding:utf-8
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib import auth
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm
from mooc.views import *
from django.contrib import messages

from django.contrib.auth.decorators import login_required
# Create your views here.


def login(request):
    if request.user.is_authenticated():
        if Student.objects.filter(userid=request.user.id):
            # 当前是学生
            return HttpResponseRedirect('/index/', content_type=RequestContext(request))
        else:
            # 当前是教师
            return HttpResponse('teacher')
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        if Student.objects.filter(userid=request.user.id):
            return HttpResponseRedirect('/index/', content_type=RequestContext(request))
        else:
            return HttpResponse('teacher')
    else:
        return render_to_response('login.html', context_instance=RequestContext(request))


def index(request):
    return render(request,'index.html')

def schedule(request):
    return render(request,'schedule.html')

def grade(request):
    return render(request,'grade.html')

def choose(request):
    return render(request,'choose.html')

def bill(request):
    return render(request,'bill.html')


def news(request):
    return render(request,'news.html')

def indexstudent(request):
    if not Student.objects.filter(userid=request.user.id):
        messages.error(request, '您不是学生!')
        return HttpResponseRedirect('/index/')
    return render_to_response('indexstudent.html', locals(), context_instance=RequestContext(request))

def indexteacher(request):
    if not Teacher.objects.filter(userid=request.user.id):
        messages.error(request,'您不是教师!')
        return HttpResponseRedirect('/index/')
    return render(request,'indexteacher.html')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/accounts/login/', content_type=RequestContext(request))

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect('/accounts/login/', content_type=RequestContext(request))
    else:
        form = UserCreationForm()
    return render_to_response('register1.html', locals(), context_instance=RequestContext(request))

