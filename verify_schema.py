import sqlite3

DB_FILE = "leads.db"


def verify_schema():

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    tables = [
        "dim_date",
        "dim_lead",
        "dim_campaign",
        "dim_account",
        "fact_outreach"
    ]

    print("\n--- Star Schema Verification ---")

    for table in tables:

        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]

        print(f"{table}: {count} records")

    print("\n--- Fact Table Sample ---")

    cursor.execute(
        """
        SELECT
            f.outreach_key,
            f.date_key,
            f.lead_key,
            f.campaign_key,
            f.account_key,
            f.invites_sent,
            f.connections_accepted,
            f.messages_sent,
            f.replies_received,
            f.meetings_booked
        FROM fact_outreach f
        LIMIT 5
        """
    )

    rows = cursor.fetchall()

    for row in rows:
        print(row)

    conn.close()


if __name__ == "__main__":
    verify_schema()
