import csv
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "data" / "db" / "banking_benchmark.db"
REF_DIR = BASE_DIR / "data" / "reference"

BANKS_CSV = REF_DIR / "banks_reference.csv"
NETWORK_CSV = REF_DIR / "network.csv"
PRODUCTS_CSV = REF_DIR / "products.csv"
DIGITAL_CSV = REF_DIR / "digital_features.csv"
FINANCIAL_CSV = REF_DIR / "financial_ratios.csv"

BANK_COLUMNS = [
    "bank_code", "bank_name", "legal_name", "head_office", "website",
    "tariff_source", "tariff_effective_date", "coverage_priority",
    "data_collection_status", "mobile_banking_app", "orange_money_integration",
    "mtn_momo_integration", "opening_hours_published", "opening_hours_source", "notes"
]

def load_csv_data(filepath, columns):
    if not filepath.exists():
        print(f"⚠️  Fichier introuvable : {filepath}")
        return []
    with filepath.open(newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        rows = []
        for row in reader:
            values = []
            for column in columns:
                value = row.get(column, "").strip() if row.get(column) else None
                values.append(value if value else None)
            rows.append(tuple(values))
        return rows


def main() -> None:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")

    # 1. Banks
    bank_rows = load_csv_data(BANKS_CSV, BANK_COLUMNS)
    if bank_rows:
        update_set = ", ".join(f"{col} = excluded.{col}" for col in BANK_COLUMNS if col != "bank_code")
        sql = f"""
        INSERT INTO banks ({", ".join(BANK_COLUMNS)})
        VALUES ({", ".join(["?"] * len(BANK_COLUMNS))})
        ON CONFLICT(bank_code) DO UPDATE SET {update_set}
        """
        conn.executemany(sql, bank_rows)
        print(f"[OK] {len(bank_rows)} banques chargees / mises a jour.")

    # 2. Network
    net_cols = ["bank_code", "region", "city", "agency_count", "source", "observation_date"]
    net_rows = load_csv_data(NETWORK_CSV, net_cols)
    if net_rows:
        conn.execute("DELETE FROM network;")
        cleaned_net = []
        for r in net_rows:
            r_list = list(r)
            if r_list[3] is not None and r_list[3] != "":
                try:
                    r_list[3] = int(r_list[3])
                except ValueError:
                    r_list[3] = None
            cleaned_net.append(tuple(r_list))
        sql = f"INSERT INTO network ({', '.join(net_cols)}) VALUES ({', '.join(['?'] * len(net_cols))})"
        conn.executemany(sql, cleaned_net)
        print(f"[OK] {len(cleaned_net)} lignes reseau chargees.")

    # 3. Products
    prod_cols = [
        "bank_code", "product_category", "product_name", "available",
        "conditions_published", "published_rate", "published_duration",
        "source", "observation_date"
    ]
    prod_rows = load_csv_data(PRODUCTS_CSV, prod_cols)
    if prod_rows:
        conn.execute("DELETE FROM products;")
        sql = f"INSERT INTO products ({', '.join(prod_cols)}) VALUES ({', '.join(['?'] * len(prod_cols))})"
        conn.executemany(sql, prod_rows)
        print(f"[OK] {len(prod_rows)} lignes produits chargees.")

    # 4. Digital features
    dig_cols = ["bank_code", "feature_key", "feature_name", "available", "source", "observation_date"]
    dig_rows = load_csv_data(DIGITAL_CSV, dig_cols)
    if dig_rows:
        conn.execute("DELETE FROM digital_features;")
        sql = f"INSERT INTO digital_features ({', '.join(dig_cols)}) VALUES ({', '.join(['?'] * len(dig_cols))})"
        conn.executemany(sql, dig_rows)
        print(f"[OK] {len(dig_rows)} lignes digital chargees.")

    # 5. Financial ratios
    fin_cols = ["bank_code", "year", "metric_key", "metric_name", "value", "unit", "source", "publication_date"]
    fin_rows = load_csv_data(FINANCIAL_CSV, fin_cols)
    if fin_rows:
        conn.execute("DELETE FROM financial_data;")
        cleaned_fin = []
        for r in fin_rows:
            r_list = list(r)
            if r_list[1] is not None:
                try:
                    r_list[1] = int(r_list[1])
                except ValueError:
                    r_list[1] = 2024
            if r_list[4] is not None and r_list[4] != "":
                try:
                    r_list[4] = float(r_list[4])
                except ValueError:
                    r_list[4] = None
            cleaned_fin.append(tuple(r_list))
        sql = f"INSERT INTO financial_data ({', '.join(fin_cols)}) VALUES ({', '.join(['?'] * len(fin_cols))})"
        conn.executemany(sql, cleaned_fin)
        print(f"[OK] {len(cleaned_fin)} lignes financieres chargees.")

    conn.commit()
    conn.close()
    print("[TERMINE] Toutes les donnees de reference ont ete chargees avec succes.")


if __name__ == "__main__":
    main()