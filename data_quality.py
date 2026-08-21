import sqlite3
from datetime import date

DB_FILE = "leads.db"


def check_completeness(conn):
    """Check that important columns do not contain NULL values."""

    checks = []

    # dim_lead
    cursor = conn.execute("""
        SELECT COUNT(*)
        FROM dim_lead
        WHERE linkedin_url IS NULL OR TRIM(linkedin_url) = ''
    """)
    missing_leads = cursor.fetchone()[0]

    checks.append(("Completeness - dim_lead", missing_leads == 0, missing_leads))

    # dim_date
    cursor = conn.execute("""
        SELECT COUNT(*)
        FROM dim_date
        WHERE full_date IS NULL
    """)
    missing_dates = cursor.fetchone()[0]

    checks.append(("Completeness - dim_date", missing_dates == 0, missing_dates))

    # dim_campaign
    cursor = conn.execute("""
        SELECT COUNT(*)
        FROM dim_campaign
        WHERE campaign_name IS NULL OR TRIM(campaign_name) = ''
    """)
    missing_campaigns = cursor.fetchone()[0]

    checks.append(
        ("Completeness - dim_campaign", missing_campaigns == 0, missing_campaigns)
    )

    # dim_account
    cursor = conn.execute("""
        SELECT COUNT(*)
        FROM dim_account
        WHERE account_name IS NULL OR TRIM(account_name) = ''
    """)
    missing_accounts = cursor.fetchone()[0]

    checks.append(
        ("Completeness - dim_account", missing_accounts == 0, missing_accounts)
    )

    return checks


def check_uniqueness(conn):
    """Check that business identifiers are unique."""

    checks = []

    # LinkedIn URLs should be unique
    cursor = conn.execute("""
        SELECT COUNT(*)
        FROM (
            SELECT linkedin_url
            FROM dim_lead
            GROUP BY linkedin_url
            HAVING COUNT(*) > 1
        )
    """)

    duplicate_leads = cursor.fetchone()[0]

    checks.append(
        ("Uniqueness - linkedin_url", duplicate_leads == 0, duplicate_leads)
    )

    # Date keys should be unique
    cursor = conn.execute("""
        SELECT COUNT(*)
        FROM (
            SELECT date_key
            FROM dim_date
            GROUP BY date_key
            HAVING COUNT(*) > 1
        )
    """)

    duplicate_dates = cursor.fetchone()[0]

    checks.append(
        ("Uniqueness - date_key", duplicate_dates == 0, duplicate_dates)
    )

    return checks


def check_validity(conn):
    """Check that values are within valid ranges."""

    checks = []

    # Outreach counts cannot be negative
    cursor = conn.execute("""
        SELECT COUNT(*)
        FROM fact_outreach
        WHERE invites_sent < 0
           OR connections_accepted < 0
           OR messages_sent < 0
           OR replies_received < 0
           OR meetings_booked < 0
    """)

    invalid_counts = cursor.fetchone()[0]

    checks.append(
        ("Validity - outreach counts", invalid_counts == 0, invalid_counts)
    )

    # Month must be between 1 and 12
    cursor = conn.execute("""
        SELECT COUNT(*)
        FROM dim_date
        WHERE month < 1 OR month > 12
    """)

    invalid_months = cursor.fetchone()[0]

    checks.append(
        ("Validity - month", invalid_months == 0, invalid_months)
    )

    # Quarter must be between 1 and 4
    cursor = conn.execute("""
        SELECT COUNT(*)
        FROM dim_date
        WHERE quarter < 1 OR quarter > 4
    """)

    invalid_quarters = cursor.fetchone()[0]

    checks.append(
        ("Validity - quarter", invalid_quarters == 0, invalid_quarters)
    )

    return checks


def check_timeliness(conn):
    """Check that actual outreach dates are not in the future."""

    checks = []

    today = date.today().isoformat()

    cursor = conn.execute("""
        SELECT COUNT(*)
        FROM fact_outreach f
        JOIN dim_date d
            ON f.date_key = d.date_key
        WHERE d.full_date > ?
    """, (today,))

    future_dates = cursor.fetchone()[0]

    checks.append(
        ("Timeliness - future dates", future_dates == 0, future_dates)
    )

    return checks


