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
        if url in visited:
            continue

        visited.add(url)

        html = fetch(url)
        soup = BeautifulSoup(html, "html.parser")

        for a in soup.find_all("a"):
            href = a.get("href")
            if not href:
                continue

            full = urljoin(url, href)

            if any(k in full.lower() for k in ["tender", "procurement", "bid", "rfp", "rfq"]):
                results.append(full)

            if "page" in full or "tender" in full:
                queue.append(full)

    return list(set(results))


# =========================
# EXTRACT PAGE
# =========================
def extract_page(url):
    html = fetch(url)
    soup = BeautifulSoup(html, "html.parser")

    title = soup.find(["h1", "h2", "title"])
    title = title.get_text(strip=True) if title else ""

    return {
        "title": title,
        "link": url,
        "source": url.split("/")[2],
        "full_text": soup.get_text(" ", strip=True)
    }
