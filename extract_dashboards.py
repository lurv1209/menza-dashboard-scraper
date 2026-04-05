from playwright.sync_api import sync_playwright
from dotenv import dotenv_values
import re
import json
import logging

logging.basicConfig(level=logging.INFO)

config = dotenv_values(".env")
EMAIL = config["MENZA_EMAIL"]
PASSWORD = config["MENZA_PASSWORD"]

def retry(action, retries=3, delay=2):
    import time
    for attempt in range(retries):
        try:
            return action()
        except Exception as e:
            if attempt == retries - 1:
                raise
            logging.warning(f"Retry {attempt+1} failed: {e}")
            time.sleep(delay)

def click_if_exists(page, selectors, timeout=3000):
    for sel in selectors:
        try:
            locator = page.locator(sel).first
            locator.wait_for(state="visible", timeout=timeout)
            locator.click()
            return True
        except:
            continue
    return False

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            logging.info("Opening site...")
            retry(lambda: page.goto("https://app.menza.ai"))

            #Step 1: Enter email
            logging.info("Waiting for email input...")
            page.wait_for_selector('#identifier-field')

            logging.info("Entering email...")
            page.fill('#identifier-field', EMAIL)

            logging.info("Clicking Continue (email step)...")
            retry(lambda: page.get_by_role("button", name="Continue", exact=True).click())

            # Step 2: Use another method
            logging.info("Waiting for 'Use another method'...")
            retry(lambda: page.wait_for_selector('a[href*="factor-one"]', timeout=5000))
            click_if_exists(page, [
                'a[href*="factor-one"]',
                'text="Use another method"',
            ])

            # Step 3: Choose password login
            logging.info("Selecting password login...")
            click_if_exists(page, [
                'text="Sign in with your password"',
                'text="Password"',
            ])

            # Step 4: Enter password
            logging.info("Waiting for password input...")
            page.wait_for_selector('#password-field')

            logging.info("Entering password...")
            page.fill('#password-field', PASSWORD)

            logging.info("Clicking Continue (password step)...")
            retry(lambda: page.get_by_role("button", name="Continue").click())

            # Wait for login to complete
            logging.info("Login flow completed")

            # Wait for app to fully load
            retry(lambda: page.wait_for_load_state("networkidle"))

            # Wait specifically for dashboards link
            retry(lambda: page.wait_for_selector('a[href$="/dashboards"]', timeout=10000))

            # Click dashboards
            if not click_if_exists(page, [
                'a[href$="/dashboards"]',
                'role=link[name="Dashboards"]',
            ]):
                raise Exception("Could not find Dashboards link")

            # Wait for dashboards to load
            retry(lambda: page.wait_for_selector('a[href*="/dashboards/"]'))

            dashboard_links = page.locator('a[href*="/dashboards/"]')

            elements = dashboard_links.element_handles()

            if not elements:
                logging.warning("No dashboards found - UI may have changed")

            texts = [el.text_content() for el in elements]
            urls = [el.get_attribute("href") for el in elements]

            dashboard_data = []

            for raw_text, url in zip(texts, urls):
                # Extract name, owner, last_modified using regex
                match = re.match(r"(.+?)(You)([\d\s\w]+ago)$", raw_text)
                if match:
                    name = match.group(1).strip()
                    owner = match.group(2).strip()
                    last_modified = match.group(3).strip()
                else:
                    name = raw_text
                    owner = None
                    last_modified = None

                dashboard_data.append({
                    "name": name,
                    "owner": owner,
                    "last_modified": last_modified,
                    "url": "https://app.menza.ai/" + url.lstrip('/')
                })

            # Save to JSON
            with open("dashboards.json", "w") as f:
                json.dump(dashboard_data, f, indent=2)

            # Save just the names
            with open("dashboard_names.txt", "w") as f:
                for d in dashboard_data:
                    f.write(d["name"] + "\n")

            logging.info("Dashboard JSON and names file created successfully!")
        except Exception as e:
            logging.error(f"Error: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    run()