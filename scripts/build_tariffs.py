#!/usr/bin/env python3
"""Construction du fichier tarifaire normalisé pour les 10 banques."""

from __future__ import annotations
import argparse
import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "data" / "processed" / "tariffs"
OUTPUT_FILE = OUTPUT_DIR / "tariffs_all_banks.csv"

SOURCE_DATE = "2026-06-22"

FIELDNAMES = [
    "bank_code", "bank_name", "customer_segment", "service_category",
    "service_key", "service_name_original", "channel", "fee_nature",
    "billing_unit", "original_amount_ht", "original_unit", "amount_annual_ht",
    "amount_per_operation_ht", "amount_one_time_ht", "amount_condition_ht",
    "rate_pct", "min_amount_ht", "max_amount_ht", "currency", "tax_status",
    "conditions", "source_document", "source_date", "is_comparable", "notes",
]

NUMERIC_FIELDS = [
    "original_amount_ht", "amount_annual_ht", "amount_per_operation_ht",
    "amount_one_time_ht", "amount_condition_ht", "rate_pct",
    "min_amount_ht", "max_amount_ht",
]

BANK_META = {
    "ACCESS": ("Access Bank Cameroon", "Conditions bancaires fusionnees Access Bank Cameroon Plc Q3 2026"),
    "AFRILAND": ("Afriland First Bank", "Conditions bancaires fusionnees Afriland First Bank 2026"),
    "BICEC": ("BICEC", "Conditions bancaires fusionnees BICEC Mars 2026"),
    "CCA": ("CCA-BANK", "Conditions bancaires fusionnees CCA-BANK T2 2026"),
    "CBC": ("Commercial Bank Cameroon", "Tarification Commercial Bank Cameroun Particulier"),
    "SCB": ("SCB Cameroun", "Conditions bancaires fusionnees SCB Cameroun Avril 2026"),
    "SGC": ("Société Générale Cameroun", "Conditions tarifaires Societe Generale Cameroun"),
    "UBA": ("UBA Cameroun", "Conditions bancaires fusionnees UBA Q3 2026"),
    "AGB": ("Africa Golden Bank", "Conditions tarifaires Africa Golden Bank"),
    "AFG": ("AFG Bank Cameroon", "Grille tarifaire AFG Bank particuliers"),
}

ROWS = []


def add(bank_code, customer_segment, service_category, service_key,
        service_name_original, channel, fee_nature, billing_unit,
        original_unit=None, **kwargs):
    if bank_code not in BANK_META:
        raise ValueError(f"bank_code inconnu : {bank_code}")

    bank_name, source_document = BANK_META[bank_code]
    if original_unit is None:
        original_unit = billing_unit

    row = {
        "bank_code": bank_code,
        "bank_name": bank_name,
        "customer_segment": customer_segment,
        "service_category": service_category,
        "service_key": service_key,
        "service_name_original": service_name_original,
        "channel": channel,
        "fee_nature": fee_nature,
        "billing_unit": billing_unit,
        "original_unit": original_unit,
        "currency": "XAF",
        "tax_status": "HT",
        "conditions": kwargs.get("conditions"),
        "source_document": source_document,
        "source_date": SOURCE_DATE,
        "is_comparable": kwargs.get("is_comparable", True),
        "notes": kwargs.get("notes"),
    }

    for field in NUMERIC_FIELDS:
        row[field] = kwargs.get(field)

    ROWS.append(row)


# === ACCESS BANK ===
add("ACCESS", "individual_salaried", "Compte", "initial_deposit_salary",
    "Initial deposit - Individual employee", "not_applicable", "condition",
    "not_applicable", amount_condition_ht=0)
add("ACCESS", "individual_non_salaried", "Compte", "initial_deposit_non_salary",
    "Initial deposit - Individuals without a salary", "not_applicable",
    "condition", "not_applicable", amount_condition_ht=25000)
add("ACCESS", "individual_student", "Compte", "initial_deposit_student",
    "Initial Deposit - Student Savings Account", "not_applicable", "condition",
    "not_applicable", amount_condition_ht=5000)
add("ACCESS", "all_individuals", "Compte", "account_maintenance",
    "Account maintenance fees Free", "not_applicable", "recurring", "annual",
    original_amount_ht=0, amount_annual_ht=0)
add("ACCESS", "all_individuals", "Compte", "account_closure",
    "Account closure fee - Natural person", "not_applicable", "one_time",
    "one_off", amount_one_time_ht=5000)
add("ACCESS", "all_individuals", "Compte", "rib_issuance",
    "Issuance of a bank identification statement Free", "not_applicable",
    "one_time", "one_off", amount_one_time_ht=0)
add("ACCESS", "all_individuals", "Virement", "local_transfer_internal",
    "Local Transfer (between Access Accounts) Free", "not_applicable",
    "transactional", "per_operation", amount_per_operation_ht=0)
add("ACCESS", "all_individuals", "Virement", "local_transfer_systac",
    "Interbank transfer Systac", "branch", "transactional", "per_operation",
    amount_per_operation_ht=500)
add("ACCESS", "all_individuals", "Virement", "local_transfer_syigma",
    "Interbank transfer Sygma", "branch", "transactional", "per_operation",
    amount_per_operation_ht=15000)
add("ACCESS", "all_individuals", "Retrait", "atm_withdrawal_own_bank",
    "Withdrawals with Access Bank ATMs Free", "atm", "transactional",
    "per_operation", amount_per_operation_ht=0)
