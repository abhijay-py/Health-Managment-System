import sqlite3
from sqlite3 import Error

#Create Table SQLS
tableSQL = [ 
    """CREATE TABLE IF NOT EXISTS patients (
        patientID int PRIMARY KEY,
        lastName varchar(255) NOT NULL,
        firstName varchar(255) NOT NULL,
        birthday varchar(255) NOT NULL,
        hasInsurance int NOT NULL,
        insuranceProvider varchar(255),
        insuranceID int,
        billID int NOT NULL,
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
        email varchar(255) PRIMARY KEY,
        publicID varchar(255) NOT NULL,
        password varchar(255) NOT NULL
    );
    """,
    """CREATE TABLE IF NOT EXISTS meetings (
        meetingID int PRIMARY KEY,
        meetingName varchar(255) NOT NULL,
        meetingDesc varchar(255),
        oneOnOne int NOT NULL,
        priPersonID varchar(255) NOT NULL,
        secPersonID varchar(255) NOT NULL,
        othPeopleIDS varchar(255),
        meetingDT varchar(255) NOT NULL,
        room varchar(255) NOT NULL
    );
    """
]

#Table Names
tables = ["patients", "accounts"]

#Create a connection to a specific db_file and return the connection.
def create_connection(db_file):
    conn = None

    try:
        conn = sqlite3.connect(db_file)
        return conn

    except Error as e:
        print(e)

    return conn

#Close the connection.
def close_connection(conn):
    try:
        conn.close()

    except Error as e:
        print(e)

#Create a new SQL table.
def create_table(conn, create_table_sql):
    try:
        curr = conn.cursor()
        curr.execute(create_table_sql)

    except Error as e:
        print(e)

#Insert new entries into the db.
def insert_data(conn, insert_data_sql, values):
    try:
        curr = conn.cursor()
        curr.execute(insert_data_sql, values)
        conn.commit()

    except Error as e:
        print(e)

#Update previous entries into the db.
def update_data(conn, update_data_sql):
    try:
        curr = conn.cursor()
        curr.execute(update_data_sql)
        conn.commit()

    except Error as e:
        print(e)

#Query the db for data.
def retrieve_data(conn, retrieve_data_sql):
    try:
        curr = conn.cursor()
        curr.execute(retrieve_data_sql)
        return curr.fetchall()

    except Error as e:
        print(e)
        return None

#Drop a specific table from the db.
def drop_table(conn, table):
    try:
        curr = conn.cursor()
        curr.execute(f"DROP TABLE {table};")
        conn.commit()

    except Error as e:
        print(e)
        return None

#Create all tables if not created already in a specific db.
def database_initialization(db_file):
    conn = create_connection(db_file)
    for create_table_sql in tableSQL:
        create_table(conn, create_table_sql)
    close_connection(conn)

#Drop all tables from the db to reset the db.
def database_reset(conn):
    for table in tables:
        drop_table(conn, table)
    close_connection(conn)
 