import json
import logging
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from .models import UniversityUser, CollegeUser, UniversityProfile, CollegeProfile, StudentProfile
from .forms import InstitutionRegistrationForm, InstitutionLoginForm, StudentRegistrationForm, StudentProfileForm
from .forms import (
    Uni_BasicInfoForm, Uni_ContactInfoForm, Uni_EnrollmentInfoForm, 
    Uni_StudentSupportServicesForm, Uni_TransferAndDegreePathwaysForm, Uni_UniversityHighlightsForm
)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import StudentLoginForm, UploadFileForm
from .transcript_scan.ocr_extract import process_pdf
import datetime
from django.contrib import messages
import openpyxl
import os
from openpyxl import Workbook
from django.conf import settings
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .models import UniversityUser, CollegeUser, UniversityProfile, CollegeProfile
from .forms import InstitutionRegistrationForm, InstitutionLoginForm, AgreementForm, Uni_BasicInfoForm, Uni_ContactInfoForm, Uni_EnrollmentInfoForm, Uni_StudentSupportServicesForm, Uni_TransferAndDegreePathwaysForm, Uni_UniversityHighlightsForm
from .models import Agreement, UniversityProfile, CollegeProfile, UniversityCourse, CollegeCourse, AgreementCourse,StudentProfile, StudentCourse
from .forms import (Col_BasicInfoForm, Col_ContactInfoForm, Col_EnrollmentInfoForm, 
                    Col_TransferInfoForm, Col_Special4YearOfferingForm, Col_SupportiveInfoForm)
# from rest_framework import viewsets
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.parsers import MultiPartParser, FormParser
# from rest_framework import status
# from weasyprint import HTML
# from .models import AgreementCourse, ArticulationAgreement
# from django.contrib.auth.decorators import login_required
# from .models import Course, Profile, University
# from .serializers import CourseSerializer, UniversitySerializer, ExcelFileSerializer, UploadDataSerializer, ArticulationAgreementSerializer, AgreementCourseSerializer
# import pandas as pd
# from rest_framework import generics

EXCEL_FILE_PATH = os.path.join(settings.BASE_DIR, 'files', 'reported_universities.xlsx')


def home(request):
    return render(request, 'ntn_app/home.html')


