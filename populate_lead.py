import sqlite3
import json

DB_FILE = "leads.db"


def populate_lead_dimension():

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Get all records from staging table
    cursor.execute("""
        SELECT linkedin_url, data
        FROM leads
    """)

    rows = cursor.fetchall()

    inserted = 0

    for linkedin_url, json_data in rows:

        try:
            data = json.loads(json_data)

            first_name = data.get("First Name")
            last_name = data.get("Last Name")
            company = data.get("Company")
            job_title = data.get("Job Title")
            location = data.get("Location")

            cursor.execute(
                """
                INSERT OR IGNORE INTO dim_lead
                (
                    linkedin_url,
                    first_name,
                    last_name,
                    company,
                    job_title,
                    location,
                    effective_from,
                    is_current
                )
                VALUES (?, ?, ?, ?, ?, ?, datetime('now'), 1)
                """,
                (
                    linkedin_url,
                    first_name,
                    last_name,
                    company,
                    job_title,
                    location
                )
            )

            inserted += cursor.rowcount

        except Exception as e:
            print(
                f"Failed to process lead {linkedin_url}: {e}"
            )

    conn.commit()
    conn.close()

    print(f"Lead dimension populated. Inserted: {inserted}")


if __name__ == "__main__":
    populate_lead_dimension()