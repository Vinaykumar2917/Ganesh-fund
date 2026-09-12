# Ganesh Chaturthi Money Manager

## Easiest Windows setup

1. Install Python 3 from https://www.python.org/downloads/
2. Extract this ZIP.
3. Open the extracted folder.
4. Click the folder address bar, type `cmd`, and press Enter.
5. Run:

```text
python -m pip install -r requirements.txt
python app.py
```

6. Open Chrome and visit:

http://127.0.0.1:5000

The app stores transactions in `money.db` in the same folder.

If `python` does not work, try:

```text
py -m pip install -r requirements.txt
py app.py
```

Features:
- Add money
- Add expenses
- Automatic available balance
- Transaction history
- Delete individual transactions
- Clear all transactions
- WhatsApp summary sharing
