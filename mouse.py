"""
Custom Joystick Mouse - Host Script
Authors: Nitish Matta & Jash Chirag Monani
LNMIIT - 24UEC217 & 24UEC206

Reads serial data from the Arduino and translates it into
real mouse movements and clicks using pyautogui.

Requirements:
    pip install pyserial pyautogui

Usage:
    python mouse.py
"""

import sys
import serial
import pyautogui

# ─────────────────────────────────────────────
#  CONFIGURATION — change COM_PORT to match your Arduino
#  Windows: "COM3", "COM4", etc.
#  macOS:   "/dev/cu.usbmodem14101"  (run: ls /dev/cu.* to find it)
#  Linux:   "/dev/ttyACM0" or "/dev/ttyUSB0"
# ─────────────────────────────────────────────
COM_PORT  = "COM3"
BAUD_RATE = 9600

# Safety: disable pyautogui's fail-safe corner (top-left moves mouse fast)
# Set to True during development to allow emergency stop
pyautogui.FAILSAFE = True
pyautogui.PAUSE    = 0  # No extra delay between pyautogui calls


def parse_packet(line: str):
    """
    Parse a serial packet from the Arduino.

    Expected format: "<click_status> <dx> <dy> m"
    Example:         "z 5 -3 m"

    Returns:
        (click_status, dx, dy) or None if the packet is invalid.
    """
    parts = line.strip().split()

    # Validate: must have exactly 4 tokens and end with 'm'
    if len(parts) != 4 or parts[3] != 'm':
        return None

    click_status = parts[0]           # 'c' = click, 'z' = no click
    try:
        dx = int(parts[1])
        dy = int(parts[2])
    except ValueError:
        return None

    return click_status, dx, dy


def main():
    print(f"[*] Connecting to Arduino on {COM_PORT} at {BAUD_RATE} baud...")

    try:
        ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=0.01)  # ← CHANGE PORT IF NEEDED
    except serial.SerialException as e:
        print(f"[ERROR] Could not open serial port: {e}")
        print("  • Check that the Arduino is connected.")
        print(f"  • Verify that '{COM_PORT}' is correct in this script.")
        print("  • On Windows: check Device Manager > Ports (COM & LPT).")
        sys.exit(1)

    print(f"[+] Connected! Move the joystick to control the cursor.")
    print("[*] Press Ctrl+C in this window to stop.\n")

    try:
        while True:
            # Read one line from the serial buffer
            raw = ser.readline()
            if not raw:
                continue

            try:
                line = raw.decode('utf-8', errors='ignore')
            except Exception:
                continue

            result = parse_packet(line)
            if result is None:
                continue  # Skip malformed packets silently

            click_status, dx, dy = result

            # Move cursor (relative to current position)
            # Negate dy because screen Y increases downward but
            # joystick "up" should move the cursor up (negative screen Y)
            if dx != 0 or dy != 0:
                pyautogui.moveRel(dx, -dy, duration=0)

            # Perform a left click if button was pressed
            if click_status == 'c':
                pyautogui.click()

            # Optional: print movement for debugging
            # print(f"dx={dx}, dy={dy}, click={click_status}")

    except KeyboardInterrupt:
        print("\n[*] Stopped by user.")
    finally:
        ser.close()
        print("[*] Serial port closed.")


if __name__ == "__main__":
    main()