add("ACCESS", "all_individuals", "Retrait", "atm_withdrawal_gimac",
    "Local withdrawal ATM in CEMAC", "atm", "transactional", "per_operation",
    rate_pct=1, min_amount_ht=500, max_amount_ht=1000,
    conditions="1% max 1 000 FCFA min 500 FCFA")
add("ACCESS", "all_individuals", "Carte", "card_visa_classic_annual",
    "VISA CLASSIC", "not_applicable", "recurring", "annual",
    original_unit="monthly", original_amount_ht=1500, amount_annual_ht=18000)
add("ACCESS", "all_individuals", "Carte", "card_visa_gold_annual",
    "VISA GOLD", "not_applicable", "recurring", "annual",
    original_unit="monthly", original_amount_ht=10000, amount_annual_ht=120000)
add("ACCESS", "all_individuals", "Banque à distance", "sms_banking_subscription",
    "E-ALERTS Subscription Free", "digital", "recurring", "annual",
    original_amount_ht=0, amount_annual_ht=0)
add("ACCESS", "all_individuals", "Chèque", "cheque_bank_issue",
    "Bank checks issuance fee", "branch", "transactional", "per_operation",
    amount_per_operation_ht=3500)

# === AFRILAND FIRST BANK ===
add("AFRILAND", "all_individuals", "Compte", "account_opening",
    "Ouverture du compte chèque", "not_applicable", "one_time", "one_off",
    amount_one_time_ht=0)
add("AFRILAND", "individual_salaried", "Compte", "account_maintenance",
    "Frais de tenue de compte - Compte chèque salarié", "not_applicable",
    "recurring", "annual", original_amount_ht=0, amount_annual_ht=0)
add("AFRILAND", "all_individuals", "Virement", "local_transfer_internal",
    "Virement émis sur nos caisses sur place", "branch", "transactional",
    "per_operation", amount_per_operation_ht=0)
add("AFRILAND", "all_individuals", "Virement", "local_transfer_systac",
    "Virement émis SYSTAC en agence", "branch", "transactional", "per_operation",
    amount_per_operation_ht=4000)
add("AFRILAND", "all_individuals", "Virement", "local_transfer_systac",
    "Virement SYSTAC en ligne E-FIRST", "digital", "transactional",
    "per_operation", amount_per_operation_ht=0,
    conditions="Virement en ligne vers autres banques SYSTAC")
add("AFRILAND", "all_individuals", "Virement", "local_transfer_syigma",
    "Frais virement émis SYGMA", "branch", "transactional", "per_operation",
    amount_per_operation_ht=30000)
add("AFRILAND", "all_individuals", "Virement", "standing_order_setup",
    "Virement permanent - mise en place", "not_applicable", "one_time",
    "one_off", amount_one_time_ht=5000)
add("AFRILAND", "all_individuals", "Retrait", "atm_withdrawal_own_bank",
    "Retrait de billets sur nos GABs", "atm", "transactional", "per_operation",
    amount_per_operation_ht=0)
add("AFRILAND", "all_individuals", "Retrait", "atm_withdrawal_gimac",
    "Retrait de billets sur les GABs/DAB confrères", "atm", "transactional",
    "per_operation", amount_per_operation_ht=500, conditions="GIMAC uniquement")
add("AFRILAND", "all_individuals", "Carte", "card_basic_annual",
    "Carte Fellow", "not_applicable", "recurring", "annual",
    original_amount_ht=6000, amount_annual_ht=6000)
add("AFRILAND", "all_individuals", "Carte", "card_visa_classic_annual",
    "I-Card VISA Classic et MasterCard Debit", "not_applicable", "recurring",
    "annual", original_amount_ht=40000, amount_annual_ht=40000)
add("AFRILAND", "all_individuals", "Carte", "card_visa_gold_annual",
    "I-Card VISA Gold et MasterCard Gold", "not_applicable", "recurring",
    "annual", original_amount_ht=70000, amount_annual_ht=70000)
add("AFRILAND", "all_individuals", "Chèque", "cheque_bank_issue",
    "Chèque banque ordinaire sur compte client", "branch", "transactional",
    "per_operation", amount_per_operation_ht=3000)
add("AFRILAND", "all_individuals", "Chèque", "cheque_certification",
    "Chèque certifié ordinaire", "branch", "transactional", "per_operation",
    amount_per_operation_ht=2500)
add("AFRILAND", "all_individuals", "Banque à distance", "internet_banking_subscription",
    "E-FIRST compte courant", "digital", "recurring", "annual",
    original_unit="monthly", original_amount_ht=0, amount_annual_ht=0)
add("AFRILAND", "all_individuals", "Banque à distance", "sms_banking_subscription",
    "SMS FIRST", "digital", "recurring", "annual", original_unit="monthly",
    original_amount_ht=2000, amount_annual_ht=24000)

# === BICEC ===
add("BICEC", "all_individuals", "Compte", "account_opening",
    "Ouverture d'un compte", "not_applicable", "one_time", "one_off",
    amount_one_time_ht=0)
add("BICEC", "individual_salaried", "Compte", "initial_deposit_salary",
    "Dépôt minimum à l'ouverture avec domiciliation de salaire", "not_applicable",
    "condition", "not_applicable", amount_condition_ht=10000)
add("BICEC", "individual_non_salaried", "Compte", "initial_deposit_non_salary",
    "Dépôt minimum à l'ouverture sans domiciliation de salaire", "not_applicable",
    "condition", "not_applicable", amount_condition_ht=50000)
