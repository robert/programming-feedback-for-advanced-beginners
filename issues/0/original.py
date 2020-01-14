import hashlib
import json
import os
import sqlite3
from getpass import getpass

path = "C:/Users/16102/Documents/Advanced Beginner Projects/login/Part 2_SQL"
os.chdir(path)

# connect to sqlite3
conn = sqlite3.connect(os.path.join(path, "users_db.db"))
c = conn.cursor()


def setup_db():  
    # creates table in database
    users_db = '''
        CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT
        );
        '''
    c.execute(users_db)


def ask_recreate():
    # count users and ask to recreate db
    count_users = '''SELECT * FROM users;'''
    c.execute(count_users)
    num_users = len(c.fetchall())
   
    print("Your users table currently holds %d users." % num_users)
   
    del_table = input("Would you like to delete the current table and start over? (y/n): ")
    if del_table.lower().strip() in ['y', 'yes']:
        del_stmt = '''DROP TABLE users;'''
        c.execute(del_stmt)
       
    setup_db()


def show_db():
    # displays all registered users
    c.execute('''SELECT * FROM users;''')
    rows = c.fetchall()
   
    for row in rows:
        print(row)  


def sha_encrypt(pw):
    # sha256 hashing
    encode_hash = hashlib.sha256(pw.encode())
    hash_pw = encode_hash.hexdigest()
   
    return hash_pw


def register():  
    username = input("Please enter a username: ").lower()
   
    # ensure passwords match      
    invalid = True
    while invalid:
        pw = getpass("Please enter a password: ")
        pw2 = getpass("Please confirm your password: ")
       
        if pw == pw2:
            invalid = False
        elif pw != pw2:
            print("Passwords are not the same")

    # hash password
    hash_pw = sha_encrypt(pw)
           
    # save to sqlite3 database. Return error if username taken
    try:
        insert_user = "INSERT INTO users VALUES (?, ?);"
        c.execute(insert_user, (username, hash_pw))
    except sqlite3.IntegrityError:
        print("ERROR: Username already exists")
        register()
   

def is_valid_credentials():
    # get username and password and check if they match db users
    username = input("Please enter a username: ")
    pw = getpass("Please enter a password: ")
    hash_pw = sha_encrypt(pw)
   
    # execute sqlite3 command. Returns None if doesn't exist
    select_users = '''SELECT * FROM users WHERE username=? AND password=?;'''
    c.execute(select_users, (username, hash_pw))
    if c.fetchone() is not None:
        print("Welcome")
    else:
        print("Login failed. Username or password is incorrect.")

   
def main():
    setup_db()
    ask_recreate()
       
    # ask to register or login
    undecided = True
    while undecided:
        log_type = input("Would you like to register or login? Type register or login: ")
        if log_type.strip().lower() == "register":
            register()
            break
        elif log_type.strip().lower() == "login":
            is_valid_credentials()
            break
        else:
            print("Please type a valid response")

    # closing connection and commiting changes
    conn.commit()
    conn.close()
   

if __name__ == "__main__":
    main()
