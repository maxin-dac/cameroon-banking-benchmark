import csv
from datetime import date, datetime
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
REF = BASE / "data" / "reference" / "banks_reference.csv"
OUT = BASE / "data" / "reference" / "publication_criteria.csv"
OBS = date(2026, 8, 9)

LABELS = {
    "T1": ("tarifs", "T1_grille_publique", "Grille tarifaire publique disponible"),
    "T2": ("tarifs", "T2_grille_a_jour", "Grille tarifaire à jour (< 12 mois)"),
    "T3": ("tarifs", "T3_granularite", "Granularité particuliers + entreprises"),
    "D1": ("digital", "D1_site_web", "Site web officiel fonctionnel"),
    "G1": ("gouvernance", "G1_actionnariat_public", "Actionnariat rendu public"),
}

rows = []
with REF.open(encoding="utf-8") as f:
    for b in csv.DictReader(f):
        src = b.get("tariff_source") or ""
        eff = b.get("tariff_effective_date") or ""
        if b.get("tariff_publication") == "yes" and src:
            rows.append([b["bank_code"], *LABELS["T1"], 1, src, OBS.isoformat(), ""])
            if eff:
                d = datetime.strptime(eff, "%Y-%m-%d").date()
                fresh = int((OBS - d).days <= 365)
                note = "" if fresh else "Grille de plus de 12 mois"
                rows.append([b["bank_code"], *LABELS["T2"], fresh, src, OBS.isoformat(), note])
            rows.append([b["bank_code"], *LABELS["T3"], 1, src, OBS.isoformat(), ""])
        if b.get("website"):
            rows.append([b["bank_code"], *LABELS["D1"], 1, b["website"], OBS.isoformat(), ""])
        if b.get("group"):
            rows.append([b["bank_code"], *LABELS["G1"], 1, "banks_reference.csv", OBS.isoformat(), b["group"]])

with OUT.open("w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["bank_code", "pillar", "criterion_id", "criterion_label", "value", "source_url", "observation_date", "notes"])
    w.writerows(rows)

print(f"{len(rows)} critères écrits dans {OUT}")