import hashlib
from datetime import datetime


# =========================
# KEYWORDS
# =========================
TENDER_KEYS = [
    "tender","bid","procurement","rfq","rfp",
    "auction","quotation","supply",
    "مناقصة","عطاء","توريد","شراء"
]

EGYPT_KEYS = ["egypt", "مصر", "cairo", "giza"]


# =========================
# CHECK TENDER
# =========================
def is_tender(text):
    t = text.lower()
    return any(k in t for k in TENDER_KEYS)


# =========================
# CHECK EGYPT
# =========================
def is_egypt(text):
    t = text.lower()
    return any(k in t for k in EGYPT_KEYS)


# =========================
# SCORE SYSTEM
# =========================
def score_item(item):
    text = item["title"] + item.get("full_text","")
    score = 0

    if is_tender(text):
        score += 4
    if is_egypt(text):
        score += 3
    if "gov" in item.get("source",""):
        score += 2
    if item.get("link"):
        score += 1

    return score


# =========================
# ID GENERATOR
# =========================
def gen_id(text):
    return hashlib.sha256(text.encode()).hexdigest()


# =========================
# CLEAN FILTER
# =========================
def process(items):
    clean = []

    for item in items:
        text = item["title"] + item.get("full_text","")

        if not is_tender(text):
            continue

        item["score"] = score_item(item)
        item["id"] = gen_id(item["title"] + item["link"])
        item["created_at"] = datetime.utcnow()

        clean.append(item)

    return clean
