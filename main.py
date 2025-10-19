from service import register, login, log_out
from utils import Response
from db import cur, auto_commit



def main_menu():
    while True:
        print("\n📋 === USER AUTH MENU ===")
        print("1️⃣  Register")
        print("2️⃣  Login")
        print("3️⃣  Logout")
        print("4️⃣  Exit")

        choice = input("\nChoose an option (1-4): ").strip()

        if choice == '1':
            username = input("Enter a new username: ").strip()
            password = input("Enter a password: ").strip()
            role = input("Enter a role (default = user): ").strip() or 'user'
            res = register(username, password, role)
            print(f"\n➡️  {res.message} (status: {res.status_code})")

        elif choice == '2':
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()
            res = login(username, password)
            print(f"\n➡️  {res.message} (status: {res.status_code})")

        elif choice == '3':
            res = log_out()
            print(f"\n➡️  {res.message} (status: {res.status_code})")

        elif choice == '4':
            print("\n👋 Exiting the program...")
            break

        else:
            print("\n❌ Invalid choice. Please enter a number from 1 to 4.")


if __name__ == "__main__":
    main_menu()
