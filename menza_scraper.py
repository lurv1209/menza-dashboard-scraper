from playwright.sync_api import sync_playwright
from dotenv import dotenv_values

config = dotenv_values(".env")
EMAIL = config["MENZA_EMAIL"]
PASSWORD = config["MENZA_PASSWORD"]

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
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

            titles = [
                text.split(" You ")[0].strip()
                for text in dashboard_links.all_text_contents()
            ]

            print("Dashboard titles:\n")
            for t in titles:
                print("-", t)
        except Exception as e:
            print("Error:", e)
        finally:
            browser.close()

if __name__ == "__main__":
    run()