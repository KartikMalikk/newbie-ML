from django.urls import path, include
from students.admin import custom_admin_site  
from students.views import CustomLoginView, logout_view, home

urlpatterns = [
    path('admin/', custom_admin_site.urls),
    path('', home, name='home'),                  # Home page at /
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('api/', include('students.urls')),      # API routes at /api/
]
