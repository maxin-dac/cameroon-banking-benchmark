import argparse
import csv
import sqlite3
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "data" / "db" / "banking_benchmark.db"
TARIFFS_DIR = BASE_DIR / "data" / "processed" / "tariffs"


REQUIRED_COLUMNS = [
    "bank_code",
    "bank_name",
    "customer_segment",
    "service_category",
    "service_key",
    "service_name_original",
    "channel",
    "fee_nature",
    "billing_unit",
    "original_amount_ht",
    "original_unit",
    "amount_annual_ht",
    "amount_per_operation_ht",
    "amount_one_time_ht",
    "amount_condition_ht",
    "rate_pct",
    "min_amount_ht",
    "max_amount_ht",
    "currency",
    "tax_status",
    "conditions",
    "source_document",
    "source_date",
    "is_comparable",
    "notes",
]


ALLOWED_CUSTOMER_SEGMENTS = {
    "individual_salaried",
    "individual_non_salaried",
    "individual_student",
    "all_individuals",
}


ALLOWED_FEE_NATURES = {
    "recurring",
    "transactional",
    "one_time",
    "condition",
}


ALLOWED_BILLING_UNITS = {
    "annual",
    "monthly",
    "quarterly",
    "semiannual",
    "per_operation",
    "one_off",
    "not_applicable",
}


INSERT_SQL = """
INSERT INTO tariffs (
    bank_code,
    customer_segment,
    service_category,
    service_key,
    service_name_original,
    channel,
    fee_nature,
    billing_unit,
    original_amount_ht,
    original_unit,
    amount_annual_ht,
    amount_per_operation_ht,
    amount_one_time_ht,
    amount_condition_ht,
    rate_pct,
    min_amount_ht,
    max_amount_ht,
    currency,
    tax_status,
    conditions,
    source_document,
    source_date,
    is_comparable,
    notes
)
VALUES (
    :bank_code,
    :customer_segment,
    :service_category,
    :service_key,
    :service_name_original,
    :channel,
    :fee_nature,
    :billing_unit,
    :original_amount_ht,
    :original_unit,
    :amount_annual_ht,
    :amount_per_operation_ht,
    :amount_one_time_ht,
    :amount_condition_ht,
    :rate_pct,
    :min_amount_ht,
    :max_amount_ht,
    :currency,
    :tax_status,
    :conditions,
    :source_document,
    :source_date,
    :is_comparable,
    :notes
)
"""


def clean_text(value):
    if value is None:
        return None

    value = value.strip()

    if value == "":
        return None

    return value


def to_float(value, field_name, errors):
    value = clean_text(value)

    if value is None:
        return None

    try:
        return float(value.replace(",", "."))
    except ValueError:
        errors.append(f"{field_name} doit être numérique")
        return None


def to_boolean_integer(value):
    value = clean_text(value)

    if value is None:
        return 1

    value = value.lower()

    if value in {"true", "1", "yes", "oui"}:
        return 1

    if value in {"false", "0", "no", "non"}:
        return 0

    return 1


def validate_date(value, field_name, errors):
    value = clean_text(value)

    if value is None:
        return None

    try:
        datetime.strptime(value, "%Y-%m-%d")
        return value
    except ValueError:
        errors.append(f"{field_name} doit être au format YYYY-MM-DD")
        return None


