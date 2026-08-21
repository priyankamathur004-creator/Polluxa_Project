import sqlite3

DB_FILE = "leads.db"


def populate_fact_outreach():

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Get the dimension keys
    cursor.execute("SELECT date_key FROM dim_date LIMIT 1")
    date_result = cursor.fetchone()

    cursor.execute("SELECT lead_key FROM dim_lead LIMIT 1")
    lead_result = cursor.fetchone()

    cursor.execute("SELECT campaign_key FROM dim_campaign LIMIT 1")
    campaign_result = cursor.fetchone()

    cursor.execute("SELECT account_key FROM dim_account LIMIT 1")
    account_result = cursor.fetchone()

    if not all([
        date_result,
        lead_result,
        campaign_result,
        account_result
    ]):
        print("Required dimension records are missing.")
        conn.close()
        return

    date_key = date_result[0]
    lead_key = lead_result[0]
    campaign_key = campaign_result[0]
    account_key = account_result[0]

    # Insert one outreach activity record
    cursor.execute(
        """
        INSERT INTO fact_outreach
        (
            date_key,
            lead_key,
            campaign_key,
            account_key,
            invites_sent,
            connections_accepted,
            messages_sent,
            replies_received,
            meetings_booked
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            date_key,
            lead_key,
            campaign_key,
            account_key,
            1,
            0,
            0,
            0,
            0
        )
    )

    conn.commit()
    conn.close()

    print("Fact outreach populated successfully.")


if __name__ == "__main__":
    populate_fact_outreach()