add("BICEC", "all_individuals", "Compte", "account_maintenance",
    "Frais de tenue de compte à vue", "not_applicable", "recurring", "annual",
    original_amount_ht=0, amount_annual_ht=0)
add("BICEC", "all_individuals", "Compte", "account_closure",
    "Clôture de compte à vue", "not_applicable", "one_time", "one_off",
    amount_one_time_ht=5000)
add("BICEC", "all_individuals", "Compte", "rib_issuance",
    "Édition de RIB", "not_applicable", "one_time", "one_off",
    amount_one_time_ht=0)
add("BICEC", "all_individuals", "Virement", "local_transfer_internal",
    "Virement de compte à compte BICEC", "branch", "transactional",
    "per_operation", amount_per_operation_ht=0)
add("BICEC", "all_individuals", "Virement", "local_transfer_systac",
    "Virement vers un confrère en agence", "branch", "transactional",
    "per_operation", amount_per_operation_ht=8500)
add("BICEC", "all_individuals", "Virement", "local_transfer_systac",
    "Virement vers un confrère via BICEC.COM", "digital", "transactional",
    "per_operation", amount_per_operation_ht=500)
add("BICEC", "all_individuals", "Virement", "standing_order_setup",
    "Virement permanent - mise en place / modification / suppression",
    "not_applicable", "one_time", "one_off", amount_one_time_ht=0)
add("BICEC", "all_individuals", "Retrait", "atm_withdrawal_own_bank",
    "Retrait par carte BICEC dans nos distributeurs", "atm", "transactional",
    "per_operation", amount_per_operation_ht=0)
add("BICEC", "all_individuals", "Retrait", "atm_withdrawal_gimac",
    "Retrait sur autre banque par carte GIMAC", "atm", "transactional",
    "per_operation", amount_per_operation_ht=400)
add("BICEC", "all_individuals", "Carte", "card_gimac_annual",
    "Express / Express GIMAC", "not_applicable", "recurring", "annual",
    original_unit="monthly", original_amount_ht=840, amount_annual_ht=10080)
add("BICEC", "all_individuals", "Carte", "card_visa_classic_annual",
    "Visa Classic", "not_applicable", "recurring", "annual",
    original_unit="monthly", original_amount_ht=4200, amount_annual_ht=50400)
add("BICEC", "all_individuals", "Carte", "card_visa_gold_annual",
    "Visa Gold", "not_applicable", "recurring", "annual",
    original_unit="monthly", original_amount_ht=7718, amount_annual_ht=92616)
add("BICEC", "all_individuals", "Chèque", "cheque_bank_issue",
    "Chèque de banque", "branch", "transactional", "per_operation",
    amount_per_operation_ht=5000)
add("BICEC", "all_individuals", "Chèque", "cheque_certification",
    "Certification de chèque", "branch", "transactional", "per_operation",
    amount_per_operation_ht=5000)
add("BICEC", "all_individuals", "Chèque", "cheque_opposition",
    "Opposition sur chèque", "branch", "transactional", "per_operation",
    amount_per_operation_ht=13500)
add("BICEC", "all_individuals", "Banque à distance", "internet_banking_subscription",
    "BICEC.COM Option Classic", "digital", "recurring", "annual",
    original_unit="monthly", original_amount_ht=1750, amount_annual_ht=21000)
add("BICEC", "all_individuals", "Banque à distance", "mobile_banking_subscription",
    "BIPAY souscription", "digital", "recurring", "annual",
    original_amount_ht=0, amount_annual_ht=0)

# === CCA-BANK ===
add("CCA", "individual_salaried", "Compte", "initial_deposit_salary",
    "Dépôt minimum à l'ouverture de compte courant avec domiciliation de salaire",
    "not_applicable", "condition", "not_applicable", amount_condition_ht=0)
add("CCA", "individual_non_salaried", "Compte", "initial_deposit_non_salary",
    "Dépôt minimum à l'ouverture de compte courant sans domiciliation de salaire",
    "not_applicable", "condition", "not_applicable", amount_condition_ht=25000)
add("CCA", "individual_student", "Compte", "initial_deposit_student",
    "CCA-STARTER - Dépôt initial", "not_applicable", "condition",
    "not_applicable", amount_condition_ht=8000)
add("CCA", "all_individuals", "Compte", "account_maintenance",
    "Frais de tenue de compte courant", "not_applicable", "recurring", "annual",
    original_amount_ht=0, amount_annual_ht=0)
add("CCA", "all_individuals", "Compte", "account_closure",
    "Clôture de compte à la demande du client", "not_applicable", "one_time",
    "one_off", amount_one_time_ht=5000)
add("CCA", "all_individuals", "Compte", "rib_issuance",
    "Délivrance du relevé d'identité bancaire", "not_applicable", "one_time",
    "one_off", amount_one_time_ht=0)
add("CCA", "all_individuals", "Virement", "local_transfer_internal",
    "Virement de compte à compte nos caisses", "branch", "transactional",
    "per_operation", amount_per_operation_ht=0)
add("CCA", "all_individuals", "Virement", "local_transfer_systac",
    "Virement vers un confrère", "branch", "transactional", "per_operation",
    amount_per_operation_ht=5000)
add("CCA", "all_individuals", "Virement", "local_transfer_systac",
    "Virement vers un confrère via C-Online", "digital", "transactional",
    "per_operation", amount_per_operation_ht=3000, conditions="Via C-Online")
