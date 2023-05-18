from sql_handler import create_connection, insert_data, update_data, retrieve_data

#Returns whether an account exists with the provided email (bool)
def account_exists(conn, email):
    query = f"SELECT email FROM accounts WHERE email = {email};"
    data = retrieve_data(conn, query)
    return not bool(data)

#Returns whether the login attempt was sucessful (bool)
def login_success(conn, email, password):
    query = f"SELECT password FROM accounts WHERE email = {email};"
    data = retrieve_data(conn, query)[0][0]
    return data == password

#Return (account_exists (bool), email (str))
#Email will return None if account does not exist.
def get_email(conn, id, accountType):
    query = f"SELECT email FROM accounts WHERE id = {id} AND accountType = {accountType};"
    data = retrieve_data(conn, query)

    account_exists = not bool(data)
    
    if not account_exists:
        return (account_exists, None)

    return (account_exists, data[0][0])

#Returns (account_exists (bool), login_success (bool), (id (int), account_type (str, 'P'/'D'/'N'/'H')))
#Last tuple will be empty if login fails or account doesn't exist.
def login_attempt(conn, email, password):
    account_exists = account_exists(conn, email)
    
    if not account_exists:
        return (account_exists, False, ())

    login_status = login_success(conn, email, password)

    if not login_status:
        return (account_exists, login_status, ())

    query = f"SELECT id, accountType FROM accounts WHERE email = {email};"
    data = retrieve_data(conn, query)[0]

    return (account_exists, login_status, data)

#Returns (account_created (bool), account_exists (bool), id_exists (bool), invalid_acc_type (bool))
#Last two booleans may return None if previous checks fail first. If account_created is true, all are true.
def create_account(conn, email, password, id, accountType):
    account_types = ['P', 'D', 'N', 'H']

    account_exists = account_exists(conn, email)
    
    if not account_exists:
        return (False, account_exists, None, None)

    query = f"SELECT id FROM accounts WHERE id = {id};"
    data = retrieve_data(conn, query)
    
    id_exists = bool(data)

    if not id_exists:
        return (False, account_exists, id_exists, None)

    valid_acc_type = accountType in account_types

    if not valid_acc_type:
        return (False, account_exists, id_exists, valid_acc_type)

    query = f"INSERT INTO accounts (email, id, accountType, password) VALUES (?, ?, ?, ?);"
    values = (email, id, accountType, password)
    insert_data(conn, query, values)

    return (True, account_exists, id_exists, valid_acc_type)

#Returns account_deleted (bool)
#Deletes an account based on email provided. If false, account does not exist.
def delete_account(conn, email):
    account_exists = account_exists(conn, email)
    
    if not account_exists:
        return False

    query = f"DELETE FROM accounts WHERE email = {email};"
    update_data(conn, query)
    
    return True