def institution_register(request):
    if request.method == 'POST':
        form = InstitutionRegistrationForm(request.POST)
        if form.is_valid():
            # Create a new user
            user = User.objects.create_user(
                username=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            # Save the institution and link to user
            form.save(user)
            login(request, user)
            return redirect('institution_landing_page')  # Redirect to a suitable page after registration
    else:
        form = InstitutionRegistrationForm()
    
    return render(request, 'ntn_app/institution_register.html', {'form': form})


def student_login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        # Check if the user is authenticated and has a student profile
        if request.user.is_authenticated and hasattr(request.user, 'student_profile'):
            return view_func(request, *args, **kwargs)
        # Redirect to login if no valid profile is found
        return redirect('student_login')
    return _wrapped_view

def institution_login(request):
    if request.method == 'POST':
        form = InstitutionLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            institution_type = form.cleaned_data['institution_type']
            
            # Authenticate user
            user = authenticate(request, username=email, password=password)
            if user is not None:
                # Check if user belongs to the specified institution type
                if institution_type == 'university':
                    if UniversityUser.objects.filter(user=user).exists():
                        login(request, user)
                        print('logged in')
                        return redirect('institution_landing_page')
                    else:
                        form.add_error(None, 'This user is not associated with a university.')
                elif institution_type == 'college':
                    if CollegeUser.objects.filter(user=user).exists():
                        login(request, user)
                        return redirect('institution_landing_page')
                    else:
                        form.add_error(None, 'This user is not associated with a college.')
            else:
                form.add_error(None, 'Invalid email or password')
    else:
        form = InstitutionLoginForm()
    
    return render(request, 'ntn_app/institution_login.html', {'form': form})


def institution_login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        # Check if the user is authenticated and if they have either a university or college profile
        if request.user.is_authenticated:
            has_university_profile = UniversityUser.objects.filter(user=request.user).exists()
            has_college_profile = CollegeUser.objects.filter(user=request.user).exists()
            if has_university_profile or has_college_profile:
                return view_func(request, *args, **kwargs)
        
        # Redirect to login if no valid profile is found
        return redirect('institution_login')
            
    return _wrapped_view


def university_login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        # Check if the user is authenticated and has a university profile
        if request.user.is_authenticated and UniversityUser.objects.filter(user=request.user).exists():
            return view_func(request, *args, **kwargs)
        else:
            return redirect('institution_login')
    return _wrapped_view


def college_login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        # Check if the user is authenticated and has a college profile
        if request.user.is_authenticated and CollegeUser.objects.filter(user=request.user).exists():
            return view_func(request, *args, **kwargs)
        else:
            return redirect('institution_login')
    return _wrapped_view


@institution_login_required
def institution_logout(request):
    logout(request)
    return redirect('home')

@institution_login_required
def institution_landing_page(request):

    if UniversityUser.objects.filter(user=request.user).exists():
        user_type = 'university'
        profile_id = UniversityUser.objects.get(user=request.user).university.id
    elif CollegeUser.objects.filter(user=request.user).exists():
        user_type = 'college'
        profile_id = CollegeUser.objects.get(user=request.user).college.id

    context = {
        'user_type': user_type,
        'profile_id': profile_id,
    }

    #     # Determine the type of institution user belongs to
    # if hasattr(request.user, 'university'):
    #     # User is a university user
    #     institution_type = 'university'
    #     profile_id = request.user.university.id
    # elif hasattr(request.user, 'college'):
    #     # User is a college user
    #     institution_type = 'college'
    #     profile_id = request.user.college.id
    # else:
    #     institution_type = None
    #     profile_id = None

    return render(request, 'ntn_app/institution_landing_page.html', context)

@student_login_required
def student_landing_page(request):
    return render(request, 'ntn_app/student_landing_page.html')

@student_login_required
def student_profile(request):
    student_profile = request.user.student_profile
    
    initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        }

    if request.method == 'POST':
        # Process course deletions and updates
        for key, value in request.POST.items():
            if key.startswith("delete_"):
                # Handle course deletion
                course_id = key.split("_")[1]
                try:
                    StudentCourse.objects.get(id=course_id).delete()
                    print(f"Deleted course with ID: {course_id}")
                except StudentCourse.DoesNotExist:
                    print(f"Course with ID {course_id} does not exist.")
            
            elif key.startswith("course_code_"):
                # Handle course updates
                course_id = key.split("_")[2]
                if f"delete_{course_id}" in request.POST:
                    continue  # Skip updates for deleted courses
                try:
                    course = StudentCourse.objects.get(id=course_id)
                    course.course_code = request.POST.get(f"course_code_{course_id}")
                    course.grade = request.POST.get(f"grade_{course_id}")
                    course.taken_year = request.POST.get(f"year_{course_id}")
                    course.taken_term = request.POST.get(f"term_{course_id}")
                    course.save()
                except StudentCourse.DoesNotExist:
                    print(f"Course with ID {course_id} does not exist.")

        # Handle profile form submission
        form = StudentProfileForm(request.POST, request.FILES, instance=student_profile)
        if form.is_valid():    
            institution = form.cleaned_data['institution']
            other_institution = form.cleaned_data['other_institution']

            if not institution and other_institution:
                college_profile, created = CollegeProfile.objects.get_or_create(college_name=other_institution, defaults={'is_partner': False})
                student_profile.institution = college_profile
            else:
                student_profile.institution = institution
            
            user = request.user
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.save()
            form.save()
            university_list = []
            # Save updated university preferences
            updated_preferences = request.POST.get('university_name[]')
            if updated_preferences:
                # Split by comma if it's a single string, else use the list directly
                if isinstance(updated_preferences, str):
                    university_list = updated_preferences.split(",")
                else:
                    university_list = updated_preferences

            other_university = request.POST.get('other_university', '').strip()
            print(other_university)
            if other_university: 
                log_university_to_excel(other_university)
                university_list.append(other_university)

            # Save all preferences as a comma-separated string
            student_profile.set_university_preference(university_list)
            student_profile.save()

            return redirect('student_profile')

    else:
        # Handle GET request: prepare initial data and load form
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        }
        form = StudentProfileForm(instance=student_profile)

    # Fetch student courses
    student_courses = StudentCourse.objects.filter(student=student_profile).order_by('taken_year', 'taken_term')
    return render(
        request,
        'ntn_app/student_profile.html',
        {
            'form': form,
            'initial_data': initial_data,
            'student_courses': student_courses,
            'university_preferences': student_profile.get_university_preference() or None,
            'universities': [uni.university_name for uni in UniversityProfile.objects.all()],
        }
    )


