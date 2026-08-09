import csv
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
REF = BASE / "data" / "reference" / "banks_reference.csv"
CRIT = BASE / "data" / "reference" / "publication_criteria.csv"

WEIGHTS = {"tarifs": 0.30, "finance": 0.30, "digital": 0.20, "gouvernance": 0.20}
TOTAL_CRITERIA = 12
MIN_CRITERIA = 4


def _read(path):
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def compute_index():
    by_bank = {}
    for row in _read(CRIT):
        by_bank.setdefault(row["bank_code"], []).append(row)

    ranked, unranked = [], []
    for bank in _read(REF):
        code = bank["bank_code"]
        rows = by_bank.get(code, [])

        pillars = {}
        for r in rows:
            pillars.setdefault(r["pillar"], []).append(float(r["value"]))
        pillar_scores = {p: round(sum(v) / len(v) * 100, 1) for p, v in pillars.items()}

        w = sum(WEIGHTS[p] for p in pillar_scores)
        index = round(sum(WEIGHTS[p] * s for p, s in pillar_scores.items()) / w, 1) if w else None

        entry = {
            "bank_code": code,
            "bank_name": bank["bank_name"],
            "index": index,
            "coverage": len(rows),
            "pillars": pillar_scores,
        }
        if index is not None and len(rows) >= MIN_CRITERIA:
            ranked.append(entry)
        else:
            unranked.append(entry)

    ranked.sort(key=lambda e: (-e["index"], e["bank_name"]))
    unranked.sort(key=lambda e: e["bank_name"])
    return ranked, unranked