# regex_parser.py
import re
import datetime

def parse_uart_data(data: str):
    """
    Apply regex patterns to UART data and return a dictionary
    of extracted values and a DUID for file naming.
    """
    patterns = {
        "RTC_configured": r"RTC configured",
        "RTC_initialized": r"RTC initialized",
        "LR_ACC_initialized": r"lowRateAccel initialized",
        "LR_ACC_self_test": r"lowRateAccel passed self-test",
        "HR_ACC_initialized": r"HR_ACC initialized",
        #"HR_ACC_self_test": r"hiRateAccel passed self-test",
        "PSRAM_initialized": r"PSRAM initialized",
        "PSRAM_test_passed": r"PSRAM test passed",
        "exFlash_size": r"exFlash initialized, size (\d+) KB",
        "Ext NFC initialized": r"Ext NFC initialized",
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

    extracted_data = {}
    for line in data.splitlines():
        line = line.strip()
        for key, pattern in patterns.items():
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                if "error" in line.lower():
                    extracted_data[key] = False
                else:
                    if "initialized" in key or "configured" in key or "self_test" in key:
                        extracted_data[key] = True
                    else:
                        extracted_data[key] = match.group(1) if match.groups() else True

    # Fill missing keys with False
    for key in patterns.keys():
        if key not in extracted_data:
            extracted_data[key] = False

    # Determine filename from DUID, fallback to timestamp
    duid = extracted_data.get("DUID", None)
    if not duid:
        duid = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    return extracted_data, duid
