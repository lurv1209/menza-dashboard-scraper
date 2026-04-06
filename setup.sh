#!/bin/bash

echo "Creating virtual environment..."
python -m venv .venv

echo "Activating virtual environment..."
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
else
    source .venv/Scripts/activate
fi

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Installing Playwright browsers..."
playwright install

if [ ! -f ".env" ]; then
  echo "Creating .env file from template..."
  cp .env.example .env
fi

echo ""
echo "Setup complete!"
echo "Next steps:"

echo "1. Update your .env file with credentials"

echo ""
echo "2. Run the scraper:"
echo "   python extract_dashboards.py           # headless (default)"
echo "   python extract_dashboards.py false     # with browser UI"

echo ""
echo "3. (Optional) Schedule automatic runs:"
echo "   python schedule_task.py"

echo ""
echo "Logs will be written to scraper.log"