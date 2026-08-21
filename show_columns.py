import sqlite3

DB_FILE = "leads.db"

tables = [
    "dim_date",
    "dim_lead",
    "dim_campaign",
    "dim_account",
    "fact_outreach"
]

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

for table in tables:

    print("\n" + "=" * 50)
    print(table)
    print("=" * 50)

    cursor.execute(f"PRAGMA table_info({table})")

    columns = cursor.fetchall()

    for column in columns:
        column_id, name, data_type, not_null, default_value, primary_key = column

        print(
            f"{name} | "
            f"Type: {data_type} | "
            f"PK: {primary_key} | "
            f"Required: {bool(not_null)}"
        )

conn.close()

columns.txt