def student_logout(request):
    logout(request)
    return redirect('home')

def student_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('student_landing_page')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'ntn_app/student_login.html')

def explore_institutions(request):
    user = request.user
    user_type = None
    institution_id = None
    if user.is_authenticated:
        if UniversityUser.objects.filter(user=user).exists():
            user_type = 'university'
            institution_id = UniversityUser.objects.get(user=user).university.id
        elif CollegeUser.objects.filter(user=user).exists():
            user_type = 'college'
            institution_id = CollegeUser.objects.get(user=user).college.id
        elif StudentProfile.objects.filter(user=user).exists():
            user_type = 'student'
    return render(request, 'ntn_app/explore_institutions.html', {"user_type": user_type, "institution_id": institution_id})

def university_profile(request, university_profile_id):
    profile = get_object_or_404(UniversityProfile, id=university_profile_id)
    
    can_edit = False
    is_edit_mode = request.GET.get('edit') == 'true'
    is_authenticated = False

    # Check if the user is authenticated
    if request.user.is_authenticated:
        is_authenticated = True
        print('user is authenticated')
        # Check if the logged-in user is associated with this university
        university_user = UniversityUser.objects.filter(user=request.user, university=profile).first()
        if university_user:
            can_edit = True  # Allow editing only if the user is the profile owner

    # If an unauthorized user tries to edit the profile, redirect to home
    if is_edit_mode and not can_edit:
        return redirect('home')
            
    if request.method == 'POST' and is_edit_mode and can_edit:
        basic_info_form = Uni_BasicInfoForm(request.POST, instance=profile)
        contact_info_form = Uni_ContactInfoForm(request.POST, instance=profile)
        enrollment_info_form = Uni_EnrollmentInfoForm(request.POST, instance=profile)
        support_services_form = Uni_StudentSupportServicesForm(request.POST, instance=profile)
        degree_pathways_form = Uni_TransferAndDegreePathwaysForm(request.POST, instance=profile)
        highlights_form = Uni_UniversityHighlightsForm(request.POST, instance=profile)

        if (basic_info_form.is_valid() and contact_info_form.is_valid() and
            enrollment_info_form.is_valid() and support_services_form.is_valid() and
            degree_pathways_form.is_valid() and highlights_form.is_valid()):
            basic_info_form.save()
            contact_info_form.save()
            enrollment_info_form.save()
            support_services_form.save()
            degree_pathways_form.save()
            highlights_form.save()
            return redirect('university_profile', university_profile_id=university_profile_id)

    else:
        basic_info_form = Uni_BasicInfoForm(instance=profile)
        contact_info_form = Uni_ContactInfoForm(instance=profile)
        enrollment_info_form = Uni_EnrollmentInfoForm(instance=profile)
        support_services_form = Uni_StudentSupportServicesForm(instance=profile)
        degree_pathways_form = Uni_TransferAndDegreePathwaysForm(instance=profile)
        highlights_form = Uni_UniversityHighlightsForm(instance=profile)

    user = request.user
    institution_id = None
    user_type = None
    if user.is_authenticated:
        if UniversityUser.objects.filter(user=user).exists():
            user_type = 'university'
            institution_id = UniversityUser.objects.get(user=user).university.id
        elif CollegeUser.objects.filter(user=user).exists():
            user_type = 'college'
            institution_id = CollegeUser.objects.get(user=user).college.id
        elif StudentProfile.objects.filter(user=user).exists():
            user_type = 'student'

    return render(request, 'ntn_app/university_profile_page.html', {
        'profile': profile,
        'basic_info_form': basic_info_form,
        'contact_info_form': contact_info_form,
        'enrollment_info_form': enrollment_info_form,
        'support_services_form': support_services_form,
        'degree_pathways_form': degree_pathways_form,
        'highlights_form': highlights_form,
        'can_edit': can_edit,
        'is_edit_mode': is_edit_mode,
        'user_type': user_type,
        'institution_id': institution_id,
        'is_authenticated': is_authenticated,
    })


