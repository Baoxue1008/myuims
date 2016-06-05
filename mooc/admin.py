from django.contrib import admin
from mooc.models import *

# Register your models here.
admin.site.register(Course, CourseAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Score, ScoreAdmin)