""" 
CHANGE STATUSES 
    UPDATE - add on to previous entries
    REPLACE - replaces previous entries
    DELETE - deletes specific data in each column 
    WIPE - removes all data from the specific colummns for the patient
"""

from sql_handler import insert_data, update_data, retrieve_data
from bill_handler import new_bill

#TODO: ADD MODIFYING FUNCTIONS TO MODIFY EXISTING PATIENTS
#TODO: Modify basic info?

#HELPER FUNCTIONS

#Returns patient_exists (bool)
def patient_exists(conn, patient_id):
    query = f"SELECT firstName FROM patients WHERE patientId = {patient_id};"
    data = retrieve_data(conn, query)
    return not bool(data)

#Returns modified_history (bool)
#Adds on to previous medical history with a new line.
def update_medical_history(conn, patient_id, allergies, vaccines, testResults, medicalHistory):
    data = get_medical_history_info(conn, patient_id)[1]

    new_data = [allergies, vaccines, testResults, medicalHistory]

    for i in range(len(new_data)):
        if new_data[i] is None:
            new_data[i] = data[i]
        elif data[i] is not None:
            new_data[i] = data[i] + '\n' + new_data[i]

    query = f"""UPDATE patients SET allergies = {new_data[0]}, vaccines = {new_data[1]}, 
                testResults = {new_data[2]}, medicalHistory = {new_data[3]} WHERE patientID = {patient_id};"""
    update_data(conn, query)

    return True

#Returns modified_history (bool)
#Replaces previous medical history entries.
def replace_medical_history(conn, patient_id, allergies, vaccines, testResults, medicalHistory):
    data = get_medical_history_info(conn, patient_id)[1]

    new_data = [allergies, vaccines, testResults, medicalHistory]

    for i in range(len(new_data)):
        if new_data[i] is None:
            new_data[i] = data[i]

    query = f"""UPDATE patients SET allergies = {new_data[0]}, vaccines = {new_data[1]}, 
                testResults = {new_data[2]}, medicalHistory = {new_data[3]} WHERE patientID = {patient_id};"""
    update_data(conn, query)

    return True

#Returns modified_history (bool)
#Removes previous medical history entries.
def delete_medical_history(conn, patient_id, allergies, vaccines, testResults, medicalHistory):
    data = get_medical_history_info(conn, patient_id)[1]
    data = [i.split('\n') for i in data if i is not None]
    
    del_data = [allergies, vaccines, testResults, medicalHistory]

    for i in range(len(del_data)):
        if del_data[i] is not None:
            if data[i] is None or del_data[i] not in data[i]:
                return False
            
            data[i].remove(del_data[i])

            if len(data[i]) == 0:
                data[i] = None

    data = [i.join('\n') for i in data if i is not None]

    query = f"""UPDATE patients SET allergies = {data[0]}, vaccines = {data[1]}, 
                testResults = {data[2]}, medicalHistory = {data[3]} WHERE patientID = {patient_id};"""
    update_data(conn, query)

    return True

#Returns modified_info (bool)
#Adds on to previous current info with a new line.
def update_current_info(conn, patient_id, prescriptions, treatmentPlan, doctorNotes):
    data = get_medical_history_info(conn, patient_id)[1]

    new_data = [prescriptions, treatmentPlan, doctorNotes]

    for i in range(len(new_data)):
        if new_data[i] is None:
            new_data[i] = data[i]
        elif data[i] is not None:
            new_data[i] = data[i] + '\n' + new_data[i]

    query = f"""UPDATE patients SET prescriptions = {new_data[0]}, treatmentPlan = {new_data[1]}, 
                doctorNotes = {new_data[2]} WHERE patientID = {patient_id};"""
    update_data(conn, query)

    return True

