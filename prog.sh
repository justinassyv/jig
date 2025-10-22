#!/bin/bash

# Script to flash and configure NRF52 using J-Link and nrfjprog

set -e  # Exit immediately if a command exits with a non-zero status

echo "Recovering device..."
nrfjprog --recover

echo "Erasing all memory..."
nrfjprog --eraseall

echo "Programming SoftDevice..."
nrfjprog --program s140_nrf52_7.3.0_softdevice.hex --verify

echo "Programming app_io..."
nrfjprog --program ./gen/app_io.hex --verify

echo "Programming app_boot..."
nrfjprog --program ./gen/app_boot.hex --verify

echo "Programming nrf_boot..."
nrfjprog --program nrf_boot.hex --verify

echo "Programming nrf_settings..."
nrfjprog --program nrf_settings.hex --verify

echo "Setting REGOUT0 to 3.0V (0x10001304 = 0xfffffffc)..."
# REGOUT0 voltage settings:
# 0xfffffffd -> 3.3V
# 0xfffffffc -> 3.0V
# 0xfffffff9 -> 2.1V
# 0xfffffff8 -> 1.8V
nrfjprog --memwr 0x10001304 --val 0xfffffffc --verify

echo "Configuring reset pin (P18)..."
nrfjprog --memwr 0x10001200 --val 0x00000012 --verify
nrfjprog --memwr 0x10001204 --val 0x00000012 --verify

echo "Resetting device..."
nrfjprog --reset

echo "Done!"
