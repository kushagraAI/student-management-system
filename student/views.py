import json
import os
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from .view_impl import StudentImpl
from utils.response_utilities import ResponseUtilities


class Student(APIView):
    """ inheriting API view class for using class based views in django """

    def post(self, request, *args, **kwargs):
        req_body = json.loads(request.body)

        student_impl = StudentImpl()
        student_data = student_impl.enroll_student(req_body)

        if 'error_message' in student_data:
            return JsonResponse(**ResponseUtilities.get_view_impl_error_context(student_data.get('error_message'),
                                                                                student_data.get('status')))

        return JsonResponse(student_data)

    def get(self, request, *args, **kwargs):
        params = request.query_params
        page = params.get('page')
        page_size = params.get('page_size')

        student_impl = StudentImpl(student_enroll_id=params.get('student_enroll_id'))
        student_data = student_impl.fetch_student(page=page, page_size=page_size)

        if 'error_message' in student_data:
            return JsonResponse(**ResponseUtilities.get_view_impl_error_context(student_data.get('error_message'),
                                                                                student_data.get('status')))

        return JsonResponse(student_data)


class UploadFiles(APIView):
    """ inheriting API view class for using class based views in django """
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        is_bulk_upload = request.query_params.get('is_bulk_upload')

        student_impl = StudentImpl(student_enroll_id=request.query_params.get('student_enroll_id'))
        student_data = student_impl.upload_file(file, is_bulk_upload)

        if 'error_message' in student_data:
            return JsonResponse(**ResponseUtilities.get_view_impl_error_context(student_data.get('error_message'),
                                                                                student_data.get('status')))

        return JsonResponse(student_data)


class DownloadFile(APIView):
    """ inheriting API view class for using class based views in django """

    def get(self, request, *args, **kwargs):
        filename = 'media/bulk_upload_sample.csv'

        with open(filename, "rb") as fprb:
            response = HttpResponse(fprb.read(), content_type="image/png")
            response['Content-Length'] = os.path.getsize(filename)
            response["Content-Disposition"] = "attachment; filename=bulk_upload_sample.csv"
            return response
