from sql_handler import create_connection, insert_data, update_data, retrieve_data

#Returns patient_exists (bool)
def patient_exists(conn, patient_id):
    query = f"SELECT firstName FROM patients WHERE patientId = {patient_id};"
    data = retrieve_data(conn, query)
    return not bool(data)
    
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
def get_current_patient_info(conn, patient_id)()
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