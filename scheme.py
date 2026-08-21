
import sqlite3

DB_FILE = "leads.db"


def create_star_schema():

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # =========================
    # Dimension: Date
    # =========================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dim_date (
            date_key INTEGER PRIMARY KEY,
            full_date TEXT NOT NULL,
            year INTEGER,
            month INTEGER,
            day INTEGER,
            quarter INTEGER
        )
    """)

    # =========================
    # Dimension: Lead
    # =========================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dim_lead (
            lead_key INTEGER PRIMARY KEY AUTOINCREMENT,
            linkedin_url TEXT NOT NULL UNIQUE,
            first_name TEXT,
            last_name TEXT,
            company TEXT,
            job_title TEXT,
            location TEXT,
            effective_from TEXT,
            effective_to TEXT,
            is_current INTEGER DEFAULT 1
        )
    """)

    # =========================
    # Dimension: Campaign
    # =========================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dim_campaign (
            campaign_key INTEGER PRIMARY KEY AUTOINCREMENT,
            campaign_name TEXT NOT NULL UNIQUE,
            campaign_type TEXT,
            target_segment TEXT,
            effective_from TEXT,
            effective_to TEXT,
            is_current INTEGER DEFAULT 1
        )
    """)

    # =========================
    # Dimension: Account
    # =========================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dim_account (
            account_key INTEGER PRIMARY KEY AUTOINCREMENT,
            account_name TEXT NOT NULL UNIQUE,
            account_age_tier TEXT,
            daily_invite_limit INTEGER,
            daily_message_limit INTEGER,
            effective_from TEXT,
            effective_to TEXT,
            is_current INTEGER DEFAULT 1
        )
    """)

    # =========================
    # Fact: Outreach
    # =========================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fact_outreach (
            outreach_key INTEGER PRIMARY KEY AUTOINCREMENT,

            date_key INTEGER,
            lead_key INTEGER,
            campaign_key INTEGER,
            account_key INTEGER,

            invites_sent INTEGER DEFAULT 0,
            connections_accepted INTEGER DEFAULT 0,
            messages_sent INTEGER DEFAULT 0,
            replies_received INTEGER DEFAULT 0,
            meetings_booked INTEGER DEFAULT 0,

            FOREIGN KEY (date_key)
                REFERENCES dim_date(date_key),

            FOREIGN KEY (lead_key)
                REFERENCES dim_lead(lead_key),

            FOREIGN KEY (campaign_key)
                REFERENCES dim_campaign(campaign_key),

            FOREIGN KEY (account_key)
                REFERENCES dim_account(account_key)
        )
    """)

    conn.commit()
    conn.close()

    print("Star schema created successfully.")


if __name__ == "__main__":
    create_star_schema()