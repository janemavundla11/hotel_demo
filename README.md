# hotel_demo

git clone https://github.com/janemavundla11/hotel_demo.git
cd hotel_demo
python -m venv .venv         # or: py -m venv .venv (Windows)
# Windows:
# .venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate
pip install -r requirements.txt
python test_hotel.py
pytest
