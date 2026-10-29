"""
Launcher script for CPU Scheduling Mini Project.
Starts the local Flask web app and opens the browser.
"""

import sys
import webbrowser
import threading
import time
from app import app

PORT = 5000
HOST = "127.0.0.1"

def open_browser():
    time.sleep(1.0)
    url = f"http://{HOST}:{PORT}"
    print(f"\n[+] Opening simulator in browser: {url}")
    try:
        webbrowser.open(url)
    except Exception:
        pass

def main():
    print("=" * 60)
    print("      CPU SCHEDULING MINI PROJECT (QUEUE & PRIORITY QUEUE)  ")
    print("=" * 60)
    print(f"[+] Python Version: {sys.version.split()[0]}")
    print(f"[+] Starting server at http://{HOST}:{PORT}")
    print("[+] Press Ctrl+C in terminal to stop.")
    print("=" * 60)

    threading.Thread(target=open_browser, daemon=True).start()
    app.run(host=HOST, port=PORT, debug=False)

if __name__ == "__main__":
    main()
