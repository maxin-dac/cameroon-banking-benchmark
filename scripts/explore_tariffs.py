#!/usr/bin/env python3
"""Exploration des tarifs normalisés : couverture et comparaisons clés."""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "data" / "db" / "banking_benchmark.db"

KEY_SERVICES = [
    "account_maintenance",
    "initial_deposit_non_salary",
    "local_transfer_systac",
    "local_transfer_syigma",
    "atm_withdrawal_own_bank",
    "atm_withdrawal_gimac",
    "card_gimac_annual",
    "card_visa_classic_annual",
    "internet_banking_subscription",
    "sms_banking_subscription",
    "cheque_bank_issue",
]


def format_tariff(row) -> str:
    if row["rate_pct"] is not None:
        text = f"{row['rate_pct']}%"
        if row["min_amount_ht"] is not None:
            text += f" min {row['min_amount_ht']:,.0f}"
        if row["max_amount_ht"] is not None:
            text += f" max {row['max_amount_ht']:,.0f}"
        return text

    for field, suffix in [
        ("amount_per_operation_ht", "/ op"),
        ("amount_annual_ht", "/ an"),
        ("amount_one_time_ht", "une fois"),
        ("amount_condition_ht", "condition"),
    ]:
        if row[field] is not None:
            return f"{row[field]:,.0f} {suffix}"

    return "?"


def main() -> None:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    print("=" * 70)
    print("COUVERTURE PAR SERVICE (nombre de banques sur 10)")
    print("=" * 70)

    for row in conn.execute(
        """
        SELECT service_key, COUNT(DISTINCT bank_code) AS n
        FROM tariffs
        GROUP BY service_key
        ORDER BY n DESC, service_key
        """
    ):
        print(f"{row['n']:>2}/10  {row['service_key']}")

    print()
    print("=" * 70)
    print("COMPARAISONS CLÉS")
    print("=" * 70)

    for service_key in KEY_SERVICES:
        print(f"\n--- {service_key} ---")

        rows = conn.execute(
            """
            SELECT bank_code, channel, rate_pct, min_amount_ht, max_amount_ht,
                   amount_per_operation_ht, amount_annual_ht,
                   amount_one_time_ht, amount_condition_ht
            FROM tariffs
            WHERE service_key = ?
            ORDER BY bank_code, channel
            """,
            (service_key,),
        ).fetchall()

        if not rows:
            print("  Aucune donnée.")
            continue

        for row in rows:
            channel = ""
            if row["channel"] not in (None, "not_applicable"):
                channel = f"[{row['channel']}] "
            print(f"  {row['bank_code']:<10} {channel:<10}{format_tariff(row)}")

    conn.close()


if __name__ == "__main__":
    main()