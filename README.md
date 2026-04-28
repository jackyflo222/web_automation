# Selenium Automation

End-to-end UI test suite for [Rahul Shetty's Automation Practice page](https://rahulshettyacademy.com/AutomationPractice/), built with Selenium 4, pytest, and the Page Object Model pattern.

---

## Project Structure

```
web_automation/
├── conftest.py          # Chrome driver fixture and BASE_URL
├── pytest.ini           # Test paths, verbosity, and custom markers
├── requirements.txt     # Python dependencies
├── pages/
│   ├── base_page.py     # Reusable Selenium helpers (waits, clicks, alerts)
│   └── practice_page.py # Page object for the practice site
└── tests/
    └── test_practice_page.py  # Full test suite
```

---

## Requirements

- Python 3.8+
- Google Chrome

---

## Setup

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## Running Tests

**Run all tests:**
```bash
pytest
```

**Run headless (no browser window):**
```bash
pytest --headless
```

**Run a specific marker/group:**
```bash
pytest -m radio
pytest -m dropdown
pytest -m checkbox
pytest -m autocomplete
pytest -m windows
pytest -m alerts
pytest -m hover
pytest -m tables
pytest -m iframe
pytest -m visibility
```

**Generate an HTML report:**
```bash
pytest --html=report.html --self-contained-html
```

---

## Test Coverage

| Marker | What is tested |
|---|---|
| `radio` | Select each radio button; verify mutual exclusivity |
| `dropdown` | Select options; verify selection changes |
| `checkbox` | Check / uncheck individual and multiple options |
| `autocomplete` | Suggestions appear and match input; select a country |
| `windows` | New window opens, has different URL, can be closed |
| `windows` | New tab opens, URL contains `qaclickacademy`, can be closed |
| `alerts` | Simple alert text; confirm dialog accept and dismiss |
| `hover` | Hover reveals Top and Reload links; clicking them works |
| `tables` | Course table has 10 rows with 3 columns and non-empty prices |
| `tables` | Fixed-header table has 9 rows; total amount is 296 |
| `iframe` | Switch into iframe, read links, return to main content |
| `visibility` | Hide and show a text element via the control buttons |

---

## Architecture

- **`BasePage`** — wraps raw Selenium calls with explicit waits so tests never need `time.sleep`.
- **`PracticePage`** — declares all locators as class-level tuples and exposes action methods; tests never touch `By` or `WebDriverWait` directly.
- **`conftest.py`** — provides a per-function `driver` fixture that opens Chrome, navigates to the base URL, and quits after each test.
