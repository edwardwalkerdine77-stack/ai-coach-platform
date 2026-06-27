import subprocess
import time
import webbrowser
import os
import signal
import sys


BACKEND_CMD = "python -m uvicorn api:app --reload"
FRONTEND_CMD = "python -m http.server 5500 --directory frontend"
URL = "http://localhost:5500"


processes = []


def start_process(command, title):
    print(f"\n[STARTING] {title}")
    return subprocess.Popen(command, shell=True)


def shutdown():
    print("\n[SHUTTING DOWN SYSTEM]")

    for p in processes:
        try:
            p.terminate()
        except:
            pass

    sys.exit(0)


def main():

    print("⚽ AI FOOTBALL COACH - PRO LAUNCHER")
    print("-----------------------------------")

    # Start backend
    backend = start_process(BACKEND_CMD, "Backend API (FastAPI)")
    processes.append(backend)

    time.sleep(3)

    # Start frontend
    frontend = start_process(FRONTEND_CMD, "Frontend Server")
    processes.append(frontend)

    time.sleep(2)

    # Open browser
    print("\n[OPENING BROWSER]")
    webbrowser.open(URL)

    print("\n✅ SYSTEM RUNNING")
    print("Frontend: http://localhost:5500")
    print("Backend:  http://127.0.0.1:8000")
    print("\nPress CTRL+C to stop everything")

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        shutdown()


if __name__ == "__main__":
    main()