#Returns modified_info (bool)
#Replaces previous current info entries.
def replace_current_info(conn, patient_id, prescriptions, treatmentPlan, doctorNotes):
    data = get_current_patient_info(conn, patient_id)[1]

    new_data = [prescriptions, treatmentPlan, doctorNotes]

    for i in range(len(new_data)):
        if new_data[i] is None:
            new_data[i] = data[i]

    query = f"""UPDATE patients SET prescriptions = {new_data[0]}, treatmentPlan = {new_data[1]}, 
                doctorNotes = {new_data[2]} WHERE patientID = {patient_id};"""
    update_data(conn, query)

    return True

#Returns modified_info (bool)
#Removes previous current info entries.
def delete_current_info(conn, patient_id, prescriptions, treatmentPlan, doctorNotes):
    data = get_medical_history_info(conn, patient_id)[1]
    data = [i.split('\n') for i in data if i is not None]
    
    del_data = [prescriptions, treatmentPlan, doctorNotes]

    for i in range(len(del_data)):
        if del_data[i] is not None:
            if data[i] is None or del_data[i] not in data[i]:
                return False
            
            data[i].remove(del_data[i])

            if len(data[i]) == 0:
                data[i] = None

    data = [i.join('\n') for i in data if i is not None]

    query = f"""UPDATE patients SET prescriptions = {del_data[0]}, treatmentPlan = {del_data[1]}, 
                doctorNotes = {del_data[2]} WHERE patientID = {patient_id};"""
    update_data(conn, query)

    return True

#USED FUNCTIONS

#Returns (valid_name (bool), patient_info (list of tuples of (id, birthday)))
#List will be empty if name doesn't exist or is invalid.
def search_patient(conn, fullName):
    names = fullName.split()
    valid_name = len(names) < 2

    if not valid_name:
        return (valid_name, [])
    
    firstName = ' '.join(names[:-1])
    lastName = names[-1]   

    query = f"SELECT patientID, birthday FROM patients WHERE firstName = {firstName} AND lastName = {lastName};"
    data = retrieve_data(conn, query)
    
    return (valid_name, data) 

#Returns (patient_exists (bool), (firstName (str), lastName (str), birthday (str, mm/dd/yyyy))) 
#Last tuple will be empty if patient doesn't exist.
def get_basic_info(conn, patient_id):
    patient_exists = patient_exists(conn, patient_id)
    
    if not patient_exists:
        return (patient_exists, ())

    query = f"SELECT firstName, lastName, birthday FROM patients WHERE patientID = {patient_id};"
    data = retrieve_data(conn, query)[0]
    
    return (patient_exists, data)

#Returns (patient_exists (bool), (hasInsurance (bool), insuranceProvider (str), insuranceID (int))) 
#Last tuple will be empty if patient doesn't exist.
def get_insurance_info(conn, patient_id):
    patient_exists = patient_exists(conn, patient_id)

    if not patient_exists:
        return (patient_exists, ())

    query = f"SELECT hasInsurance, insuranceProvider, insuranceID FROM patients WHERE patientID = {patient_id};"
    data = retrieve_data(conn, query)[0]

    if int(data[0]) == 1:
        data = (True, data[1], data[2])
    else:
        data[0] = (False, data[1], data[2])

    return (patient_exists, data)

#Returns (patient_exists (bool), (allergies (str), vaccines (str), testResults (str), medicalHistory (str))) 
#Last tuple will be empty if patient doesn't exist.
def get_medical_history_info(conn, patient_id):
    patient_exists = patient_exists(conn, patient_id)

    if not patient_exists:
        return (patient_exists, ())

    query = f"SELECT allergies, vaccines, testResults, medicalHistory FROM patients WHERE patientID = {patient_id};"
    data = retrieve_data(conn, query)[0]

    return (patient_exists, data)

#Returns (patient_exists (bool), (primaryCareDocID (int), prescriptions (str), treatmentPlan (str), doctorNotes (str), room (str))) 
#Last tuple will be empty if patient doesn't exist.
def get_current_patient_info(conn, patient_id):
    patient_exists = patient_exists(conn, patient_id)

    if not patient_exists:
        return (patient_exists, ())

    query = f"SELECT primaryCareDocID, prescriptions, treatmentPlan, doctorNotes, room FROM patients WHERE patientID = {patient_id};"
    data = retrieve_data(conn, query)[0]

    return (patient_exists, data)

