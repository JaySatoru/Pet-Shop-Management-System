import mysql.connector

# ================= DATABASE CONNECTION =================
conn = mysql.connector.connect(
    host="localhost",
    user="root",          
    password="Sai@2003#",
    database="PetShopDB"
)

cursor = conn.cursor()


# ================= USER FUNCTIONS =================
def add_user(username, password):
    try:
        query = "INSERT INTO Users (username, password) VALUES (%s, %s)"
        cursor.execute(query, (username, password))
        conn.commit()
        print("Account created successfully.")
    except:
        print("Username already exists!")


def login_user(username, password):
    query = "SELECT * FROM Users WHERE username=%s AND password=%s"
    cursor.execute(query, (username, password))
    return cursor.fetchone() is not None


# ================= PET FUNCTIONS =================
def add_pet(name, age, cost):
    cursor.execute("SELECT * FROM Pets WHERE name=%s", (name,))
    pet = cursor.fetchone()

    if pet:
        cursor.execute(
            "UPDATE Pets SET count = count + 1 WHERE name=%s",
            (name,)
        )
    else:
        cursor.execute(
            "INSERT INTO Pets (name, age, cost, count) VALUES (%s, %s, %s, 1)",
            (name, age, cost)
        )

    conn.commit()
    print("Pet added successfully.")


def display_pets():
    cursor.execute("SELECT name, age, cost, count FROM Pets")
    rows = cursor.fetchall()

    if not rows:
        print("No pets available.")
        return

    print("\nList of Pets:")
    for row in rows:
        print(f"Name: {row[0]}, Age: {row[1]}, Cost: {row[2]:.2f}, Available: {row[3]}")


def search_pet(name):
    cursor.execute("SELECT * FROM Pets WHERE name=%s", (name,))
    pet = cursor.fetchone()

    if pet:
        print(f"Pet found: Name: {pet[1]}, Age: {pet[2]}, Cost: {pet[3]:.2f}")
    else:
        print("Pet not found.")


# ================= MAIN PROGRAM =================
def main():
    logged_in = False

    while True:
        if not logged_in:
            print("\n===== Login Menu =====")
            print("1. Create an account")
            print("2. Login")
            print("3. Exit")

            try:
                choice = int(input("Enter your choice: "))
            except:
                print("Invalid input!")
                continue

            if choice == 1:
                username = input("Enter username: ")
                password = input("Enter password: ")
                add_user(username, password)

            elif choice == 2:
                username = input("Enter username: ")
                password = input("Enter password: ")

                if login_user(username, password):
                    print("Login successful.")
                    logged_in = True
                else:
                    print("Invalid username or password.")

            elif choice == 3:
                print("Exiting...")
                break

            else:
                print("Invalid choice!")

        else:
            print("\n===== Pet Shop Menu =====")
            print("1. Add a pet")
            print("2. Display all pets")
            print("3. Search for a pet")
            print("4. Logout")

            try:
                choice = int(input("Enter your choice: "))
            except:
                print("Invalid input!")
                continue

            if choice == 1:
                name = input("Enter pet name: ")
                age = int(input("Enter pet age: "))
                cost = float(input("Enter pet cost: "))
                add_pet(name, age, cost)

            elif choice == 2:
                display_pets()

            elif choice == 3:
                name = input("Enter pet name to search: ")
                search_pet(name)

            elif choice == 4:
                logged_in = False
                print("Logged out successfully.")

            else:
                print("Invalid choice!")


# ================= RUN =================
if __name__ == "__main__":
    try:
        main()
    finally:
        cursor.close()
        conn.close()