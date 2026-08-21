from fastapi import FastAPI, Header, HTTPException
from dotenv import load_dotenv
import pandas as pd
import sqlite3
import os
import json

load_dotenv()

app = FastAPI()

API_KEY = os.getenv("API_KEY")

CSV_FILE = "newton-leads-all-63-2026-08-20.csv"
DB_FILE = "leads.db"


# Home

@app.get("/")
def home():
    return {"message": "API is working"}



# Health

@app.get("/health")
def health():
    return {"status": "healthy"}



# Secure endpoint

@app.get("/secure")
def secure(api_key: str = Header(None)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )

    return {"message": "Access granted"}



# Get leads from CSV

@app.get("/leads")
def get_leads():

    leads_df = pd.read_csv(CSV_FILE)

    # Convert NaN to None so JSON works correctly
    leads_df = leads_df.astype(object).where(
        pd.notna(leads_df),
        None
    )

    return leads_df.to_dict(orient="records")



# Create database

def create_database():

    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            linkedin_url TEXT UNIQUE,
            data TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Create database when application starts
create_database()



# Idempotent load

@app.post("/load")
def load_leads():

    leads_df = pd.read_csv(CSV_FILE)

    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()

    inserted = 0
    skipped = 0

    for _, row in leads_df.iterrows():

        linkedin_url = row["LinkedIn URL"]

        # Skip rows without LinkedIn URL
        if pd.isna(linkedin_url):
            skipped += 1
            continue

        linkedin_url = str(linkedin_url).strip()

        data = row.to_dict()

        # Convert NaN values to None
        data = {
            key: None if pd.isna(value) else value
            for key, value in data.items()
        }

        cursor.execute(
            """
            INSERT OR IGNORE INTO leads
            (linkedin_url, data)
            VALUES (?, ?)
            """,
            (
                linkedin_url,
                json.dumps(data)
            )
        )

        if cursor.rowcount == 1:
            inserted += 1
        else:
            skipped += 1

    conn.commit()
    conn.close()

    return {
        "message": "Load completed",
        "inserted": inserted,
        "skipped": skipped
    }

# incremental
@app.post("/load")
def load_leads():

    df = pd.read_csv(CSV_FILE)

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Get last loaded date
    cursor.execute(
        "SELECT last_added_on FROM metadata WHERE id = 1"
    )
    result = cursor.fetchone()

    last_date = result[0] if result else None

    # Keep only new records
    if last_date:
        df = df[df["Added On"] > last_date]

    inserted = 0

    for _, row in df.iterrows():

        cursor.execute(
            """
            INSERT OR IGNORE INTO leads
            (linkedin_url, data)
            VALUES (?, ?)
            """,
            (
                row["LinkedIn URL"],
                json.dumps(row.to_dict(), default=str)
            )
        )

        inserted += cursor.rowcount

    # Save latest date
    if not df.empty:
        latest_date = df["Added On"].max()

        cursor.execute(
            """
            INSERT OR REPLACE INTO metadata
            (id, last_added_on)
            VALUES (1, ?)
            """,
            (str(latest_date),)
        )

    conn.commit()
    conn.close()

    return {
        "message": "Load completed",
        "inserted": inserted
    }

def create_database():

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            linkedin_url TEXT UNIQUE,
            data TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS metadata (
            id INTEGER PRIMARY KEY,
            last_added_on TEXT
        )
    """)

    conn.commit()
    conn.close()

# part 3
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


    import sqlite3

conn = sqlite3.connect("leads.db")
cursor = conn.cursor()

cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
    ORDER BY name
""")

tables = cursor.fetchall()

print("Tables in database:")

for table in tables:
    print("-", table[0])

conn.close()

# Documet the grain
"""
PART 3 - STAR SCHEMA

Fact table grain:
One row in fact_outreach represents one lead's
outreach activity for one account, one campaign,
and one calendar date.

Dimension tables:
dim_date     -> Calendar information
dim_lead     -> Lead/person information
dim_campaign -> Outreach campaign information
dim_account  -> LinkedIn account/agent information

Surrogate keys:
lead_key
campaign_key
account_key
date_key

SCD strategy:
Lead, campaign, and account dimensions use
SCD Type 2 where historical attribute changes
need to be preserved.
"""


