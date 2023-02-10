# <center>**Dentist clinic**</center>
## **Vision**
"Dentist clinic" is a web-application which allows administrator of a clinic to make an appointment to doctor for a patient.

Application should provide:  
* Display list of patients;
* Display information about patient (fields: full name, year of birthday, kind of ache (none, mild, middle, strong));
* Enable to create, read, update, delete patient;
* Enable to make an appointment to a doctor;
* If patient has an appointment, show doctor's specialty, full name and time of the appointment;


* Display list of doctors;
* Display information about doctor (fields: full name, seniority, specialty (therapist, orthopedist, surgeon, radiologist), amount of assigned pacients);
* Enable to create, read, update, delete doctor;
* Sorting list of appointments of patients by appointment time or by kind of ache (from hard to mild);
* Sorting doctors by their workload;
* Filtering doctors by their specialty;

## **1. Patients**

### **1.1 Display list of patients**
The mode is designed to view the list of patients. Enable to filter patients whom has an appointment and whom doesn't. Also, if it posible to display sorting list of patients by their full name, kind of ache or year of birth.  
***Main scenario***
* Administrator select item "Patient";
* Application displays list of Patients. 
