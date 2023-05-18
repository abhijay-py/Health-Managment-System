import sqlite3
from sqlite3 import Error

tableSQL = [ 
    """CREATE TABLE IF NOT EXISTS patients (
        patientID int PRIMARY KEY,
        lastName varchar(255) NOT NULL,
        firstName varchar(255) NOT NULL,
        birthday varchar(255) NOT NULL,
        hasInsurance int NOT NULL,
        insuranceProvider varchar(255),
        insuranceID int,
        priceDue decimal NOT NULL,
        primaryCareDocID int,
        prescriptions varchar(255),
        treatmentPlan varchar(255),
        doctorNotes varchar(255),
        testResults varchar(255),
        allergies varchar(255),
        vaccines varchar(255),
        medicalHistory varchar(255),
        room varchar(255)
    );
    """,
    """CREATE TABLE IF NOT EXISTS accounts (
        id varchar(255) PRIMARY KEY,
        accountType varchar(255) NOT NULL,
        email varchar(255) NOT NULL,
        username varchar(255) NOT NULL,
        password varchar(255) NOT NULL
    );
    """
]

tables = ["patients", "accounts"]

def create_connection(db_file):
    conn = None

    try:
        conn = sqlite3.connect(db_file)
        return conn

    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    try:
        curr = conn.cursor()
        curr.execute(create_table_sql)

    except Error as e:
        print(e)

def insert_data(conn, insert_data_sql, values):
    try:
        curr = conn.cursor()
        curr.execute(insert_data_sql, values)
        conn.commit()

    except Error as e:
        print(e)

def update_data(conn, update_data_sql):
    try:
        curr = conn.cursor()
        curr.execute(update_data_sql)
        conn.commit()

    except Error as e:
        print(e)

def retrieve_data(conn, retrieve_data_sql):
    try:
        curr = conn.cursor()
        curr.execute(retrieve_data_sql)
        return curr.fetchall()

    except Error as e:
        print(e)
        return None

def drop_table(conn, table):
    try:
        curr = conn.cursor()
        curr.execute(f"DROP TABLE {table};")
        conn.commit()

    except Error as e:
        print(e)
        return None

def database_initialization(db_file):
    conn = create_connection(db_file)
    for create_table_sql in tableSQL:
        create_table(conn, create_table_sql)
    conn.close()

def database_reset(conn):
    for table in tables:
        drop_table(conn, table)
    conn.close()