def check_referential_integrity(conn):
    """Check that fact table foreign keys exist in dimension tables."""

    checks = []

    # date_key
    cursor = conn.execute("""
        SELECT COUNT(*)
        FROM fact_outreach f
        LEFT JOIN dim_date d
            ON f.date_key = d.date_key
        WHERE d.date_key IS NULL
    """)

    missing_dates = cursor.fetchone()[0]

    checks.append(
        ("Referential integrity - date_key", missing_dates == 0, missing_dates)
    )

    # lead_key
    cursor = conn.execute("""
        SELECT COUNT(*)
        FROM fact_outreach f
        LEFT JOIN dim_lead l
            ON f.lead_key = l.lead_key
        WHERE l.lead_key IS NULL
    """)

    missing_leads = cursor.fetchone()[0]

    checks.append(
        ("Referential integrity - lead_key", missing_leads == 0, missing_leads)
    )

    # campaign_key
    cursor = conn.execute("""
        SELECT COUNT(*)
        FROM fact_outreach f
        LEFT JOIN dim_campaign c
            ON f.campaign_key = c.campaign_key
        WHERE c.campaign_key IS NULL
    """)

    missing_campaigns = cursor.fetchone()[0]

    checks.append(
        (
            "Referential integrity - campaign_key",
            missing_campaigns == 0,
            missing_campaigns
        )
    )

    # account_key
    cursor = conn.execute("""
        SELECT COUNT(*)
        FROM fact_outreach f
        LEFT JOIN dim_account a
            ON f.account_key = a.account_key
        WHERE a.account_key IS NULL
    """)

    missing_accounts = cursor.fetchone()[0]

    checks.append(
        (
            "Referential integrity - account_key",
            missing_accounts == 0,
            missing_accounts
        )
    )

    return checks


def run_quality_checks():
    conn = sqlite3.connect(DB_FILE)

    print("\n" + "=" * 60)
    print("DATA QUALITY CHECKS")
    print("=" * 60)

    all_checks = []

    all_checks.extend(check_completeness(conn))
    all_checks.extend(check_uniqueness(conn))
    all_checks.extend(check_validity(conn))
    all_checks.extend(check_timeliness(conn))
    all_checks.extend(check_referential_integrity(conn))

    passed = 0
    failed = 0

    print()

    for name, status, issue_count in all_checks:

        if status:
            print(f"PASS | {name}")
            passed += 1
        else:
            print(f"FAIL | {name} | Issues: {issue_count}")
            failed += 1

    print()
    print("=" * 60)
    print(f"Total checks : {len(all_checks)}")
    print(f"Passed       : {passed}")
    print(f"Failed       : {failed}")
    print("=" * 60)

    conn.close()


if __name__ == "__main__":
    run_quality_checks()

def run_quality_checks():
    conn = sqlite3.connect("leads.db")

    all_checks = []

    all_checks.extend(check_completeness(conn))
    all_checks.extend(check_uniqueness(conn))
    all_checks.extend(check_validity(conn))
    all_checks.extend(check_timeliness(conn))
    all_checks.extend(check_referential_integrity(conn))

    print("\nDATA QUALITY CHECKS")
    print("=" * 70)

    passed = 0
    failed = 0

    for name, status, issues in all_checks:
        result = "PASS" if status else "FAIL"

        if status:
            passed += 1
        else:
            failed += 1

        print(f"{result} | {name}")

    total = len(all_checks)

    print("\n" + "=" * 70)
    print(f"Total checks : {total}")
    print(f"Passed       : {passed}")
    print(f"Failed       : {failed}")

    # Composite Data Quality Score
    if total > 0:
        dq_score = (passed / total) * 100
    else:
        dq_score = 0

    threshold = 90

    print("\n" + "=" * 70)
    print("COMPOSITE DATA QUALITY SCORE")
    print("=" * 70)
    print(f"Score     : {dq_score:.2f}%")
    print(f"Threshold : {threshold}%")

    if dq_score >= threshold:
        print("Status    : PASS")
    else:
        print("Status    : FAIL")

    conn.close()


if __name__ == "__main__":
    run_quality_checks()