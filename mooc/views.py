# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response,render
from django.contrib.auth.decorators import login_required
from mooc.models import *
from django.http import Http404, HttpResponseRedirect,HttpResponse
from django.contrib import messages
from forms import *
from django.forms.formsets import formset_factory
from django.contrib.auth.models import User
# Create your views here.

CURRENT_TERM = '7th'


@login_required
def student_course_list(request):
    ml = Course.objects.filter(course_teach__isnull = False,course_term=CURRENT_TERM)
    return render(request,'student_course_list.html', {'ml': ml})

@login_required
def teacher_course_list(request):
    ml = Course.objects.filter(course_term=CURRENT_TERM)
    return render(request,'teacher_course_list.html', {'ml': ml})

@login_required
def student_course_detail(request, id):
    try:
        md = Course.objects.get(id=str(id))
    except Course.DoesNotExist:
        raise Http404
    return render(request,'student_course_detail.html', {'md': md})

@login_required
def teacher_course_detail(request, id):
    try:
        md = Course.objects.get(id=str(id))
    except Course.DoesNotExist:
        raise Http404
    return render(request,'teacher_course_detail.html', {'md': md})

@login_required
def course_add(request, id):
    student = Student.objects.filter(userid=request.user)
    course = Course.objects.get(id=id)
    if len(student) != 0:
        dir = '/mooc/student/' + id
        student = student[0]
        verify = Course.objects.filter(id=id, course_choose=student)
        if verify:
            messages.error(request, '您已选择学习此课程！')
        elif student.course_set.filter(course_term=course.course_term,course_week=course.course_week,course_time=course.course_time):
            messages.error(request, '该课程与其他课程时间冲突！')
        elif course.course_choose.count() == 10:
            messages.error(request,'该课程选课人数已超过10人！')
        else:
            course.course_choose.add(student)
            course.save()
            messages.success(request, "选课成功！")
    else:
        dir = '/mooc/teacher/' + id
        teacher = Teacher.objects.get(userid=request.user)
        verify = Course.objects.filter(id=id, course_teach=teacher)
        if verify:
            messages.error(request, '您已选择教授此课程！')
        elif course.course_teach != None:
            messages.error(request,'已有其他教师教授此课！')
        elif teacher.course_set.filter(course_term=course.course_term, course_week=course.course_week,course_time=course.course_time):
            messages.error(request, '该课程与其他课程时间冲突！')
        else :
            course.course_teach = teacher
            course.save()
            messages.success(request, "选课成功！")
    return HttpResponseRedirect(dir)


@login_required
def course_delete(request, id):
    student = Student.objects.filter(userid=request.user)
    course = Course.objects.get(id=id)
    if len(student) != 0:
        dir = '/mooc/student/' + id
        student = student[0]
        verify = Course.objects.filter(id=id, course_choose=student)
        if not verify:
            messages.error(request, '您未选择学习此课程')
        else:
            course.course_choose.remove(student)
            course.save()
            messages.success(request, "删除课程成功")
    else:
        dir = '/mooc/teacher/' + id
        teacher = Teacher.objects.get(userid=request.user)
        verify = Course.objects.filter(id=id, course_teach=teacher)

        if not verify:
            messages.error(request, '您未选择教授此课程')
        else:
            course.course_teach = None
            course.save()
            messages.success(request, "取消授课成功")
    return HttpResponseRedirect(dir)

@login_required
def show_scores(request):
    try:
        student = Student.objects.get(userid=request.user)
        scores = Score.objects.filter(student_id=student)
        return render(request,'show_scores.html',{'my_scores':scores})
    except Student.DoesNotExist:
        return HttpResponse('只有学生可以操作')




@login_required
def show_my_course(request):
    student = Student.objects.filter(userid=request.user)
    if len(student) != 0:
        student = student[0]
        my_course = student.course_set.filter(course_term=CURRENT_TERM).order_by('id')
        sumPrice = sum([c.course_price for c in my_course])
        return render(request,'student_select_show.html', {'my_course': my_course,'sumPrice':sumPrice})
    else:
        teacher = Teacher.objects.get(userid=request.user)
        my_course = teacher.course_set.filter(course_term=CURRENT_TERM).order_by('id')
        return render(request,'teacher_select_show.html', {'my_course': my_course})


@login_required
def show_who_choose_this_class(request, id):
    course = Course.objects.get(id=id)
    class_mates = course.course_choose.all()
    return render_to_response('mooc_class_mates.html', {'class_mates': class_mates})

@login_required
def set_scores(request,id):
    course = Course.objects.get(id=id)
    students = course.course_choose.all()
    stunum = len(students)
    ScoreFormSet = formset_factory(ScoreForm,extra = stunum)

    teacher = Teacher.objects.get(userid=request.user.id)

    if request.method == 'POST':
        formset = ScoreFormSet(request.POST)
        if formset.is_valid():
            cnt = 0
            for form in formset:
                if form.has_changed():

                    alscore = Score.objects.filter(student_id = students[cnt],teacher_id = teacher,course_id = course)
                    if alscore:
                        # 已有成绩
                        score = alscore[0]
                        score.value = form.cleaned_data['score']
                        score.save()
                    else:
                        # 新建成绩
                        score = Score(student_id = students[cnt],teacher_id = teacher,course_id = course, value = form.cleaned_data['score'])
                        score.save()
                cnt += 1
            messages.success(request,'修改成绩成功')
        #return HttpResponseRedirect('/accounts/login/')
        return render(request, 'set_scores.html', {'formset': ScoreFormSet(), 'students': students, 'id': id})
    else:
        return render(request,'set_scores.html', {'formset': ScoreFormSet(), 'students':students,'id': id})

