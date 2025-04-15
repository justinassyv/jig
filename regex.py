import re

# Sample data
data = """
- RTC configured.
- RTC initialized.
- lowRateAccel initialized.
- lowRateAccel passed self-test
- hiRateAccel initialized
- Ext temperature sensor initialized.
- PSRAM initialized.
- PSRAM test passed.
- exFlash initialized, size 8192 KB.
- Ext NFC configuring ...
- Ext NFC initialized.
- DUID          : F0B00D136D4DXXXX
- MAC Address   : C7662F8CXXXX
- Hw ver        : 2.1
- Appl ver      : 0.4
- Ble adv. name : PRABS_F0B00D136D4DXXX
- VSC_V  3.500
- VMC_V  2.964
- DET_RANGE_G     8
- DET_SAMPLING_HZ 400
- DET_TRESHOLD_G  1.000
- DET_TRESHOLD_MS 10.000
- RTC initialization error.
- PSRAM test error.
"""

# Regex patterns
patterns = {
    "RTC_configured": r"RTC configured",
    "RTC_initialized": r"RTC initialized",
    "lowRateAccel_initialized": r"lowRateAccel initialized",
    "lowRateAccel_self_test": r"lowRateAccel passed self-test",
    "hiRateAccel_initialized": r"hiRateAccel initialized",
    "temperature_sensor_initialized": r"Ext temperature sensor initialized",
    "PSRAM_initialized": r"PSRAM initialized",
    "PSRAM_test_passed": r"PSRAM test passed",
    "exFlash_size": r"exFlash initialized, size (\d+) KB",
    "DUID": r"DUID\s+:\s+([A-F0-9]+)",
    "MAC_address": r"MAC Address\s+:\s+([A-F0-9]+)",
    "Hw_ver": r"Hw ver\s+:\s+([\d\.]+)",
    "Appl_ver": r"Appl ver\s+:\s+([\d\.]+)",
    "Ble_adv_name": r"Ble adv\. name\s+:\s+(\S+)",
    "VSC_V": r"VSC_V\s+([\d\.]+)",
    "VMC_V": r"VMC_V\s+([\d\.]+)",
    "DET_RANGE_G": r"DET_RANGE_G\s+(\d+)",
    "DET_SAMPLING_HZ": r"DET_SAMPLING_HZ\s+(\d+)",
    "DET_TRESHOLD_G": r"DET_TRESHOLD_G\s+([\d\.]+)",
    "DET_TRESHOLD_MS": r"DET_TRESHOLD_MS\s+([\d\.]+)"
}

# Extract data
extracted_data = {}

# Process each line individually
for line in data.splitlines():
    line = line.strip()
    for key, pattern in patterns.items():
        match = re.search(pattern, line, re.IGNORECASE)
        if match:
            # Check if the word 'error' appears in the same line
            if "error" in line.lower():
                extracted_data[key] = False
            else:
                # Set boolean for initialized/configured/self-test or capture the matched value
                if "initialized" in key or "configured" in key or "self_test" in key:
                    extracted_data[key] = True
                else:
                    extracted_data[key] = match.group(1) if match.groups() else True

# Ensure all keys are printed even if False
for key in patterns.keys():
    if key in extracted_data:
        print(f"{key}: {extracted_data[key]}")
    else:
        print(f"{key}: False")  # Default to False if key is missing
