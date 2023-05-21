#ENSURE EMAIL IS VALID (NO CHECKS HERE)

from Account_Access.Databases.database_handler import insert_data, update_data, retrieve_data
import re

#HELPER FUNCTIONS

#Returns whether an account exists with the provided email (bool)
def account_exists(conn, email):
    query = f"SELECT email FROM accounts WHERE email = {email};"
    data = retrieve_data(conn, query)
    return not bool(data)

#Returns whether a password is valid. 
#No white space, at least one caps, at least 8 letters, at least 1 number and 1 symbol.
def valid_password(password):
    if len(password) < 8:
        return False
    elif not re.search("[A-Z]", password):
        return False
    elif not re.search("[0-9]", password):
        return False
    elif not re.search("[~`!@#\$%\^&\*\(\)_-\+=\{\}\[\]\|:;\"'\?/>\.<,]", password) and "\\" not in password:
        return False
    elif re.search("\s", password):
        return False
    
    return True 

#Returns whether an email is valid.
def valid_email(email):
    regex = "[A-Za-z0-9\+-~_]+@[A-Za-z0-9\+-~_]+\.[A-Z|a-z]{2,7}"
    return re.fullmatch(regex, email)

#Returns whether the login attempt was sucessful (bool)
def login_success(conn, email, password):
    query = f"SELECT password FROM accounts WHERE email = {email};"
    data = retrieve_data(conn, query)[0][0]
    return data == password

#USED FUNCTIONS

#Return (account_exists (bool), email (str))
#Email will return None if account does not exist.
def get_email(conn, public_id):
    query = f"SELECT email FROM accounts WHERE publicID = {public_id};"
    data = retrieve_data(conn, query)

    account_exists = not bool(data)
    
    if not account_exists:
        return (account_exists, None)

    return (account_exists, data[0][0])

#Returns (account_exists (bool), login_success (bool), public_id (str))
#Last tuple will be empty if login fails or account doesn't exist.
def login_attempt(conn, email, password):
    account_exists = account_exists(conn, email)
    
    if not account_exists:
        return (account_exists, False, ())

    login_status = login_success(conn, email, password)

    if not login_status:
        return (account_exists, login_status, ())

    query = f"SELECT publicID FROM accounts WHERE email = {email};"
    data = retrieve_data(conn, query)[0][0]

    return (account_exists, login_status, data)

#Returns (account_created (bool), account_exists (bool), id_exists (bool), valid_acc_type (bool), valid_email (bool), valid_password (bool))
#Last three booleans may return None if previous checks fail first. If account_created is true, all are true.
def create_account(conn, email, password, id, accountType):
    account_types = ['P', 'D', 'N', 'A']

    account_exists = account_exists(conn, email)
    
    if not account_exists:
        return (False, account_exists, None, None, None, None)

    public_id = accountType + str(id)
    query = f"SELECT publicID FROM accounts WHERE publicID = {public_id};"
    data = retrieve_data(conn, query)
    
    id_exists = bool(data)

    if not id_exists:
        return (False, account_exists, id_exists, None, None, None)

    valid_acc_type = accountType in account_types

    if not valid_acc_type:
        return (False, account_exists, id_exists, valid_acc_type, None, None)
    
    email_is_valid = valid_email(password)

    if not email_is_valid:
        return (False, account_exists, id_exists, valid_acc_type, email_is_valid, None)

    password_is_valid = valid_password(password)

    if not password_is_valid:
        return (False, account_exists, id_exists, valid_acc_type, email_is_valid, password_is_valid)

    query = "INSERT INTO accounts (email, id, accountType, password) VALUES (?, ?, ?, ?);"
    values = (email, public_id, accountType, password)
    insert_data(conn, query, values)

    return (True, account_exists, id_exists, valid_acc_type, email_is_valid, password_is_valid)

#Return (password_resetted (bool), account_exists (bool), valid_password (bool))
#Last boolean may return None if previous checks fail first. If password_resetted is true, all are true.
def change_password(conn, email, password):
    account_exists = account_exists(conn, email)
    
    if not account_exists:
        return (False, account_exists, None)
    
    password_is_valid = valid_password(password)

    if not password_is_valid:
        return (False, account_exists, password_is_valid)

    query = f"UPDATE accounts SET password = {password} WHERE email = {email};"
    update_data(conn, query)
    
    return (True, account_exists, password_is_valid)

#Return (email_changed (bool), account_exists (bool), email_is_used (bool), email_is_valid (bool))
def change_email(conn, old_email, new_email):
    account_exists = account_exists(conn, old_email)
    email_is_used = account_exists(conn, new_email)
    email_is_valid = valid_email(new_email)

    if not account_exists or email_is_used or not email_is_valid:
        return (False, account_exists, email_is_used, email_is_valid)

    query = f"UPDATE accounts SET email = {new_email} WHERE email = {old_email};"
    update_data(conn, query)
    
    return (True, account_exists, email_is_used, email_is_valid)

#Returns account_deleted (bool)
#Deletes an account based on email provided. If false, account does not exist.
def delete_account(conn, email):
    account_exists = account_exists(conn, email)
    
    if not account_exists:
        return False

    query = f"DELETE FROM accounts WHERE email = {email};"
    update_data(conn, query)
    
    return True