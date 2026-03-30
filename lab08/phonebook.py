from connect import get_connection

def call_upsert(name, phone):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
    conn.commit()
    cur.close()
    conn.close()
    print("Upsert done")

def search_pattern(pattern):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM get_contacts_by_pattern(%s)", (pattern,))
    rows = cur.fetchall()
    for r in rows:
        print(r)
    cur.close()
    conn.close()

def bulk_insert(names, phones):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL bulk_insert_contacts(%s, %s)", (names, phones))
    conn.commit()
    cur.close()
    conn.close()
    print(" Bulk insert done")

def paginated(limit, offset):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
    rows = cur.fetchall()
    for r in rows:
        print(r)
    cur.close()
    conn.close()

def delete_contact(value):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL delete_contact(%s)", (value,))
    conn.commit()
    cur.close()
    conn.close()
    print(" Contact deleted")

def menu():
    while True:
        print("\n--- PhoneBook Menu ---")
        print("1. Upsert contact")
        print("2. Search by pattern")
        print("3. Bulk insert")
        print("4. Paginated query")
        print("5. Delete contact")
        print("0. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            name = input("Enter name: ")
            phone = input("Enter phone: ")
            call_upsert(name, phone)
        elif choice == "2":
            pattern = input("Enter search pattern: ")
            search_pattern(pattern)
        elif choice == "3":
            names = ["Jasulan", "Meirambek", "Dimash"]
            phones = ["87000000000", "87271722222", "87001009090"]
            bulk_insert(names, phones)
        elif choice == "4":
            limit = int(input("Limit: "))
            offset = int(input("Offset: "))
            paginated(limit, offset)
        elif choice == "5":
            value = input("Enter name or phone to delete: ")
            delete_contact(value)
        elif choice == "0":
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    menu()
