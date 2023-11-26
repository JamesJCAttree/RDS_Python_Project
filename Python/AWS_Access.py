from tkinter import messagebox
import pymysql
import bcrypt
import json
import tkinter as tk
from tkinter import Label, Entry, Button
from dotenv import load_dotenv
from dotenv import load_dotenv
import os

usersName = "Null"
usersRealName = ""
usersID = "Null"
isLoggedin = False
currentCash = ""

def Configure(): # Gets database credentials
    load_dotenv()

# Connect to the database with DictCursor
def GetDbConfig(): # Depreciated database credentials grabber
    with open("config.json", "r") as config_file:
        config_data = json.load(config_file)
    return config_data["database"]

def ConnectToDatabase(): # Conects to the database
    db_config = GetDbConfig()
    db = pymysql.connect(
        host=os.getenv('host'),
        user=os.getenv('user'),
        password=os.getenv('password'),
        charset=os.getenv('charset'),
        cursorclass=pymysql.cursors.DictCursor
    )
    return db

Configure()
db = ConnectToDatabase()
GetDbConfig()
ConnectToDatabase()

def UsernameExists(username): # This checks if a username already exists
    cursor = db.cursor()
    cursor.execute("USE userinfo")
    select_query = "SELECT * FROM person WHERE username = %s"
    cursor.execute(select_query, (username,))
    existing_user = cursor.fetchone()
    return existing_user is not None

def getUserById(userId): # Gets the user by database ID
    cursor = db.cursor()
    cursor.execute("USE userinfo")
    select_query = "SELECT * FROM UserInformation WHERE id = %s"
    cursor.execute(select_query, (userId,))
    user_data = cursor.fetchone()
    cursor.close()
    return user_data

def CreateTables(): # This is a test to create if database's tables were deleted
    cursor = db.cursor()
    cursor.execute("USE userinfo")
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS person (
            id INT NOT NULL AUTO_INCREMENT,
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            PRIMARY KEY (id)
        )
        '''
    cursor.execute(create_table_query)
    cursor = db.cursor()
    cursor.execute("USE userinfo")
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS UserInformation (
        id INT NOT NULL AUTO_INCREMENT,
        personalName VARCHAR(255) NOT NULL,
        cash VARCHAR(255) NOT NULL,
        slot2 VARCHAR(255) NOT NULL,
        slot3 VARCHAR(255) NOT NULL,
        slot4 VARCHAR(255) NOT NULL,
        slot5 VARCHAR(255) NOT NULL,
        slot6 VARCHAR(255) NOT NULL,
        slot7 VARCHAR(255) NOT NULL,
        slot8 VARCHAR(255) NOT NULL,
        slot9 VARCHAR(255) NOT NULL,
        slot10 VARCHAR(255) NOT NULL,
        PRIMARY KEY (id)
    )
    '''
    cursor.execute(create_table_query)
    db.commit()
CreateTables()

