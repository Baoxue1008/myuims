# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.


class Student(models.Model):
    name = models.CharField(max_length=50)
    #id = models.IntegerField(primary_key=True)
    userid = models.OneToOneField(User,blank=True,null=True)
    birthdate = models.DateField(blank=True,null=True)
    socialNumber = models.IntegerField(blank=True,null=True)
    status = models.CharField(max_length=50,blank=True,null=True)
    graduationdate = models.DateField(blank=True,null=True)

    def __unicode__(self):
        return self.name

class StudentAdmin(admin.ModelAdmin):
    list_display = ['name']



class Teacher(models.Model):
    name = models.CharField(max_length=50)
    userid = models.OneToOneField(User,blank=True,null=True)
    birthdate = models.DateField(blank=True,null=True)
    socialNumber = models.IntegerField(blank=True,null=True)
    status = models.CharField(max_length=50,blank=True,null=True)
    department = models.CharField(max_length=50,blank=True,null=True)
    def __unicode__(self):
        return self.name

class TeacherAdmin(admin.ModelAdmin):
    list_display = ['name']


class Course(models.Model):
    course_name = models.CharField(max_length=50)
    course_choose = models.ManyToManyField(Student, blank=True)
    course_teach = models.ManyToManyField(Teacher, blank=True)


    WEEK_CHOICE = (('Mon','Mon'),('Tue','Tue'), ('Wed','Wed') ,('Thur','Thur'),('Fri','Fri'),('Sat','Sat'),('Sun','Sun'))
    course_week = models.CharField(max_length=50,blank=True,null=True,choices=WEEK_CHOICE)

    TIME_CHOICE = (('1st','1st'),('2nd','2nd'),('3rd','3rd'),('4th','4th'),('5th','5th'),('6th','6th'),('7th','7th'),('8th','8th'))
    course_time = models.CharField(max_length=50,blank=True,null=True,choices=TIME_CHOICE)

    course_price = models.IntegerField(blank=True,null=True)

    TERM_CHOICE = TIME_CHOICE
    course_term = models.CharField(max_length=50,blank=True,null=True,choices=TERM_CHOICE)
    def __unicode__(self):
        return self.course_name

class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_name']


ScoreChoice = (
    ('A','A'),
    ('B','B'),
    ('C','C'),
    ('D','D'),
    ('E','E'),
    ('F','F'),
    ('I','I'),
)

class Score(models.Model):
    student_id = models.ForeignKey('mooc.Student')
    teacher_id = models.ForeignKey('mooc.Teacher')
    course_id = models.ForeignKey('mooc.Course')
    value = models.CharField(max_length=3,choices=ScoreChoice)

class ScoreAdmin(admin.ModelAdmin):
    list_display = ['student_id','teacher_id','course_id','value']







