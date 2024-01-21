# Student Enrollment System
 
### Key Features
 - Enrol a specific student by using enrolment form.
 - Admin can upload bulk student .csv file as well to enrol i.e. to save data in db.
 - Send mail to student who is enrolled and also to `Ambani@Ambanischool.com` (admin).
 - Admin can see the list of all students.
 - Admin can see the details of the student and also can upload specific docs like pdf and images corresponding to specific students.
 - 
### Assumptions
 - Each student should have unique enrolment ID and email.
 - No more than 999 users with same first 3 initial name letters can be registered in one day.
### Tech Used
 - Django
 - Django Rest Framework
 - Celery
 - SQL DB
 - HTML
 - CSS
 - Js
### DB Design
#### DB Tables
I have created 3 tables primarily
 - **Student**: This table contains all the personal details of students.
 - **Student Academic detail**: This table contains all academic related information for specific user. It has one to one mapping with *Student* schema.
 - **StudentAttachment**: This table contains all the attachments related info like their paths. It has many to one mapping with *Student* schema.
#### Data dictionary
##### Student
|Field name|Data type|
|--|--|
|id  |char(32), primary_key|
|name|varchar(100), not null|
|adhar_number|text, not null|
|dob|bigint, not null|
|identification_marks|text, not null|
|category|text, not null|
|height|text, not null|
|weight|text, not null|
|mail_id|varchar(255), unique, not null|
|contact_detail|text, not null|
|address|text, not null|
|fathers_name|varchar(100), null|
|fathers_qualification|text, null|
|fathers_profession|text, null|
|fathers_designation|text, null|
|fathers_adhar_card|text, null|
|fathers_mobile_no|integer, null|
|fathers_mail_id|text, null|
|mothers_name|varchar(100), null|
|mothers_qualification|text, null|
|mothers_profession|text, null|
|mothers_designation|text, null|
|mothers_adhar_card|text, null|
|mothers_mobile_no|integer, null|
|mothers_mail_id|text, null|
|created_at|bigint, not null|
|updated_at|bigint, not null|
##### Student Academic Detail
|Field name|Data type|
|--|--|
|id  |integer, primary_key, not null, autoincrement|
|enrollment_id|varchar(14), not null, unique|
|academic_class|varchar(100), not null|
|section|varchar(100), not null|
|doj|bigint, not null|
|created_at|bigint, not null|
|updated_at|bigint, not null|
##### Student documents
|Field name|Data type|
|--|--|
|id  |integer, primary_key, not null, autoincrement|
|student_id|char(32), null, references "student" ("id")|
|name|text, not null|
|doc_path|varchar(100), not null|
|created_at|bigint, not null|
|updated_at|bigint, not null|

### API Reference
- `/student/student` *POST*: This API will be used to enroll one student using data.
- `/student/student` *GET*: This API is used to fetches all students data.
- `/student/upload` *POST*: This API is used to upload documents for student like images, pdf and also used for bulk importing of student data.
- `/student/download_sample`:  Used to download sample .csv for bulk load student enrolment data.
### Get started
- Clone this repo.
- Initialise a virtualenv of python. Preferred python3.7
- Install requirements using the following command
  > pip install -t requirements.txt
- Run the server using
  > python manage.py runserver
- In another tab run `celery` using following command
  > celery -A habrie worker -l info

Now, app is up and running.
