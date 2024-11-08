import logging
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from .models import UniversityUser, CollegeUser, UniversityProfile, CollegeProfile, StudentProfile
from .forms import InstitutionRegistrationForm, InstitutionLoginForm, StudentRegistrationForm, StudentProfileForm
from .forms import (
    Uni_BasicInfoForm, Uni_ContactInfoForm, Uni_EnrollmentInfoForm, 
    Uni_StudentSupportServicesForm, Uni_TransferAndDegreePathwaysForm, Uni_UniversityHighlightsForm, ExploreUniversitiesForm
)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import StudentLoginForm
# from rest_framework import viewsets
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.parsers import MultiPartParser, FormParser
# from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from django.template.loader import render_to_string
from django.http import HttpResponse
# from weasyprint import HTML
# from .models import AgreementCourse, ArticulationAgreement
# from django.contrib.auth.decorators import login_required
# from ntn_app.forms import LoginForm, RegistrationForm
# from .models import Course, Profile, University
# from .serializers import CourseSerializer, UniversitySerializer, ExcelFileSerializer, UploadDataSerializer, ArticulationAgreementSerializer, AgreementCourseSerializer
# import pandas as pd
# from rest_framework import generics


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



# def student_login_required(view_func):
#     def _wrapped_view(request, *args, **kwargs):
#         # Check if the user is authenticated and has a student profile
#         if request.user.is_authenticated and hasattr(request.user, 'student_profile'):
#             return view_func(request, *args, **kwargs)
#         # Redirect to login if no valid profile is found
#         return redirect('institution_login')
#     return _wrapped_view

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

# def university_login_required(view_func):
#     def _wrapped_view(request, *args, **kwargs):
#         # Check if the user is authenticated and has an institution profile
#         if request.user.is_authenticated and hasattr(request.user, 'university_profile'):
#             return view_func(request, *args, **kwargs)
#         else:
#             return HttpResponseForbidden("You must be logged in as an university to access this page.")
#     return _wrapped_view


# def college_login_required(view_func):
#     def _wrapped_view(request, *args, **kwargs):
#         # Check if the user is authenticated and has an institution profile
#         if request.user.is_authenticated and hasattr(request.user, 'college_profile'):
#             return view_func(request, *args, **kwargs)
#         else:
#             return HttpResponseForbidden("You must be logged in as a college to access this page.")
#     return _wrapped_view


def entry_page_view(request):
    return render(request, 'ntn_app/entry_page.html')

@institution_login_required
def institution_landing_page_view(request):
    return render(request, 'ntn_app/institution_landing_page.html')

@login_required
def student_landing(request):
    return render(request, 'ntn_app/student_landing_page.html')


@login_required
def student_profile(request):
    student_profile = request.user.student_profile
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=student_profile)
        if form.is_valid():
            user = request.user
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.save()
            form.save()
            return redirect('student_profile')
    else:
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        }
        form = StudentProfileForm(instance=student_profile)
    return render(request, 'ntn_app/student_profile.html', {'form': form, 'initial_data': initial_data})



def logout_view(request):
    logout(request)
    return redirect('/')

# def student_login(request):
#     if request.method == 'POST':
#         form = StudentLoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('student_dashboard')  # Redirect to student dashboard after login
#             else:
#                 messages.error(request, 'Invalid username or password')
#     else:
#         form = StudentLoginForm()
#     return render(request, 'student_login.html', {'form': form})

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