add("CCA", "all_individuals", "Virement", "local_transfer_syigma",
    "Virement vers un confrère SYGMA", "branch", "transactional",
    "per_operation", amount_per_operation_ht=25000)
add("CCA", "all_individuals", "Virement", "standing_order_setup",
    "Virement permanent - mise en place", "not_applicable", "one_time",
    "one_off", amount_one_time_ht=5000)
add("CCA", "all_individuals", "Retrait", "atm_withdrawal_own_bank",
    "Retrait d'espèces sur DAB CCA-BANK", "atm", "transactional",
    "per_operation", amount_per_operation_ht=0)
add("CCA", "all_individuals", "Retrait", "atm_withdrawal_gimac",
    "Retrait d'espèces sur DAB réseau GIMAC autre banque", "atm",
    "transactional", "per_operation", rate_pct=1, min_amount_ht=500,
    max_amount_ht=1000, conditions="500 < 1% < 1000")
add("CCA", "all_individuals", "Carte", "card_gimac_annual",
    "Carte Cauris GIMAC", "not_applicable", "recurring", "annual",
    original_amount_ht=8000, amount_annual_ht=8000)
add("CCA", "all_individuals", "Carte", "card_visa_classic_annual",
    "VISA EQUILIBRE (CLASSIC)", "not_applicable", "recurring", "annual",
    original_amount_ht=30000, amount_annual_ht=30000)
add("CCA", "all_individuals", "Chèque", "cheque_bank_issue",
    "Émission chèque de banque", "branch", "transactional", "per_operation",
    amount_per_operation_ht=5000, conditions="24 heures")
add("CCA", "all_individuals", "Chèque", "cheque_certification",
    "Certification de chèques", "branch", "transactional", "per_operation",
    amount_per_operation_ht=5000, conditions="24 heures")
add("CCA", "all_individuals", "Banque à distance", "internet_banking_subscription",
    "Abonnement C-Online particulier", "digital", "recurring", "annual",
    original_unit="monthly", original_amount_ht=1500, amount_annual_ht=18000)
add("CCA", "all_individuals", "Banque à distance", "sms_banking_subscription",
    "C-Alert / SMS Banking", "digital", "recurring", "annual",
    original_amount_ht=0, amount_annual_ht=0)
add("CCA", "individual_student", "Package", "package_student_monthly",
    "STUDENT BANKING CCA STARTER", "not_applicable", "recurring", "annual",
    original_unit="monthly", original_amount_ht=500, amount_annual_ht=6000)

# === COMMERCIAL BANK CAMEROON ===
add("CBC", "all_individuals", "Compte", "account_opening",
    "Ouverture de compte", "not_applicable", "one_time", "one_off",
    amount_one_time_ht=0)
add("CBC", "individual_salaried", "Compte", "initial_deposit_salary",
    "Dépôt initial particuliers salariés", "not_applicable", "condition",
    "not_applicable", amount_condition_ht=0)
add("CBC", "individual_non_salaried", "Compte", "initial_deposit_non_salary",
    "Dépôt initial particuliers non salariés", "not_applicable", "condition",
    "not_applicable", amount_condition_ht=50000)
add("CBC", "all_individuals", "Compte", "account_maintenance",
    "Frais de tenue de compte", "not_applicable", "recurring", "annual",
    original_amount_ht=0, amount_annual_ht=0)
add("CBC", "all_individuals", "Compte", "account_closure",
    "Frais de clôture de compte", "not_applicable", "one_time", "one_off",
    amount_one_time_ht=5000)
add("CBC", "all_individuals", "Virement", "local_transfer_internal",
    "Virement interne - frais d'exécution SP", "branch", "transactional",
    "per_operation", amount_per_operation_ht=0)
add("CBC", "all_individuals", "Virement", "local_transfer_systac",
    "Virements SYSTAC", "branch", "transactional", "per_operation",
    amount_per_operation_ht=5000)
add("CBC", "all_individuals", "Virement", "local_transfer_systac",
    "Virement SYSTAC via CB-Online", "digital", "transactional",
    "per_operation", amount_per_operation_ht=100,
    conditions="Montant inférieur à 100 millions")
add("CBC", "all_individuals", "Virement", "local_transfer_syigma",
    "Virements SYGMA", "branch", "transactional", "per_operation",
    amount_per_operation_ht=20000)
add("CBC", "all_individuals", "Virement", "standing_order_setup",
    "Virements permanents / différés - mise en place", "not_applicable",
    "one_time", "one_off", amount_one_time_ht=5000)
add("CBC", "all_individuals", "Virement", "standing_order_execution",
    "Virements permanents / différés - exécution", "not_applicable",
    "transactional", "per_operation", amount_per_operation_ht=0)
add("CBC", "all_individuals", "Retrait", "atm_withdrawal_own_bank",
    "Retrait sur GAB CBC", "atm", "transactional", "per_operation",
    amount_per_operation_ht=0)
add("CBC", "all_individuals", "Retrait", "atm_withdrawal_gimac",
    "Frais retrait GAB confrère CEMAC", "atm", "transactional", "per_operation",
    rate_pct=1, min_amount_ht=500, max_amount_ht=1000,
    conditions="500 < 1% <= 1000")
add("CBC", "all_individuals", "Carte", "card_gimac_annual",
    "Carte GIMAC", "not_applicable", "recurring", "annual",
    original_amount_ht=10000, amount_annual_ht=10000)
