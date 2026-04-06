import platform
import os
import subprocess
import sys
import logging

LOG_FILE = os.path.join(os.path.dirname(__file__), "scraper.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

SCRIPT_PATH = os.path.abspath("extract_dashboards.py")
PYTHON_PATH = sys.executable

def setup_mac_cron():
    print("\nSetting up macOS/Linux cron job...\n")

    cron_job = f'0 * * * * {PYTHON_PATH} {SCRIPT_PATH} >> {os.path.abspath("scraper.log")} 2>&1\n'

    try:
        # Get existing crontab
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
        existing = result.stdout if result.returncode == 0 else ""

        if cron_job.strip() in existing:
            print("✅ Cron job already exists.")
            return

        # Append safely
        new_cron = existing + cron_job

        subprocess.run(["crontab", "-"], input=new_cron, text=True, check=True)

        print("✅ Cron job added successfully (runs hourly).")

    except Exception as e:
        print("❌ Failed to set up cron automatically.")
        print("Error:", e)
        print("\nFallback: run `crontab -e` and add:\n")
        print(cron_job)


def setup_windows_task():
    logging.info("Setting up Windows Task Scheduler...")

    task_name = "MenzaDashboardScraper"

    command = f'{PYTHON_PATH} "{SCRIPT_PATH}"'

    try:
        subprocess.run([
            "schtasks",
            "/create",
            "/sc", "hourly",
            "/mo", "1",
            "/tn", task_name,
            "/tr", command,
            "/f"
        ], check=True)

        logging.info(f"Task '{task_name}' created successfully (runs hourly).")

    except Exception as e:
        print("❌ Failed to create task automatically.")
        print("Error:", e)
        print("\nYou can create it manually in Task Scheduler.")


def main():
    os_type = platform.system()

    print(f"Detected OS: {os_type}")

    if os_type in ["Darwin", "Linux"]:
        setup_mac_cron()
    elif os_type == "Windows":
        setup_windows_task()
    else:
        print("Unsupported OS")


if __name__ == "__main__":
    main()