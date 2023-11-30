import sqlite3, hashlib, random, string


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
def encyrpt_password(con, cur):
    pass

# Decryption for stored passwords
def decrypt_password(con, cur):
    pass

# Registers a new user
def register(con, cur):
    # Checks if username does not exist
    while True:
        username = input("Please enter in a username: ")
        
        # Checks username is not blank
        if username == "":
            print("Username cannot be blank!")
            continue
        
        # Check username is not already in use
        users = cur.execute(f"""SELECT Username FROM tbl_accounts WHERE Username = '{username}'""").fetchall()
        try:
            users = users[0]
            print("User already exists")
        except:
            break
    
    # User enters password the password is hashed then added
    password = input("Please enter in a password: ")
    salt = generate_salt()
    hash = generate_hash(password+salt)
    try:
        userid = cur.execute("SELECT UserID FROM tbl_accounts ORDER BY UserID ASC").fetchall()[-1][0]
    except:
        userid = 0
    cur.execute(f"""INSERT INTO tbl_accounts (UserID, Username, salt, hash) VALUES ({userid+1}, '{username}', '{salt}', '{hash}')""")
    con.commit()
    print("User Created!")
    main_menu(con, cur)

# Login to an already exisiting user
def login(con, cur):
    while True:
        username = input("Please enter in your username: ")
        users = cur.execute(f"""SELECT Username FROM tbl_accounts WHERE Username = '{username}'""").fetchone()
        
        if username not in users:
            print("User does not exist")
            choice = input("Retry Login? (y/n): ").lower()
            if choice == "n":
                break
            continue
        
        password = input("Please enter your password: ")
        salt = cur.execute(f"""SELECT salt FROM tbl_accounts WHERE Username='{username}'""")[0]
        hash = generate_hash(password+salt)
        
        if hash == cur.execute(f"""SELECT hash from tbl_accounts WHERE USername='{username}'""")[0]:
            print("Login Successfull")
            break
        else:
            print("Incorrect password")
            choice = input("Retry Login? (y/n): ").lower()
            if choice == "n":
                break
    main_menu(con, cur)

# Main menu
def main_menu(con, cur):
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
        while True:
            descision = input()
            try:
                descision = int(descision)
            except:
                print("\nPlease enter in a valid option")

            match descision:
                case 1:
                    login(con, cur)
                    break
                case 2:
                    register(con, cur)
                    break
                case 3:
                    open = False
                    break
                case other:
                    pass


def main():
    con = sqlite3.connect("account.db")
    cur = con.cursor()
    main_menu(con, cur)


if __name__ == "__main__":
    main()
