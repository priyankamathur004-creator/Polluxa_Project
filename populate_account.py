import sqlite3

DB_FILE = "leads.db"


def populate_account_dimension():

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE INTO dim_account
        (
            account_name,
            account_age_tier,
            daily_invite_limit,
            daily_message_limit,
            effective_from,
            is_current
        )
        VALUES (?, ?, ?, ?, datetime('now'), 1)
        """,
        (
            "Primary LinkedIn Account",
            "Established",
            20,
            100
        )
    )

    conn.commit()
    conn.close()

    print("Account dimension populated successfully.")


if __name__ == "__main__":
    populate_account_dimension()
