from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, UploadExcelFile, upload_page
from .api_root import api_root  # import your new root view
from students import views

router = DefaultRouter()
router.register(r'students', StudentViewSet)

urlpatterns = [
    path("", api_root),  # use custom api root here to show upload endpoint too
    path("upload/", upload_page, name="upload"),  # optional HTML upload form
    path("", include(router.urls)),               # /students/ API endpoints
    path("upload-file/", UploadExcelFile.as_view(), name="api-upload"),  # file upload API
    path('api/students/', views.student_list, name='student_list'),
]
