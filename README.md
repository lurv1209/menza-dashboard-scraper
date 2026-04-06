# **Menza AI Platform Scraper**

## Description

This project is a Python-based scraper using **Playwright** to log into the Menza AI platform and extract all dashboards.

It automatically saves the dashboard data in two formats:

1. **`dashboards.json`** - structured JSON containing (for each dashboard):
   - `name`
   - `owner`
   - `created`
   - `updated_at`
   - `url`
2. **`dashboard_names.txt`** - plain text file listing only dashboard names

The script handles dashboard names containing `"You"` without incorrect parsing and can be run repeatedly to fetch the latest dashboard information.

---

## Approach

- Automated login using Playwright
- Implemented retry logic to handle transient UI/network issues
- Used flexible selectors to handle UI changes
- Extracted dashboard data using robust parsing
- Added deduplication and sorting for consistent outputs
- Implemented cross-platform scheduling (Windows Task Scheduler and cron)
- Added logging for observability of scheduled runs

---

## Getting Started

### Dependencies

- Python 3.9+
- [Playwright](https://playwright.dev/python/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- OS: Windows, macOS, or Linux

---

### Installing

### 1. Clone this repository:

```bash
git clone https://github.com/lurv1209/menza-dashboard-scraper.git
cd menza-dashboard-scraper
```

---

### 2. Setup the project

#### Option A: Automated Setup

```bash
chmod +x setup.sh
source setup.sh
```

This will:

- Create a virtual environment
- Install dependencies
- Install Playwright browsers
- Create a `.env` file from the template (if it doesn’t exist)

After this, activate the virtual environment before running the scraper:

#### macOS/Linux

`source .venv/bin/activate`

#### Windows (Git Bash)

`source .venv/Scripts/activate`

#### Windows PowerShell

`.venv\Scripts\Activate.ps1`

---

#### Option B: Manual Setup

(i) Create a virtual environment:

```
python -m venv .venv
```

(ii) Activate the virtual environment

#### Windows (Git Bash)

`source .venv/Scripts/activate`

#### Windows (PowerShell)

`.venv\Scripts\Activate.ps1`

#### Mac/Linux

`source .venv/bin/activate`

(iii) Install Python dependencies:

```bash
pip install -r requirements.txt
playwright install
```

---

### 3. Configure environment variables

If you used the automated setup, a `.env` file will be created automatically.

Otherwise, for manual setup, create a `.env` file in the project root. (see `.env.example` for reference)

Update it with your credentials:

```
MENZA_EMAIL=your_email
MENZA_PASSWORD=your_password
```

---

### 4. Run the scraper

**Default (headless browser):**

```
python extract_dashboards.py
```

**Run with browser visible (headed mode) for debugging:**

```
python extract_dashboards.py false
```

- true or 1 → headless (default)
- false, 0, no → headed (browser visible, for debugging)

After running, the following files will be created automatically:

- **dashboards.json** → structured JSON of dashboards
- **dashboard_names.txt** → list of dashboard names

Note: Both files are ignored by Git and are regenerated on each run.

---

### 5. (Optional) Schedule automatic runs

You can schedule the scraper to run hourly:

```bash
python schedule_task.py
```

**On Windows**: creates a `Task Scheduler` job

**On macOS/Linux**: adds a `cron` job

Logs are written to `scraper.log`.

## Notes

- The script runs headless by default but can be run with a visible browser for debugging.
- Handles dashboard names containing "You" correctly to avoid truncation.
- Both output files are regenerated each time the script is executed.
- The `.env` file stores credentials and should never be committed.
- The scraper is designed to handle UI changes by using flexible selectors and retry logic.
- Data extraction is implemented defensively to avoid breaking when the UI structure changes.
- All runs (manual and scheduled) are logged to `scraper.log`.

## Authors

Lurvish Polodoo ([@Lurvish's Portfolio](https://www.lurvish.space/))
