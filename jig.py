#!/usr/bin/env python3
import RPi.GPIO as GPIO
import subprocess
import os
import time
import serial

# Import the parsing function
from regex_parser import parse_uart_data

# ─── Configuration ─────────────────────────────────────────────────────────────
SCRIPT_PATH = "/home/rpi/Documents/sonora/prog.sh"
UART_PORT = "/dev/ttyACM0"   # UART device path
BAUD_RATE = 115200           # UART baud rate
READ_TIMEOUT = 2             # seconds to listen for UART data
USE_BOARD = True             # BOARD = physical pins, BCM = GPIO numbers
RESET_PIN = 7                # Reset signal (BOARD pin 7 = GPIO4)
RESET_PULSE = 0.1            # seconds to hold reset LOW

# ─── Multiplexer Pins ─────────────────────────────────────────────────────────
if USE_BOARD:
    GPIO.setmode(GPIO.BOARD)
    PIN_A1, PIN_B1, PIN_C1 = 11, 13, 15
    PIN_A2, PIN_B2, PIN_C2 = 29, 31, 33
    PIN_ENABLE = 18
else:
    GPIO.setmode(GPIO.BCM)
    PIN_A1, PIN_B1, PIN_C1 = 17, 27, 22
    PIN_A2, PIN_B2, PIN_C2 = 5, 6, 13
    PIN_ENABLE = 24

# ─── GPIO Setup ───────────────────────────────────────────────────────────────
def setup_gpio():
    for p in [PIN_A1, PIN_B1, PIN_C1, PIN_A2, PIN_B2, PIN_C2, PIN_ENABLE, RESET_PIN]:
        GPIO.setup(p, GPIO.OUT)
        GPIO.output(p, GPIO.LOW)
    GPIO.output(PIN_ENABLE, GPIO.HIGH)
    GPIO.output(RESET_PIN, GPIO.HIGH)
    print("GPIO initialized")

def select_channel_dual(channel):
    bit_a = channel & 1
    bit_b = (channel >> 1) & 1
    bit_c = (channel >> 2) & 1
    for (pa, pb, pc) in [(PIN_A1, PIN_B1, PIN_C1), (PIN_A2, PIN_B2, PIN_C2)]:
        GPIO.output(pa, bit_a)
        GPIO.output(pb, bit_b)
        GPIO.output(pc, bit_c)
    print(f"Both MUXes → Channel {channel}  (C={bit_c}, B={bit_b}, A={bit_a})")

def pulse_reset():
    GPIO.output(RESET_PIN, GPIO.LOW)
    time.sleep(RESET_PULSE)
    GPIO.output(RESET_PIN, GPIO.HIGH)
    print("Reset pulse done")

def cleanup():
    GPIO.output(PIN_ENABLE, GPIO.LOW)
    GPIO.output(RESET_PIN, GPIO.HIGH)
    GPIO.cleanup()
    print("GPIO cleaned up")

# ─── Flashing & UART ─────────────────────────────────────────────────────────
def flash_board():
    if not os.path.exists(SCRIPT_PATH):
        print(f"Error: File not found → {SCRIPT_PATH}")
        return False
    os.chmod(SCRIPT_PATH, 0o755)
    try:
        subprocess.run(["bash", SCRIPT_PATH], cwd=os.path.dirname(SCRIPT_PATH), check=True)
        print("✓ Programming completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Flashing failed (exit code {e.returncode})")
        return False

def read_uart_and_save():
    try:
        with serial.Serial(UART_PORT, BAUD_RATE, timeout=1) as ser:
            print(f"Listening on {UART_PORT} ({BAUD_RATE} baud)...")
            start_time = time.time()
            data = b""
            while time.time() - start_time < READ_TIMEOUT:
                if ser.in_waiting:
                    data += ser.read(ser.in_waiting)
                time.sleep(0.1)
            if data:
                decoded = data.decode(errors="ignore")
                print("📡 UART response:\n", decoded)
                parsed, duid = parse_uart_data(decoded)
                filename = f"{duid}.txt"
                with open(filename, "w") as f:
                    for k, v in parsed.items():
                        f.write(f"{k}: {v}\n")
                print(f"✅ Parsed data saved to {filename}")
            else:
                print("⚠️ No UART data received")
    except serial.SerialException as e:
        print(f"⚠️ UART error: {e}")

# ─── Main Logic ───────────────────────────────────────────────────────────────
def main():
    setup_gpio()
    try:
        for ch in range(1, 7):
            print(f"\n=== Selecting channel {ch} ===")
            select_channel_dual(ch)
            time.sleep(0.5)

            print(f"Flashing board on channel {ch}...")
            if flash_board():
                pulse_reset()
                time.sleep(0.5)
                read_uart_and_save()
            else:
                print(f"⚠️ Flash failed on channel {ch}.")
            time.sleep(1)
    finally:
        cleanup()

if __name__ == "__main__":
    main()