def CreateUser(): # Create a new user in database
    if not UsernameExists(entryUsername.get()):
        cursor = db.cursor()
        cursor.execute("USE userinfo")
        username = entryUsername.get()
        password = bytes(entryPassword.get(), 'utf-8')
        salt = bcrypt.gensalt(rounds=15)
        password = bcrypt.hashpw(password, salt)
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS person (
            id INT NOT NULL AUTO_INCREMENT,
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            PRIMARY KEY (id)
        )
        '''
        cursor.execute(create_table_query)
        insert_data_query = '''
        INSERT INTO person (username, password) VALUES (%s, %s)
        '''
        cursor.execute(insert_data_query, (username, password))
        cursor = db.cursor()
        cursor.execute("USE userinfo")
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS UserInformation (
            id INT NOT NULL AUTO_INCREMENT,
            personalName VARCHAR(255) NOT NULL,
            cash VARCHAR(255) NOT NULL,
            slot2 VARCHAR(255) NOT NULL,
            slot3 VARCHAR(255) NOT NULL,
            slot4 VARCHAR(255) NOT NULL,
            slot5 VARCHAR(255) NOT NULL,
            slot6 VARCHAR(255) NOT NULL,
            slot7 VARCHAR(255) NOT NULL,
            slot8 VARCHAR(255) NOT NULL,
            slot9 VARCHAR(255) NOT NULL,
            slot10 VARCHAR(255) NOT NULL,
            PRIMARY KEY (id)
        )
        '''
        cursor.execute(create_table_query)
        personalName = "Unused"
        slot = ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"] # Placeholder list for slots
        insert_data_query = '''
        INSERT INTO UserInformation (personalName, cash, slot2, slot3, slot4, slot5, slot6, slot7, slot8, slot9, slot10)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        cursor.execute(insert_data_query, (personalName, slot[0], slot[1], slot[2], slot[3], slot[4], slot[5], slot[6], slot[7], slot[8], slot[9]))
        print("Data inserted successfully.")
        db.commit() # Commit the changes to the database

def ReadAll(): # This should never be run for anything past development
    cursor = db.cursor()
    cursor.execute("USE userinfo")
    select_query = "SELECT * FROM person"
    cursor.execute(select_query)
    rows = cursor.fetchall()
    for row in rows:
        print(f"ID: {row['id']}, Username: {row['username']}, Password: {row['password']}")

def UserSearch(): # Search for a specific user
    cursor = db.cursor()
    cursor.execute("USE userinfo")
    username_to_retrieve = input("Enter the username to retrieve: ")
    select_query = "SELECT * FROM person WHERE username = %s"
    cursor.execute(select_query, (username_to_retrieve,))
    user_data = cursor.fetchone()
    if user_data:
        print(f"User found - ID: {user_data['id']}, Username: {user_data['username']}, Password: {user_data['password']}")
    else:
        print(f"No user found with the username: {username_to_retrieve}")

def PrintDataBase(): # This shouldn't be run past development
    cursor = db.cursor()
    cursor.execute("SHOW DATABASES")
    databases = cursor.fetchall()
    print(databases)

def Login(): # This is how the login system functions
    cursor = db.cursor()
    cursor.execute("USE userinfo")
    username_to_retrieve = entryUsername.get()
    select_query = "SELECT * FROM person WHERE username = %s"
    cursor.execute(select_query, (username_to_retrieve,))
    user_data = cursor.fetchone()
    password = bytes(entryPassword.get(), 'utf-8')
    salt = bcrypt.gensalt(rounds=15)
    hashed_password = bcrypt.hashpw(password, salt)
    if user_data is not None:
        if bcrypt.checkpw(password, bytes(user_data['password'], 'utf-8')):
            global usersName 
            global usersID
            global usersRealName
            usersID = user_data['id']
            usersName = user_data['username']
            return True
        else:
            return False
    else:
        return False

def UpdateCash(change): # Update the balance value in database
    cursor = db.cursor()
    cursor.execute("USE userinfo")
    select_query = "SELECT * FROM UserInformation WHERE id = %s"
    cursor.execute(select_query, (usersID,))
    user_data = cursor.fetchone()
    currentCash = float(user_data['cash'])
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS UserInformation (
        id INT NOT NULL AUTO_INCREMENT,
        personalName VARCHAR(255) NOT NULL,
        cash VARCHAR(255) NOT NULL,
        slot2 VARCHAR(255) NOT NULL,
        slot3 VARCHAR(255) NOT NULL,
        slot4 VARCHAR(255) NOT NULL,
        slot5 VARCHAR(255) NOT NULL,
        slot6 VARCHAR(255) NOT NULL,
        slot7 VARCHAR(255) NOT NULL,
        slot8 VARCHAR(255) NOT NULL,
        slot9 VARCHAR(255) NOT NULL,
        slot10 VARCHAR(255) NOT NULL,
        PRIMARY KEY (id)
    )
    '''
    update_query = "UPDATE UserInformation SET cash = %s WHERE id = %s"
    updated_value = str(float(user_data['cash']) + change)
    cursor.execute(update_query, (updated_value, usersID))
    db.commit()

def CheckCash(): # Gets the balance from database
    cursor = db.cursor()
    cursor.execute("USE userinfo")
    select_query = "SELECT * FROM UserInformation WHERE id = %s"
    cursor.execute(select_query, (usersID,))
    user_data = cursor.fetchone()
    currentCash = str(float(user_data['cash']))
    return float(user_data['cash'])

window = tk.Tk()

def TestLogin(): # This tests the credentials inputed
    if Login():
        isLoggedin = True
        window.destroy()
    else:
        messagebox.showerror("Error", "The username/password was incorrect")
        entryUsername.delete(0, tk.END)
        entryPassword.delete(0, tk.END)
        print(f"Sorry, but the username/password was incorrect")

def LoggingOn(): # This is the login window creation
    window.title("Login")
    global entryUsername
    global entryPassword
    labelUsername = Label(window, text="Username:")
    labelUsername.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
    entryUsername = Entry(window)
    entryUsername.grid(row=0, column=1, padx=10, pady=10)
    labelPassword = Label(window, text="Password:")
    labelPassword.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
    entryPassword = Entry(window, show="*") # Show * for password input
    entryPassword.grid(row=1, column=1, padx=10, pady=10)
    loginButton = Button(window, text="Login", command=TestLogin)
    loginButton.grid(row=2, column=0, columnspan=2, pady=10)
    createButton = Button(window, text="Create account", command=CreateUser)
    createButton.grid(row=3, column=0, columnspan=3, pady=10)
    screenWidth = window.winfo_screenwidth()
    screenHeight = window.winfo_screenheight()
    xCoordinate = (screenWidth / 2) - (window.winfo_reqwidth() / 2)
    yCoordinate = (screenHeight / 2) - (window.winfo_reqheight() / 2)
    window.geometry(f"+{int(xCoordinate)}+{int(yCoordinate)}")

    if not isLoggedin: # Kills login window kind of
        window.mainloop()

