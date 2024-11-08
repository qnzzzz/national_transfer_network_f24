from rest_framework.routers import DefaultRouter
# from .views import AgreementCourseDetail, AgreementCourseListCreate, AgreementDetailAPIView, AgreementListCreateAPIView, AgreementPDFAPIView, ExcelUploadView, UniversityViewSet, CourseViewSet, UploadDataView

from . import views
from django.urls import path, include


router = DefaultRouter()
# router.register(r'universities', UniversityViewSet)
# router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('', views.entry_page_view, name="home"),
    
    # institution api
    path('institution-landing-page/', views.institution_landing_page_view, name='institution_landing_page'),
    path('institution-register', views.institution_register, name="institution_register"),
    path('institution-login', views.institution_login, name="institution_login"),
    path("institution-logout", views.institution_logout, name="institution_logout"),
    path('university-profile/<int:university_profile_id>', views.edit_university_profile, name='university_profile_view'),
    path('university-profile/edit/<int:university_profile_id>', views.edit_university_profile, name='university_edit_profile'),
    path('college-profile/<int:college_profile_id>', views.edit_college_profile, name='college_profile_view'),
    path('college-profile/edit/<int:college_profile_id>', views.edit_college_profile, name='college_edit_profile'),
    path('university-profile/edit/<int:university_profile_id>', views.edit_university_profile, name='edit_profile'),
    path('new-agreement/', views.new_agreement, name='new_agreement'),
    path('manage-agreements', views.manage_agreements, name='manage_agreements'),
    path('all-agreements/<str:institution_type>/<int:profile_id>/', views.all_agreements, name='all_agreements'),
    path('delete_agreement/<int:agreement_id>', views.delete_agreement, name='delete_agreement'),

    # student api
    path('student-landing-page/', views.student_landing, name='student_landing_page'),
    path('student-register/', views.student_register, name="student_register"),
    path('student-login/', views.student_login, name="student_login"),
    path('add-course', views.add_course, name="add_course"),
    path('student-profile/', views.student_profile, name='student_profile'), 
    path("student-logout", views.logout_view, name="student_logout"),
    path('explore-universities/', views.explore_universities, name='explore_universities'),
    path('get-institutions/', views.get_institutions, name='get_institutions'),

    
    # path('two-year-upload/', views.two_year_upload, name='two_year_upload'),
    # path('four-year-upload/', views.four_year_upload, name='four_year_upload'),
    # # path('agreement/<int:pk>/', views.agreement_detail, name='agreement_detail'),
    # # path('agreement/<int:pk>/pdf/', views.agreement_pdf, name='agreement_pdf'),
    
    # # student api
    # path('student-landing-page/', views.student_landing, name='student_landing_page'),
    # path('student-register', views.inst_register_view, name="student_register"),
    # path('student-login', views.login_view, name="student_login"),
    # path('add-course', views.add_course, name="add_course"),
    
    
    # django built-in api
    path('api/', include(router.urls)),
    # path('api/upload_excel/', ExcelUploadView.as_view(), name='upload_excel'),
    # path('api/agreements/', AgreementListCreateAPIView.as_view(), name='agreement_list_create_api'),
    # path('api/agreements/<int:pk>/', AgreementDetailAPIView.as_view(), name='agreement_detail_api'),
    # path('api/agreements/pdf/<int:pk>/', AgreementPDFAPIView.as_view(), name='agreement_pdf_api'),
    # path('agreement-courses/', AgreementCourseListCreate.as_view(), name='agreement_course_list_create'),
    # path('agreement-courses/<int:pk>/', AgreementCourseDetail.as_view(), name='agreement_course_detail'),
    # path('upload-data/', UploadDataView.as_view(), name='upload_data'),
]