from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        print("Opening site...")
        page.goto("https://app.menza.ai")

        page.wait_for_timeout(5000)

        browser.close()

if __name__ == "__main__":
    run()