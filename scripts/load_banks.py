import csv
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "data" / "db" / "banking_benchmark.db"
BANKS_CSV = BASE_DIR / "data" / "reference" / "banks_reference.csv"

COLUMNS = [
    "bank_code", "bank_name", "legal_name", "head_office", "website",
    "tariff_source", "tariff_effective_date", "coverage_priority",
    "data_collection_status", "notes"
]

def main() -> None:
    if not BANKS_CSV.exists():
        raise SystemExit(f"Fichier introuvable : {BANKS_CSV}")

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")

    # utf-8-sig gère automatiquement le BOM (caractère invisible ajouté par Excel)
    with BANKS_CSV.open(newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        
        if not reader.fieldnames:
            raise SystemExit("Le fichier CSV est vide ou mal formaté.")

        rows = []
        for row in reader:
            values = []
            for column in COLUMNS:
                # Si la colonne n'existe pas dans le CSV ou est vide, on met None (NULL en SQL)
                value = row.get(column, "").strip() if row.get(column) else None
                values.append(value if value else None)
            rows.append(tuple(values))

    if not rows:
        print("Aucune donnée trouvée dans le CSV.")
        return

    sql = f"""
    INSERT OR REPLACE INTO banks (
        {", ".join(COLUMNS)}
    )
    VALUES (
        {", ".join(["?"] * len(COLUMNS))}
    )
    """

    conn.executemany(sql, rows)
    conn.commit()
    conn.close()
    print(f"{len(rows)} banques chargées avec succès.")

if __name__ == "__main__":
    main()