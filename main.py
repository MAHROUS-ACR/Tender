from crawler import crawl_links, extract_page
from processor import process
from firebase_config import db


# =========================
# SOURCES
# =========================
SEED_URLS = [
    "https://www.tendersinfo.com/global-egypt-tenders.php",
    "https://www.dgmarket.com/tenders"
]


# =========================
# SAVE FIRESTORE
# =========================
def save(items):
    saved = 0

    for item in items:

        ref = db.collection("tenders").document(item["id"])

        if ref.get().exists:
            continue

        ref.set({
            "title": item["title"],
            "link": item["link"],
            "source": item["source"],
            "score": item["score"],
            "created_at": item["created_at"]
        })

        saved += 1
        print("✔ SAVED:", item["title"][:80])

    print("\nDONE SAVED:", saved)


# =========================
# MAIN
# =========================
def run():

    print("\n🚀 PRO TENDER BOT STARTED")

    all_links = []

    # 1. CRAWL
    for url in SEED_URLS:
        links = crawl_links(url)
        all_links += links

    print("LINKS FOUND:", len(all_links))

    # 2. EXTRACT
    raw = []
    for link in all_links:
        data = extract_page(link)
        if data["title"]:
            raw.append(data)

    print("EXTRACTED:", len(raw))

    # 3. PROCESS
    clean = process(raw)

    print("FILTERED:", len(clean))

    # 4. SAVE
    save(clean)


if __name__ == "__main__":
    run()
