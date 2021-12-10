from rest_framework.serializers import ModelSerializer, ValidationError

from grades.models import Course, Grade, Semester


class SemesterSerializer(ModelSerializer):
    class Meta:
        model = Semester
        exclude = ['user']


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

    def validate_semester(self, semester):
        '''
        Checks if the user the owner of the semester 
        '''
        if semester.user != self.context['request'].user:
            raise ValidationError("You do not have permission")
        return semester


class GradeSerializer(ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'

    def validate_course(self, course):
        '''
        Checks if the user the owner of the semester 
        '''
        if course.semester.user != self.context['request'].user:
            raise ValidationError("You do not have permission")
        return course
