from django.contrib.admin import AdminSite
from django.shortcuts import redirect
from .models import Student


class CustomAdminSite(AdminSite):
    site_header = "EduPredict Admin"
    site_title = "EduPredict Admin"

    def index(self, request, extra_context=None):
        if request.user.is_authenticated:
            return redirect('/api/upload-file/')
        return super().index(request, extra_context)

    def login(self, request, extra_context=None):
        response = super().login(request, extra_context)
        if request.user.is_authenticated:
            return redirect('/api/upload-file/')
        return response


# ✅ THIS NAME MUST MATCH urls.py
custom_admin_site = CustomAdminSite(name='custom_admin')

custom_admin_site.register(Student)
