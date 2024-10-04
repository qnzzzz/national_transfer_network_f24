from rest_framework.routers import DefaultRouter
from .views import AgreementCourseDetail, AgreementCourseListCreate, AgreementDetailAPIView, AgreementListCreateAPIView, AgreementPDFAPIView, ExcelUploadView, UniversityViewSet, CourseViewSet, UploadDataView, TwoYearUpload, FourYearUpload

from . import views
from django.urls import path, include



router = DefaultRouter()
router.register(r'universities', UniversityViewSet)
router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/upload_excel/', ExcelUploadView.as_view(), name='upload_excel'),
     path('upload-data/', UploadDataView.as_view(), name='upload_data'),
    path('two_year_upload/', views.TwoYearUpload, name='upload-two-years'),
    path('four_year_upload/', views.FourYearUpload, name='upload-four-years'),
    path('add_course', views.add_course, name="add-course"),
    path('login_institution', views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path('institution_sign_up', views.inst_register_view, name="institution-register"),
    path('', views.entry_page_view, name="entry"),
    path('agreement/', views.agreements, name='agreement'),
    path('api/agreements/', AgreementListCreateAPIView.as_view(), name='agreement_list_create_api'),
    path('api/agreements/<int:pk>/', AgreementDetailAPIView.as_view(), name='agreement_detail_api'),
    path('api/agreements/pdf/<int:pk>/', AgreementPDFAPIView.as_view(), name='agreement_pdf_api'),
    path('agreement-courses/', AgreementCourseListCreate.as_view(), name='agreement-course-list-create'),
    path('agreement-courses/<int:pk>/', AgreementCourseDetail.as_view(), name='agreement-course-detail'),
    path('student-landing-page/', views.student_landing, name='student_landing_page'),
    path('institution-landing-page/', views.institution_landing, name='institution_landing_page'),
    # path('agreement/<int:pk>/', views.agreement_detail, name='agreement_detail'),
    # path('agreement/<int:pk>/pdf/', views.agreement_pdf, name='agreement_pdf'),
]