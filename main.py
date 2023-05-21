#Modify login, new_account, pre_login_menu, and indivdual class menus after MVP is achieved.
#Also modify how error states are handled.

from Account_Access.Databases.accounts_handler import login_attempt, create_account
from Account_Access.Databases.database_handler import create_connection, database_initialization
from Account_Access.patient import Patient
from Account_Access.doctor import Doctor
from Account_Access.hospital import Admin
from Account_Access.nurse import Nurse
from getpass import getpass

#Returns logged_in_acc (Account)
#Keeps asking for login info until you're logged in
def login(conn):
    logged_in = False
    
    while not logged_in:
        email = input("Please enter your email: ")
        password = getpass("Please enter your password: ")
        
        account_exists, login_success, public_id  = login_attempt(conn, email, password)

        if not account_exists:
            print("There is no account with this email.")

        elif not login_success:
            print("Invalid Password.")

        else:
            logged_in = True

    id = public_id[1:]
    account_type = public_id[0]

    if account_type == "P":
        return Patient(conn, email, id)

    elif account_type == "D":
        return Doctor(conn, email, id)
    
    elif account_type == "N":
        return Nurse(conn, email, id)

    else:
        return Admin(conn, email, id)

#TODO: Implement
#Returns new_acc (Account)
#Keeps asking for new account info until you created a new account
def new_account(conn):
    pass

#Returns logged_in_acc (Account)
#The menu that is displayed before the user is logged in
def pre_login_menu(conn):
    logged_in = False

    while not logged_in:
        choice = input("Login/Create an Account (L/C): ")

        if choice.upper() != "L" and choice.upper() != "C":
            print("Please enter a valid choice.") 

        elif choice.upper() == "L":
            return login(conn)
        
        elif choice.upper() == "C":
            return new_account(conn)

#The menu that is displayed after the user is logged in
def post_login_menu(account):
    account.menu()

def main():
    db_file = "hospital_data.db"
    conn = create_connection(db_file)
    database_initialization(db_file)
    account = pre_login_menu(conn)
    post_login_menu(account)

if __name__ == "__main__":
    main()