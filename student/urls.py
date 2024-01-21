from django.urls import path
from django.views.generic import (TemplateView)
from .views import (Student, UploadFiles, DownloadFile)

urlpatterns = [
    path('', TemplateView.as_view(template_name='student_enroll_form.html')),
    path('404', TemplateView.as_view(template_name='404page.html')),
    path('list_students', TemplateView.as_view(template_name='list_students.html')),
    path('student', Student.as_view(), name="student"),
    path('student/<str:student_id>', TemplateView.as_view(template_name='student_info.html')),
    path('upload', UploadFiles.as_view(), name="upload_files"),
    path('download_sample', DownloadFile.as_view(), name="download_sample")
]
