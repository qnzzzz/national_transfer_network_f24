from rest_framework import serializers
from .models import AgreementCourse, Course, University
from .models import ArticulationAgreement

class UniversitySerializer(serializers.ModelSerializer):
    university_type = serializers.ChoiceField(choices=University.UNIVERSITY_TYPES)
    class Meta:
        model = University
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'       

class AgreementCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgreementCourse
        fields = '__all__'      

class ExcelFileSerializer(serializers.Serializer):
    file = serializers.FileField()         

class UploadDataSerializer(serializers.Serializer):
    fourYearInstitutionName = serializers.CharField(max_length=255)
    fourYearInstitutionLocation = serializers.CharField(max_length=300)
    effectiveTerm = serializers.CharField(max_length=10)
    ccSubject = serializers.CharField(max_length=255)
    uniSubject = serializers.CharField(max_length=255)
    credits = serializers.IntegerField()
    twoYearInstitutionName = serializers.CharField(max_length=255)    
    twoYearInstitutionLocation = serializers.CharField(max_length=300)


class ArticulationAgreementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticulationAgreement
        fields = '__all__'    