def OnSubmit(): # Changes the balance value
    enteredText = text2.get("1.0", tk.END).strip()
    if ValidateFloatInput(enteredText):
        print(f"Entered float value: {float(enteredText)}")
        UpdateCash(float(enteredText))
        text2.delete("1.0", tk.END)
        UpdateLabels()
    else:
        messagebox.showerror("Error", "Invalid float input. Please enter a valid float.")

def SubmitNewPersonalName(): # Change user's personal name
    enteredText = text1.get("1.0", tk.END).strip()
    if len(str(text1.get("1.0", tk.END).strip())) < 15:
        cursor = db.cursor()
        cursor.execute("USE userinfo")
        select_query = "SELECT * FROM UserInformation WHERE id = %s"
        cursor.execute(select_query, (usersID,))
        user_data = cursor.fetchone()
        currentCash = float(user_data['cash'])
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS UserInformation (
            id INT NOT NULL AUTO_INCREMENT,
            personalName VARCHAR(255) NOT NULL,
            cash VARCHAR(255) NOT NULL,
            slot2 VARCHAR(255) NOT NULL,
            slot3 VARCHAR(255) NOT NULL,
            slot4 VARCHAR(255) NOT NULL,
            slot5 VARCHAR(255) NOT NULL,
            slot6 VARCHAR(255) NOT NULL,
            slot7 VARCHAR(255) NOT NULL,
            slot8 VARCHAR(255) NOT NULL,
            slot9 VARCHAR(255) NOT NULL,
            slot10 VARCHAR(255) NOT NULL,
            PRIMARY KEY (id)
        )
        '''
        update_query = "UPDATE UserInformation SET personalName = %s WHERE id = %s"
        updated_value = str(text1.get("1.0", tk.END).strip())
        cursor.execute(update_query, (updated_value, usersID))
        text1.delete("1.0", tk.END)
        db.commit()
        UpdateLabels()
    else:
        messagebox.showerror("Error", "Your name is too long")

def ValidateFloatInput(new_value): # Checks and validates input
    try:
        float(new_value)
        return True
    except ValueError:
        return False

def UpdateLabels(): # Updates logged in window
    # Update the balance label
    negativeBal = CheckCash()
    dollarSign = "$"
    if negativeBal < 0:
        dollarSign = "-$"
        negativeBal *= -1
    textLabel2.config(text=f"Current Balance: {dollarSign}{negativeBal}")
    usersRealName = getUserById(usersID)['personalName']
    textLabel1.config(text=f"Welcome {usersRealName}")

LoggingOn()
# Create the main window
window = tk.Tk()
if usersName != "Null": # This is a really dumb way to do it
    window.title(f"{usersName}'s Information")
    usersRealName = getUserById(usersID)['personalName']
    window.geometry("600x500")
    if usersRealName != "Unused":
        welcome = f"Welcome {usersRealName}"
    else:
        welcome = f"Welcome {usersName}"
    textLabel1 = tk.Label(window, text=welcome, justify='center', font=('Helvetica', 16))
    textLabel1.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W)
    negativeBal = CheckCash()
    dollarSign = "$"
    if negativeBal < 0:
        dollarSign = "-$"
        negativeBal *= -1
    textLabel2 = tk.Label(window, text=f"Current Balance: {dollarSign}{negativeBal}", font=('Helvetica', 12))
    textLabel2.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
    textLabel3 = tk.Label(window, text=f"Update personal name", justify='center', font=('Helvetica', 12))
    textLabel3.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W)
    text1 = tk.Text(window, height=2, width=10)
    text1.grid(row=5, column=0, padx=10, pady=10)
    submitButton = tk.Button(window, text="Submit", command=SubmitNewPersonalName)
    submitButton.grid(row=5, column=1, columnspan=2, pady=10)
    textLabel4 = tk.Label(window, text=f"Update balance", justify='center', font=('Helvetica', 12))
    textLabel4.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W)
    text2 = tk.Text(window, height=2, width=10)
    text2.grid(row=3, column=0, padx=10, pady=10)
    submitButton = tk.Button(window, text="Submit", command=OnSubmit)
    submitButton.grid(row=3, column=1, columnspan=2, pady=10)
    screenWidth = window.winfo_screenwidth()
    screenHeight = window.winfo_screenheight()
    screenWidth = window.winfo_screenwidth()
    screenHeight = window.winfo_screenheight()
    xCoordinate = (screenWidth / 2) - (window.winfo_reqwidth() * 1.5)
    yCoordinate = (screenHeight / 2) - (window.winfo_reqheight() * 1.5)
    window.geometry(f"+{int(xCoordinate)}+{int(yCoordinate)}")

    window.mainloop()

db.close() # Clear ties to db