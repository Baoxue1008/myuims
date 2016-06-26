#coding:utf-8
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib import auth
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from mooc.models import *
from django.contrib.auth.decorators import login_required
# Create your views here.


def login(request):
    if request.user.is_authenticated():
        if Student.objects.filter(userid=request.user.id):
            # 当前是学生
            return HttpResponseRedirect('/indexstudent/', content_type=RequestContext(request))
        else:
            # 当前是教师
            return HttpResponseRedirect('/indexteacher/', content_type=RequestContext(request))
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        if Student.objects.filter(userid=request.user.id):
            return HttpResponseRedirect('/indexstudent/', content_type=RequestContext(request))
        else:
            return HttpResponseRedirect('/indexteacher/', content_type=RequestContext(request))
    else:
        return render_to_response('login.html', context_instance=RequestContext(request))


def indexstudent(request):
    return render(request,'indexstudent.html')

def indexteacher(request):
    return render(request,'indexteacher.html')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/accounts/login/', content_type=RequestContext(request))


def course_canceled(request):
    noteach = Course.objects.filter(course_teach__isnull = True)
    allCourse = Course.objects.all()
    insuffStu = [ c.course_name for c in allCourse if c.course_choose.count()<3 ]
    if Student.objects.filter(userid=request.user.id):
        # 当前是学生
        return render(request, 'student_course_canceled.html', {'noteach': noteach, 'insuffStu': insuffStu})
    else:
        # 当前是教师
        return render(request, 'teacher_course_canceled.html', {'noteach': noteach, 'insuffStu': insuffStu})

