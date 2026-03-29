from connect import get_connection
import csv

def insert_contact(name, phone):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO contacts (name, phone) VALUES (%s, %s)", (name, phone))
    conn.commit()
    cur.close()
    conn.close()
    print(" Contact added")

def update_contact(name, new_phone):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE contacts SET phone=%s WHERE name=%s", (new_phone, name))
    conn.commit()
    cur.close()
    conn.close()
    print(" Contact updated")

def query_contacts():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM contacts")
    rows = cur.fetchall()
    for r in rows:
        print(r)
    cur.close()
    conn.close()

def delete_contact(name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM contacts WHERE name=%s", (name,))
    conn.commit()
    cur.close()
    conn.close()
    print(" Contact deleted")

def menu():
    while True:
        print("\n--- PhoneBook Menu ---")
        print("1. Insert contact")
        print("3. Update contact")
        print("4. Show all contacts")
        print("5. Delete contact")
        print("0. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            name = input("Enter name: ")
            phone = input("Enter phone: ")
            insert_contact(name, phone)
        elif choice == "3":
            name = input("Enter name to update: ")
            new_phone = input("Enter new phone: ")
            update_contact(name, new_phone)
        elif choice == "4":
            query_contacts()
        elif choice == "5":
            name = input("Enter name to delete: ")
            delete_contact(name)
        elif choice == "0":
            break
        else:
            print(" Invalid choice")

if __name__ == "__main__":
    menu()
