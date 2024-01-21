from celery import shared_task
from django.core.mail import send_mass_mail
from django.conf import settings
from utils.time_utilities import TimeUtilities

from_mail_address = settings.EMAIL_HOST_USER
admins_mail_id = 'durganand.jha@habrie.com'
student_mail_subject = 'Welcome to Habrie'
student_mail_body = """Dear {},
You got enroll in Habrie School. Your Enrollment ID is {} let’s provide us the hard documents for the future references.

Team
Habrie School"""

admin_mail_subject = 'New Admission'
admin_mail_body = """Dear Admin,
You got new student {} enrolled in class {}, section {} with enrollment id {} this in {} session.

Bot Msg."""


def create_mass_mail_data_tuple(mail_dict_list):
    mail_list = []

    for mail_dict in mail_dict_list:
        mail_body = student_mail_body.format(mail_dict.get('name'),
                                             mail_dict.get('enrollment_id'))

        student_tuple = (student_mail_subject, mail_body, from_mail_address, [mail_dict.get('mail_id')])
        mail_list.append(student_tuple)

        mail_body = admin_mail_body.format(mail_dict.get('name'),
                                           mail_dict.get('class'),
                                           mail_dict.get('section'),
                                           mail_dict.get('enrollment_id'),
                                           TimeUtilities.convert_epoch_time_to_yyyy(TimeUtilities.current_time_in_sec()))
        admin_tuple = (admin_mail_subject, mail_body, from_mail_address, [admins_mail_id])
        mail_list.append(admin_tuple)

    return tuple(mail_list)


@shared_task
def send_email(mail_data_dict):
    mail_list = create_mass_mail_data_tuple(mail_data_dict)
    send_mass_mail(mail_list, fail_silently=False)
