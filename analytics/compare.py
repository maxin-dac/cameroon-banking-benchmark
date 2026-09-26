"""
compare.py — Comparaisons factuelles, sans score ni classement.

Ce module fournit des fonctions de lecture et de mise en regard
des données bancaires. Aucun scoring, aucun ranking, aucune
interprétation de type « bon » ou « mauvais ».
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "data" / "db" / "banking_benchmark.db"


# ── Connexion ────────────────────────────────────────────────

def connect():
    """Ouvre une connexion SQLite en mode Row."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ── Tarifs ───────────────────────────────────────────────────

def row_value(row, std=None):
    """Extrait la valeur numérique d'une ligne tarifaire.
    Si la ligne est une formule variable (rate_pct), évalue au montant `std`."""
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
    """Formatte une ligne tarifaire en texte lisible."""
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
    return "—"


def pick_row(conn, bank, keys):
    """Sélectionne la ligne tarifaire pertinente pour un service donné.
    Priorité au canal digital quand il existe."""
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


# Panier standard pour la comparaison tarifaire
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


def get_tariff_comparison(conn):
    """Retourne les valeurs tarifaires du panier standard pour toutes les banques.
    Pas de tri par prix, pas de best/worst. Données brutes."""
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


# ── Réseau ───────────────────────────────────────────────────

def get_network_summary(conn):
    """Retourne le nombre d'agences par banque, par région.
    Données brutes, pas de classement."""
    rows = conn.execute("""
        SELECT n.bank_code, b.bank_name, n.region, n.city, n.agency_count,
               n.source, n.observation_date
        FROM network n
        JOIN banks b ON n.bank_code = b.bank_code
        ORDER BY b.bank_name, n.region, n.city
    """).fetchall()
    return [dict(r) for r in rows]


def get_network_totals(conn):
    """Retourne le total d'agences par banque (somme de toutes les villes).
    Pas de classement."""
    rows = conn.execute("""
        SELECT n.bank_code, b.bank_name, SUM(n.agency_count) as total_agencies
        FROM network n
        JOIN banks b ON n.bank_code = b.bank_code
        WHERE n.agency_count IS NOT NULL
        GROUP BY n.bank_code
        ORDER BY b.bank_name
    """).fetchall()
    return [dict(r) for r in rows]


# ── Produits ─────────────────────────────────────────────────

def get_product_matrix(conn):
    """Retourne la matrice produits par banque.
    Colonnes : banque × catégorie de produit → oui/non/inconnu."""
    rows = conn.execute("""
        SELECT p.bank_code, b.bank_name, p.product_category, p.product_name,
               p.available, p.conditions_published, p.published_rate,
               p.published_duration, p.source
        FROM products p
        JOIN banks b ON p.bank_code = b.bank_code
        ORDER BY b.bank_name, p.product_category
    """).fetchall()
    return [dict(r) for r in rows]


# ── Digital ──────────────────────────────────────────────────

def get_digital_matrix(conn):
    """Retourne la matrice des fonctionnalités digitales par banque.
    Chaque fonctionnalité est oui/non/inconnu, sans note de maturité."""
    rows = conn.execute("""
        SELECT d.bank_code, b.bank_name, d.feature_key, d.feature_name,
               d.available, d.source, d.observation_date
        FROM digital_features d
        JOIN banks b ON d.bank_code = b.bank_code
        ORDER BY b.bank_name, d.feature_key
    """).fetchall()
    return [dict(r) for r in rows]


# ── Données financières ─────────────────────────────────────

def get_financial_overview(conn, year=None):
    """Retourne les ratios financiers publiés par la COBAC.
    Présentés tels quels, sans interprétation."""
    if year:
        rows = conn.execute("""
            SELECT f.bank_code, b.bank_name, f.year, f.metric_key, f.metric_name,
                   f.value, f.unit, f.source, f.publication_date
            FROM financial_data f
            JOIN banks b ON f.bank_code = b.bank_code
            WHERE f.year = ?
            ORDER BY b.bank_name, f.metric_key
        """, (year,)).fetchall()
    else:
        rows = conn.execute("""
            SELECT f.bank_code, b.bank_name, f.year, f.metric_key, f.metric_name,
                   f.value, f.unit, f.source, f.publication_date
            FROM financial_data f
            JOIN banks b ON f.bank_code = b.bank_code
            ORDER BY f.year DESC, b.bank_name, f.metric_key
        """).fetchall()
    return [dict(r) for r in rows]


# ── Services accessibilité (depuis banks) ────────────────────

def get_accessibility_overview(conn):
    """Retourne les données d'accessibilité depuis la table banks :
    mobile banking, intégrations mobile money, horaires."""
    rows = conn.execute("""
        SELECT bank_code, bank_name, mobile_banking_app,
               orange_money_integration, mtn_momo_integration,
               opening_hours_published, opening_hours_source
        FROM banks
        ORDER BY bank_name
    """).fetchall()
    return [dict(r) for r in rows]