def edit_university_profile(request, university_profile_id):
    university_user = get_object_or_404(UniversityUser, user=request.user)
    
    # check if the user has permission to edit the profile
    profile = get_object_or_404(UniversityProfile, id=university_profile_id)

    can_edit = university_user.university.id == university_profile_id

    # if university_user.university.id != university_profile_id:
    #     # if the user is not the owner of the profile, redirect to the profile view page
    #     # return redirect('university_profile_view', university_profile_id=university_profile_id)
    #     return redirect(reverse('university_profile_view', args=[university_profile_id]))

    if request.method == 'POST' and can_edit:
        basic_info_form = Uni_BasicInfoForm(request.POST, request.FILES, instance=profile)
        contact_info_form = Uni_ContactInfoForm(request.POST, instance=profile)
        enrollment_info_form = Uni_EnrollmentInfoForm(request.POST, instance=profile)
        support_services_form = Uni_StudentSupportServicesForm(request.POST, instance=profile)
        degree_pathways_form = Uni_TransferAndDegreePathwaysForm(request.POST, instance=profile)
        highlights_form = Uni_UniversityHighlightsForm(request.POST, instance=profile)

        # check if all forms are valid
        if (basic_info_form.is_valid() and contact_info_form.is_valid() and
            enrollment_info_form.is_valid() and support_services_form.is_valid() and
            degree_pathways_form.is_valid() and highlights_form.is_valid()):
            
            basic_info_form.save()
            contact_info_form.save()
            enrollment_info_form.save()
            support_services_form.save()
            degree_pathways_form.save()
            highlights_form.save()
            return redirect('university_profile_view', university_profile_id=university_profile_id)

    else:
        # data is not submitted, create forms with the current profile data
        basic_info_form = Uni_BasicInfoForm(instance=profile)
        contact_info_form = Uni_ContactInfoForm(instance=profile)
        enrollment_info_form = Uni_EnrollmentInfoForm(instance=profile)
        support_services_form = Uni_StudentSupportServicesForm(instance=profile)
        degree_pathways_form = Uni_TransferAndDegreePathwaysForm(instance=profile)
        highlights_form = Uni_UniversityHighlightsForm(instance=profile)

    return render(request, 'ntn_app/university_profile_page.html', {
        'profile': profile,
        'basic_info_form': basic_info_form,
        'contact_info_form': contact_info_form,
        'enrollment_info_form': enrollment_info_form,
        'support_services_form': support_services_form,
        'degree_pathways_form': degree_pathways_form,
        'highlights_form': highlights_form,
        'can_edit': can_edit # check if the user can edit the profile
    })
    
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


def add_course(request):
    return render(request, 'ntn_app/add_course.html')

logger = logging.getLogger(__name__)

@login_required
def explore_universities(request):
    if request.method == 'POST':
        form = ExploreUniversitiesForm(request.POST)
        if form.is_valid():
            institution_id = form.cleaned_data['institution']
            institution_type = form.cleaned_data['institution_type']
            
            if institution_type == 'four_year_university':
                return redirect('edit_profile', university_profile_id=institution_id)
            elif institution_type == 'two_year_college':
                # Handle the case for two-year colleges if needed
                pass
        else:
            print(form.errors)  # Print form errors for debugging
    else:
        form = ExploreUniversitiesForm()
    
    return render(request, 'ntn_app/explore_universities.html', {'form': form})
# def explore_universities(request):
#     if request.method == 'POST':
#         form = ExploreUniversitiesForm(request.POST)
#         if form.is_valid():
#             institution_name = form.cleaned_data['institution']
#             institution_type = form.cleaned_data['institution_type']
#             institution_id = get_university_id(institution_name)
            
            
#             if institution_type == 'four_year_university':
#                 return redirect('/')
#             elif institution_type == 'two_year_college':
#                 college = get_object_or_404(CollegeProfile, college_name=institution_name)
#                 # Handle the case for two_year_college if needed
#                 pass
#     else:
#         form = ExploreUniversitiesForm()
#     return render(request, 'ntn_app/explore_universities.html', {'form': form})

def get_university_id(university_name):
    try:
        university = UniversityProfile.objects.get(university_name=university_name)
        return university.id
    except UniversityProfile.DoesNotExist:
        return None
 
def get_institutions(request):
    institution_type = request.GET.get('institution_type')
    if institution_type == 'four_year_university':
        institutions = UniversityProfile.objects.all().values('id', 'university_name')
    elif institution_type == 'two_year_college':
        institutions = CollegeProfile.objects.all().values('id', 'college_name')
    else:
        institutions = []
    
    return JsonResponse(list(institutions), safe=False)
# def student_landing(request):
#     return render(request, 'ntn_app/student_landing_page.html')

# def institution_landing(request):
#     return render(request, 'ntn_app/institution_landing_page.html')

# class UniversityViewSet(viewsets.ModelViewSet):
#     queryset =  University.objects.all()
#     print(str(queryset.query))
#     serializer_class = UniversitySerializer

# class CourseViewSet(viewsets.ModelViewSet):
#     queryset = Course.objects.all()
#     print(str(queryset.query))
#     serializer_class = CourseSerializer    

 
# class AgreementCourseListCreate(generics.ListCreateAPIView):
#     queryset = AgreementCourse.objects.all()
#     serializer_class = AgreementCourseSerializer

# class AgreementCourseDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = AgreementCourse.objects.all()
#     serializer_class = AgreementCourseSerializer

# @login_required
# def two_year_upload(request):
#     return render(request,'ntn_app/two_year_upload.html')

