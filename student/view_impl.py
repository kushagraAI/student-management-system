import json
import uuid
import csv
from celery import shared_task

from utils.response_utilities import ResponseUtilities
from utils.time_utilities import (TimeUtilities)
from rest_framework import status as status_codes
from .serializers import (StudentSerializer, AcademicDetailsSerializer)
from .models import (Student, AcademicDetails, StudentAttachments)
from .tasks import (send_email)


class StudentImpl:

    def __init__(self, student_enroll_id: str = None):
        self.student_enroll_id = student_enroll_id

    def get_student_enroll_id(self) -> str:
        return self.student_enroll_id

    @staticmethod
    def enroll_student(req_body: dict = None) -> dict:
        validate_req = StudentHelper.validate_enroll_student_request(req_body)

        if validate_req.get('error_message'):
            return ResponseUtilities.get_impl_error_context(validate_req.get('error_message'),
                                                            status_code=status_codes.HTTP_400_BAD_REQUEST)

        student_filter = validate_req.get('student_filter')

        if not student_filter:
            student_serializer = StudentSerializer(data=req_body, partial=True)

            if student_serializer.is_valid():
                student_serializer.save()

            else:
                return ResponseUtilities.get_impl_error_context(student_serializer.errors,
                                                                status_code=status_codes.HTTP_400_BAD_REQUEST)

            student_instance = student_serializer.instance

        else:
            student_instance = student_filter[0]

        academic_detail_req = {
            'enrollment_id': validate_req.get('enrollment_id'),
            'student': student_instance.id,
            'academic_class': req_body.get('academic_class'),
            'section': req_body.get('section'),
            'doj': TimeUtilities.current_time_in_sec(),
        }

        academic_serializer = AcademicDetailsSerializer(data=academic_detail_req, partial=True)

        if academic_serializer.is_valid():
            academic_serializer.save()

            mail_data_dict = [{
                'enrollment_id': academic_serializer.instance.enrollment_id,
                'name': academic_serializer.instance.student.name,
                'section': academic_serializer.instance.section,
                'class': academic_serializer.instance.academic_class,
                'mail_id': academic_serializer.instance.student.mail_id
            }]

            send_email.delay(mail_data_dict)

            return {'success': True}

        return ResponseUtilities.get_impl_error_context(academic_serializer.errors,
                                                        status_code=status_codes.HTTP_400_BAD_REQUEST)

    def fetch_student(self, page: int = None, page_size: int = None) -> dict:
        is_valid = False

        if self.get_student_enroll_id():
            try:
                uuid.UUID(self.get_student_enroll_id(), version=4)
                is_valid = True
            except:
                return ResponseUtilities.get_impl_error_context("Invalid enroll ID!",
                                                                status_code=status_codes.HTTP_400_BAD_REQUEST)

        if self.get_student_enroll_id() and is_valid:
            academic_details_filter = AcademicDetails.objects.filter(student__id=self.get_student_enroll_id())
            total_values = 1

        else:
            academic_details_filter = AcademicDetails.objects.all().order_by('id')
            total_values = academic_details_filter.count()

            if str(page).isdigit() and str(page_size).isdigit():
                page = int(page)
                page_size = int(page_size)
                lower_limit = (page - 1) * page_size
                upper_limit = page * page_size
                academic_details_filter = academic_details_filter[lower_limit: upper_limit]

        academic_serializer = AcademicDetailsSerializer(academic_details_filter, many=True).data
        return {'success': True, 'students_data': academic_serializer, 'total_results': total_values}

    def upload_file(self, file, is_bulk_upload: bool = False) -> dict:
        if not file:
            return ResponseUtilities.get_impl_error_context("Please send file to upload!",
                                                            status_code=status_codes.HTTP_400_BAD_REQUEST)
        student_instance = None

        if not is_bulk_upload:
            student_filter = Student.objects.filter(id=self.get_student_enroll_id())

            if not student_filter:
                return ResponseUtilities.get_impl_error_context("Invalid enroll ID!")

            student_instance = student_filter[0]

        attachment_instance = StudentAttachments.objects.create(student=student_instance, name=file.name, doc_path=file)

        if is_bulk_upload:
            validated_upload_dict = StudentHelper.validate_bulk_upload_students(attachment_instance.doc_path)

            if validated_upload_dict.get('error_message'):
                return ResponseUtilities.get_impl_error_context(validated_upload_dict.get('error_message'),
                                                                status_code=status_codes.HTTP_400_BAD_REQUEST)

            students_data_list = validated_upload_dict.get('students_data_list')
            StudentHelper.bulk_import_students.delay(students_data_list)

        return {'success': True}


