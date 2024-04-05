import mysql.connector
import glob
import json
import csv
from io import StringIO
import itertools
import hashlib
import os
import cryptography
from cryptography.fernet import Fernet
from math import pow

class database:

    def __init__(self, purge = False):

        # Grab information from the configuration file
        self.database       = 'db'
        self.host           = '127.0.0.1'
        self.user           = 'master'
        self.port           = 3306
        self.password       = 'master'
        self.tables         = ['institutions', 'positions', 'experiences', 'skills','feedback', 'users']
        
        # NEW IN HW 3-----------------------------------------------------------------
        self.encryption     =  {   'oneway': {'salt' : b'averysaltysailortookalongwalkoffashortbridge',
                                                 'n' : int(pow(2,5)),
                                                 'r' : 9,
                                                 'p' : 1
                                             },
                                'reversible': { 'key' : '7pK_fnSKIjZKuv_Gwc--sZEMKn2zc8VvD6zS96XcNHE='}
                                }
        #-----------------------------------------------------------------------------

    def query(self, query = "SELECT * FROM users", parameters = None):

        cnx = mysql.connector.connect(host     = self.host,
                                      user     = self.user,
                                      password = self.password,
                                      port     = self.port,
                                      database = self.database,
                                      charset  = 'latin1'
                                     )


        if parameters is not None:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query, parameters)
        else:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query)

        # Fetch one result
        row = cur.fetchall()
        cnx.commit()

        if "INSERT" in query:
            cur.execute("SELECT LAST_INSERT_ID()")
            row = cur.fetchall()
            cnx.commit()
        cur.close()
        cnx.close()
        return row

    def createTables(self, purge=False, data_path = 'flask_app/database/'):
        """
        Creates tables and populates them with initial data.
        This method reads SQL files to create tables and CSV files to populate them.

        Args:
            purge (bool): If True, existing tables will be dropped before creation.
            data_path (str): The base directory path for SQL creation scripts and initial data.
        """
        if purge:
            # Drop tables in reverse dependency order
            drop_order = ['skills', 'experiences', 'positions', 'institutions', 'feedback', 'users']
            for table in drop_order:
                drop_query = f"DROP TABLE IF EXISTS `{table}`"
                self.query(drop_query)

        # Explicit order to respect dependencies
        sql_files_order = ['institutions.sql', 'positions.sql', 'experiences.sql', 'skills.sql', 'feedback.sql','users.sql']

        # Create Tables from SQL Files
        for sql_filename in sql_files_order:
            sql_file_path = os.path.join(data_path, 'create_tables', sql_filename)
            if os.path.exists(sql_file_path):
                with open(sql_file_path, 'r') as file:
                    sql_command = file.read()
                    try:
                        self.query(sql_command)
                        print(f"Successfully created table from {sql_filename}")
                    except Exception as e:
                        print(f"Failed to create table from {sql_filename}: {e}")
            else:
                print(f"SQL file {sql_filename} not found.")

        # Populate Tables with Initial Data from CSV Files
        initial_data_order = ['institutions.csv', 'positions.csv', 'experiences.csv', 'skills.csv']
        for csv_filename in initial_data_order:
            csv_file_path = os.path.join(data_path, 'initial_data', csv_filename)
            if os.path.exists(csv_file_path):
                table_name = os.path.splitext(csv_filename)[0]
                with open(csv_file_path, mode='r') as file:
                    csv_reader = csv.reader(file)
                    columns = next(csv_reader)
                    for row in csv_reader:
                        placeholders = ', '.join(['%s'] * len(row))
                        insert_query = f"INSERT INTO `{table_name}` ({', '.join(columns)}) VALUES ({placeholders})"
                        try:
                            self.query(insert_query, row)
                            print(f"Successfully inserted data into {table_name}")
                        except Exception as e:
                            print(f"Failed to insert data into {table_name}: {e}")
            else:
                print(f"CSV file {csv_filename} not found.")

    def insertRows(self, table='table', columns=['x','y'], parameters=[['v11','v12'],['v21','v22']]):
        """
        Inserts rows into the specified table.

        Args:
            table (str): The name of the table into which data will be inserted.
            columns (list): A list of column names for the table.
            parameters (list of lists): A list where each sub-list represents the values to be inserted into one row.
        """
        # Construct the base of the INSERT query
        columns_str = ', '.join(columns)  # Convert the list of columns into a comma-separated string
        placeholders_str = ', '.join(['%s' for _ in columns])  # Create a string of placeholders for the values
        insert_query = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders_str})"
        
        # Connect to the database
        cnx = mysql.connector.connect(host=self.host, user=self.user, password=self.password, port=self.port, database=self.database)
        cursor = cnx.cursor()
        
        # Execute the INSERT query for each set of parameters
        for param in parameters:
            cursor.execute(insert_query, param)
        
        # Commit the transactions and close the connection
        cnx.commit()
        cursor.close()
        cnx.close()


    def getResumeData(self):
        """
        Fetches and organizes data from the institutions, positions, experiences, and skills tables
        into a nested dictionary structure.

        Returns:
            A nested dictionary representing the hierarchical structure of the resume data.
        """
        resume_data = {}

        # Step 1: Fetch all institutions
        institutions = self.query("SELECT * FROM institutions")
        for institution in institutions:
            inst_id = institution['inst_id']
            # Initialize institution entry in resume_data
            resume_data[inst_id] = {
                'address': institution['address'],
                'city': institution['city'],
                'state': institution['state'],  
                'type': institution['type'],  
                'zip': institution.get('zip', 'NULL'), 
                'department': institution['department'],
                'name': institution['name'],
                'positions': {}
            }

            # Step 2: Fetch positions related to the current institution
            positions = self.query("SELECT * FROM positions WHERE inst_id = %s", [inst_id])
            for position in positions:
                pos_id = position['position_id']
                resume_data[inst_id]['positions'][pos_id] = {
                    'end_date': position['end_date'],
                    'responsibilities': position['responsibilities'],
                    'start_date': position['start_date'],
                    'title': position['title'],
                    'experiences': {}
                }

                # Step 3: Fetch experiences related to the current position
                experiences = self.query("SELECT * FROM experiences WHERE position_id = %s", [pos_id])
                for experience in experiences:
                    exp_id = experience['experience_id']
                    resume_data[inst_id]['positions'][pos_id]['experiences'][exp_id] = {
                        'description': experience['description'],
                        'end_date': experience['end_date'],
                        'hyperlink': experience['hyperlink'],
                        'name': experience['name'],
                        'skills': {},
                        'start_date': experience['start_date']
                    }

                    # Step 4: Fetch skills related to the current experience
                    skills = self.query("SELECT * FROM skills WHERE experience_id = %s", [exp_id])
                    for skill in skills:
                        skill_id = skill['skill_id']
                        resume_data[inst_id]['positions'][pos_id]['experiences'][exp_id]['skills'][skill_id] = {
                            'name': skill['name'],
                            'skill_level': skill['skill_level']
                        }

        return resume_data

