from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse

from ntn_app.forms import LoginForm, RegistrationForm
from .models import Course, University
from .serializers import CourseSerializer, UniversitySerializer, ExcelFileSerializer
import pandas as pd

class UniversityViewSet(viewsets.ModelViewSet):
    queryset =  University.objects.all()
    print(str(queryset.query))
    serializer_class = UniversitySerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    print(str(queryset.query))
    serializer_class = CourseSerializer    

def TwoYearUpload(request):
    return render(request,'ntn_app/2year_upload.html')

def FourYearUpload(request):
    return render(request,'ntn_app/4year_upload.html')


def add_course(request):
    return render(request, 'ntn_app/add_course.html')

def inst_register_view(request):
    context = {}

    if request.method == "GET":
        context['form'] =  RegistrationForm()
        return render(request, 'ntn_app/register.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = RegistrationForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        print("\n"*20)
        print("form is not valid")
        return render(request, 'ntn_app/register.html', context)

    return render(request, 'ntn_app/2year_upload.html', context)

    # # At this point, the form data is valid.  Register and login the user.
    # new_user = User.objects.create_user(username=form.cleaned_data['username'], 
    #                                     password=form.cleaned_data['password1'],
    #                                     email=form.cleaned_data['email'],
    #                                     first_name=form.cleaned_data['first_name'],
    #                                     last_name=form.cleaned_data['last_name'])
    # new_user.save()

    # new_user = authenticate(username=form.cleaned_data['username'],
    #                         password=form.cleaned_data['password1'])

    # login(request, new_user)
    # return redirect(reverse('home'))

def login_view(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'ntn_app/login.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = LoginForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        context['message'] = 'wrong username or password'
        return render(request, 'ntn_app/login.html', context)

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('add-course'))


class ExcelUploadView(APIView):
    print('called the excel upload function')
    parser_classes = (MultiPartParser, FormParser,)

    def post(self, request, *args, **kwargs):
        file_serializer = ExcelFileSerializer(data=request.data)
        if file_serializer.is_valid():
            excel_file = request.FILES['file']
            df = pd.read_excel(excel_file)

            for index, row in df.iterrows():
                four_year_university, _ = University.objects.get_or_create(
                    name=row['4yearCollegeName'],
                    location=row['4yearCollegeLocation'],
                    defaults={'university_type': 'FOUR_YEAR'}
                )
                two_year_university, _ = University.objects.get_or_create(
                    name=row['2yearCollegeName'],
                    location=row['2yearCollegeLocation'],
                    defaults={'university_type': 'TWO_YEAR'}
                )
                #2 year course
                two_year_course = Course.objects.create(
                    course_name=row['CC_Subject'],
                    effective_term=row['EffectiveTerm'],
                    credits=row['Credits'],
                    university=four_year_university,
                )

                #4year course
                four_year_course = Course.objects.create(
                    course_name=row['CC_Subject'],
                    effective_term=row['EffectiveTerm'],
                    credits=row['Credits'],
                    university=two_year_university,
                    equivalent_course=two_year_course
                )

                # Update the 2-year course to link back to the 4-year course
                two_year_course.equivalent_course = four_year_course
                two_year_course.save()
            return Response({"message": "Data imported successfully"}, status=201)
        else:
            return Response(file_serializer.errors, status=400)
