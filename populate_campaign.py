import sqlite3

DB_FILE = "leads.db"


def populate_campaign_dimension():

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE INTO dim_campaign
        (
            campaign_name,
            campaign_type,
            target_segment,
            effective_from,
            is_current
        )
        VALUES (?, ?, ?, datetime('now'), 1)
        """,
        (
            "Default LinkedIn Outreach",
            "LinkedIn",
            "Lead Generation"
        )
    )

    conn.commit()
    conn.close()

    print("Campaign dimension populated successfully.")


if __name__ == "__main__":
    populate_campaign_dimension()