#######################################################################################
# AUTHENTICATION RELATED
#######################################################################################
    def createUser(self, email='me@email.com', password='password', role='user'):
        # Check if user already exists
        existing_user_query = "SELECT * FROM users WHERE email = %s"
        existing_users = self.query(existing_user_query, [email])
        if existing_users:
            return {'success': 0, 'error': 'User already exists'}

        # Encrypt the password
        encrypted_password = self.onewayEncrypt(password)

        # Insert new user into the database
        insert_query = "INSERT INTO users (email, password, role) VALUES (%s, %s, %s)"
        try:
            self.query(insert_query, [email, encrypted_password, role])
            return {'success': 1}
        except Exception as e:
            return {'success': 0, 'error': str(e)}

    def authenticate(self, email='me@email.com', password='password'):
        # Encrypt the provided password to match the database's encryption
        encrypted_password = self.onewayEncrypt(password)

        # Query the database for a matching user
        user_query = "SELECT * FROM users WHERE email = %s AND password = %s"
        user = self.query(user_query, [email, encrypted_password])
        if user:
            return {'success': 1, 'user': user[0]}
        else:
            return {'success': 0, 'error': 'Authentication failed'}

    def onewayEncrypt(self, string):
        encrypted_string = hashlib.scrypt(string.encode('utf-8'),
                                          salt = self.encryption['oneway']['salt'],
                                          n    = self.encryption['oneway']['n'],
                                          r    = self.encryption['oneway']['r'],
                                          p    = self.encryption['oneway']['p']
                                          ).hex()
        return encrypted_string


    def reversibleEncrypt(self, type, message):
        fernet = Fernet(self.encryption['reversible']['key'])
        
        if type == 'encrypt':
            message = fernet.encrypt(message.encode())
        elif type == 'decrypt':
            message = fernet.decrypt(message).decode()

        return message


