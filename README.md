# High-Performance E-Commerce Scraper — 10,000+ Products in 30 Minutes

A production-ready web scraper that extracts large-scale product data from e-commerce platforms at high speed. Built to handle 10,000+ product listings in under 30 minutes with full error handling, retry logic, and structured output.

## Features

- Scrapes 10,000+ products in ~30 minutes
- Anti-bot bypass — rotating headers, request delays, session management
- Cloudflare & CAPTCHA handling via Selenium
- Full error handling & automatic retry on failure
- Structured output — Excel, CSV, or JSON
- Extracts: product name, price, rating, review count, stock status, images, URL

## Tech Stack

- Python 3.10+
- Selenium (JS-heavy pages, anti-bot bypass)
- BeautifulSoup4 (HTML parsing)
- Pandas (data cleaning & export)
- openpyxl (Excel output)

## Setup

1. Clone the repo
```bash
git clone https://github.com/Hacer-B/ecommerce-scraper
cd ecommerce-scraper
```

2. Install dependencies
```bash
pip install selenium beautifulsoup4 pandas openpyxl requests
```

3. Configure settings
```python
TARGET_URL    = "https://www.trendyol.com/erkek-ayakkabi"
KATEGORI      = "erkek-ayakkabi"
MAX_SAYFA     = 500        # max pages to scrape
CIKTI_FORMAT  = "excel"    # "excel", "csv", or "json"
BEKLEME_SURESI = 1.5       # seconds between requests
```

4. Run
```bash
python scraper.py
```

## Output Example

| Product | Price | Rating | Reviews | Stock |
|---------|-------|--------|---------|-------|
| Nike Air Max 270 | ₺2,499 | 4.8 | 1,204 | In Stock |
| Adidas Ultraboost | ₺3,199 | 4.7 | 876 | In Stock |
| New Balance 574 | ₺1,899 | 4.6 | 543 | Low Stock |

## Performance

| Products | Time | Pages |
|----------|------|-------|
| 1,000 | ~3 min | 50 |
| 5,000 | ~15 min | 250 |
| 10,000 | ~30 min | 500 |

## How It Works

```
Launch browser (Selenium)
        ↓
Loop through category pages
        ↓
Parse product cards (BeautifulSoup)
        ↓
Save to DataFrame (Pandas)
        ↓
Export → Excel / CSV / JSON
```

## Use Cases

- Price monitoring & competitor analysis
- Product catalog migration
- Market research & trend analysis
- Inventory tracking

## Author

**Hacer B.** — Python Automation & Web Scraping Expert

- Upwork: https://www.upwork.com/freelancers/~01ff7cdd896ef9c905
- GitHub: https://github.com/Hacer-B
