# <center>**Dentist clinic**</center>
## **Vision**
"Dentist clinic" is a web-application which allows administrator of a clinic to make an appointment to doctor for a patient.

Application should provide:  
* Display list of patients;
* Display information about patient (fields: full name, year of birth, kind of ache (none, mild, middle, strong), phone number, email);
* Enable to create, read, update, delete patient;
* Enable to make an appointment to a doctor;
* If patient has an appointment, show doctor's specialty, full name and time of the appointment;
* Display list of doctors;
* Display information about doctor (fields: full name, seniority, specialty (therapist, orthopedist, surgeon, radiologist), amount of assigned pacients, phone number, email);
* Enable to create, read, update, delete doctor;
* Sorting list of appointments of patients by appointment time or by kind of ache (from hard to mild);
* Sorting doctors by their workload;
* Filtering doctors by their specialty;

## **1. Patients**

### **1.1 Display list of patients**
The mode is designed to view the list of patients. Enable to filter patients whom has an appointment and whom doesn't. Also, if it's possible to display sorting list of patients by their full name, kind of ache or year of birth.  

***Main scenario***
* Administrator selects item "Patients";
* Application displays list of Patients;

![img.png](img.png)  
Pic. 1.1 View the Patients list  

The list displays patients' full name and year of birth.

***Sorting and filtering:***
* Administrator selects kind of sorting (by kind of ache, by full name or by year of birth);
* Selects, he needs list of appointed patients or don't (default both);
* Press button "Submit";
* Application shows filtered and sorted list of patients.

### **1.2 Display info about patient**
The mode is designed to view information about patient. Enable to make or cancel an appointment, edit information about patient or delete him.  

***Main scenario***
* Administrator clicks button "Open" on the page with list of patients on in the selected patient line;
* Application opens page with information about selected patient;
* If administrator click on doctor, application change page to page with information about this doctor.  

***Cancel scenario:***
* Administrator clicks button "Cancel";
* Application cancel appointment, remove information about it and add button to make an appointment.

***Back scenario:***
* Administrator clicks button "Back" on the page with information about patient;
* Application opens page with patients list.

![img_1.png](img_1.png)  
Pic. 1.2 Page with info about appointed patient

![img_4.png](img_4.png)  
Pic. 1.3 Page with info about isn't appointed patient

Page displays information about patient: 
* Full name - unique full name(first name and last name) of patient; 
* Year - year of patient's birth;
* Kind fo ache - how hard is patient's ache;
* Email - unique patient's email;
* Phone number - unique patient's phone number;
* If the patient is appointed, show doctor and date of appointment.  

### **1.3 Making appointment**
The mode is designed to making an appointment of person.

***Main scenario***
* Administrator clicks button "Make an appointment";
* Application opens the modal window for making an appointment;
* Administrator selects kind of doctor specialty, date of appointment and then chooses doctor (application shows doctors who have less than 7 clients in chosen day and sorting doctors by amount of clients in this day);
* After pressing button "Make", application creates an appointment to chosen doctor;

***Close scenario:***
* Administrator clicks button "Close";
* Application close modal window, opens page with info about patient without making an appointment.

![img_3.png](img_3.png)  
Pic. 1.4 Modal window for making an appointment

### **1.4 Edit patient**
The mode is designed to edit patient's personal information.

***Main scenario***
* Administrator clicks button "Edit" on the page with patient's information;
* Application opens page for editing;
* Administrator changes information and presses “Save” button;
* If any data is entered incorrectly, incorrect data messages are displayed;
* If entered data is valid, then record is adding to database;
* If error occurs, then error message is displaying;
* If changed patient's information is successfully added, then page with information of person is displaying.

***Cancel scenario:***
* Administrator clicks the “Edit” button in the patient information view mode;
* Application opens page for editing;
* Administrator presses “Cancel” button;
* Entered data don’t save in Data Base, then page with edit information of person is displaying.  

![img_2.png](img_2.png)
Pic. 1.5 Edit page  

When editing a patient's information, the following details are entered:
* Full name – patient’s first and last name;
* Email - patient's email;
* Phone number - patient's phone number;
* Kind of ache – how hard is patient's ache;
* Year of birth - patient's year of birth.

Constraints for data validation:
* Full name – maximum length of 90 characters, format First name Last name;
* Email - email standards;
* Phone number - begins on +380 and has 13 symbols;
* Year of birth - not less than 1930.

### **1.5 Add new patient**
The mode is designed to add new patient.

***Main scenario***
* Administrator clicks button "Add" on the page with list of patients;
* Application opens page for enter new patient's information;
* Administrator enters information and presses “Save” button;
* If any data is entered incorrectly, incorrect data messages are displayed;
* If entered data is valid, then record is adding to database;
* If error occurs, then error message is displaying;
* If new patient record is successfully added, then page with information of new patient is displaying.

***Cancel scenario:***
* Administrator clicks the “Add” button in the page with list of patients;
* Application opens page for creating new patient;
* Administrator presses “Cancel” button;
* Entered data don’t save in Data Base, then page with list of patients is displaying.    

![img_5.png](img_5.png)
Pic. 1.6 Creating new patient page

When editing a patient's information, the following details are entered:
* Full name – patient’s first and last name;
* Email - patient's email;
* Phone number - patient's phone number;
* Kind of ache – how hard is patient's ache;
* Year of birth - patient's year of birth.

Constraints for data validation:
* Full name – maximum length of 90 characters, format First name Last name;
* Email - email standards;
* Phone number - begins on +380 and has 13 symbols;
* Year of birth - not less than 1930.

### **1.6 Delete patient**
The mode is designed to delete a selected patient.

