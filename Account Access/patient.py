from account import Account
class Patient(Account):
    def __init__(self, email, patient_id):
        super().__init__(email)
        self.patient_id = patient_id





    