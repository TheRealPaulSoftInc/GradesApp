from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.deletion import CASCADE

User = get_user_model()


class Semester(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default="")
    term = models.PositiveSmallIntegerField(
        default=None, blank=True, null=True)
    progress_score = models.DecimalField(
        default=None, blank=True, null=True, decimal_places=4, max_digits=7)
    target_score = models.DecimalField(
        default=None, blank=True, null=True, decimal_places=4, max_digits=7)
    total_credits = models.IntegerField(default=0)
    is_completed = models.BooleanField(default=False)

    def calculate_all(self):
        self.progress_score = 0.0
        self.target_score = 0.0
        self.total_credits = 0
        self.is_completed = True
        for course in self.course_set.all():
            self.total_credits += course.credit
        for course in self.course_set.all():
            if course.is_completed:
                self.progress_score += course.progress_grade * \
                    (course.credit/self.total_credits)
                self.is_completed = False
            else:
                self.target_score += course.target_grade * \
                    (course.credit/self.total_credits)
        self.save()
    # @property
    # def progress_grade(self):
    #     '''
    #     returns the average of progress grade of its courses considering their credits
    #     '''
    #     progress = 0
    #     credits = 0
    #     courses = self.course_set.all()
    #     for course in courses:
    #         progress += course.progress_grade * course.credit
    #         credits += course.credit
    #     progress = progress / (len(courses) * credits)
    #     return progress

    # @property
    # def target_grade(self):
    #     '''
    #     returns the average of target grade of its courses considering their credits
    #     '''
    #     target = 0
    #     credits = 0
    #     courses = self.course_set.all()
    #     for course in courses:
    #         target += course.target_grade * course.credit
    #         credits += course.credit
    #     target = target / (len(courses) * credits)
    #     return target

    # @property
    # def is_completed(self):
    #     '''
    #     returns true if every course of this semester has been completed
    #     '''
    #     if len(self.course_set.all()) > 0 and len(self.course_set.filter(is_completed=False) == 0):
    #         return True
    #     return False

    def __str__(self):
        return f"Semester {self.term}"


class Course(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default="")
    credit = models.DecimalField(
        default=None, blank=True, null=True, decimal_places=2, max_digits=4)
    professor = models.CharField(max_length=255, blank=True)
    progress_score = models.DecimalField(
        default=None, blank=True, null=True, decimal_places=4, max_digits=7)
    target_score = models.DecimalField(
        default=None, blank=True, null=True, decimal_places=4, max_digits=7)
    progress_percent = models.DecimalField(
        default=None, blank=True, null=True, decimal_places=4, max_digits=7)
    target_percent = models.DecimalField(
        default=None, blank=True, null=True, decimal_places=4, max_digits=7)
    is_completed = models.BooleanField(default=False)
    # order in which this element will be displayed
    order = models.PositiveSmallIntegerField(default=0)

    def calculate_all(self):
        self.is_completed = True
        self.progress_percent = 0.0
        self.progress_score = 0.0
        self.target_percent = 0.0
        self.target_score = 0.0
        for grade in self.grade_set.all():
            if grade.is_confirmed:
                self.progress_percent += grade.weight
                self.progress_score += grade.grade * grade.weight
            else:
                self.is_completed = False
                self.target_percent += grade.weight
                self.target_score += grade.grade * grade.weight
        self.semester.calculate_all()
        self.save()
    # def save(self,*args, **kwargs):
    #     if not self.id:
    #         self.super.save()
    #     else:
    #         print(kwargs['credit'])
    #         if self.credit!=kwargs['credit']:
    #             #Test
    #             self.course.calculate_all()
    #         self.super.save()
    # @property
    # def progress_percent(self):
    #     '''
    #     returns the sum of weight of grades that has been officially asigned
    #     '''
    #     progress = 0
    #     for grade in self.grade_set.filter(is_confirmed=True):
    #         progress += grade.weight
    #     return progress

    # @property
    # def progress_grade(self):
    #     '''
    #     returns the sum of grades that has been officially asigned
    #     '''
    #     progress = 0
    #     for grade in self.grade_set.filter(is_confirmed=True):
    #         progress += grade.grade * grade.weight
    #     return progress

    # @property
    # def target_grade(self):
    #     '''
    #     returns the sum of officially and non officially grades
    #     '''
    #     target = 0
    #     for grade in self.grade_set.all():
    #         target += grade.grade * grade.weight
    #     return target

    # @property
    # def is_completed(self):
    #     '''
    #     returns True if the sum of weight of comfirmed grades is 100%
    #     '''
    #     confirmed_grades = self.grade_set.filter(is_confirmed=True)
    #     if len(confirmed_grades) == 0:
    #         return False
    #     total_weight = 0
    #     for grade in confirmed_grades:
    #         total_weight += grade.weight
    #     if total_weight == 100:
    #         return True
    #     return False

    def __str__(self):
        return self.name


class Grade(models.Model):
    name = models.CharField(max_length=255, default="")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    score = models.DecimalField(
        default=None, blank=True, null=True, decimal_places=4, max_digits=7)
    weight = models.DecimalField(
        default=None, blank=True, null=True, decimal_places=4, max_digits=7)
    # defines if the grade has been officially asigned
    is_confirmed = models.BooleanField(default=False)
    # order in which this element will be displayed
    order = models.PositiveSmallIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.id:
            super(Grade, self).save(*args, **kwargs)
        else:
            print(kwargs['score'])
            if self.score != kwargs['score']:
                # Test
                self.course.calculate_all()
            super(Grade, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
