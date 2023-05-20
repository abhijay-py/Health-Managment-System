from Databases.accounts_handler import change_password, change_email
from Databases.database_handler import create_connection

class Account():
    def __init__(self, email):
        self.conn = create_connection("hospital_data.db")
        self.email = email
    
    def change_account_password(self, new_password):
        password_change = change_password(self.conn, self.email, new_password)

        if password_change[0]:
            return "Your password was changed."
        
        elif not password_change[2]:
            return "Invalid password. Please ensure your password has a minimum of 8 characters, one capital letter, one number, and one symbol."

        elif not password_change[1]:
            return "ERROR INV-EM-PWCHG"

        return "ERROR INV-ST-PWCHG"
    
    def change_account_email(self, new_email):
        email_change = change_email(self.conn, self.email, new_email)

        if email_change[0]:
            self.email = new_email
            return "Your email was changed."

        elif email_change[2]:
            return "This email is already in use."

        elif not email_change[1]:
            return "ERROR INV-EM-EMCHG" 
        
        return "ERROR INV-ST-EMCHG"