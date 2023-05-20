from account import Account

class Doctor(Account):
    def __init__(self, conn, email, doctor_id):
        super().__init__(conn, email)
        self.doctor_id = doctor_id
