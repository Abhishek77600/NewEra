import asyncio
import csv
from playwright.async_api import async_playwright

async def scrape_bbc():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://www.bbc.com/news", wait_until="networkidle")

        # Wait for some article link to appear
        await page.wait_for_selector('a[href*="/news/"]', timeout=30000)

        # Grab text of all news links containing "/news/"
        headlines = await page.locator('a[href*="/news/"]').all_inner_texts()

        # Clean and filter headlines
        clean_headlines = [h.strip() for h in headlines if h.strip()]

        print("BBC News headlines:")
        for h in clean_headlines:
            print(h)

        # Write to CSV file
        with open("bbc_headlines.csv", mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["headline"])  # header
            for headline in clean_headlines:
                writer.writerow([headline])

        await browser.close()

asyncio.run(scrape_bbc())