***Main scenario:***
* Administrator presses the "Delete" button in the selected order line on the page with list of patients or on the page with information about definite patient;
* If the patient can be removed, a confirmation dialog window is displayed;
* Administrator confirms the deleting of the patient;
* Record is deleted from database;
* If error occurs, then error message displays;
* If patient record is successfully deleted, then list of patients without deleted records is displaying.

***Cancel operation scenario:***
* Administrator presses the "Delete" button;
* Application displays confirmation dialog window “Please confirm delete patient?”;
* User press “Cancel” button;
* List of patients without changes is displaying. 

![img_6.png](img_6.png)
Pic. 1.7 Deleting patient dialog window

## **2. Doctors**

### **2.1 Display list of Doctors**
The mode is designed to view the list of doctors. Enable to filter doctors by their specialty. Also, if it's possible to display sorting list of doctors by their full name, seniority, amount of appointed clients.  

***Main scenario***
* Administrator selects item "Doctors";
* Application displays list of Doctors;

![img_10.png](img_10.png)!
Pic. 2.1 View the Doctors list  

The list displays doctors' full name and specialty.

***Sorting and filtering:***
* Administrator selects kind of sorting (by their full name, seniority, amount of appointed clients);
* Selects which specialty doctors are need (therapist, orthopedist, surgeon, radiologist);
* Press button "Submit";
* Application shows filtered and sorted list of doctors.

### **2.2 Display info about doctor**
The mode is designed to view information about doctor. Enable to open appointed patient, edit information about doctor or delete him.  

***Main scenario***
* Administrator clicks button "Open" on the page with list of doctors on in the selected doctor line;
* Application opens page with information about selected doctor;
* If administrator click on patient, application change page to page with information about this patient.  

***Back scenario:***
* Administrator clicks button "Back" on the page with information about doctor;
* Application opens page with doctors list.

**Choosing date scenario:**
* Administrator clicks "Choose date";
* Opens calendar form;
* Administrator choose wished date;
* Applications show list of patients appointed to this doctor in chosen day;

![img_8.png](img_8.png)
Pic. 2.2 Page with info about appointed doctor

Page displays information about doctor: 
* Full name - unique full name(first name and last name) of doctor; 
* Specialty - what doctor's specialty (therapist, orthopedist, surgeon, radiologist);
* Seniority - doctor's seniority;
* Email - unique doctor's email;
* Phone number - unique doctor's phone number;
* List and amount of appointed patients to this doctor (all or in chosen day);

### **2.3 Edit doctor**
The mode is designed to edit doctor's personal information.

***Main scenario***
* Administrator clicks button "Edit" on the page with doctor's information;
* Application opens page for editing;
* Administrator changes information and presses “Save” button;
* If any data is entered incorrectly, incorrect data messages are displayed;
* If entered data is valid, then record is adding to database;
* If error occurs, then error message is displaying;
* If changed doctor's information is successfully added, then page with information of doctor is displaying.

***Cancel scenario:***
* Administrator clicks the “Edit” button in the doctor information view mode;
* Application opens page for editing;
* Administrator presses “Cancel” button;
* Entered data don’t save in Data Base, then page with edit information of doctor is displaying.  

![img_7.png](img_7.png)
Pic. 2.3 Edit page  

When editing a doctor's information, the following details are entered:
* Full name – doctor’s first and last name;
* Specialty - what doctor's specialty (therapist, orthopedist, surgeon, radiologist);
* Seniority - doctor's seniority;
* Email - doctor's email;
* Phone number - doctor's phone number;

Constraints for data validation:
* Full name – maximum length of 90 characters, format First name Last name;
* Email - email standards;
* Phone number - begins on +380 and has 13 symbols;

### **2.4 Add new doctor**
The mode is designed to add new doctor.

***Main scenario***
* Administrator clicks button "Add" on the page with list of doctors;
* Application opens page for enter new doctor's information;
* Administrator enters information and presses “Save” button;
* If any data is entered incorrectly, incorrect data messages are displayed;
* If entered data is valid, then record is adding to database;
* If error occurs, then error message is displaying;
* If new doctor record is successfully added, then page with information of new doctor is displaying.

***Cancel scenario:***
* Administrator clicks the “Add” button in the page with list of doctors;
* Application opens page for creating new doctor;
* Administrator presses “Cancel” button;
* Entered data don’t save in Data Base, then page with list of doctors is displaying.    

![img_9.png](img_9.png)  
Pic. 2.4 Creating new doctor page

When editing a patient's information, the following details are entered:
* Full name – doctor’s first and last name;
* Specialty - what doctor's specialty (therapist, orthopedist, surgeon, radiologist);
* Seniority - doctor's seniority;
* Email - doctor's email;
* Phone number - doctor's phone number;  

Constraints for data validation:
* Full name – maximum length of 90 characters, format First name Last name;
* Email - email standards;
* Phone number - begins on +380 and has 13 symbols;

### **2.5 Delete doctor**
The mode is designed to delete a selected doctor.

***Main scenario:***
* Administrator presses the "Delete" button in the selected order line on the page with list of doctors or on the page with information about definite doctor;
* If the doctor can be removed, a confirmation dialog window is displayed;
* Administrator confirms the deleting of the doctor;
* Record is deleted from database;
* If error occurs, then error message displays;
* If doctor record is successfully deleted, then list of doctors without deleted records is displaying.

***Cancel operation scenario:***
* Administrator presses the "Delete" button;
* Application displays confirmation dialog window “Please confirm delete doctor?”;
* User press “Cancel” button;
* List of doctors without changes is displaying. 

![img_11.png](img_11.png)
Pic. 2.5 Deleting doctor dialog window