SERVICE_LABELS = {
    "account_opening": "Ouverture de compte",
    "account_maintenance": "Tenue de compte",
    "account_closure": "Clôture de compte",
    "rib_issuance": "Délivrance du RIB",
    "initial_deposit_salary": "Dépôt initial (salarié)",
    "initial_deposit_non_salary": "Dépôt initial (non salarié)",
    "initial_deposit_student": "Dépôt initial (étudiant)",
    "local_transfer_internal": "Virement interne",
    "local_transfer_systac": "Virement SYSTAC",
    "local_transfer_syigma": "Virement SYGMA",
    "standing_order_setup": "Mise en place virement permanent",
    "standing_order_execution": "Exécution virement permanent",
    "atm_withdrawal_own_bank": "Retrait GAB propre banque",
    "atm_withdrawal_gimac": "Retrait GAB confrère (GIMAC)",
    "card_basic_annual": "Carte locale (annuelle)",
    "card_gimac_annual": "Carte GIMAC (annuelle)",
    "card_visa_classic_annual": "Carte Visa Classic (annuelle)",
    "card_visa_gold_annual": "Carte Visa Gold (annuelle)",
    "cheque_bank_issue": "Chèque de banque",
    "cheque_certification": "Certification de chèque",
    "cheque_opposition": "Opposition chèque",
    "internet_banking_subscription": "Internet banking (abonnement)",
    "mobile_banking_subscription": "Mobile banking (abonnement)",
    "sms_banking_subscription": "SMS banking (abonnement)",
    "package_student_monthly": "Package étudiant",
}

CHANNEL_LABELS = {
    "branch": "Agence",
    "digital": "Digital",
    "internet": "Internet",
    "mobile": "Mobile",
    "atm": "GAB",
    "ussd": "USSD",
    "any": "Tous canaux",
    "not_applicable": "—",
}

def service_label(key):
    return SERVICE_LABELS.get(key, key)

def channel_label(key):
    return CHANNEL_LABELS.get(key, "—")