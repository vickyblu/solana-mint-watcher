# mint_watch_test_v4_sim.py
# Testing version with simulated inflow + mint activity

import requests, time, csv, os
from datetime import datetime, timedelta, timezone

# --- CONFIG ---
HELIUS_API_KEY = "cd832688-fa12-4307-9abc-9d2b809c73fb"
WATCH_ADDRESS = "9NERQjLetzquGwdKt3X4gZ8fE8fPfSkj2xo2esmUjWsz"
TOKEN_PROGRAM = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
CHECK_INTERVAL = 10
WATCH_DURATION = 300
OUTPUT_FILE = "mint_watch_log.csv"

# --- TELEGRAM CONFIG ---
TELEGRAM_BOT_TOKEN = "8347319352:AAH_Hd07t5XCbAdvFYhDlZYmJnGCvF90DmA"
CHAT_ID = "779164477"
# -------------------------

# --- TEST MODE ---
TEST_MODE = True
FAKE_SENDER = "FakeSenderWallet1111111111111111111111111111111"
FAKE_MINT = "FakeMintAddress2222222222222222222222222222222"
# -----------------

def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"}
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print("⚠️ Telegram send failed:", e)

def save_log(record):
    file_exists = os.path.isfile(OUTPUT_FILE)
    with open(OUTPUT_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=record.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(record)

def simulate_activity():
    """Simulates one inflow and one mint after 10s"""
    print("\n🧪 Simulation mode active — generating test inflow and mint...\n")
    now = datetime.now(timezone.utc)
    inflow_sig = "TESTINFLOW-" + now.strftime("%H%M%S")
    mint_sig = "TESTMINT-" + now.strftime("%H%M%S")

    # Step 1: Simulate inflow
    inflow_msg = (f"📥 <b>New inflow detected (test)</b>\n"
                  f"From: <code>{FAKE_SENDER}</code>\n"
                  f"Mint: <code>FakeMint</code>\n"
                  f"Amount: 5\n"
                  f"Tx: {inflow_sig}")
    print(inflow_msg)
    send_telegram(inflow_msg)

    record = {
        "detected_at": now.isoformat(),
        "sender_wallet": FAKE_SENDER,
        "mint": "FakeMint",
        "destination": WATCH_ADDRESS,
        "signature": inflow_sig,
        "block_time": now.isoformat()
    }
    save_log(record)

    # Step 2: Wait, then simulate mint
    time.sleep(10)
    mint_msg = (f"💥 <b>Mint Detected (test)</b>\n"
                f"By: <code>{FAKE_SENDER}</code>\n"
                f"Mint: <code>{FAKE_MINT}</code>\n"
                f"Destination: <code>FakeDest999</code>\n"
                f"Tx: {mint_sig}")
    print(mint_msg)
    send_telegram(mint_msg)

    record2 = {
        "detected_at": datetime.now(timezone.utc).isoformat(),
        "sender_wallet": FAKE_SENDER,
        "mint": FAKE_MINT,
        "destination": "FakeDest999",
        "signature": mint_sig,
        "block_time": datetime.now(timezone.utc).isoformat()
    }
    save_log(record2)
    print("\n✅ Simulation complete — check your Telegram and CSV.\n")

def main():
    print(f"🚀 Starting Mint Watcher (Test Mode: {TEST_MODE})")
    if TEST_MODE:
        simulate_activity()
    else:
        print("Switch TEST_MODE=False once ready for live blockchain tracking.")

if __name__ == "__main__":
    main()
