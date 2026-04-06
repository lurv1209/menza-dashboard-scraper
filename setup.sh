#!/bin/bash

echo "Creating virtual environment..."
python -m venv .venv

echo "Installing dependencies..."
if [ -f ".venv/bin/pip" ]; then
    .venv/bin/pip install -r requirements.txt
    .venv/bin/playwright install
else
    .venv/Scripts/pip.exe install -r requirements.txt
    .venv/Scripts/playwright.exe install
fi

if [ ! -f ".env" ]; then
  echo "Creating .env file from template..."
  cp .env.example .env
fi

echo ""
echo "Setup complete!"
echo "Next steps:"
echo ""
echo "1. Activate the virtual environment:"
echo ""
echo "   # macOS/Linux"
echo "   source .venv/bin/activate"
echo ""
echo "   # Windows Git Bash"
echo "   source .venv/Scripts/activate"

echo ""
echo "2. Update your .env file with credentials"
echo ""

echo "3. Run the scraper:"
echo "   python extract_dashboards.py           # headless (default)"
echo "   python extract_dashboards.py false     # with browser UI"
echo ""

echo "4. (Optional) Schedule automatic runs:"
echo "   python schedule_task.py"
echo ""
echo "Logs will be written to scraper.log"