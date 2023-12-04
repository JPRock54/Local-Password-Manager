import sqlite3, hashlib, random, string, sys


# Generate the salt
def generate_salt():
    characters = string.ascii_letters + string.digits
    salt = [random.choice(characters) for i in range(32)]
    return "".join(salt)


# Generates the hash
def generate_hash(word):
    word = word.encode("utf-8")
    hash = hashlib.sha512(word).hexdigest()
    return hash


# Encryption for stored passwords
def encyrpt_password():
    con = sqlite3.connect("account.db")
    cur = con.cursor()
    pass


# Decryption for stored passwords
def decrypt_password():
    con = sqlite3.connect("account.db")
    cur = con.cursor()
    pass


# Asks the user if they should retry logging in
def retry(word):
    while True:
        choice = input(f"Retry {word}? (y/n): ").lower()
        if choice == "n":
            return False
        elif choice == "y":
            return True
        else:
            print("Enter a valid option!")


# Registers a new user
def register():
    con = sqlite3.connect("account.db")
    cur = con.cursor()

    # Checks if username does not exist
    while True:
        username = input("Please enter in a username: ")

        # Checks username is not blank
        if username == "":
            print("Username cannot be blank!")
            if not retry("Registering"):
                break
            else:
                continue

        # Checks the length of the username
        if len(username) > 16 or len(username) < 4:
            print("Username must be between 4 and 16 characters long!")
            if not retry("Registering"):
                break
            else:
                continue

        # Check username is not already in use
        if cur.execute(
            f"SELECT Username FROM tbl_accounts WHERE Username = '{username}'"
        ).fetchall():
            print("User already exists")
            if not retry("Registering"):
                break
            else:
                continue

        # User enters password the password is hashed then added

        password = input("Please enter in a password: ")

        # Checks password isn't blank
        if password == "":
            print("Password cannot be blank")
            if not retry("Registering"):
                break
            else:
                continue

        # Cehcks password is between 8 and 32 characters
        if 8 < len(password) < 32:
            print("Password must be between 8 and 32 characters!")
            if not retry("Registering"):
                break
            else:
                continue

        # Hashes password
        salt = generate_salt()
        hash = generate_hash(password + salt)

        # Determines userid
        try:
            userid = cur.execute(
                "SELECT UserID FROM tbl_accounts ORDER BY UserID ASC"
            ).fetchall()[-1][0]
        except:
            userid = 0

        # Adds user to databse
        cur.execute(
            f"""INSERT INTO tbl_accounts (UserID, Username, salt, hash) VALUES ({userid+1}, '{username}', '{salt}', '{hash}')"""
        )
        con.commit()
        print("User Created!")
        break


# Login to an already exisiting user
def login():
    con = sqlite3.connect("account.db")
    cur = con.cursor()

    # Login Loop
    while True:
        username = input("Please enter in your username: ")
        users = cur.execute(
            f"""SELECT Username FROM tbl_accounts WHERE Username = '{username}'"""
        ).fetchone()

        # Finds if user exists
        try:
            users = users[0]
        except:
            print("User does not exist")
            if not retry("Login"):
                break
            else:
                continue

        # Hashes inputed Password
        password = input("Please enter your password: ")
        salt = cur.execute(
            f"""SELECT salt FROM tbl_accounts WHERE Username='{username}'"""
        ).fetchone()[0]
        hash = generate_hash(password + salt)

        # Compares Hashes
        if (
            hash
            == cur.execute(
                f"""SELECT hash from tbl_accounts WHERE Username='{username}'"""
            ).fetchone()[0]
        ):
            print("Login Successfull")
            break
        else:
            print("Incorrect password")
            # Asks the user if they want to stop logging in
            if not retry("Login"):
                break
            else:
                continue


def login_screen(username, password):
    while True:
        print(
            f"""
#############################################################
# Hello {username} what do you want to do?                  #
#                                                           #
# 1. Login                                                  #
# 2. Register                                               #
# 3. Exit to desktop                                        #
#                                                           #
#############################################################
"""
        )


# Main menu
def main_menu():
    # Prints main menu
    open = True
    while open:
        print(
            """
###########################################
# Please select one of the following:     #
#                                         #
# 1. View accounts                        #
# 2. Generate a password                  #
# 3. Exit to menu                         #
#                                         #
###########################################
    """
        )

        # Allows the user to choose their option
        choosing = True
        while choosing:
            descision = input()
            try:
                descision = int(descision)
            except:
                print("\nPlease enter in a valid option")
                continue

            match descision:
                case 1:
                    choosing = False
                    login()
                    login_screen()
                case 2:
                    choosing = False
                    register()
                case 3:
                    sys.exit(), True
                case other:
                    print("\nPlease enter in a valid option")


# Main program
def main():
    main_menu()


# Runs program
if __name__ == "__main__":
    main()