def college_profile(request, college_profile_id):
    profile = get_object_or_404(CollegeProfile, id=college_profile_id)
    
    can_edit = False
    is_edit_mode = request.GET.get('edit') == 'true'

    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Check if the logged-in user is associated with this college
        college_user = CollegeUser.objects.filter(user=request.user, college=profile).first()
        if college_user:
            can_edit = True  # Allow editing only if the user is the profile owner

    # If an unauthorized user tries to edit the profile, redirect to home
    if is_edit_mode and not can_edit:
        return redirect('home')

    if request.method == 'POST' and can_edit:
        basic_info_form = Col_BasicInfoForm(request.POST, instance=profile)
        contact_info_form = Col_ContactInfoForm(request.POST, instance=profile)
        enrollment_info_form = Col_EnrollmentInfoForm(request.POST, instance=profile)
        transfer_info_form = Col_TransferInfoForm(request.POST, instance=profile)
        special_4year_info_form =Col_Special4YearOfferingForm(request.POST, instance=profile)
        supportive_info_form = Col_SupportiveInfoForm(request.POST, instance=profile)

        if (basic_info_form.is_valid() and contact_info_form.is_valid() and
            enrollment_info_form.is_valid() and transfer_info_form.is_valid() and
            special_4year_info_form.is_valid() and supportive_info_form.is_valid()):
            
            basic_info_form.save()
            contact_info_form.save()
            enrollment_info_form.save()
            transfer_info_form.save()
            special_4year_info_form.save()
            supportive_info_form.save()
            return redirect('college_profile', college_profile_id=college_profile_id)
    
    else:
        basic_info_form = Col_BasicInfoForm(instance=profile)
        contact_info_form = Col_ContactInfoForm(instance=profile)
        enrollment_info_form = Col_EnrollmentInfoForm(instance=profile)
        transfer_info_form = Col_TransferInfoForm(instance=profile)
        special_4year_info_form =Col_Special4YearOfferingForm(instance=profile)
        supportive_info_form = Col_SupportiveInfoForm(instance=profile)

    user = request.user
    institution_id = None
    user_type = None
    if user.is_authenticated:
        if UniversityUser.objects.filter(user=user).exists():
            user_type = 'university'
            institution_id = UniversityUser.objects.get(user=user).university.id
        elif CollegeUser.objects.filter(user=user).exists():
            user_type = 'college'
            institution_id = CollegeUser.objects.get(user=user).college.id
        elif StudentProfile.objects.filter(user=user).exists():
            user_type = 'student'

    return render(request, 'ntn_app/college_profile_page.html', {
        'profile': profile,
        'basic_info_form': basic_info_form,
        'contact_info_form': contact_info_form,
        'enrollment_info_form': enrollment_info_form,
        'transfer_info_form': transfer_info_form,
        'special_4year_info_form': special_4year_info_form,
        'supportive_info_form': supportive_info_form,
        'can_edit': can_edit,
        'is_edit_mode': is_edit_mode,
        'user_type': user_type,
        'institution_id': institution_id,
    })


def get_profile_url(user):
    if hasattr(user, 'UniversityUser'):
        # User is a university user, redirect to university profile
        return reverse('university_profile', args=[user.UniversityUser.university.id])
    elif hasattr(user, 'CollegeUser'):
        # User is a college user, redirect to college profile
        return reverse('college_profile', args=[user.UniversityUser.college.id])
    return None

    
