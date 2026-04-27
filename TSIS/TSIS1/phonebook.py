import csv, json, os, sys
from datetime import date, datetime

import psycopg2
import psycopg2.extras

from connect import get_connection, init_schema

# HELPERS

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def pause():
    input("\nPress Enter...")

def execute(conn, query, params=(), fetch=False):
    with conn.cursor(
        cursor_factory=psycopg2.extras.RealDictCursor if fetch else None
    ) as cur:
        cur.execute(query, params)
        if fetch:
            return cur.fetchall()
    conn.commit()

def fmt_row(r):
    print(
        f"[{r['contact_id']:>3}] {r['name']:<20} | "
        f"{r.get('group_name') or '-'} | "
        f"{r.get('email') or '-'} | "
        f"{r.get('birthday') or '-'} | "
        f"{r.get('phones_list') or '-'}"
    )

# GROUPS

def get_groups(conn):
    return execute(conn, "SELECT id,name FROM groups ORDER BY name", fetch=True)

def get_or_create_group(conn, name):
    execute(conn,
        "INSERT INTO groups(name) VALUES(%s) ON CONFLICT DO NOTHING",
        (name,))
    return execute(conn,
        "SELECT id FROM groups WHERE name=%s",
        (name,), fetch=True
    )[0]["id"]

# CONTACTS

def add_contact(conn):
    print("\nAdd contact")

    name = input("Name: ").strip()
    if not name:
        return

    email = input("Email: ").strip() or None
    bday = input("Birthday YYYY-MM-DD: ").strip()
    birthday = None
    if bday:
        try:
            birthday = datetime.strptime(bday, "%Y-%m-%d").date()
        except:
            pass

    # group
    groups = get_groups(conn)
    for g in groups:
        print(f"{g['id']}. {g['name']}")

    g_input = input("Group (id/name): ").strip()
    group_id = int(g_input) if g_input.isdigit() else get_or_create_group(conn, g_input or "Other")

    # phones
    phones = []
    while ph := input("Phone (blank stop): ").strip():
        t = input("Type [mobile/home/work]: ").lower() or "mobile"
        if t not in ("home","work","mobile"): t = "mobile"
        phones.append((ph, t))

    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO contacts(name,email,birthday,group_id) VALUES(%s,%s,%s,%s) RETURNING id",
            (name, email, birthday, group_id)
        )
        cid = cur.fetchone()[0]

        for ph,t in phones:
            cur.execute(
                "INSERT INTO phones(contact_id,phone,type) VALUES(%s,%s,%s)",
                (cid, ph, t)
            )

    conn.commit()
    print("Added")

def delete_contact(conn):
    name = input("Name: ").strip()
    rows = execute(conn,
        "SELECT id,name FROM contacts WHERE LOWER(name)=LOWER(%s)",
        (name,), fetch=True)

    if not rows:
        print("Not found"); return

    for r in rows:
        print(f"[{r['id']}] {r['name']}")

    if input("Delete? y/n: ")=="y":
        execute(conn,
            "DELETE FROM contacts WHERE LOWER(name)=LOWER(%s)",
            (name,))
        print("Deleted")

# SEARCH

def search(conn):
    q = input("Search: ").strip()
    rows = execute(conn,
        "SELECT * FROM search_contacts(%s)",
        (q,), fetch=True)

    for r in rows: fmt_row(r)

def search_email(conn):
    q = input("Email contains: ").strip()
    rows = execute(conn, """
        SELECT c.id AS contact_id,c.name,c.email,c.birthday,
               g.name AS group_name,
               STRING_AGG(p.phone,' , ') AS phones_list
        FROM contacts c
        LEFT JOIN groups g ON g.id=c.group_id
        LEFT JOIN phones p ON p.contact_id=c.id
        WHERE c.email ILIKE %s
        GROUP BY c.id,g.name
        ORDER BY c.name
    """,(f"%{q}%",), fetch=True)

    for r in rows: fmt_row(r)

# PAGINATION

def browse(conn):
    limit, offset = 5, 0
    sort = input("Sort [name/birthday]: ") or "name"

    while True:
        rows = execute(conn,
            "SELECT * FROM get_contacts_page(%s,%s,NULL,%s)",
            (limit, offset, sort), fetch=True)

        clear()
        for r in rows: fmt_row(r)

        cmd = input("[n/p/q]: ")
        if cmd=="q": break
        elif cmd=="n": offset += limit
        elif cmd=="p" and offset>=limit: offset -= limit
        
# IMPORT / EXPORT

def export_json(conn):
    rows = execute(conn, """
        SELECT c.name,c.email,c.birthday,g.name AS group_name
        FROM contacts c LEFT JOIN groups g ON g.id=c.group_id
    """, fetch=True)

    with open("contacts.json","w",encoding="utf-8") as f:
        json.dump(rows,f,default=str,indent=2)

    print("Exported")

def import_json(conn):
    if not os.path.exists("contacts.json"):
        print("No file"); return

    data = json.load(open("contacts.json",encoding="utf-8"))

    for d in data:
        gid = get_or_create_group(conn, d.get("group_name") or "Other")
        execute(conn,
            "INSERT INTO contacts(name,email,birthday,group_id) VALUES(%s,%s,%s,%s)",
            (d["name"], d["email"], d["birthday"], gid)
        )

    print("Imported")

def import_csv(conn):
    if not os.path.exists("contacts.csv"):
        print("No file"); return

    with open("contacts.csv") as f:
        for r in csv.DictReader(f):
            gid = get_or_create_group(conn, r.get("group") or "Other")
            execute(conn,
                "INSERT INTO contacts(name,email,group_id) VALUES(%s,%s,%s)",
                (r["name"], r.get("email"), gid)
            )

    print("CSV Imported")

# PROCEDURES

def add_phone(conn):
    name = input("Name: ")
    phone = input("Phone: ")
    execute(conn, "CALL add_phone(%s,%s,'mobile')", (name,phone))
    print("Added")

def move_group(conn):
    name = input("Name: ")
    group = input("Group: ")
    execute(conn, "CALL move_to_group(%s,%s)", (name,group))
    print("Moved")
# MENU

MENU = """
1 Browse
2 Add
3 Delete
4 Search
5 Search email
6 Add phone
7 Move group
8 CSV import
9 JSON import
10 JSON export
0 Exit
"""

def main():
    init_schema()
    conn = get_connection()

    actions = {
        "1": browse,
        "2": add_contact,
        "3": delete_contact,
        "4": search,
        "5": search_email,
        "6": add_phone,
        "7": move_group,
        "8": import_csv,
        "9": import_json,
        "10": export_json
    }

    while True:
        print(MENU)
        c = input("> ")

        if c=="0": break
        elif c in actions:
            actions[c](conn)
            pause()
        else:
            print("Wrong input")

    conn.close()

if __name__ == "__main__":
    main()