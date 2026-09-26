from pathlib import Path
import sqlite3


BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "data" / "db" / "banking_benchmark.db"


SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS banks (
    bank_code TEXT PRIMARY KEY,
    bank_name TEXT NOT NULL,
    legal_name TEXT,
    head_office TEXT,
    website TEXT,
    tariff_source TEXT,
    tariff_effective_date TEXT,
    coverage_priority TEXT,
    data_collection_status TEXT,
    mobile_banking_app TEXT,
    orange_money_integration TEXT,
    mtn_momo_integration TEXT,
    opening_hours_published TEXT,
    opening_hours_source TEXT,
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS tariffs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    bank_code TEXT NOT NULL,
    customer_segment TEXT NOT NULL,
    service_category TEXT NOT NULL,
    service_key TEXT NOT NULL,
    service_name_original TEXT,

    channel TEXT,
    fee_nature TEXT NOT NULL,
    billing_unit TEXT NOT NULL,

    original_amount_ht REAL,
    original_unit TEXT,

    amount_annual_ht REAL,
    amount_per_operation_ht REAL,
    amount_one_time_ht REAL,
    amount_condition_ht REAL,

    rate_pct REAL,
    min_amount_ht REAL,
    max_amount_ht REAL,

    currency TEXT NOT NULL DEFAULT 'XAF',
    tax_status TEXT NOT NULL DEFAULT 'HT',

    conditions TEXT,
    source_document TEXT,
    source_date TEXT,

    is_comparable INTEGER NOT NULL DEFAULT 1,
    notes TEXT,

    created_at TEXT NOT NULL DEFAULT (datetime('now')),

    FOREIGN KEY (bank_code)
        REFERENCES banks (bank_code)
        ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_tariffs_bank_service
ON tariffs (
    bank_code,
    service_key,
    customer_segment,
    channel
);

CREATE INDEX IF NOT EXISTS idx_tariffs_fee_nature
ON tariffs (fee_nature);

CREATE INDEX IF NOT EXISTS idx_tariffs_service_key
ON tariffs (service_key);

-- ============================================================
-- Nouvelles tables v2 — données factuelles comparatives
-- ============================================================

-- Réseau d'agences par ville/région
CREATE TABLE IF NOT EXISTS network (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bank_code TEXT NOT NULL,
    region TEXT NOT NULL,
    city TEXT NOT NULL,
    agency_count INTEGER,
    source TEXT,
    observation_date TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (bank_code) REFERENCES banks(bank_code) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_network_bank
ON network (bank_code);

-- Matrice produits (présence/absence)
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bank_code TEXT NOT NULL,
    product_category TEXT NOT NULL,
    product_name TEXT NOT NULL,
    available TEXT NOT NULL DEFAULT 'inconnu',
    conditions_published TEXT DEFAULT 'non',
    published_rate TEXT,
    published_duration TEXT,
    source TEXT,
    observation_date TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (bank_code) REFERENCES banks(bank_code) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_products_bank
ON products (bank_code, product_category);

-- Fonctionnalités digitales (oui/non/inconnu)
CREATE TABLE IF NOT EXISTS digital_features (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bank_code TEXT NOT NULL,
    feature_key TEXT NOT NULL,
    feature_name TEXT NOT NULL,
    available TEXT NOT NULL DEFAULT 'inconnu',
    source TEXT,
    observation_date TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (bank_code) REFERENCES banks(bank_code) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_digital_bank
ON digital_features (bank_code, feature_key);

-- Données financières publiées (ratios COBAC, taille bilan)
CREATE TABLE IF NOT EXISTS financial_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bank_code TEXT NOT NULL,
    year INTEGER NOT NULL,
    metric_key TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    value REAL,
    unit TEXT NOT NULL,
    source TEXT,
    publication_date TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (bank_code) REFERENCES banks(bank_code) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_financial_bank_year
ON financial_data (bank_code, year, metric_key);
"""


def main() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA)

    # Migrations de schéma : ajouter les colonnes manquantes dans 'banks'
    existing_cols = {r[1] for r in conn.execute("PRAGMA table_info(banks)").fetchall()}
    new_cols = [
        ("mobile_banking_app", "TEXT"),
        ("orange_money_integration", "TEXT"),
        ("mtn_momo_integration", "TEXT"),
        ("opening_hours_published", "TEXT"),
        ("opening_hours_source", "TEXT"),
    ]
    for col_name, col_type in new_cols:
        if col_name not in existing_cols:
            conn.execute(f"ALTER TABLE banks ADD COLUMN {col_name} {col_type}")

    conn.commit()
    conn.close()

    print(f"Base de données initialisée et synchronisée : {DB_PATH}")


if __name__ == "__main__":
    main()