def student_register(request):
    if request.user.is_authenticated:
        logout(request)
        
    context = {}

    if request.method == "GET":
        context['form'] = StudentRegistrationForm()
        return render(request, 'ntn_app/student_register.html', context)

    form = StudentRegistrationForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'ntn_app/student_register.html', context)

    new_user = User.objects.create_user(
        username=form.cleaned_data['username'],
        password=form.cleaned_data['password'],
        email=form.cleaned_data['email'],
        first_name=form.cleaned_data['first_name'],
        last_name=form.cleaned_data['last_name']
    )
    new_user.save()

    new_student_profile = StudentProfile(
        user=new_user
    )
    new_student_profile.save()

    messages.success(request, 'Registration successful. Please log in.')
    return redirect('student_login')

@login_required
def add_course(request):
    form = UploadFileForm(request.POST or None, request.FILES or None)
    years = range(2000, datetime.datetime.now().year + 1)
    
    university_options = UniversityProfile.objects.values_list('university_name', flat=True)

    # Clear session data for a fresh state on the initial GET request (but not after form submission)
    if request.method == 'GET':
        request.session.pop('results', None)
        request.session.pop('selected_course_codes', None)
        request.session.pop('university', None)
        request.session.pop('pass_column_extractions', None)
        request.session.pop('added_courses', None)
        
    selected_university = request.session.get('university', None)
    if request.method == 'POST':

        # Handle file upload only if the file is in the POST request and form is valid
        if 'file' in request.FILES and form.is_valid():
            file_handle = request.FILES['file']
            
            if not file_handle.name.endswith('.pdf'):
                return redirect('add_course')
            
            results= process_pdf(file_handle)
            
            pass_column_extractions = []

            # Iterate through each line to check for "pass" and extract grades
            for line in results:
                words = line.split()
                if "pass" in [word.lower() for word in words]:
                    pass_column_index = [word.lower() for word in words].index("pass")
                    if len(words) > pass_column_index:
                        pass_column_extractions.append(words[pass_column_index])
                    else:
                        pass_column_extractions.append("")

            # Update session data only after processing the file successfully
            request.session['results'] = results
            request.session['pass_column_extractions'] = pass_column_extractions
            request.session.modified = True
        
        # Handle course code extraction if course_code_column is posted
        elif 'course_code_column' in request.POST:
            column_index = int(request.POST.get('course_code_column')) - 1
            results = request.session.get('results', [])
            if results:
                selected_course_codes = [
                    result.split()[column_index] for result in results if len(result.split()) > column_index
                ]
                request.session['selected_course_codes'] = selected_course_codes
        elif 'university_name[]' in request.POST:
            university_choices = request.POST.getlist('university_name[]')
            other_university = request.POST.get('other_university', '').strip()

            if 'Other' in university_choices and other_university:
                # Add manually entered university to session
                request.session['university'] = other_university
                log_university_to_excel(other_university)
                selected_university = other_university
            else:
                # Save selected universities to session
                request.session['university'] = university_choices
                selected_university = university_choices

        # Handle dynamically added courses
        course_codes = request.POST.getlist('course_codes[]')
        grades = request.POST.getlist('grades[]')
        terms = request.POST.getlist('terms[]')
        taken_years = request.POST.getlist('years[]')
 
        student = request.user.student_profile

        if course_codes or grades or terms or taken_years:
            added_courses = []
            for course_code, grade, term, year in zip(course_codes, grades, terms, taken_years):
                # Provide default values if any field is None or empty
                if not course_code or not grade or not term or not year:
                    continue

                grade = grade or "None"
                term = term or "None"
                year = year or 0 

                # Check if a StudentCourse record already exists
                if not StudentCourse.objects.filter(
                    student=student,
                    course_code=course_code,
                    taken_year=year,
                    taken_term=term
                ).exists():
                    # If it does not exist, create a new StudentCourse record
                    new_course = StudentCourse.objects.create(
                        student=student,
                        course_code=course_code,
                        grade=grade,
                        taken_year=year,
                        taken_term=term
                    )
                    added_courses.append(new_course)


            # Update session data for added courses for display
            request.session['added_courses'] = [
                (course.course_code, course.grade, course.taken_year, course.taken_term) 
                for course in added_courses
            ]
            
            return redirect('student_profile')

    # Retrieve session data for template context
    results = request.session.get('results', [])
    selected_course_codes = request.session.get('selected_course_codes', [])
    pass_column_extractions = request.session.get('pass_column_extractions', [])
    added_courses = request.session.get('added_courses', [])
    course_grade_pairs = list(zip(selected_course_codes, pass_column_extractions))
    
    context = {
        'form': form,
        'results': results,
        'selected_course_codes': selected_course_codes,
        'course_grade_pairs': course_grade_pairs,
        'years': list(years),
        'added_courses': added_courses,
        'university': selected_university,
        'universities': list(university_options),
    }

    return render(request, 'ntn_app/add_course.html', context)