# def four_year_upload(request):
#     return render(request,'ntn_app/four_year_upload.html')

# def add_course(request):
#     return render(request, 'ntn_app/add_course.html')

# def logout_view(request):
#     logout(request)
#     return redirect(reverse('home'))

# def agreements(request):
#     return render(request,'ntn_app/agreement_detail.html')


# def inst_register_view(request):
#     if request.user.is_authenticated:
#         logout(request)
        
#     context = {}

#     if request.method == "GET":
#         context['form'] =  RegistrationForm()
#         return render(request, 'ntn_app/register.html', context)

#     # Creates a bound form from the request POST parameters and makes the 
#     # form available in the request context dictionary.
#     form = RegistrationForm(request.POST)
#     context['form'] = form

#     # Validates the form.
#     if not form.is_valid():
#         return render(request, 'ntn_app/register.html', context)


#     # # At this point, the form data is valid.  Register and login the user.
#     new_user = User.objects.create_user(
#         username=form.cleaned_data['email'],
#         password=form.cleaned_data['password1'],
#         email=form.cleaned_data['email'],
#         first_name=form.cleaned_data['name_of_contact_person']
#     )
#     new_user.save()

#     new_profile = Profile(
#         user = new_user,
#         name_of_institution = form.cleaned_data['name_of_institution'],
#         state = form.cleaned_data['state'],
#         website = form.cleaned_data['website'],
#         title = form.cleaned_data['title'],
#         phone = form.cleaned_data['phone'],
#     )

#     new_profile.save()

#     new_user = authenticate(username=form.cleaned_data['email'],
#                             password=form.cleaned_data['password1'])

#     login(request, new_user)
    
#     return redirect(reverse('institution_landing_page'))

# def login_view(request):
#     if request.user.is_authenticated:
#         return redirect(reverse('institution_landing_page'))

#     context = {}

#     # Just display the registration form if this is a GET request.
#     if request.method == 'GET':
#         context['form'] = LoginForm()
#         return render(request, 'ntn_app/login.html', context)

#     # Creates a bound form from the request POST parameters and makes the 
#     # form available in the request context dictionary.
#     form = LoginForm(request.POST)
#     context['form'] = form

#     # Validates the form.
#     if not form.is_valid():
#         context['message'] = 'wrong username or password'
#         return render(request, 'ntn_app/login.html', context)

#     new_user = authenticate(username=form.cleaned_data['username'],
#                             password=form.cleaned_data['password'])

#     login(request, new_user)
#     return redirect(reverse('institution_landing_page'))


# class ExcelUploadView(APIView):
#     print('called the excel upload function')
#     parser_classes = (MultiPartParser, FormParser,)

#     def post(self, request, *args, **kwargs):
#         file_serializer = ExcelFileSerializer(data=request.data)
#         if file_serializer.is_valid():
#             excel_file = request.FILES['file']
#             df = pd.read_excel(excel_file)

#             required_columns = [
#                 '2yearCollegeName', '2yearCollegeLocation', 'EffectiveTerm',
#                 'CC_Subject', 'Uni_Subject', 'Credits', '4yearCollegeName', '4yearCollegeLocation'
#             ]

#             # Check if all required columns are present
#             if not all(column in df.columns for column in required_columns):
#                 missing_columns = [column for column in required_columns if column not in df.columns]
#                 return Response({"error": f"Missing columns: {', '.join(missing_columns)}"}, status=400)

#             # Check if there is no data or all rows are empty
#             if df[required_columns].dropna(how='all').empty:
#                 return Response({"error": "Please add some data before uploading."}, status=400)

#             for index, row in df.iterrows():
#                 four_year_university, _ = University.objects.get_or_create(
#                     name=row['4yearCollegeName'],
#                     location=row['4yearCollegeLocation'],
#                     defaults={'university_type': 'FOUR_YEAR'}
#                 )
#                 two_year_university, _ = University.objects.get_or_create(
#                     name=row['2yearCollegeName'],
#                     location=row['2yearCollegeLocation'],
#                     defaults={'university_type': 'TWO_YEAR'}
#                 )
#                 #2 year course
#                 two_year_course = Course.objects.create(
#                     course_name=row['CC_Subject'],
#                     effective_term=row['EffectiveTerm'],
#                     credits=row['Credits'],
#                     university=four_year_university,
#                 )

#                 #4year course
#                 four_year_course = Course.objects.create(
#                     course_name=row['CC_Subject'],
#                     effective_term=row['EffectiveTerm'],
#                     credits=row['Credits'],
#                     university=two_year_university,
#                     equivalent_course=two_year_course
#                 )