add("CBC", "all_individuals", "Carte", "card_visa_classic_annual",
    "VISA CLASSIC", "not_applicable", "recurring", "annual",
    original_amount_ht=25000, amount_annual_ht=25000)
add("CBC", "all_individuals", "Carte", "card_visa_gold_annual",
    "CARTE VISA GOLD", "not_applicable", "recurring", "annual",
    original_amount_ht=100000, amount_annual_ht=100000)
add("CBC", "all_individuals", "Chèque", "cheque_bank_issue",
    "Chèque de banque - agence du compte", "branch", "transactional",
    "per_operation", amount_per_operation_ht=5000)
add("CBC", "all_individuals", "Chèque", "cheque_certification",
    "Certification de chèque sur place", "branch", "transactional",
    "per_operation", amount_per_operation_ht=3500)
add("CBC", "all_individuals", "Banque à distance", "internet_banking_subscription",
    "Abonnement mensuel BASIC CB-ONLINE", "digital", "recurring", "annual",
    original_unit="monthly", original_amount_ht=1000, amount_annual_ht=12000)
add("CBC", "all_individuals", "Banque à distance", "sms_banking_subscription",
    "Frais CBC INFOS (Alerte / Consultation solde)", "digital", "recurring",
    "annual", original_unit="monthly", original_amount_ht=500,
    amount_annual_ht=6000)
add("CBC", "individual_student", "Package", "package_student_monthly",
    "Abonnement Etudiant", "not_applicable", "recurring", "annual",
    original_amount_ht=0, amount_annual_ht=0)

# === SCB CAMEROUN ===
add("SCB", "all_individuals", "Virement", "local_transfer_internal",
    "Virement e-banknet en faveur client SCB", "digital", "transactional",
    "per_operation", amount_per_operation_ht=0)
add("SCB", "all_individuals", "Virement", "local_transfer_systac",
    "Virement e-banknet faveur client confrère", "digital", "transactional",
    "per_operation", amount_per_operation_ht=250)
add("SCB", "all_individuals", "Virement", "local_transfer_systac",
    "Virement manuel occasionnel faveur bénéficiaire confrère", "branch",
    "transactional", "per_operation", amount_per_operation_ht=7000,
    conditions="Par ligne bénéficiaire")
add("SCB", "all_individuals", "Virement", "standing_order_setup",
    "Virement permanent (ouverture)", "not_applicable", "one_time", "one_off",
    amount_one_time_ht=3500)
add("SCB", "all_individuals", "Virement", "standing_order_execution",
    "Traitement du virement permanent", "not_applicable", "transactional",
    "per_operation", amount_per_operation_ht=500)
add("SCB", "all_individuals", "Retrait", "atm_withdrawal_own_bank",
    "Retrait automate SCB", "atm", "transactional", "per_operation",
    amount_per_operation_ht=0)
add("SCB", "all_individuals", "Carte", "card_gimac_annual",
    "GIMAC Electrik", "not_applicable", "recurring", "annual",
    original_unit="monthly", original_amount_ht=1006, amount_annual_ht=12072)
add("SCB", "all_individuals", "Carte", "card_basic_annual",
    "Aisance Mastercard", "not_applicable", "recurring", "annual",
    original_unit="monthly", original_amount_ht=1425, amount_annual_ht=17100)
add("SCB", "all_individuals", "Chèque", "cheque_bank_issue",
    "Émission chèque de banque", "branch", "transactional", "per_operation",
    amount_per_operation_ht=3500)
add("SCB", "all_individuals", "Banque à distance", "internet_banking_subscription",
    "E-Banknet", "digital", "recurring", "annual", original_unit="quarterly",
    original_amount_ht=5000, amount_annual_ht=20000)
add("SCB", "all_individuals", "Banque à distance", "sms_banking_subscription",
    "Avertis", "digital", "recurring", "annual", original_unit="monthly",
    original_amount_ht=1250, amount_annual_ht=15000)

# === SOCIÉTÉ GÉNÉRALE CAMEROUN ===
add("SGC", "all_individuals", "Compte", "account_opening",
    "Ouverture de compte", "not_applicable", "one_time", "one_off",
    amount_one_time_ht=0)
add("SGC", "individual_salaried", "Compte", "initial_deposit_salary",
    "Dépôt minimum à l'ouverture avec domiciliation de salaire", "not_applicable",
    "condition", "not_applicable", amount_condition_ht=0)
add("SGC", "individual_non_salaried", "Compte", "initial_deposit_non_salary",
    "Dépôt minimum à l'ouverture sans domiciliation de salaire", "not_applicable",
    "condition", "not_applicable", amount_condition_ht=50000)
add("SGC", "all_individuals", "Compte", "account_maintenance",
    "Frais de tenue de compte", "not_applicable", "recurring", "annual",
    original_amount_ht=0, amount_annual_ht=0)
add("SGC", "all_individuals", "Compte", "account_closure",
    "Frais de fermeture de compte à la demande du client", "not_applicable",
    "one_time", "one_off", amount_one_time_ht=5000)
add("SGC", "all_individuals", "Compte", "rib_issuance",
    "Délivrance du relevé d'identité bancaire", "not_applicable", "one_time",
    "one_off", amount_one_time_ht=0)
add("SGC", "all_individuals", "Virement", "local_transfer_internal",
    "Virement de compte à compte SG Cameroun", "not_applicable",
    "transactional", "per_operation", amount_per_operation_ht=0)
