"""
mint_watch_test_v4_sim.py
Auto-switch startup logic for Render 24/7 runtime
Detects TEST_MODE from environment or defaults to live tracking.
"""

import os
import time
from datetime import datetime, timezone
import requests

# Environment variables
TEST_MODE = os.getenv("TEST_MODE", "false").lower() == "true"
HELIUS_API_KEY = os.getenv("HELIUS_API_KEY")
TARGET_ADDRESS = os.getenv("TARGET_ADDRESS", "9NERQjLetzquGwdKt3X4gZ8fE8fPfSkj2xo2esmUjWsz")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Telegram alert function
def send_telegram(message: str):
    if not TELEGRAM_BOT_TOKEN or not CHAT_ID:
        print("⚠️ Telegram configuration missing, skipping alert.")
        return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": message})
    except Exception as e:
        print("❌ Telegram error:", e)

# --- TEST MODE ---
def run_test_mode():
    print("🧪 Running in TEST MODE (simulated inflows/mints)...")
    send_telegram("🧪 Mint Watcher started in TEST MODE (simulation running).")
    while True:
        time.sleep(20)
        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        msg = f"📥 [TEST] Simulated inflow + mint at {now}"
        print(msg)
        send_telegram(msg)

# --- LIVE MODE ---
def run_live_mode():
    print(f"🚀 Mint Watcher live-tracking inflows for {TARGET_ADDRESS}")
    send_telegram(f"✅ Mint Watcher is LIVE on Render, monitoring inflows for:\n{TARGET_ADDRESS}")
    while True:
        # Replace this placeholder with your inflow detection + mint logic
        try:
            # Example check: simple heartbeat ping
            now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
            print(f"🕒 Live check at {now}")
            time.sleep(60)  # check interval
        except Exception as e:
            print("❌ Live loop error:", e)
            send_telegram(f"⚠️ Live tracker error: {e}")
            time.sleep(10)

# --- STARTUP LOGIC ---
if __name__ == "__main__":
    mode_label = "TEST" if TEST_MODE else "LIVE"
    print(f"🚀 Starting Mint Watcher (Mode: {mode_label})")
    if TEST_MODE:
        run_test_mode()
    else:
        run_live_mode()

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
