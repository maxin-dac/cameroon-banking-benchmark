import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "data" / "db" / "banking_benchmark.db"

MIN_COVERAGE = 5

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


def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def row_value(row, std):
    if row["rate_pct"] is not None:
        if std is None:
            return None
        v = std * row["rate_pct"] / 100.0
        if row["min_amount_ht"] is not None:
            v = max(v, row["min_amount_ht"])
        if row["max_amount_ht"] is not None:
            v = min(v, row["max_amount_ht"])
        return v
    for f in ("amount_per_operation_ht", "amount_annual_ht", "amount_one_time_ht", "amount_condition_ht"):
        if row[f] is not None:
            return float(row[f])
    return None


def format_tariff(row):
    if row["rate_pct"] is not None:
        t = f"{row['rate_pct']}%"
        if row["min_amount_ht"] is not None:
            t += f" min {row['min_amount_ht']:,.0f}"
        if row["max_amount_ht"] is not None:
            t += f" max {row['max_amount_ht']:,.0f}"
        return t
    for f, s in (
        ("amount_per_operation_ht", "/ op"),
        ("amount_annual_ht", "/ an"),
        ("amount_one_time_ht", "une fois"),
        ("amount_condition_ht", "condition"),
    ):
        if row[f] is not None:
            return f"{row[f]:,.0f} {s}"
    return "-"


def pick_row(conn, bank, keys):
    for key in keys:
        rows = conn.execute(
            "SELECT * FROM tariffs WHERE bank_code = ? AND service_key = ?",
            (bank, key),
        ).fetchall()
        if not rows:
            continue
        dig = [r for r in rows if r["channel"] in ("digital", "internet", "mobile")]
        return dig[0] if dig else rows[0]
    return None


def item_values(conn):
    banks = [b["bank_code"] for b in conn.execute("SELECT bank_code FROM banks ORDER BY bank_code")]
    out = {}
    for item_id, label, keys, std in BASKET:
        vals = {}
        for b in banks:
            row = pick_row(conn, b, keys)
            if row is None:
                continue
            v = row_value(row, std)
            if v is not None:
                vals[b] = v
        out[item_id] = (label, vals, std)
    return out


def compute_ranking():
    conn = connect()
    detail = item_values(conn)
    conn.close()

    scores = {}
    for item_id, (label, vals, std) in detail.items():
        n = len(vals)
        if n < 2 or max(vals.values()) == min(vals.values()):
            continue
        for b, v in vals.items():
            worse = sum(1 for o in vals.values() if o > v)
            scores.setdefault(b, []).append(worse / (n - 1) * 100)

    ranking = []
    for b, items in scores.items():
        ranking.append({
            "bank_code": b,
            "score": round(sum(items) / len(items), 1),
            "coverage": len(items),
        })
    ranking.sort(key=lambda x: -x["score"])

    rank = 0
    for r in ranking:
        if r["coverage"] >= MIN_COVERAGE:
            rank += 1
            r["rank"] = rank
        else:
            r["rank"] = None
    return ranking


def market_standards():
    conn = connect()
    detail = item_values(conn)
    conn.close()
    return [
        (label, next(iter(vals.values())))
        for _, (label, vals, std) in detail.items()
        if len(vals) >= 2 and max(vals.values()) == min(vals.values())
    ]