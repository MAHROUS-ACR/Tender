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
        try:
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

        except Exception as e:
            print("❌ SAVE ERROR:", e)

    print("\n✅ TOTAL SAVED:", saved)


# =========================
# MAIN
# =========================
def run():
    print("\n🚀 PRO TENDER BOT STARTED")

    all_links = []

    # =========================
    # CRAWL
    # =========================
    for url in SEED_URLS:
        try:
            links = crawl_links(url)
            all_links += links
            print(f"✔ Crawled {url} -> {len(links)} links")

        except Exception as e:
            print(f"❌ Crawl error {url}:", e)

    print("🔗 LINKS FOUND:", len(all_links))

    # =========================
    # EXTRACT
    # =========================
    raw = []
    for link in all_links:
        try:
            data = extract_page(link)

            if data and data.get("title"):
                raw.append(data)

        except Exception as e:
            print("❌ Extract error:", e)

    print("📄 EXTRACTED:", len(raw))

    # =========================
    # PROCESS
    # =========================
    try:
        clean = process(raw)
    except Exception as e:
        print("❌ Process error:", e)
        clean = []

    print("🧹 FILTERED:", len(clean))

    # =========================
    # SAVE
    # =========================
    save(clean)


# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        print("🔥 MAIN ERROR:", e)
