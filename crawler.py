import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import urljoin
import time


HEADERS = {"User-Agent": "Mozilla/5.0"}


# =========================
# SELENIUM DRIVER
# =========================
def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)


# =========================
# SMART FETCH (requests + selenium fallback)
# =========================
def fetch(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        if r.status_code == 200 and len(r.text) > 1000:
            return r.text
    except:
        pass

    print("⚠️ Selenium fallback:", url)

    driver = get_driver()
    driver.get(url)
    time.sleep(3)
    html = driver.page_source
    driver.quit()
    return html


# =========================
# DEEP CRAWLER
# =========================
def crawl_links(start_url, max_pages=10):
    visited = set()
    queue = [start_url]
    results = []

    while queue and len(visited) < max_pages:
        url = queue.pop(0)

        if not url or url in visited:
            continue

        visited.add(url)

        try:
            html = fetch(url)
            soup = BeautifulSoup(html, "html.parser")
        except:
            continue

        for a in soup.find_all("a"):
            href = a.get("href")

            # ❌ ignore bad links
            if not href:
                continue
            if href.startswith("mailto:") or href.startswith("javascript:"):
                continue

            # build full URL safely
            if href.startswith("http"):
                full = href
            else:
                full = urljoin(url, href)

            if not full:
                continue

            low = full.lower()

            # 🎯 filter relevant links
            if any(k in low for k in ["tender", "procurement", "bid", "rfp", "rfq"]):
                results.append(full)

            # 🔁 crawling expansion
            if any(k in low for k in ["page", "tender", "procurement", "bid"]):
                if full not in visited:
                    queue.append(full)

    return list(set(results))


# =========================
# EXTRACT PAGE (SAFE VERSION)
# =========================
def extract_page(url):
    try:
        html = fetch(url)
        soup = BeautifulSoup(html, "html.parser")

        # title safe extraction
        title_tag = soup.find(["h1", "h2", "title"])
        title = title_tag.get_text(strip=True) if title_tag else ""

        # safe source extraction
        try:
            source = url.split("/")[2]
        except:
            source = "unknown"

        full_text = soup.get_text(" ", strip=True)

        return {
            "title": title,
            "link": url,
            "source": source,
            "full_text": full_text
        }

    except Exception as e:
        print("❌ Extract page error:", url, e)
        return None
