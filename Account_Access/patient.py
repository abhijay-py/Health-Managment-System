from account import Account

class Patient(Account):
    def __init__(self, conn, email, patient_id):
        super().__init__(conn, email)
        self.patient_id = patient_id
