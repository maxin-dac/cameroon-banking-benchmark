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
"""


def main() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()

    print(f"Base de données initialisée : {DB_PATH}")


if __name__ == "__main__":
    main()