add("SGC", "all_individuals", "Virement", "local_transfer_systac",
    "Virement vers un confrère via SG CONNECT", "digital", "transactional",
    "per_operation", amount_per_operation_ht=1000,
    conditions="Tranche 0 à 999 000 XAF")
add("SGC", "all_individuals", "Virement", "local_transfer_systac",
    "Virement vers un confrère papier", "branch", "transactional",
    "per_operation", amount_per_operation_ht=10000)
add("SGC", "all_individuals", "Virement", "standing_order_setup",
    "Frais d'ouverture virement permanent", "not_applicable", "one_time",
    "one_off", amount_one_time_ht=5000)
add("SGC", "all_individuals", "Virement", "standing_order_execution",
    "Traitement du virement permanent", "not_applicable", "transactional",
    "per_operation", amount_per_operation_ht=500,
    conditions="Hors port et confrère")
add("SGC", "all_individuals", "Retrait", "atm_withdrawal_own_bank",
    "Retrait par carte dans les distributeurs SG Cameroun", "atm",
    "transactional", "per_operation", amount_per_operation_ht=0)
add("SGC", "all_individuals", "Retrait", "atm_withdrawal_gimac",
    "Retrait par carte dans les distributeurs CEMAC", "atm", "transactional",
    "per_operation", amount_per_operation_ht=1000)
add("SGC", "all_individuals", "Carte", "card_visa_classic_annual",
    "VISA CLASSIC", "not_applicable", "recurring", "annual",
    original_unit="monthly", original_amount_ht=4000, amount_annual_ht=48000)
add("SGC", "all_individuals", "Carte", "card_visa_gold_annual",
    "VISA PREMIER", "not_applicable", "recurring", "annual",
    original_unit="monthly", original_amount_ht=7300, amount_annual_ht=87600,
    notes="Carte haut de gamme assimilée à Visa Gold dans le benchmark")
add("SGC", "all_individuals", "Banque à distance", "internet_banking_subscription",
    "Abonnement SG CAM CONNECT PACKAGE", "digital", "recurring", "annual",
    original_unit="monthly", original_amount_ht=1000, amount_annual_ht=12000)
add("SGC", "all_individuals", "Banque à distance", "sms_banking_subscription",
    "MESSALIA NEW VERSION SMS", "digital", "recurring", "annual",
    original_unit="monthly", original_amount_ht=1000, amount_annual_ht=12000)

# === UBA CAMEROUN ===
add("UBA", "all_individuals", "Compte", "account_opening",
    "Ouverture de compte", "not_applicable", "one_time", "one_off",
    amount_one_time_ht=0)
add("UBA", "individual_salaried", "Compte", "initial_deposit_salary",
    "Dépôt initial salariés", "not_applicable", "condition", "not_applicable",
    amount_condition_ht=0)
add("UBA", "individual_non_salaried", "Compte", "initial_deposit_non_salary",
    "Dépôt initial non salariés", "not_applicable", "condition",
    "not_applicable", amount_condition_ht=10000)
add("UBA", "individual_student", "Compte", "initial_deposit_student",
    "Dépôt initial étudiants", "not_applicable", "condition", "not_applicable",
    amount_condition_ht=5000)
add("UBA", "all_individuals", "Compte", "account_maintenance",
    "Frais de tenue de compte particuliers", "not_applicable", "recurring",
    "annual", original_amount_ht=0, amount_annual_ht=0)
add("UBA", "all_individuals", "Compte", "account_closure",
    "Frais de clôture particuliers", "not_applicable", "one_time", "one_off",
    amount_one_time_ht=5000)
add("UBA", "all_individuals", "Compte", "rib_issuance",
    "Relevé d'identité bancaire", "not_applicable", "one_time", "one_off",
    amount_one_time_ht=0)
add("UBA", "all_individuals", "Virement", "local_transfer_internal",
    "Virement de compte à compte", "not_applicable", "transactional",
    "per_operation", amount_per_operation_ht=0)
add("UBA", "all_individuals", "Virement", "local_transfer_systac",
    "Virement interbancaire SYSTAC", "branch", "transactional", "per_operation",
    amount_per_operation_ht=5000)
add("UBA", "all_individuals", "Virement", "local_transfer_systac",
    "Virement interbanque via banque à distance", "digital", "transactional",
    "per_operation", amount_per_operation_ht=500,
    conditions="Via internet banking / mobile banking")
add("UBA", "all_individuals", "Virement", "local_transfer_syigma",
    "Virement interbancaire SYGMA", "branch", "transactional", "per_operation",
    amount_per_operation_ht=25000)
add("UBA", "all_individuals", "Virement", "standing_order_setup",
    "Mise en place virement permanent", "not_applicable", "one_time",
    "one_off", amount_one_time_ht=2500,
    conditions="En faveur de soi-même ou de son enfant / conjoint")
add("UBA", "all_individuals", "Retrait", "atm_withdrawal_own_bank",
    "Retrait domestique via GAB/DAB UBA", "atm", "transactional",
    "per_operation", amount_per_operation_ht=0)
add("UBA", "all_individuals", "Retrait", "atm_withdrawal_gimac",
    "Retrait domestique via GAB/DAB autres banques", "atm", "transactional",
    "per_operation", amount_per_operation_ht=400, max_amount_ht=1000,
    conditions="400 FCFA max 1 000 FCFA")
