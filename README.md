# How to use
1. Create/update .env file with your settings.  (Most specifically your FMP API Key.)
2. Run `pip install -U -r requirements.txt` to install needed Python packages.
3. Run `main.py` or `python3 main.py` to build graph.

## FMP API Key
https://site.financialmodelingprep.com/developer/docs/

## .env file format
Create a `.env` file in your project folder.  At least add your FMP API key.
```text
API_KEY=your_fmp_api_key

START_YEAR = 2023
END_YEAR = 2027

ARK_BEAR_PRICE = 1400
ARK_EXPECTED_PRICE = 2000
ARK_BULL_PRICE = 2500

TARGET_TICKER = TSLA

Y_GRAPH_TICKS_STEP = 10
X_GRAPH_TICKS_STEP = 7
```