#Returns (patient_exists (bool), billID (int))
#billID will be None if patient doesn't exist.
def get_bill_id(conn, patient_id):
    patient_exists = patient_exists(conn, patient_id)

    if not patient_exists:
        return (patient_exists, None)

    query = f"SELECT billID FROM patients WHERE patientID = {patient_id};"
    data = retrieve_data(conn, query)[0][0]

    return (patient_exists, data)

#Ensure hasInsurance matches with whether or not you input insurance data or you'll keep getting False for modified_insurance
#Returns (modified_insurance (bool), patient_exists (bool))
#While all vars are default None, they will take the values in the DB.
def modify_insurance(conn, patient_id:int, hasInsurance:bool = None, insuranceProvider:str = None, insurance_id:int = None):
    patient_exists = patient_exists(conn, patient_id)

    if not patient_exists or (hasInsurance is None and insuranceProvider is None and insurance_id is None):
        return (False, patient_exists)
    
    data = get_insurance_info(conn, patient_id)[1]

    new_data = [hasInsurance, insuranceProvider, insurance_id]

    if hasInsurance is not None and not hasInsurance:
        new_data = [int(hasInsurance), None, None]

    elif hasInsurance is None and not data[0]:
        return (False, patient_exists)
    
    elif hasInsurance and not data[0] and insuranceProvider is None and insurance_id is None:
        return (False, patient_exists)

    else:
        if hasInsurance is not None:
            int(hasInsurance)

        for i in range(len(new_data)):
            if new_data[i] is None:
                if i == 0:
                    new_data[i] = int(data[i])
                else:
                    new_data[i] = data[i]

    query = f"""UPDATE patients SET hasInsurance = {new_data[0]}, insuranceProvider = {new_data[1]}, 
                insuranceID = {new_data[2]} WHERE patientID = {patient_id};"""
    update_data(conn, query)

    return (True, patient_exists)

#Returns (modified_history (bool), patient_exists(bool), valid_status (bool))
#If empty strings are not passed with replace status, the db entries will not be removed.
#Last bool will be empty if patient doesn't exist
def modify_medical_history(conn, patient_id:int, changeStatus:str = "update", allergies:str = None, 
                           vaccines:str = None,  testResults:str = None, medicalHistory:str = None):
    patient_exists = patient_exists(conn, patient_id)

    if not patient_exists:
        return (False, patient_exists, None)

    valid_status = changeStatus == "update" or changeStatus == "replace" or changeStatus == "delete" or changeStatus == "wipe"
    allNone = allergies is None and vaccines is None and testResults is None and medicalHistory is None
    
    if not valid_status or allNone and changeStatus != "wipe" or not allNone and changeStatus == "wipe":
        return (False, patient_exists, valid_status)
    
    if changeStatus == "update":
        return (update_medical_history(conn, patient_id, allergies, vaccines, testResults, medicalHistory), valid_status)

    elif changeStatus == "replace":
        return (replace_medical_history(conn, patient_id, allergies, vaccines, testResults, medicalHistory), valid_status)
    
    elif changeStatus == "delete":
        return (delete_medical_history(conn, patient_id, allergies, vaccines, testResults, medicalHistory), valid_status)
    
    else:
        return (replace_medical_history(conn, "", "", "", "", ""))

#ENSURE DOCTOR_ID IS VALID (no checks)
#Returns (changed_doctor(bool), patient_exists (bool))
def change_doctor(conn, patient_id, doctor_id:int = None):
    patient_exists = patient_exists(conn, patient_id)

    if not patient_exists:
        return (False, patient_exists)
    
    query = f"UPDATE patients SET primaryCareDocID = {doctor_id} WHERE patientID = {patient_id};"
    update_data(conn, query)
    
    return (True, patient_exists)

