import requests
import os
import time
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

# step1: function to extract the linlks from the website
def crawl_all_links(base_url, delay=1.5):
    """Crawl all internal links of a website with progress output."""
    visited, to_visit = set(), [base_url]
    domain = urlparse(base_url).netloc

    while to_visit:
        url = to_visit.pop(0)
        if url in visited:
            continue
        if any(url.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".gif", ".pdf", ".mp4"]):
            continue

        try:
            print(f"🔗 Crawling: {url}", flush=True)
            resp = requests.get(url, timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser")
            visited.add(url)

            for a in soup.find_all("a", href=True):
                link = urljoin(base_url, a["href"])
                if urlparse(link).netloc == domain and link not in visited:
                    to_visit.append(link)

        except Exception as e:
            print(f"Failed: {url} | {e}", flush=True)

        time.sleep(delay)
        if len(visited) > 200:  # safety cap
            break

    print(f"Total pages found: {len(visited)}", flush=True)
    return list(visited)



# step2: function to fetch the content from the all links
def extract_page_content(url):
    """Extract text, tables, and image info from a single page with progress output."""
    if any(url.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".gif", ".pdf", ".mp4"]):
        return ""

    try:
        print(f"Extracting content: {url}", flush=True)
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(separator="\n", strip=True)

        tables = []
        for table in soup.find_all("table"):
            rows = []
            for tr in table.find_all("tr"):
                cells = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
                if cells:
                    rows.append(cells)
            tables.append(rows)

        images = []
        for img in soup.find_all("img"):
            img_src = urljoin(url, img.get("src"))
            alt_text = img.get("alt", "")
            images.append({"src": img_src, "alt": alt_text})

        return f"URL: {url}\n\n{text}\n\nTables: {tables}\n\nImages: {images}"

    except Exception as e:
        print(f"Error extracting {url}: {e}", flush=True)
        return ""


# step3: start crawling the website link and saving in a text file

base_url = "https://namal.edu.pk/"

print(f"\n Starting crawl for: {base_url}\n", flush=True)
urls = crawl_all_links(base_url)

with open("urls.txt", "w", encoding="utf-8") as f:
    for url in urls:
        f.write(url + "\n")

print(f"\nSaved {len(urls)} URLs to 'urls.txt'\n")


# step4: Calling the function to Extract page content against all the urls

documents = []
output_dir = "Textfiles"
output_file_path = os.path.join(output_dir, "Webcontents.txt")

with open(output_file_path, "w", encoding="utf-8") as content_file:
    for idx, u in enumerate(urls, start=1):
        print(f"\n [{idx}/{len(urls)}] Processing: {u}", flush=True)
        page_data = extract_page_content(u)

        if page_data:
            documents.append({
                "page_content": page_data,
                "metadata": {"source": u}
            })
            # Save only the content (no URLs)
            content_file.write(page_data)
            content_file.write("\n\n" + "="*80 + "\n\n")

print(f"\nSaved content from {len(documents)} pages to 'Webcontents.txt'\n")

