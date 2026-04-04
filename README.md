# **Menza AI Platform Scraper**

## Description

This project is a Python-based scraper using **Playwright** to log into the Menza AI platform and extract all dashboards.

It automatically saves the dashboard data in two formats:

1. **`dashboards.json`** - structured JSON containing `name`, `owner`, `last_modified`, and `url` for each dashboard
2. **`dashboard_names.txt`** - plain text file listing only dashboard names

The script handles dashboard names containing `"You"` correctly and can be run repeatedly to fetch the latest dashboard information.

---

## Getting Started

### Dependencies

- Python 3.9+
- [Playwright](https://playwright.dev/python/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- OS: Windows, macOS, or Linux

---

### Installing

1. Clone this repository:

```bash
git clone https://github.com/lurv1209/menza-dashboard-scraper.git
cd menza-dashboard-scraper
```

2. Install Python dependencies:

```bash
pip install -r requirements.txt
playwright install
```

3. Create a .env file in the project root with your Menza credentials (see .env.example for format).

### Executing program

1. Run the scraper:

```bash
python extract_dashboards.py
```

2. After running, the following files will be created automatically:

- **dashboards.json** → structured JSON of dashboards
- **dashboard_names.txt** → list of dashboard names

3. Both files are ignored by Git and are regenerated on each run.

<!-- ### Example Output -->

## Notes

- The script runs headless by default but can be run with a visible browser for debugging.
- Handles dashboard names containing "You" correctly to avoid truncation.
- Both output files are regenerated each time the script is executed.
- The .env file stores credentials and should never be committed.

## Authors

Contributors names and contact info

ex. Lurvish Polodoo
ex. [@Lurvish'sPortfolio](https://www.lurvish.space/)
