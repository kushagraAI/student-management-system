import uuid
from utils.time_utilities import TimeUtilities

from django.db import models


def get_uuid():
    return uuid.uuid4()


class Student(models.Model):
    # Student info
    id = models.UUIDField(primary_key=True, default=get_uuid)
    name = models.CharField(max_length=100)
    adhar_number = models.TextField()
    dob = models.BigIntegerField(default=0)
    identification_marks = models.TextField(null=True)
    category = models.TextField()
    height = models.TextField()
    weight = models.TextField()
    mail_id = models.CharField(max_length=255, unique=True)
    contact_detail = models.TextField()
    address = models.TextField()

    # Father details
    fathers_name = models.CharField(max_length=100, null=True)
    fathers_qualification = models.TextField(null=True)
    fathers_profession = models.TextField(null=True)
    fathers_designation = models.TextField(null=True)
    fathers_adhar_card = models.TextField(null=True)
    fathers_mobile_no = models.IntegerField(null=True)
    fathers_mail_id = models.TextField(null=True)

    # Mother details
    mothers_name = models.CharField(max_length=100, null=True)
    mothers_qualification = models.TextField(null=True)
    mothers_profession = models.TextField(null=True)
    mothers_designation = models.TextField(null=True)
    mothers_adhar_card = models.TextField(null=True)
    mothers_mobile_no = models.IntegerField(null=True)
    mothers_mail_id = models.TextField(null=True)

    # DB entry creation meta info
    created_at = models.BigIntegerField(default=0)
    updated_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'student'

    def save(self, *args, **kwargs):
        current_time = TimeUtilities.current_time_in_sec()

        if self.created_at == 0:
            self.created_at = current_time

        self.updated_at = current_time

        super(Student, self).save(*args, **kwargs)


class AcademicDetails(models.Model):
    # Student academic details
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    enrollment_id = models.CharField(max_length=14, unique=True)
    academic_class = models.CharField(max_length=100)
    section = models.CharField(max_length=100)
    doj = models.BigIntegerField(default=0)

    # DB entry creation meta info
    created_at = models.BigIntegerField(default=0)
    updated_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'student_academic_details'

    def save(self, *args, **kwargs):
        current_time = TimeUtilities.current_time_in_sec()

        if self.created_at == 0:
            self.created_at = current_time

        self.updated_at = current_time

        super(AcademicDetails, self).save(*args, **kwargs)


class StudentAttachments(models.Model):
    # Student documents details
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    name = models.TextField()
    doc_path = models.FileField(upload_to='documents')

    # DB entry creation meta info
    created_at = models.BigIntegerField(default=0)
    updated_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'student_documents'

    def save(self, *args, **kwargs):
        current_time = TimeUtilities.current_time_in_sec()

        if self.created_at == 0:
            self.created_at = current_time

        self.updated_at = current_time

        super(StudentAttachments, self).save(*args, **kwargs)
