import hashlib
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import SimpleStatement
from cassandra import ConsistencyLevel
import json

cloud_config = {
    'secure_connect_bundle': 'secure-connect-electronics-ecommerce.zip'
}

with open("Electronics_ecommerce-token.json") as f:
    secrets = json.load(f)

CLIENT_ID = secrets["clientId"]
CLIENT_SECRET = secrets["secret"]

auth_provider = PlainTextAuthProvider(CLIENT_ID, CLIENT_SECRET)

cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()

keyspace_name = 'database'

session.execute(f"USE {keyspace_name}")


def create_tables():

    create_register_table = """
    CREATE TABLE IF NOT EXISTS register (
        id INT PRIMARY KEY,
        name TEXT,
        email TEXT,
        password TEXT
    )
    """
    try:
        session.execute(create_register_table)
        print("Table 'register' created successfully!")
    except Exception as e:
        print(f"Failed to create 'register' table. Error: {e}")



def register_account(fname, lname, email, password,ids):

    name = f"{fname} {lname}"
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    try:
        session.execute(
            "INSERT INTO register (id ,name, email, password) VALUES (%s,%s, %s, %s)",
            (ids, name, email, hashed_password)
        )
        print("Account registered successfully!")
    except Exception as e:
        print(f"Failed to register account. Error: {e}")

def login(email, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    result = session.execute(
        "SELECT email, password FROM register WHERE email = %s",
        (email,)
    )
    for row in result:
        if row.password == hashed_password:
            return True
    return False


def get_name(email):
    result = session.execute("SELECT name,email FROM register WHERE email = %s", (email,))
    if not result:
        return None  

    for row in result:
        return row.name

    
def get_id_by_email(email):
    try:
        result = session.execute(
            "SELECT id FROM register WHERE email = %s LIMIT 1",(email,))
        if result:
            return result[0].id
        else:
            return None
    except Exception as e:
        print(f"Failed to get id by email. Error: {e}")
        return None
    
if __name__ == '__main__':
    # Create the 'register' table
    # create_tables()
    # print("Created table...")
    # create_email_index = "CREATE INDEX IF NOT EXISTS email_index ON register (email)"
    # session.execute(create_email_index)
    # print("Indexed on email...")
    # delete_table = "DROP TABLE IF EXISTs register"
    # session.execute(delete_table)
    # print("deleted table")
    # session.execute("TRUNCATE TABLE register")
    rows = session.execute("SELECT * FROM register")
    for row in rows:
        print(row)
    user_email = 'himajakadari123@gmail.com'
    user = get_id_by_email(user_email)

    if user:
        print(f"User details for email {user_email}: ", user)
    else:
        print(f"No user found with email {user_email}")
