import sqlite3
from datetime import datetime, timedelta

DB_FILE = "leads.db"


def populate_date_dimension():

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    start_date = datetime(2026, 1, 1)
    end_date = datetime(2026, 12, 31)

    current_date = start_date

    while current_date <= end_date:

        date_key = int(current_date.strftime("%Y%m%d"))
        full_date = current_date.strftime("%Y-%m-%d")
        year = current_date.year
        month = current_date.month
        day = current_date.day
        quarter = (month - 1) // 3 + 1

        cursor.execute(
            """
            INSERT OR IGNORE INTO dim_date
            (
                date_key,
                full_date,
                year,
                month,
                day,
                quarter
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                date_key,
                full_date,
                year,
                month,
                day,
                quarter
            )
        )

        current_date += timedelta(days=1)

    conn.commit()
    conn.close()

    print("Date dimension populated successfully.")


if __name__ == "__main__":
    populate_date_dimension()