add("UBA", "all_individuals", "Carte", "card_visa_classic_annual",
    "Visa Classic", "not_applicable", "recurring", "annual",
    original_unit="monthly", original_amount_ht=3000, amount_annual_ht=36000)
add("UBA", "all_individuals", "Carte", "card_visa_gold_annual",
    "Visa Gold", "not_applicable", "recurring", "annual",
    original_unit="monthly", original_amount_ht=12500, amount_annual_ht=150000)
add("UBA", "all_individuals", "Chèque", "cheque_bank_issue",
    "Émission chèque de banque", "branch", "transactional", "per_operation",
    amount_per_operation_ht=3500)
add("UBA", "all_individuals", "Chèque", "cheque_certification",
    "Chèque certifié - frais d'émission", "branch", "transactional",
    "per_operation", amount_per_operation_ht=5000)
add("UBA", "all_individuals", "Chèque", "cheque_opposition",
    "Opposition au paiement - émetteur", "branch", "transactional",
    "per_operation", amount_per_operation_ht=10000)
add("UBA", "all_individuals", "Banque à distance", "internet_banking_subscription",
    "Internet Banking particuliers", "digital", "recurring", "annual",
    original_unit="monthly", original_amount_ht=1000, amount_annual_ht=12000)
add("UBA", "all_individuals", "Banque à distance", "sms_banking_subscription",
    "Alertes SMS", "digital", "recurring", "annual", original_amount_ht=0,
    amount_annual_ht=0)

# === AFRICA GOLDEN BANK ===
add("AGB", "all_individuals", "Compte", "account_opening",
    "Ouverture de compte", "not_applicable", "one_time", "one_off",
    amount_one_time_ht=0)
add("AGB", "individual_salaried", "Compte", "initial_deposit_salary",
    "Ouverture de compte - particuliers salariés", "not_applicable",
    "condition", "not_applicable", amount_condition_ht=0)
add("AGB", "individual_non_salaried", "Compte", "initial_deposit_non_salary",
    "Ouverture de compte - particuliers non-salariés", "not_applicable",
    "condition", "not_applicable", amount_condition_ht=50000)
add("AGB", "all_individuals", "Compte", "account_maintenance",
    "Frais de tenue de compte", "not_applicable", "recurring", "annual",
    original_amount_ht=0, amount_annual_ht=0)
add("AGB", "all_individuals", "Compte", "account_closure",
    "Clôture de compte", "not_applicable", "one_time", "one_off",
    amount_one_time_ht=5000)
add("AGB", "all_individuals", "Compte", "rib_issuance",
    "Délivrance du RIB", "not_applicable", "one_time", "one_off",
    amount_one_time_ht=0)
add("AGB", "all_individuals", "Virement", "local_transfer_internal",
    "Virement de compte à compte", "not_applicable", "transactional",
    "per_operation", amount_per_operation_ht=0)
add("AGB", "all_individuals", "Virement", "local_transfer_systac",
    "Virement SYSTAC émis", "branch", "transactional", "per_operation",
    amount_per_operation_ht=4000)
add("AGB", "all_individuals", "Virement", "local_transfer_syigma",
    "Virement SYGMA émis", "branch", "transactional", "per_operation",
    amount_per_operation_ht=25000)
add("AGB", "all_individuals", "Virement", "standing_order_setup",
    "Mise en place du virement", "not_applicable", "one_time", "one_off",
    amount_one_time_ht=5000)
add("AGB", "all_individuals", "Retrait", "atm_withdrawal_own_bank",
    "Retrait sur GAB de l'établissement", "atm", "transactional",
    "per_operation", amount_per_operation_ht=0)
add("AGB", "all_individuals", "Retrait", "atm_withdrawal_gimac",
    "Retrait d'espèces sur GAB confrères GIMAC", "atm", "transactional",
    "per_operation", rate_pct=1, min_amount_ht=500,
    conditions="1% min 500 XAF")
add("AGB", "all_individuals", "Carte", "card_basic_annual",
    "Carte Access", "not_applicable", "recurring", "annual",
    original_amount_ht=8000, amount_annual_ht=8000)
add("AGB", "all_individuals", "Carte", "card_gimac_annual",
    "Carte My Combi", "not_applicable", "recurring", "annual",
    original_amount_ht=10000, amount_annual_ht=10000)
add("AGB", "all_individuals", "Chèque", "cheque_bank_issue",
    "Émission chèque de banque ordinaire", "branch", "transactional",
    "per_operation", amount_per_operation_ht=5000)
add("AGB", "all_individuals", "Chèque", "cheque_certification",
    "Émission chèque certifié ordinaire", "branch", "transactional",
    "per_operation", amount_per_operation_ht=5000)
add("AGB", "all_individuals", "Banque à distance", "internet_banking_subscription",
    "Golden Online particuliers", "digital", "recurring", "annual",
    original_unit="monthly", original_amount_ht=1000, amount_annual_ht=12000)
add("AGB", "all_individuals", "Banque à distance", "sms_banking_subscription",
    "Golden Mobile SMS - personnes physiques", "digital", "recurring",
    "annual", original_amount_ht=0, amount_annual_ht=0)

# === AFG BANK CAMEROON ===
add("AFG", "all_individuals", "Compte", "account_opening",
    "Ouverture de compte", "not_applicable", "one_time", "one_off",
    amount_one_time_ht=0)
add("AFG", "individual_salaried", "Compte", "initial_deposit_salary",
    "Dépôt initial compte chèque - particuliers salariés", "not_applicable",
    "condition", "not_applicable", amount_condition_ht=0)
