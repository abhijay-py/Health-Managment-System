#Menu System/Login System through main

from Account_Access.Databases.accounts_handler import login_attempt, create_account
from Account_Access.Databases.database_handler import create_connection
from Account_Access.patient import Patient
from Account_Access.doctor import Doctor
from Account_Access.hospital import Admin
from Account_Access.nurse import Nurse

def email_checker(email):
    pass

def login(conn):
    logged_in = False
    
    while not logged_in:
        email = input("Please enter your email: ")
        password = input("Please enter your password: ")

        if not email_checker(email):
            print("Please enter a valid email address.")
        
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

def new_account(conn):
    pass

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

def post_login_menu(account):
    account.menu()

def main():
    conn = create_connection("hospital_data.db")
    account = pre_login_menu(conn)
    post_login_menu(account)

if __name__ == "__main__":
    main()