class StudentHelper:

    @staticmethod
    def parse_enroll_student_request_body(req_body: dict):
        student_dob = '-'.join([req_body.get('dob_day'), req_body.get('dob_month'), req_body.get('dob_year')])
        req_body['dob'] = TimeUtilities.get_epoch_time_from_dd_mm_yyyy(student_dob)

        req_body['address'] = json.dumps({
            'address': req_body.get('address'),
            'city': req_body.get('city'),
            'state': req_body.get('state'),
            'pin_code': req_body.get('pin_code'),
            'country': req_body.get('country')
        })

        req_body['fathers_qualification'] = json.dumps({
            'class_xii': {
                'board': req_body.get('f_12_board'),
                'percentage': req_body.get('f_12_percentage'),
                'year_of_passing': req_body.get('f_12_yop')
            },
            'grad': {
                'board': req_body.get('f_g_board'),
                'percentage': req_body.get('f_g_percentage'),
                'year_of_passing': req_body.get('f_g_yop')
            },
            'masters': {
                'board': req_body.get('f_m_board'),
                'percentage': req_body.get('f_m_percentage'),
                'year_of_passing': req_body.get('f_m_yop')
            }
        })

        req_body['mothers_qualification'] = json.dumps({
            'class_xii': {
                'board': req_body.get('m_12_board'),
                'percentage': req_body.get('m_12_percentage'),
                'year_of_passing': req_body.get('m_12_yop')
            },
            'grad': {
                'board': req_body.get('m_g_board'),
                'percentage': req_body.get('m_g_percentage'),
                'year_of_passing': req_body.get('m_g_yop')
            },
            'masters': {
                'board': req_body.get('m_m_board'),
                'percentage': req_body.get('m_m_percentage'),
                'year_of_passing': req_body.get('m_m_yop')
            }
        })

    @staticmethod
    def generate_enrollment_id(req_body):
        enroll_id_filter = "".join([TimeUtilities.convert_epoch_time_to_ddmmyy(TimeUtilities.current_time_in_sec()),
                                    (req_body.get('name')[:3]).upper()])

        academic_filter = AcademicDetails.objects.filter(enrollment_id__icontains=enroll_id_filter).order_by('-id')

        student_seq = "001"
        is_done = True
        err_msg = ""

        if academic_filter:
            academic_filter = academic_filter.first()

            if academic_filter.enrollment_id:
                seq_number = academic_filter.enrollment_id[-3:]

                if seq_number.isdigit():
                    seq_number = int(seq_number) + 1

                    if seq_number < 10:
                        student_seq = "00" + str(seq_number)

                    elif seq_number < 100:
                        student_seq = "0" + str(seq_number)

                    elif seq_number < 1000:
                        student_seq = str(seq_number)

                    else:
                        is_done = False
                        err_msg = "More than 999 students cannot be enrolled in one day!"

        return "".join([TimeUtilities.convert_epoch_time_to_ddmmyy(TimeUtilities.current_time_in_sec()),
                        (req_body.get('name')[:3]).upper(), student_seq]), is_done, err_msg

    @staticmethod
    def validate_enroll_student_request(req_body: dict = None):
        if not req_body:
            return ResponseUtilities.get_inner_error_context('Invalid request body!')

        StudentHelper.parse_enroll_student_request_body(req_body)
        enrollment_id, is_success, err_msg = StudentHelper.generate_enrollment_id(req_body)

        if not is_success:
            return ResponseUtilities(err_msg)

        student_filter = Student.objects.filter(mail_id=req_body.get('mail_id'))

        if student_filter:
            academic_filter = AcademicDetails.objects.filter(student=student_filter[0])

            if academic_filter:
                return ResponseUtilities.get_inner_error_context('Student with similar mail ID already exists!')

        return {"enrollment_id": enrollment_id, 'student_filter': student_filter}

    @staticmethod
    def validate_bulk_upload_dict(student_data_list):
        is_valid = True
        error_message = ""
        mail_ids_list = []
        enrollment_ids_count_dict = {}

        for student_data in student_data_list:
            mail_ids_list.append(student_data.get('mail_id'))

            if len(student_data.get('name')) < 3:
                is_valid = False
                error_message = "Name of student should be greater than 3 characters!"
                break

            enrollment_key = "".join([TimeUtilities.convert_epoch_time_to_ddmmyy(TimeUtilities.current_time_in_sec()),
                                      (student_data.get('name')[:3]).upper()])

            if enrollment_key in enrollment_ids_count_dict:

                if enrollment_ids_count_dict.get(enrollment_key) >= 999:
                    is_valid = False
                    error_message = "Records with same first 3 characters reached 999 limit!"
                    break

            else:
                enrollment_id, is_done, err_msg = StudentHelper.generate_enrollment_id(
                    {'name': student_data.get('name')})

                if not is_done:
                    is_valid = False
                    error_message = err_msg
                    break

                enrollment_ids_count_dict[enrollment_key] = int(enrollment_id[-3:]) + 1

        if is_valid:
            student_filter = Student.objects.filter(mail_id__in=mail_ids_list)

            if student_filter:
                is_valid = False
                error_message = "Students with below email ids already exists!"

                for student_instance in student_filter:
                    error_message += "\n{}".format(student_instance.mail_id)

        return is_valid, error_message

    @staticmethod
    def validate_bulk_upload_students(filepath):
        students_data_list = []
        with open(filepath.path, mode='r') as infile:
            reader = csv.DictReader(infile)

            for row in reader:
                students_data_list.append(dict(row))

        is_valid, err_msg = StudentHelper.validate_bulk_upload_dict(students_data_list)

        if not is_valid:
            return ResponseUtilities.get_inner_error_context(err_msg)

        return {'students_data_list': students_data_list}

    @staticmethod
    @shared_task
    def bulk_import_students(student_data_list):
        mail_data_dict = []

        for student_data in student_data_list:
            validated_dict = StudentHelper.validate_enroll_student_request(student_data)

            if validated_dict.get('error_message'):
                print(validated_dict.get('error_message'))
                continue

            student_filter = validated_dict.get('student_filter')

            if not student_filter:
                student_serializer = StudentSerializer(data=student_data, partial=True)

                if student_serializer.is_valid():
                    student_serializer.save()

                else:
                    print(student_serializer.errors)
                    continue

                student_instance = student_serializer.instance

            else:
                student_instance = student_filter[0]

            academic_detail_req = {
                'enrollment_id': validated_dict.get('enrollment_id'),
                'student': student_instance.id,
                'academic_class': student_data.get('academic_class'),
                'section': student_data.get('section'),
                'doj': TimeUtilities.current_time_in_sec(),
            }

            academic_serializer = AcademicDetailsSerializer(data=academic_detail_req, partial=True)

            if academic_serializer.is_valid():
                academic_serializer.save()

                mail_data_dict.append({
                    'enrollment_id': academic_serializer.instance.enrollment_id,
                    'name': academic_serializer.instance.student.name,
                    'section': academic_serializer.instance.section,
                    'class': academic_serializer.instance.academic_class,
                    'mail_id': academic_serializer.instance.student.mail_id
                })

        send_email.delay(mail_data_dict)
