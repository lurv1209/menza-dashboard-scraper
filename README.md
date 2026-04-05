# **Menza AI Platform Scraper**

## Description

This project is a Python-based scraper using **Playwright** to log into the Menza AI platform and extract all dashboards.

It automatically saves the dashboard data in two formats:

1. **`dashboards.json`** - structured JSON containing `name`, `owner`, `last_modified`, and `url` for each dashboard
2. **`dashboard_names.txt`** - plain text file listing only dashboard names

The script handles dashboard names containing `"You"` without incorrect parsing and can be run repeatedly to fetch the latest dashboard information.

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

### 2. Setup the project

#### Option A: Automated Setup

```bash
chmod +x setup.sh
./setup.sh
```

This will:

- Create a virtual environment
- Activate it
- Install dependencies
- Install Playwright browsers

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

### 3. Configure environment variables

Create a .env file in the project root:

```
MENZA_EMAIL=your_email
MENZA_PASSWORD=your_password
```

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
- false, 0, no → headed (browser visible)

After running, the following files will be created automatically:

- **dashboards.json** → structured JSON of dashboards
- **dashboard_names.txt** → list of dashboard names

Note: Both files are ignored by Git and are regenerated on each run.

<!-- ### Example Output -->

## Notes

- The script runs headless by default but can be run with a visible browser for debugging.
- Handles dashboard names containing "You" correctly to avoid truncation.
- Both output files are regenerated each time the script is executed.
- The .env file stores credentials and should never be committed.

## Authors

Lurvish Polodoo ([@Lurvish's Portfolio](https://www.lurvish.space/))
