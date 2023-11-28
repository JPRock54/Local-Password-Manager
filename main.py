import sqlite3, bcrypt, hashlib


def generate_salt():
    salt = bcrypt.gensalt()
    return salt


def generate_hash(word):
    word = word.encode("utf-8")
    hash = hashlib.sha512(word).hexdigest()
    return hash


def encyrpt_password():
    pass


def decrypt_password():
    pass


def register(cur):
    while True:
        username = input("Please enter in a username: ")
        users = cur.execute("SELECT Username FROM tbl_accounts")
        if username in users:
            print("User already exists")
        break
    password = input("Please enter in a password: ")
    salt = generate_salt()
    hash = generate_hash(password)
    userid = max(cur.execute("SELECT UserID FROM tbl_accounts"))
    cur.execute(
        f"INSERT INTO tbl_accounts VALUES ({userid}, '{username}', '{salt}', '{hash}')"
    )
    print("User Created!")


def login(cur):
    username = input("Please enter in your username: ")
    users = cur.execute("SELECT Username FROM tbl_accounts")
    if username not in users:
        print("User does not exist")


def main_menu(cur):
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
                login(cur)
                break
            case 2:
                pass
                break
            case 3:
                pass
                break
            case other:
                pass


def main():
    con = sqlite3.connect("account.db")
    cur = con.cursor()
    main_menu(cur)


if __name__ == "__main__":
    main()
