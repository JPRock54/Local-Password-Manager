import sqlite3, hashlib, random, string, sys


# Asks a y/n question
def ask_question(phrase):
    question = input(f"{phrase} (y/n): ").lower()
    if question == "" or question == "y":
        return True
    elif question == "n":
        return False
    print("Invalid Input!")
    ask_question(phrase)


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
            if ask_question("Retry Registering?"):
                continue
            break

        # Checks the length of the username
        if not (4 <= len(username) <= 16):
            print("Username must be between 4 and 16 characters long!")
            if ask_question("Retry Registering?"):
                continue
            break

        # Check username is not already in use
        if cur.execute(
            f"SELECT Username FROM tbl_accounts WHERE Username = '{username}'"
        ).fetchall():
            print("User already exists")
            if ask_question("Retry Registering?"):
                continue
            break

        # User enters password the password is hashed then added

        password = input("Please enter in a password: ")

        # Checks password isn't blank
        if password == "":
            print("Password cannot be blank")
            if ask_question("Retry Registering?"):
                continue
            break

        # Checks password is between 8 and 32 characters
        if not (8 <= len(password) <= 32):
            print("Password must be between 8 and 32 characters!")
            if ask_question("Retry Registering?"):
                continue
            break

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
            if ask_question("Retry Login?"):
                continue
            break

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
            login_screen(username, password)
            break
        else:
            print("Incorrect password")
            # Asks the user if they want to stop logging in
            if ask_question("Retry Login?"):
                continue
            break


def view_accounts():
    print("Currently WEP")


def add_account():
    print("Currently WEP")


def generate_password():
    while True:
        capitals = ask_question("Should the password contain capital letters?")
        numbers = ask_question("Should the password contain numbers?")
        special_charatcers = ask_question(
            "Should the password contain special characters?"
        )
        length = input("How long should the password be? (16 by default): ")
        if length != "":
            try:
                length = int(length)
            except:
                print("Must be a number!")
                if ask_question("Retry?"):
                    continue
                break

        if capitals and numbers and special_charatcers:
            password = []
            for i in range(0, length):
                password.append(
                    random.choice(
                        string.ascii_letters + string.digits + string.punctuation
                    )
                )
            return "".join(password)

        elif capitals and numbers:
            password = []
            for i in range(0, length):
                password.append(random.choice(string.ascii_letters + string.digits))
            return "".join(password)

        elif capitals and special_charatcers:
            password = []
            for i in range(0, length):
                password.append(
                    random.choice(string.ascii_letters + string.punctuation)
                )
            return "".join(password)

        elif numbers and special_charatcers:
            password = []
            for i in range(0, length):
                password.append(
                    random.choice(
                        string.ascii_lowercase + string.digits + string.punctuation
                    )
                )
            return "".join(password)

        else:
            password = []
            for i in range(0, length):
                password.append(random.choice(string.ascii_lowercase))


def login_screen(username, password):
    while True:
        # Prints login menu
        print(
            f"""
Hello {username} what do you want to do?   
#############################################################
#                                                           #
# 1. View Accounts                                          #
# 2. Add Account                                            #
# 3. Generate a password                                    #
# 4. Exit to menu                                           #
#                                                           #
#############################################################
"""
        )

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
                    view_accounts()
                case 2:
                    choosing = False
                    add_account()
                case 3:
                    choosing = False
                    print(f"Your password is: {generate_password()}")
                case 4:
                    main_menu()
                case other:
                    print("\nPlease enter in a valid option")


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
# 1. Login                                #
# 2. Register                             #
# 3. Exit to desktop                      #
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
