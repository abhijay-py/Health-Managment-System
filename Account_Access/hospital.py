from account import Account

class Admin(Account):
    def __init__(self, conn, email, admin_id):
        super().__init__(conn, email)
        self.admin_id = admin_id
