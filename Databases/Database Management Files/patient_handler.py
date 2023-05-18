from sql_handler import insert_data, update_data, retrieve_data
from bill_handler import new_bill

#TODO: ADD MODIFYING FUNCTIONS TO MODIFY EXISTING PATIENTS

#Returns patient_exists (bool)
def patient_exists(conn, patient_id):
    query = f"SELECT firstName FROM patients WHERE patientId = {patient_id};"
    data = retrieve_data(conn, query)
    return not bool(data)
    
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
    
    query = f"SELECT hasInsurance, insuranceProvider, insuranceID FROM patients WHERE patientID = {patient_id};"
    data = retrieve_data(conn, query)[0]

    new_data = [hasInsurance, insuranceProvider, insurance_id]

    

    if hasInsurance is not None and not hasInsurance:
        new_data = [int(hasInsurance), None, None]

    elif hasInsurance is None and data[0] == 0:
        return (False, patient_exists)
    
    elif hasInsurance and data[0] == 0 and insuranceProvider is None and insurance_id is None:
        return (False, patient_exists)

    else:
        if hasInsurance is not None:
            int(hasInsurance)

        for i in range(len(new_data)):
            if new_data[i] is None:
                new_data[i] = data[i]

    query = f"""UPDATE patients SET hasInsurance = {new_data[0]}, insuranceProvider = {new_data[1]}, 
                insuranceID = {new_data[2]} WHERE patientID = {patient_id};"""
    update_data(conn, query)

    return (True, patient_exists)
    
#ENSURE THIS PATIENT IS NEW + BIRTHDAY IS VALID (no checks)
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