#                 # Update the 2-year course to link back to the 4-year course
#                 two_year_course.equivalent_course = four_year_course
#                 two_year_course.save()
#             return Response({"message": "Data imported successfully"}, status=201)
#         else:
#             return Response(file_serializer.errors, status=400)

# class UploadDataView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = UploadDataSerializer(data=request.data)
#         if serializer.is_valid():
#             data = serializer.validated_data

#             twoYearInstitutionName = data['twoYearInstitutionName']
#             twoYearInstitutionLocation = data['twoYearInstitutionLocation']
#             effective_term = data['effectiveTerm']
#             cc_subject = data['ccSubject']
#             uni_subject = data['uniSubject']
#             credits = data['credits']
#             fourYearInstitutionName = data['fourYearInstitutionName']
#             fourYearInstitutionLocation = data['fourYearInstitutionLocation']

#             try:
#                 four_year_university, _ = University.objects.get_or_create(
#                     name=fourYearInstitutionName,
#                     location=fourYearInstitutionLocation,
#                     university_type='FOUR_YEAR'
#                 )
#                 two_year_university, _ = University.objects.get_or_create(
#                     name=twoYearInstitutionName,
#                     location=twoYearInstitutionLocation,
#                     university_type='TWO_YEAR'
#                 )

#                 # 2-year course
#                 two_year_course = Course.objects.create(
#                     course_name=cc_subject,
#                     effective_term=effective_term,
#                     credits=credits,
#                     university=two_year_university,
#                 )

#                 # 4-year course
#                 four_year_course = Course.objects.create(
#                     course_name=uni_subject,
#                     effective_term=effective_term,
#                     credits=credits,
#                     university=four_year_university,
#                     equivalent_course=two_year_course
#                 )

#                 # Update the 2-year course to link back to the 4-year course
#                 two_year_course.equivalent_course = four_year_course
#                 two_year_course.save()

#                 return Response({"message1": "Data uploaded successfully!"}, status=status.HTTP_201_CREATED)
#             except Exception as e:
#                 return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# from django.shortcuts import render, get_object_or_404, redirect
# from .models import ArticulationAgreement

# class AgreementListCreateAPIView(APIView):
#     def get(self, request, format=None):
#         agreements = ArticulationAgreement.objects.all()
#         serializer = ArticulationAgreementSerializer(agreements, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = ArticulationAgreementSerializer(data=request.data)
#         print(request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class AgreementDetailAPIView(APIView):
#     def get(self, request, pk, format=None):
#         agreement = get_object_or_404(ArticulationAgreement, pk=pk)
#         serializer = ArticulationAgreementSerializer(agreement)
#         return Response(serializer.data)

#     def patch(self, request, pk, format=None):
#         agreement = get_object_or_404(ArticulationAgreement, pk=pk)
#         serializer = ArticulationAgreementSerializer(agreement, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class AgreementPDFAPIView(APIView):
#     def get(self, request, pk, format=None):
#         agreement = get_object_or_404(ArticulationAgreement, pk=pk)
#         html_string = render_to_string('ntn_app/agreement_detail.html', {'agreement': agreement})
#         html = HTML(string=html_string)
#         pdf = html.write_pdf()

#         response = HttpResponse(pdf, content_type='application/pdf')
#         response['Content-Disposition'] = f'attachment; filename="agreement_{pk}.pdf"'
#         return response

# class AgreementPDFAPIView(APIView):
#     def get(self, request, pk, format=None):
#         try:
#             # Fetch the agreement using the primary key
#             agreement = get_object_or_404(ArticulationAgreement, pk=pk)
#             courses = agreement.courses.all()  # Fetch all related courses
            
#             # Generate the HTML content using a Django template
#             html_string = render_to_string(
#                 'ntn_app/agreement-pdf-details.html', 
#                 {'agreement': agreement, 'courses': courses}
#             )
#             # Create an HTML object with WeasyPrint
#             html = HTML(string=html_string)
            
#             # Generate the PDF from the HTML string
#             pdf = html.write_pdf()
            
#             # Prepare the HTTP response with the correct content-type
#             response = HttpResponse(pdf, content_type='application/pdf')
#             response['Content-Disposition'] = f'attachment; filename="agreement_{pk}.pdf"'
            
#             return response
#         except Exception as e:
#             # Log the error or print it
#             print(f"Error generating PDF: {str(e)}")
#             return HttpResponse("Error generating PDF", status=500)
