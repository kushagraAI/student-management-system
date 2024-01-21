import json

from utils.time_utilities import TimeUtilities
from rest_framework import serializers
from .models import (Student, AcademicDetails)


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = "__all__"


class AcademicDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = AcademicDetails
        fields = "__all__"

    def to_representation(self, academic_detail):
        data = super(AcademicDetailsSerializer, self).to_representation(academic_detail)

        for key in ['id', 'created_at', 'updated_at']:
            del data[key]

        data = dict(**data, **StudentSerializer(academic_detail.student).data)

        for key in ['created_at', 'updated_at']:
            del data[key]

        # address = json.loads(data.get('address', {}))
        # data['address'] = ", ".join(address.values())
        # data['fathers_qualification'] = json.loads(data.get('fathers_qualification', {}))
        # data['mothers_qualification'] = json.loads(data.get('mothers_qualification', {}))

        for key in ['dob', 'doj']:
            data[key] = TimeUtilities.convert_epoch_time_to_ddmmyyyy(data[key])

        return data
