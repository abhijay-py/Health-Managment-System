from account import Account

class Nurse(Account):
    def __init__(self, conn, email, nurse_id):
        super().__init__(conn, email)
        self.nurse_id = nurse_id