def validate_row(row, bank_codes):
    errors = []

    bank_code = clean_text(row.get("bank_code"))
    customer_segment = clean_text(row.get("customer_segment"))
    service_category = clean_text(row.get("service_category"))
    service_key = clean_text(row.get("service_key"))
    channel = clean_text(row.get("channel"))
    fee_nature = clean_text(row.get("fee_nature"))
    billing_unit = clean_text(row.get("billing_unit"))
    tax_status = clean_text(row.get("tax_status"))
    currency = clean_text(row.get("currency")) or "XAF"

    if bank_code not in bank_codes:
        errors.append(f"bank_code inconnu : {bank_code}")

    if customer_segment not in ALLOWED_CUSTOMER_SEGMENTS:
        errors.append(f"customer_segment invalide : {customer_segment}")

    if not service_category:
        errors.append("service_category obligatoire")

    if not service_key:
        errors.append("service_key obligatoire")

    if fee_nature not in ALLOWED_FEE_NATURES:
        errors.append(f"fee_nature invalide : {fee_nature}")

    if billing_unit not in ALLOWED_BILLING_UNITS:
        errors.append(f"billing_unit invalide : {billing_unit}")

    if tax_status is None or tax_status.upper() != "HT":
        errors.append("tax_status doit être HT")

    original_amount_ht = to_float(
        row.get("original_amount_ht"),
        "original_amount_ht",
        errors,
    )

    amount_annual_ht = to_float(
        row.get("amount_annual_ht"),
        "amount_annual_ht",
        errors,
    )

    amount_per_operation_ht = to_float(
        row.get("amount_per_operation_ht"),
        "amount_per_operation_ht",
        errors,
    )

    amount_one_time_ht = to_float(
        row.get("amount_one_time_ht"),
        "amount_one_time_ht",
        errors,
    )

    amount_condition_ht = to_float(
        row.get("amount_condition_ht"),
        "amount_condition_ht",
        errors,
    )

    rate_pct = to_float(
        row.get("rate_pct"),
        "rate_pct",
        errors,
    )

    min_amount_ht = to_float(
        row.get("min_amount_ht"),
        "min_amount_ht",
        errors,
    )

    max_amount_ht = to_float(
        row.get("max_amount_ht"),
        "max_amount_ht",
        errors,
    )

    source_date = validate_date(
        row.get("source_date"),
        "source_date",
        errors,
    )

    amount_values = {
        "original_amount_ht": original_amount_ht,
        "amount_annual_ht": amount_annual_ht,
        "amount_per_operation_ht": amount_per_operation_ht,
        "amount_one_time_ht": amount_one_time_ht,
        "amount_condition_ht": amount_condition_ht,
        "rate_pct": rate_pct,
        "min_amount_ht": min_amount_ht,
        "max_amount_ht": max_amount_ht,
    }

    for field_name, amount_value in amount_values.items():
        if amount_value is not None and amount_value < 0:
            errors.append(f"{field_name} ne peut pas être négatif")

    if fee_nature == "recurring" and amount_annual_ht is None:
        errors.append("amount_annual_ht est obligatoire pour un frais récurrent")

    if fee_nature == "transactional":
        if amount_per_operation_ht is None and rate_pct is None:
            errors.append(
                "un frais transactionnel doit avoir amount_per_operation_ht ou rate_pct"
            )

    if fee_nature == "one_time" and amount_one_time_ht is None:
        errors.append("amount_one_time_ht est obligatoire pour un frais ponctuel")

    if fee_nature == "condition" and amount_condition_ht is None:
        errors.append("amount_condition_ht est obligatoire pour une condition")

    cleaned_row = {
        "bank_code": bank_code,
        "customer_segment": customer_segment,
        "service_category": service_category,
        "service_key": service_key,
        "service_name_original": clean_text(row.get("service_name_original")),
        "channel": channel,
        "fee_nature": fee_nature,
        "billing_unit": billing_unit,
        "original_amount_ht": original_amount_ht,
        "original_unit": clean_text(row.get("original_unit")),
        "amount_annual_ht": amount_annual_ht,
        "amount_per_operation_ht": amount_per_operation_ht,
        "amount_one_time_ht": amount_one_time_ht,
        "amount_condition_ht": amount_condition_ht,
        "rate_pct": rate_pct,
        "min_amount_ht": min_amount_ht,
        "max_amount_ht": max_amount_ht,
        "currency": currency,
        "tax_status": "HT",
        "conditions": clean_text(row.get("conditions")),
        "source_document": clean_text(row.get("source_document")),
        "source_date": source_date,
        "is_comparable": to_boolean_integer(row.get("is_comparable")),
        "notes": clean_text(row.get("notes")),
    }

    return cleaned_row, errors


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Importe les tarifs normalisés dans SQLite."
    )

    parser.add_argument(
        "--truncate",
        action="store_true",
        help="Supprime toutes les lignes existantes de la table tariffs avant import.",
    )

    args = parser.parse_args()

    if not DB_PATH.exists():
        raise SystemExit(
            "Base de données introuvable. Exécute d'abord scripts/init_database.py."
        )

    if not TARIFFS_DIR.exists():
        raise SystemExit(
            f"Dossier introuvable : {TARIFFS_DIR}. "
            "Crée ce dossier et ajoute les fichiers CSV tarifaires."
        )

    csv_files = sorted(TARIFFS_DIR.glob("*.csv"))

    if not csv_files:
        raise SystemExit(
            f"Aucun fichier CSV trouvé dans {TARIFFS_DIR}."
        )

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")

    bank_codes = {
        row[0]
        for row in conn.execute("SELECT bank_code FROM banks")
    }

    if not bank_codes:
        raise SystemExit(
            "Aucune banque présente dans la base. "
            "Exécute d'abord scripts/load_banks.py."
        )

    if args.truncate:
        conn.execute("DELETE FROM tariffs")
        print("Table tariffs vidée avant import.")

    inserted_count = 0
    rejected_count = 0

    for csv_file in csv_files:
        print(f"Traitement du fichier : {csv_file.name}")

        with csv_file.open(newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            missing_columns = [
                column for column in REQUIRED_COLUMNS
                if column not in reader.fieldnames
            ]

            if missing_columns:
                raise SystemExit(
                    f"Colonnes manquantes dans {csv_file.name} : {missing_columns}"
                )

            for line_number, row in enumerate(reader, start=2):
                cleaned_row, errors = validate_row(row, bank_codes)

                if errors:
                    rejected_count += 1
                    error_message = " | ".join(errors)
                    print(f"[REJETÉ] {csv_file.name}:{line_number} -> {error_message}")
                    continue

                conn.execute(INSERT_SQL, cleaned_row)
                inserted_count += 1

    conn.commit()

    total_count = conn.execute("SELECT COUNT(*) FROM tariffs").fetchone()[0]

    conn.close()

    print("Import terminé.")
    print(f"Lignes insérées : {inserted_count}")
    print(f"Lignes rejetées : {rejected_count}")
    print(f"Total actuellement en base : {total_count}")


if __name__ == "__main__":
    main()