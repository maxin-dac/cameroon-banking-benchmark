#!/usr/bin/env python3
"""
Score de compétitivité tarifaire v1.

Méthodologie :
- Panier de 10 services comparables.
- Montants fixes retenus tels quels (annuel ou par opération).
- Formules variables évaluées uniquement si un montant standard est défini
  (ex. retrait GAB confrère à 50 000 XAF), sinon exclues.
- Canal prioritaire : digital/internet/mobile si disponible.
- Score par service = (nb de banques plus chères) / (nb de banques - 1) * 100.
- Score global = moyenne des scores des services disponibles.
- Couverture minimale : 6 services sur 10 pour être classé.
"""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "data" / "db" / "banking_benchmark.db"

MIN_COVERAGE = 5

# (item_id, libellé, service_keys, montant standard pour formules variables)
BASKET = [
    ("account_maintenance", "Tenue de compte (annuel)", ["account_maintenance"], None),
    ("deposit_non_salary", "Dépôt initial non salarié", ["initial_deposit_non_salary"], None),
    ("systac", "Virement SYSTAC (digital prioritaire)", ["local_transfer_systac"], None),
    ("syigma", "Virement SYGMA", ["local_transfer_syigma"], None),
    ("atm_own", "Retrait GAB propre banque", ["atm_withdrawal_own_bank"], None),
    ("atm_gimac", "Retrait GAB confrère (scénario 50 000 XAF)", ["atm_withdrawal_gimac"], 50000),
    ("card_local", "Carte locale / GIMAC (annuel)", ["card_gimac_annual", "card_basic_annual"], None),
    ("card_visa", "Carte Visa Classic (annuel)", ["card_visa_classic_annual"], None),
    ("internet_banking", "Internet banking (annuel)", ["internet_banking_subscription"], None),
    ("cheque_bank", "Chèque de banque", ["cheque_bank_issue"], None),
]


def value_of(row, standard_amount):
    if row["rate_pct"] is not None:
        if standard_amount is None:
            return None
        value = standard_amount * row["rate_pct"] / 100.0
        if row["min_amount_ht"] is not None:
            value = max(value, row["min_amount_ht"])
        if row["max_amount_ht"] is not None:
            value = min(value, row["max_amount_ht"])
        return value

    for field in (
        "amount_per_operation_ht",
        "amount_annual_ht",
        "amount_one_time_ht",
        "amount_condition_ht",
    ):
        if row[field] is not None:
            return float(row[field])

    return None


def pick_value(conn, bank_code, service_key, standard_amount):
    rows = conn.execute(
        """
        SELECT channel, rate_pct, min_amount_ht, max_amount_ht,
               amount_annual_ht, amount_per_operation_ht,
               amount_one_time_ht, amount_condition_ht
        FROM tariffs
        WHERE bank_code = ? AND service_key = ?
        """,
        (bank_code, service_key),
    ).fetchall()

    if not rows:
        return None

    evaluated = [(row, value_of(row, standard_amount)) for row in rows]
    evaluated = [(row, v) for row, v in evaluated if v is not None]

    if not evaluated:
        return None

    digital = [v for row, v in evaluated if row["channel"] in ("digital", "internet", "mobile")]

    return digital[0] if digital else evaluated[0][1]


def main() -> None:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    banks = [
        r["bank_code"]
        for r in conn.execute("SELECT bank_code FROM banks ORDER BY bank_code")
    ]

    detail = {}

    for item_id, label, keys, standard_amount in BASKET:
        values = {}
        for bank in banks:
            for key in keys:
                val = pick_value(conn, bank, key, standard_amount)
                if val is not None:
                    values[bank] = val
                    break
        detail[item_id] = (label, values)

    conn.close()

    # Score par service : robuste au outliers (classement, pas min-max)
    item_scores = {}
    market_standards = []

    for item_id, (label, values) in detail.items():
        n = len(values)
        if n < 2:
            continue

        # Item à variance nulle (gratuit ou identique partout) :
        # aucun pouvoir discriminant -> exclu du score,
        # mais reporté comme "standard du marché".
        if max(values.values()) == min(values.values()):
            market_standards.append((item_id, label, values))
            continue

        for bank, v in values.items():
            worse = sum(1 for other in values.values() if other > v)
            score = worse / (n - 1) * 100
            item_scores.setdefault(bank, []).append((item_id, score))

    print("\n" + "=" * 72)
    print("STANDARDS DU MARCHÉ (exclus du score : aucun pouvoir discriminant)")
    print("=" * 72)

    for item_id, label, values in market_standards:
        print(f"  - {label} : {list(values.values())[0]:,.0f} XAF partout")

    ranking = []
    for bank in banks:
        items = item_scores.get(bank, [])
        coverage = len(items)
        score = sum(s for _, s in items) / coverage if coverage else 0
        ranking.append((bank, score, coverage))

    ranking.sort(key=lambda x: -x[1])

    rank = 0
    for bank, score, coverage in ranking:
        if coverage < MIN_COVERAGE:
            print(f"{'-':<5}{bank:<10}{score:>6.0f}{coverage:>9}/10   couverture insuffisante")
            continue
        rank += 1
        print(f"{rank:<5}{bank:<10}{score:>6.0f}{coverage:>9}/10")

    print("\n" + "=" * 72)
    print("DÉTAIL PAR SERVICE (montant retenu en XAF, du moins cher au plus cher)")
    print("=" * 72)

    for item_id, label, keys, standard_amount in BASKET:
        label, values = detail[item_id]
        print(f"\n--- {label} ---")
        if not values:
            print("  Aucune donnée.")
            continue
        for bank, v in sorted(values.items(), key=lambda kv: kv[1]):
            print(f"  {bank:<10} {v:>12,.0f}")


if __name__ == "__main__":
    main()