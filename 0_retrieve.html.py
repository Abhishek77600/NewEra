import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def scrape_with_login(target_url, login_url, email, password, 
                            email_selector, password_selector, submit_selector,
                            wait_for_selector_after_login,
                            tag_name='h2', class_name=None):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # Change to False to see browser actions
        context = await browser.new_context()
        page = await context.new_page()

        try:
            # Go to login page
            await page.goto(login_url, timeout=60000)

            # Fill in email and password, then submit
            await page.fill(email_selector, email)
            await page.fill(password_selector, password)
            await page.click(submit_selector)

            # Wait a bit to let the page update after login
            await page.wait_for_timeout(3000)

            # Save page content after login for debugging
            html_after_login = await page.content()
            with open("after_login.html", "w", encoding="utf-8") as f:
                f.write(html_after_login)
            print("Saved after_login.html for debugging")

            # Optionally print current URL after login
            print("After login, current URL:", page.url)

            # Try waiting for the selector confirming login success
            try:
                await page.wait_for_selector(wait_for_selector_after_login, timeout=30000)
                print(f"Selector '{wait_for_selector_after_login}' found after login.")
            except Exception as e:
                print(f"Warning: Selector '{wait_for_selector_after_login}' not found after login. Exception: {e}")

            # Navigate to target page if different from login page
            if target_url != login_url:
                await page.goto(target_url, timeout=60000)
                await page.wait_for_selector(tag_name, timeout=15000)

            # Get page content
            html = await page.content()
            soup = BeautifulSoup(html, 'html.parser')

            print(f"\nExtracted <{tag_name}> elements:\n")
            if class_name:
                elements = soup.find_all(tag_name, class_=class_name)
            else:
                elements = soup.find_all(tag_name)

            for elem in elements:
                text = elem.get_text(strip=True)
                if text:
                    print(text)

        except Exception as e:
            # Removed emoji to avoid encoding errors in Windows console
            print(f"Error: {e}")

        finally:
            await browser.close()

if __name__ == "__main__":
    login_url = 'https://atria.bizoticedtech.com/login'  
    target_url = 'https://atria.bizoticedtech.com/learn/mock-test/694160/report?id=694160&lessonId=3895349'  
    
    email = 'acharyaabhishek801@gmail.com'      
    password = 'Abhi@7899'       

    email_selector = 'input[name="email"]'       
    password_selector = 'input[name="password"]' 
    submit_selector = 'button[type="submit"]'    

    # Update this selector after inspecting after_login.html
    wait_for_selector_after_login = 'div.dashboard'  
    
    asyncio.run(scrape_with_login(
        target_url=target_url,
        login_url=login_url,
        email=email,
        password=password,
        email_selector=email_selector,
        password_selector=password_selector,
        submit_selector=submit_selector,
        wait_for_selector_after_login=wait_for_selector_after_login,
        tag_name='h2'    
    ))
