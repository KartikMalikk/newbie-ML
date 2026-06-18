from rest_framework import viewsets
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from django.http import HttpResponse
from .models import Student
from .serializers import StudentSerializer
from .ml import train_and_predict
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

def home(request):
    return render(request, 'students/home.html')


@login_required
def student_list(request):
    students = Student.objects.all()
    return render(request, 'students/student_list.html', {'students': students})


@login_required
def upload_page(request):
    return render(request, 'students/upload.html')

from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('/')   # or redirect('home') if you have name="home"

class CustomLoginView(LoginView):
    template_name = 'login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/api/')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return '/api/'



class StudentViewSet(viewsets.ModelViewSet):
    queryset=Student.objects.all()
    serializer_class = StudentSerializer

class UploadExcelFile(View):

    def get(self, request):
        # Render HTML page
        return render(request, 'students/upload.html')
    
    def post(self, request):
        file = request.FILES.get('file')


        # file validation
        if not file:
            return Response(
                {"error" : "No File Uploaded"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not file.name.lower().endswith(('.xls', '.xlsx', '.csv')):
            return Response(
                {'error' : 'Only Excel (.xls or .xslx) or CSV (.csv) files are allowed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        
        try:
            # read file (csv or excel)
            if file.name.lower().endswith('.csv'):
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)
        
            required_columns = {
                "name",
                "gender",
                "hours_studied",
                "attendance",
                "previous_score",
                "marks"
            }

            # Validate columns
            missing_columns = required_columns - set(df.columns)
            if missing_columns:
                return Response(
                    {
                        'error' : 'invalid file format',
                        "missing_columns" : list(missing_columns)
                    },
                    status=status.HTTP_400_BAD_REQUEST
                    )
            

            # Handle Empty Dataframe
            if df.empty:
                return Response(
                    {
                        "error" : "Uploaded file cotains no data"
                    },status=status.HTTP_400_BAD_REQUEST
                )
            
            def to_scalar(value):
                if hasattr(value, 'item'):
                    return value.item()
                return value
            


            Students = []
            # save data to db
            for _,row in df.iterrows():

                Students.append(
                    Student(
                        name = str(row["name"]).strip(),
                        gender = str(row["gender"]).strip(),
                        hours_studied = float(to_scalar(row["hours_studied"])),
                        attendance = float(to_scalar(row["attendance"])),
                        previous_score = float(to_scalar(row["previous_score"])),
                        marks = None if pd.isna(row['marks']) else float(to_scalar(row['marks']))

                    )
                )
            
            Student.objects.bulk_create(Students)

            # ML Training and prediction
            train_and_predict()

            return redirect('student_list')
            
        except pd.errors.EmptyDataError:
            return Response(
                {"error": "Uploaded file is empty"},
                status= status.HTTP_400_BAD_REQUEST
            )
        except ValueError as e:
            return Response(
                {"error": "Invalid datatype in file",
                 "details":str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            # Catch-all (DB / ML / unknown errors)
            return Response(
                {
                    "error":"Something went wrong while processing the file",
                    "details" : str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
