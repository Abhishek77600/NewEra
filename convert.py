import asyncio
from playwright.async_api import async_playwright
import pandas as pd
from urllib.parse import urlparse

async def scrape_bbc_and_save_structured():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto("https://www.bbc.com/news", wait_until="load", timeout=60000)
        await page.wait_for_timeout(3000)

        # Get all news article links and their hrefs
        links = await page.locator('a[href*="/news/"]').element_handles()

        data = []
        for link in links:
            title = (await link.inner_text()).strip()
            href = await link.get_attribute('href')
            if title and href:
                # Parse category from href path
                path_parts = urlparse(href).path.split('/')
                # Example: /news/world-123456 => category = "world"
                category = None
                for part in path_parts:
                    if part and not part.isdigit() and '-' not in part:
                        category = part
                        break
                data.append({"title": title, "url": href, "category": category or "unknown"})

        df = pd.DataFrame(data)
        df.to_csv("bbc_headlines_structured.csv", index=False)
        print(f"Saved {len(data)} structured headlines to bbc_headlines_structured.csv")

        await browser.close()

asyncio.run(scrape_bbc_and_save_structured())
