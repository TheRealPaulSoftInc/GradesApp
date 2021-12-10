from django.contrib import admin
from grades.models import Semester, Course, Grade

admin.site.register(Semester)
admin.site.register(Course)
admin.site.register(Grade)
