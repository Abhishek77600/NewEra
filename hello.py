import asyncio
from playwright.async_api import async_playwright
import pandas as pd
from urllib.parse import urlparse

async def scrape_bbc_and_save_structured():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto("https://www.bbc.com/news", wait_until="load", timeout=60000)
        await page.wait_for_timeout(3000)  # Wait for extra content to load if any

        # Get all links on the page with href containing /news/
        links = await page.locator('a[href*="/news/"]').element_handles()

        seen_urls = set()
        data = []
        for link in links:
            title = (await link.inner_text()).strip()
            href = await link.get_attribute('href')
            if title and href and href not in seen_urls:
                seen_urls.add(href)

                # Parse category from href path
                path_parts = urlparse(href).path.strip('/').split('/')
                # Usually path like: news/world-123456 or news/world/123456
                # We'll pick the first non-numeric part after "news"
                category = "unknown"
                if path_parts and path_parts[0] == 'news':
                    for part in path_parts[1:]:
                        # pick first part that is not numeric and doesn't contain '-'
                        if part and not part.isdigit() and '-' not in part:
                            category = part
                            break

                data.append({"title": title, "url": href, "category": category})

        df = pd.DataFrame(data)
        df.to_csv("bbc_headlines_structured.csv", index=False)
        print(f"Saved {len(data)} structured headlines to bbc_headlines_structured.csv")

        await browser.close()

asyncio.run(scrape_bbc_and_save_structured())
