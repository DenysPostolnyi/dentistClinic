# Dentist clinic
Web application for dentist clinic. 
### Task: 
Dentist clinic wants to introduce a digital appointment to doctors. I need to develop a web application for them. Administrator should be able to register clients and appoint them to doctor therapist. In turn, the therapist should be able reassign patient to another doctor.
### Entity: 
  • Patient (fields: full name, year of birthday, kind of ache (none, little, middle, strong), time of appointment);  
  • Doctor (fields: full name, seniority, specialty (therapist, orthopedist, surgeon, radiologist), amount of assigned pacients);  
  
Relationship between entities: one to many (patient can be registered only to one doctor, but doctor can have many patients).

### Starting project:
Before starting project you must build it. 
1) Set env variables 'MYSQL_DATABASE=travis_db MYSQL_USER=root MYSQL_PORT=3306 MYSQL_HOST=127.0.0.1 DATABASE_URL=mysql://$MYSQL_USER:@$MYSQL_HOST:$MYSQL_PORT/$MYSQL_DATABASE'
2) Download useful packages by commands: 'pip install -r requirements.txt' and 'pip install mysqlclient'
3) Create new DB 'mysql -e 'CREATE DATABASE IF NOT EXISTS travis_db;''
4) Update DB with migrations 'flask --app=src/ db upgrade'
5) Start app with Gunicorn 'gunicorn wsgi:app -b 127.0.0.1:5000 -D'
!!! For finish program enter 'pkill gunicorn'

### Available URLs
1) Doctor
- Web service: http://127.0.0.1:5000/doctor-api
- Web application: http://127.0.0.1:5000/doctors
2) Patient
- Web service: http://127.0.0.1:5000/patient-api
- Web application: http://127.0.0.1:5000/patients
