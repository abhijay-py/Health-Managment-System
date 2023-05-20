#Menu System/Login System through main

from Account_Access.Databases.accounts_handler import login_attempt, create_account
from Account_Access.patient import Patient

def pre_login_menu():
    input("Please enter your email: ")

def post_login_menu(account):
    account.menu()

def main():
    account = pre_login_menu()
    post_login_menu(account)

if __name__ == "__main__":
    main()