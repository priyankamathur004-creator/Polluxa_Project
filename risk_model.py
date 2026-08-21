import sqlite3
import statistics
import csv

DB_PATH = "leads.db"


def calculate_account_metrics(conn):
    """
    Calculate account-level outreach performance metrics.
    """

    cursor = conn.execute("""
        SELECT
            a.account_key,
            a.account_name,
            a.account_age_tier,
            a.daily_invite_limit,
            a.daily_message_limit,

            SUM(f.invites_sent) AS invites_sent,
            SUM(f.connections_accepted) AS connections_accepted,
            SUM(f.messages_sent) AS messages_sent,
            SUM(f.replies_received) AS replies_received,
            SUM(f.meetings_booked) AS meetings_booked

        FROM fact_outreach f
        JOIN dim_account a
            ON f.account_key = a.account_key

        GROUP BY
            a.account_key,
            a.account_name,
            a.account_age_tier,
            a.daily_invite_limit,
            a.daily_message_limit
    """)

    rows = cursor.fetchall()

    metrics = []

    for row in rows:

        (
            account_key,
            account_name,
            account_age_tier,
            daily_invite_limit,
            daily_message_limit,
            invites_sent,
            connections_accepted,
            messages_sent,
            replies_received,
            meetings_booked
        ) = row

        invites_sent = invites_sent or 0
        connections_accepted = connections_accepted or 0
        messages_sent = messages_sent or 0
        replies_received = replies_received or 0
        meetings_booked = meetings_booked or 0

        acceptance_rate = (
            connections_accepted / invites_sent
            if invites_sent > 0 else 0
        )

        reply_rate = (
            replies_received / messages_sent
            if messages_sent > 0 else 0
        )

        metrics.append({
            "account_key": account_key,
            "account_name": account_name,
            "account_age_tier": account_age_tier,
            "daily_invite_limit": daily_invite_limit,
            "daily_message_limit": daily_message_limit,
            "invites_sent": invites_sent,
            "connections_accepted": connections_accepted,
            "messages_sent": messages_sent,
            "replies_received": replies_received,
            "meetings_booked": meetings_booked,
            "acceptance_rate": acceptance_rate,
            "reply_rate": reply_rate
        })

    return metrics


def calculate_anomaly_score(metrics):
    """
    Calculate a simple statistically based anomaly score.

    Z-score is used when there are enough observations.
    With very small samples, the model avoids declaring
    performance anomalous.
    """

    insufficient_data = len(metrics) < 3

    if insufficient_data:
     for m in metrics:
        m["anomaly_score"] = 0
        m["risk_level"] = "INSUFFICIENT DATA"
        m["risk_signals"] = []
     return metrics

    acceptance_rates = [
        m["acceptance_rate"]
        for m in metrics
    ]

    reply_rates = [
        m["reply_rate"]
        for m in metrics
    ]

    if not insufficient_data:
     acceptance_mean = statistics.mean(acceptance_rates)
     reply_mean = statistics.mean(reply_rates)

     acceptance_std = statistics.stdev(acceptance_rates)
     reply_std = statistics.stdev(reply_rates)

    # Hidden risk signals
    for m in metrics:

        risk_signals = []

        # Acceptance-rate collapse
        if m["invites_sent"] >= 10 and m["acceptance_rate"] < 0.10:
            risk_signals.append("Acceptance-rate collapse")

        # Reply decay
        if m["messages_sent"] >= 10 and m["reply_rate"] < 0.05:
            risk_signals.append("Reply decay")

        # Ghosting pattern
        if m["messages_sent"] >= 10 and m["replies_received"] == 0:
            risk_signals.append("Ghosting pattern")

        m["risk_signals"] = risk_signals

    return metrics

def main():

    conn = sqlite3.connect(DB_PATH)

    metrics = calculate_account_metrics(conn)

    print("Number of accounts:", len(metrics))

    metrics = calculate_anomaly_score(metrics)

    # Export results for Power BI
    if metrics:
        with open("risk_output.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=metrics[0].keys())
            writer.writeheader()
            writer.writerows(metrics)

        print("risk_output.csv created successfully")
    else:
        print("No account data found. CSV was not created.")

    print("\nANOMALY & RISK ANALYSIS")
    print("=" * 80)

    for m in metrics:

        print(f"\nAccount: {m['account_name']}")
        print(f"Tier: {m['account_age_tier']}")
        print(f"Acceptance Rate: {m['acceptance_rate']:.2%}")
        print(f"Reply Rate: {m['reply_rate']:.2%}")
        print(f"Anomaly Score: {m['anomaly_score']:.2f}")
        print(f"Risk Level: {m['risk_level']}")
        if m.get("risk_signals", []):
         print("Risk Signals: " + ", ".join(m.get("risk_signals", [])))
        else:
         print("Risk Signals: None detected")

    print("\n" + "=" * 80)

    conn.close()


if __name__ == "__main__":
    main()

import sqlite3

conn = sqlite3.connect("leads.db")

tables = conn.execute("""
SELECT name
FROM sqlite_master
WHERE type='table'
""").fetchall()

print(tables)

conn.close()