add("AFG", "individual_non_salaried", "Compte", "initial_deposit_non_salary",
    "Dépôt initial compte chèque - particuliers non-salariés", "not_applicable",
    "condition", "not_applicable", amount_condition_ht=10000)
add("AFG", "individual_student", "Compte", "initial_deposit_student",
    "Dépôt initial compte chèque - particuliers étudiants", "not_applicable",
    "condition", "not_applicable", amount_condition_ht=5000)
add("AFG", "all_individuals", "Compte", "account_maintenance",
    "Frais de tenue de compte - particuliers non commerçants", "not_applicable",
    "recurring", "annual", original_amount_ht=0, amount_annual_ht=0,
    conditions="Particuliers non commerçants")
add("AFG", "all_individuals", "Compte", "account_closure",
    "Clôture de compte", "not_applicable", "one_time", "one_off",
    amount_one_time_ht=5000)
add("AFG", "all_individuals", "Compte", "rib_issuance",
    "Délivrance du Relevé d'Identité Bancaire", "not_applicable", "one_time",
    "one_off", amount_one_time_ht=0)
add("AFG", "all_individuals", "Virement", "local_transfer_internal",
    "Virement de compte à compte", "not_applicable", "transactional",
    "per_operation", amount_per_operation_ht=0)
add("AFG", "all_individuals", "Virement", "local_transfer_systac",
    "Virement interbancaire SYSTAC", "branch", "transactional", "per_operation",
    amount_per_operation_ht=5000)
add("AFG", "all_individuals", "Virement", "local_transfer_systac",
    "Frais de virement interbancaire SYSTAC via E-RELEVE", "digital",
    "transactional", "per_operation", amount_per_operation_ht=3000,
    conditions="Via E-Relevé / canal digital")
add("AFG", "all_individuals", "Virement", "local_transfer_syigma",
    "Virement interbancaire SYGMA", "branch", "transactional", "per_operation",
    amount_per_operation_ht=25000)
add("AFG", "all_individuals", "Virement", "standing_order_setup",
    "Mise en place du virement permanent", "not_applicable", "one_time",
    "one_off", amount_one_time_ht=10000,
    conditions="Hors fonctionnaires et salariés gratuits")
add("AFG", "all_individuals", "Retrait", "atm_withdrawal_own_bank",
    "Retrait billets dans les guichets automatiques de l'établissement",
    "atm", "transactional", "per_operation", amount_per_operation_ht=0)
add("AFG", "all_individuals", "Retrait", "atm_withdrawal_gimac",
    "Retrait d'espèces sur GAB confrères GIMAC", "atm", "transactional",
    "per_operation", rate_pct=1, min_amount_ht=500, max_amount_ht=1000,
    conditions="1% du montant avec min 500 FCFA max 1 000 FCFA")
add("AFG", "all_individuals", "Chèque", "cheque_bank_issue",
    "Émission chèque de banque", "branch", "transactional", "per_operation",
    amount_per_operation_ht=4000)
add("AFG", "all_individuals", "Banque à distance", "internet_banking_subscription",
    "AFG e-Bank", "digital", "recurring", "annual", original_unit="monthly",
    original_amount_ht=1500, amount_annual_ht=18000)


def validate_rows():
    for index, row in enumerate(ROWS, start=1):
        identifier = f"{row['bank_code']}:{row['service_key']}:{row['customer_segment']}:{index}"
        if row["fee_nature"] == "recurring" and row["amount_annual_ht"] is None:
            raise SystemExit(f"Ligne invalide {identifier} : amount_annual_ht obligatoire")
        if row["fee_nature"] == "transactional":
            if row["amount_per_operation_ht"] is None and row["rate_pct"] is None:
                raise SystemExit(f"Ligne invalide {identifier} : transactional exige amount_per_operation_ht ou rate_pct")
        if row["fee_nature"] == "one_time" and row["amount_one_time_ht"] is None:
            raise SystemExit(f"Ligne invalide {identifier} : amount_one_time_ht obligatoire")
        if row["fee_nature"] == "condition" and row["amount_condition_ht"] is None:
            raise SystemExit(f"Ligne invalide {identifier} : amount_condition_ht obligatoire")


def write_csv():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with OUTPUT_FILE.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        for row in ROWS:
            writer.writerow(row)


def check_output():
    with OUTPUT_FILE.open("r", encoding="utf-8", newline="") as file:
        reader = csv.reader(file)
        header = next(reader)
        if len(header) != len(FIELDNAMES):
            raise SystemExit(f"Header invalide : {len(header)} colonnes au lieu de {len(FIELDNAMES)}")
        count = 0
        for line_number, row in enumerate(reader, start=2):
            if len(row) != len(FIELDNAMES):
                raise SystemExit(f"Ligne invalide {line_number} : {len(row)} colonnes au lieu de {len(FIELDNAMES)}")
            count += 1
    return count


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--clean", action="store_true")
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if args.clean:
        for csv_file in OUTPUT_DIR.glob("*.csv"):
            csv_file.unlink()
        print(f"{len(list(OUTPUT_DIR.glob('*.csv')))} fichier(s) CSV supprimé(s).")

    validate_rows()
    write_csv()
    count = check_output()
    print(f"OK : {count} lignes tarifaires construites.")
    print(f"Fichier de sortie : {OUTPUT_FILE}")


if __name__ == "__main__":
    main()