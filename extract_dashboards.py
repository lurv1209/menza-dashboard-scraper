import os
from playwright.sync_api import sync_playwright
from dotenv import dotenv_values
import re
import json
import logging
import sys

LOG_FILE = os.path.join(os.path.dirname(__file__), "scraper.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

config = dotenv_values(".env")
EMAIL = config["MENZA_EMAIL"]
PASSWORD = config["MENZA_PASSWORD"]

# Default to headless
headless_arg = sys.argv[1].lower() if len(sys.argv) > 1 else "true"
HEADLESS = headless_arg in ["true", "1", "yes"]

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
        except Exception as e:
            logging.debug(f"Selector failed: {sel} -> {e}")
    return False

def run():
    with sync_playwright() as p:
        logging.info(f"Launching browser headless={HEADLESS}")
        browser = p.chromium.launch(headless=HEADLESS)
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

            page.pause()

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
                parts = raw_text.split("You", 1)

                name = parts[0].strip()
                owner = "You" if len(parts) > 1 else None
                rest = parts[1] if len(parts) > 1 else ""

                times = re.findall(r"\d+\s+\w+\s+ago", rest)

                updated_at = times[0] if len(times) > 0 else None
                created_at = times[1] if len(times) > 1 else None

                dashboard_data.append({
                    "name": name,
                    "owner": owner,
                    "last_updated": updated_at,
                    "created": created_at,
                    "url": "https://app.menza.ai/" + url.lstrip('/')
                })
            
            # Deduplicate
            seen = set()
            unique_dashboards = []

            for d in dashboard_data:
                if d["url"] not in seen:
                    seen.add(d["url"])
                    unique_dashboards.append(d)

            dashboard_data = unique_dashboards

            dashboard_data.sort(key=lambda x: x["name"].lower())

            # Save to JSON
            with open("dashboards.json", "w") as f:
                json.dump(dashboard_data, f, indent=2)

            # Save just the names
            with open("dashboard_names.txt", "w") as f:
                for d in dashboard_data:
                    f.write(d["name"] + "\n")

            logging.info(f"Extracted {len(dashboard_data)} dashboards")
            logging.info("Dashboard JSON and names file created successfully!")
        except Exception as e:
            logging.error(f"Error: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    run()