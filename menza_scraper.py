from playwright.sync_api import sync_playwright
from dotenv import dotenv_values
import re
import json

config = dotenv_values(".env")
EMAIL = config["MENZA_EMAIL"]
PASSWORD = config["MENZA_PASSWORD"]

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()


        try:
            print("Opening site...")
            page.goto("https://app.menza.ai")

            #Step 1: Enter email
            print("Waiting for email input...")
            page.wait_for_selector('#identifier-field')

            print("Entering email...")
            page.fill('#identifier-field', EMAIL)

            print("Clicking Continue (email step)...")
            page.locator('button:has-text("Continue")').nth(1).click()

            # Step 2: Use another method
            print("Waiting for 'Use another method'...")
            page.get_by_text("Use another method").click()

            # Step 3: Choose password login
            print("Selecting password login...")
            page.get_by_text("Sign in with your password").click()

            # Step 4: Enter password
            print("Waiting for password input...")
            page.wait_for_selector('#password-field')

            print("Entering password...")
            page.fill('#password-field', PASSWORD)

            print("Clicking Continue (password step)...")
            page.get_by_role("button", name="Continue").click()

            # Wait for login to complete
            page.wait_for_timeout(5000)

            print("Login flow completed")

            page.get_by_role("link", name="Dashboards").click()

            page.wait_for_selector('a[href*="/dashboards/"]')

            dashboard_links = page.locator('a[href*="/dashboards/"]')
            texts = dashboard_links.all_text_contents()
            urls = [link.get_attribute("href") for link in dashboard_links.element_handles()]

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

            print("Dashboard JSON and names file created successfully!")
        except Exception as e:
            print("Error:", e)
        finally:
            browser.close()

if __name__ == "__main__":
    run()