def log_university_to_excel(university_name):
    # Check if the Excel file exists
    if not os.path.exists(EXCEL_FILE_PATH):
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Unknown Universities"
        sheet.append(["University Name", "Date Reported"])
    else:
        # Load the existing workbook
        workbook = openpyxl.load_workbook(EXCEL_FILE_PATH)
        sheet = workbook.active

    # Append the university name and the current date to the Excel sheet
    sheet.append([university_name, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')])

    # Save the workbook
    workbook.save(EXCEL_FILE_PATH)

logger = logging.getLogger(__name__)

def handle_college_selection(request):
    if request.method == 'POST':
            institution_id = request.POST.get('institution')
            institution_type = request.POST.get('institution_type')
            
            if institution_type == 'two_year_college':
                return redirect('college_profile', college_profile_id=institution_id)
            elif institution_type == 'four_year_university':
                return redirect('university_profile', university_profile_id=institution_id)

    return render(request, 'ntn_app/explore_institutions.html')
            
def get_university_id(university_name):
    try:
        university = UniversityProfile.objects.get(university_name=university_name)
        return university.id
    except UniversityProfile.DoesNotExist:
        return None
 
def get_institutions(request):
    institution_type = request.GET.get('institution_type')
    if institution_type == 'four_year_university':
        institutions = UniversityProfile.objects.filter(is_partner=True).values('id', 'university_name')   
    elif institution_type == 'two_year_college':
        institutions = CollegeProfile.objects.filter(is_partner=True).values('id', 'college_name')
    else:
        institutions = []
    
    return JsonResponse(list(institutions), safe=False)


@institution_login_required
def new_agreement(request):
    user = request.user
    institution_type = None
    institution_name = None
    institution_id = None
    if user.is_authenticated:
        if UniversityUser.objects.filter(user=user).exists():
            institution_type = 'university'
            institution_name = UniversityUser.objects.get(user=user).university.university_name
            institution_id = UniversityUser.objects.get(user=user).university.id
        elif CollegeUser.objects.filter(user=user).exists():
            institution_type = 'college'
            institution_name = CollegeUser.objects.get(user=user).college.college_name
            institution_id = CollegeUser.objects.get(user=user).college.id
    
    context = {
        'institution_type': institution_type,
        'institution_name': institution_name,
        'institution_id': institution_id,
    }
        
    if request.method == 'POST':
        # Remove any fields with '_duplicate' in the name
        filtered_data = {key: value for key, value in request.POST.items() if '_duplicate' not in key}

        # Extract university and college names from filtered_data
        university_name = filtered_data.get('university')
        college_name = filtered_data.get('college')

        # Get or create university and college instances
        university, created_university = UniversityProfile.objects.get_or_create(university_name=university_name)
        college, created_college = CollegeProfile.objects.get_or_create(college_name=college_name)
        
        # Set the is_partnered flag to True for university and college
        university.is_partner = True
        college.is_partner = True
        university.save()
        college.save() 

        # Update filtered_data to include the foreign key IDs for university and college
        filtered_data['university'] = university.id
        filtered_data['college'] = college.id

        # Create the Agreement form with filtered data
        form = AgreementForm(filtered_data)
        if form.is_valid():
            # Save new agreement
            agreement = form.save()

            # Process course data for the AgreementCourse relationships
            course_index = 0
            while f"courses[{course_index}][cc_subject]" in request.POST:
                college_course_subject_code = request.POST.get(f"courses[{course_index}][cc_subject]")
                college_course_digit_code = request.POST.get(f"courses[{course_index}][cc_digit]")
                college_course_credits = request.POST.get(f"courses[{course_index}][cc_credits]")
                university_course_subject_code = request.POST.get(f"courses[{course_index}][uc_subject]")
                university_course_digit_code = request.POST.get(f"courses[{course_index}][uc_digit]")
                university_course_credits = request.POST.get(f"courses[{course_index}][uc_credits]")

                # Get or create the CollegeCourse
                college_course, _ = CollegeCourse.objects.get_or_create(
                    institution=college,
                    subject_code=college_course_subject_code,
                    digit_code=college_course_digit_code,
                    defaults={'credits': college_course_credits}
                )

                # Get or create the UniversityCourse
                university_course, _ = UniversityCourse.objects.get_or_create(
                    institution=university,
                    subject_code=university_course_subject_code,
                    digit_code=university_course_digit_code,
                    defaults={'credits': university_course_credits}
                )

                # Create the AgreementCourse
                AgreementCourse.objects.create(
                    agreement=agreement,
                    college_course=college_course,
                    university_course=university_course,
                    credits=university_course_credits  # Use university credits for the agreement
                )

                course_index += 1

            return redirect('all_agreements', institution_type=institution_type, profile_id=institution_id)
    else:
        form = AgreementForm()

    return render(request, 'ntn_app/new_agreement.html', {'form': form, 'context': context})


@institution_login_required
def manage_agreements(request):
    user = request.user
    institution_type = None
    institution_id = None

    agreements = []
    institution_name = None
    if UniversityUser.objects.filter(user=user).exists():
        university_profile = UniversityUser.objects.get(user=user).university
        institution_name = university_profile.university_name
        agreements = Agreement.objects.filter(university=university_profile.id)
        institution_type = 'university'
        institution_id = university_profile.id
        
    elif CollegeUser.objects.filter(user=user).exists():
        college_profile = CollegeUser.objects.get(user=user).college
        institution_name = college_profile.college_name
        agreements = Agreement.objects.filter(college=college_profile.id)
        institution_type = 'college'
        institution_id = college_profile.id
        
    print(institution_name)
    print(institution_type)
    print(institution_id)
    return render(request, 'ntn_app/manage_agreements.html', 
    {'agreements': agreements, 
    'institution_name': institution_name,
    'institution_type': institution_type,
    'institution_id': institution_id,
    })

@institution_login_required
def delete_agreement(request, agreement_id):
    user = request.user
    institution_type = None
    profile_id = None

    if UniversityUser.objects.filter(user=user).exists():
        university_profile = UniversityUser.objects.get(user=user).university
        institution_type = 'university'
        profile_id = university_profile.id
        
    elif CollegeUser.objects.filter(user=user).exists():
        college_profile = CollegeUser.objects.get(user=user).college
        institution_type = 'college'
        profile_id = college_profile.id

    agreement = get_object_or_404(Agreement, id=agreement_id)
    agreement.delete()

    return redirect('all_agreements', institution_type=institution_type, profile_id=profile_id)


def all_agreements(request, institution_type, profile_id):
    agreements=[]
    user = request.user
    user_type = None
    institution_id = None
    institution_name = None
    is_authenticated = False

    if user.is_authenticated:
        is_authenticated = True
        if UniversityUser.objects.filter(user=user).exists():
            user_type = 'university'
            institution_id = UniversityUser.objects.get(user=user).university.id
        elif CollegeUser.objects.filter(user=user).exists():
            user_type = 'college'
            institution_id = CollegeUser.objects.get(user=user).college.id
        elif StudentProfile.objects.filter(user=user).exists():
            user_type = 'student'

    if institution_type == 'university':
        university = get_object_or_404(UniversityProfile, id=profile_id)
        agreements = Agreement.objects.filter(university=university.id)
        institution_name = university.university_name
    elif institution_type == 'college':
        college = get_object_or_404(CollegeProfile, id=profile_id)
        agreements = Agreement.objects.filter(college=college.id)
        institution_name = college.college_name

    print(institution_id)
    print(profile_id)
    context = {
        'agreements': agreements,
        'user_type': user_type,
        'institution_type': institution_type,
        "profile_id": profile_id,
        'institution_name': institution_name,
        "institution_id": institution_id,
        'is_authenticated': is_authenticated,
    }
    
    return render(request, 'ntn_app/all_agreements.html', context)
