import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from concurrent.futures import ThreadPoolExecutor

# AYARLAR
filename = "A5IT_10K_Fiyatli_Final.csv"
columns = ["sku", "upc", "prod_title", "category", "msrp_price", "customer_price", "qty_in_stock", "description", "brand", "specification", "images", "pdfs"]
TARGET_COUNT = 10000
WORKER_COUNT = 12 # Hız için 12 yaptım, sistemin kaldırır

def setup_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

drivers = [setup_driver() for _ in range(WORKER_COUNT)]

# --- DEVAM ETME MANTIĞI ---
existing_skus = set()
if os.path.exists(filename):
    try:
        df_existing = pd.read_csv(filename)
        existing_skus = set(df_existing['sku'].astype(str).tolist())
        print(f"[*] {len(existing_skus)} adet kayıt zaten var. Kaldığım yerden devam ediyorum...")
    except:
        pass

def fetch_item(data):
    link, worker_id = data
    driver = drivers[worker_id]
    try:
        driver.get(link)
        
        # Sayfa içeriğini alıp SKU kontrolü yapalım
        body_text = driver.find_element(By.TAG_NAME, "body").text
        sku = "N/A"
        if "MPN:" in body_text:
            sku = body_text.split("MPN:")[1].split("\n")[0].split()[0].strip()

        # EĞER BU SKU ZATEN VARSA ÇEKME
        if sku in existing_skus:
            return

        # Fiyat çekme (Bekleme süresini 3 sn yaptım hız için)
        price = "N/A"
        try:
            price_element = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.text-3xl"))
            )
            price = price_element.text.strip()
        except: pass

        title = driver.find_element(By.TAG_NAME, "h1").text.strip()
        brand = "N/A"
        try:
            brand = driver.find_element(By.XPATH, "//div[contains(@class, 'text-primary')]").text.strip()
        except: pass

        row = [sku, "", title, "Hardware", price, price, "1", title, brand, "", link, ""]
        pd.DataFrame([row]).to_csv(filename, mode='a', header=False, index=False, encoding='utf-8-sig')
        print(f"[YENİ] {sku} eklendi.")
    except: pass

def start():
    if not os.path.isfile(filename):
        pd.DataFrame(columns=columns).to_csv(filename, index=False, encoding='utf-8-sig')

    main_driver = setup_driver()
    total = len(existing_skus)
    page = 46 # İstersen bunu 25. sayfadan başlatabilirsin

    try:
        while total < TARGET_COUNT:
            print(f"\n[*] Sayfa {page} taranıyor...")
            main_driver.get(f"https://a5it.com/shop?page={page}")
            time.sleep(2)
            
            links = [el.get_attribute("href") for el in main_driver.find_elements(By.CSS_SELECTOR, "a.group.flex") if "/product/" in el.get_attribute("href")]
            
            if not links: break

            work_data = [(link, i % WORKER_COUNT) for i, link in enumerate(links)]
            with ThreadPoolExecutor(max_workers=WORKER_COUNT) as executor:
                executor.map(fetch_item, work_data)
            
            page += 1
            # Mevcut kayıt sayısını güncellemek için dosyayı tekrar sayabiliriz veya manuel artırabiliriz
            print(f"--- Sayfa {page} bitti. Toplam ilerleme artıyor... ---")

    finally:
        for d in drivers: d.quit()
        main_driver.quit()

if __name__ == "__main__":
    start()