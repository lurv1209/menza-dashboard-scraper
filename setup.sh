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

echo ""
echo "Setup complete!"
echo "Next steps:"
echo "1. Create a .env file with your credentials (see .env.example for reference)"
echo "2. Run: python extract_dashboards.py"