#!/usr/bin/env python3
import RPi.GPIO as GPIO
import subprocess
import os
import sys
import time

# ─── Multiplexer Pin Definitions ───────────────────────────────────────────────
PIN_A1, PIN_B1, PIN_C1 = 11, 13, 15   # MUX 1 control pins (BOARD numbering)
PIN_A2, PIN_B2, PIN_C2 = 29, 31, 33   # MUX 2 control pins
PIN_ENABLE = 18                        # Enable line (always HIGH)

# ─── Helper Functions for MUX Control ──────────────────────────────────────────
def setup_gpio():
    """Initialize GPIOs for both multiplexers."""
    GPIO.setmode(GPIO.BOARD)
    for p in [PIN_A1, PIN_B1, PIN_C1, PIN_A2, PIN_B2, PIN_C2, PIN_ENABLE]:
        GPIO.setup(p, GPIO.OUT)
        GPIO.output(p, GPIO.LOW)
    GPIO.output(PIN_ENABLE, GPIO.HIGH)
    print(f"GPIO ready, enable pin {PIN_ENABLE} set HIGH")

def select_channel_dual(channel):
    """
    Set both MUX 1 and MUX 2 to the same channel (0–7).
    """
    if not (0 <= channel <= 7):
        raise ValueError("Channel must be between 0 and 7")

    # Compute 3-bit binary values for A/B/C lines
    bit_a = channel & 0x01
    bit_b = (channel & 0x02) >> 1
    bit_c = (channel & 0x04) >> 2

    # Apply same bits to both MUX 1 and MUX 2
    for (pa, pb, pc) in [(PIN_A1, PIN_B1, PIN_C1), (PIN_A2, PIN_B2, PIN_C2)]:
        GPIO.output(pa, GPIO.HIGH if bit_a else GPIO.LOW)
        GPIO.output(pb, GPIO.HIGH if bit_b else GPIO.LOW)
        GPIO.output(pc, GPIO.HIGH if bit_c else GPIO.LOW)

    print(f"Both MUXes → Channel {channel}  (C={bit_c}, B={bit_b}, A={bit_a})")

def cleanup():
    """Clean up GPIO pins safely."""
    GPIO.output(PIN_ENABLE, GPIO.LOW)
    GPIO.cleanup()
    print("GPIO cleaned up.")

# ─── Flashing Function ─────────────────────────────────────────────────────────
def flash_board(script_path):
    """Execute prog.sh using bash and return True/False for success."""
    if not os.path.exists(script_path):
        print(f"Error: File not found → {script_path}")
        return False

    os.chmod(script_path, 0o755)
    work_dir = os.path.dirname(script_path)
    try:
        subprocess.run(["bash", script_path], cwd=work_dir, check=True)
        print("✓ Programming completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Flashing failed (exit code {e.returncode})")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

# ─── Main Logic ────────────────────────────────────────────────────────────────
def main():
    script_path = "/home/rpi/Documents/sonora/prog.sh"
    setup_gpio()

    try:
        for ch in range(1, 7):   # channels 1 → 6
            print(f"\n=== Selecting channel {ch} on BOTH multiplexers ===")
            select_channel_dual(ch)
            time.sleep(0.5)      # allow signals to stabilize

            print(f"Flashing board on channel {ch}…")
            if flash_board(script_path):
                print(f"✓ Board on channel {ch} flashed successfully.")
            else:
                print(f"⚠️ Flash failed on channel {ch}, continuing to next.")
            time.sleep(1)        # short delay between boards

        print("\n✅ All channels processed successfully.")
    except KeyboardInterrupt:
        print("\n⛔ User interrupted.")
    finally:
        cleanup()

if __name__ == "__main__":
    main()