#ENSURE ROOM IS VALID (no checks)
#Returns (changed_room(bool), patient_exists (bool))
def change_room(conn, patient_id, room:str = None):
    patient_exists = patient_exists(conn, patient_id)

    if not patient_exists:
        return (False, patient_exists)
    
    query = f"UPDATE patients SET room = {room} WHERE patientID = {patient_id};"
    update_data(conn, query)
    
    return (True, patient_exists)

#Returns (modified_info (bool), patient_exists(bool), valid_status (bool))
#If empty strings are not passed with replace status, the db entries will not be removed.
#Last bool will be empty if patient doesn't exist
def modify_current_info(conn, patient_id:int, changeStatus:str = "update", prescriptions:str = None, 
                        treatmentPlan:str = None, doctorNotes:str = None):
    patient_exists = patient_exists(conn, patient_id)

    if not patient_exists:
        return (False, patient_exists, None)

    valid_status = changeStatus == "update" or changeStatus == "replace" or changeStatus == "delete" or changeStatus == "wipe"
    allNone = prescriptions is None and treatmentPlan is None and doctorNotes is None
    
    if not valid_status or allNone and changeStatus != "wipe" or not allNone and changeStatus == "wipe":
        return (False, patient_exists, valid_status)
    
    if changeStatus == "update":
        return (update_current_info(conn, patient_id, prescriptions, treatmentPlan, doctorNotes), valid_status)

    elif changeStatus == "replace":
        return (replace_current_info(conn, patient_id, prescriptions, treatmentPlan, doctorNotes), valid_status)
    
    elif changeStatus == "delete":
        return (delete_current_info(conn, patient_id, prescriptions, treatmentPlan, doctorNotes), valid_status)
    
    else:
        return (replace_current_info(conn, "", "", "", "", ""))

#ENSURE THIS PATIENT IS NEW + BIRTHDAY + ROOM + DOCTOR IS VALID (no checks).
#Returns (patient_id (int), valid_name (bool))
#If valid name, patient_id will not be None.
def new_patient(conn, fullName:str, birthday:str, hasInsurance:bool, insuranceProvider:str = None, insurance_id:int = None, 
                doctor_id:int = None, prescriptions:str = None, treatmentPlan:str = None, doctorNotes:str = None, 
                testResults:str = None, allergies:str = None, vaccines:str = None, medicalHistory:str = None, room:str = None):
    names = fullName.split()
    valid_name = len(names) < 2

    if not valid_name:
        return (None, valid_name)
    
    firstName = ' '.join(names[:-1])
    lastName = names[-1]    
    
    hasInsuranceInt = int(hasInsurance)

    bill_id = -1

    query = """INSERT INTO patients (firstName, lastName, hasInsurance, billID, insuranceProvider, insuranceID,
                                        primaryCareDocID, prescriptions, treatmentPlan, doctorNotes, testResults, 
                                        allergies, vaccines, medicalHistory, room) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
    values = (firstName, lastName, hasInsuranceInt, bill_id, insuranceProvider, insurance_id, doctor_id, prescriptions,
              treatmentPlan, doctorNotes, testResults, allergies, vaccines, medicalHistory, room)
    insert_data(conn, query, values)

    query = "SELECT patientID FROM patients WHERE billID = -1;"
    patient_id = retrieve_data(conn, query)[0][0]

    bill_id = new_bill(conn, patient_id)

    query = f"UPDATE patients SET billID = {bill_id} WHERE patientID = {patient_id};"
    update_data(conn, query)

    return (patient_id, valid_name)

#Returns patient_removed (bool)
#Deletes an patient based on id provided. If false, patient does not exist.  
def remove_patient(conn, patient_id):
    patient_exists = patient_exists(conn, patient_id)

    if not patient_id:
        return False

    query = f"DELETE FROM patients WHERE patientID = {patient_id};"
    update_data(conn, query)
    
    return True
