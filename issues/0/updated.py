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


def sha256(inp):
    """
    Calculates the SHA256 hash of the input and returns it as a
    hexstring.
    """
    return hashlib.sha256(inp.encode()).hexdigest()


def create_user(username, pw):
    """
    Inserts a row into the user table in the DB with the given
    credentials. Returns True if the insertion succeeds and
    False if the username has already been taken.
    """
    hash_pw = sha256(pw)

    # Save to sqlite3 database. Will throw an IntegrityError
    # if username already taken.
    try:
        insert_user = "INSERT INTO users VALUES (?, ?);"
        c.execute(insert_user, (username, hash_pw))
        return True
    except sqlite3.IntegrityError:
        # Username is already taken
        return False


def is_valid_credentials(username, pw):
    """
    Returns True if the given credential match a user in the database,
    and False if they do not.
    """
    hash_pw = sha256(pw)

    # execute sqlite3 command. Returns None if doesn't exist
    c.execute('''SELECT * FROM users WHERE username=? AND password=?;''', (username, hash_pw))
    return c.fetchone() is not None


def main():
    setup_db()
    ask_recreate()

    # ask to register or login
    while True:
        log_type = input("Would you like to register or login? Type register or login: ").strip().lower()
        if log_type == "register":
            while True:
                username = input("Please enter a username: ").lower()

                # ensure passwords match
                while True:
                    pw = getpass("Please enter a password: ")
                    pw2 = getpass("Please confirm your password: ")

                    if pw == pw2:
                        break
                    else:
                        print("Passwords are not the same. Please try again.")

                if create_user(username, pw):
                    print("Success!")
                    break
                else:
                    print("Username already taken, please try again")

            break
        elif log_type == "login":
            # get username and password and check if they match db users
            username = input("Please enter a username: ")
            pw = getpass("Please enter a password: ")

            if is_valid_credentials(username, pw):
                print("Welcome")
            else:
                print("Login failed. Username or password is incorrect.")

            break
        else:
            print("Please type a valid response")

    # closing connection and commiting changes
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
