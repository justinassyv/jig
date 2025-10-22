nrfjprog --recover
:: reset pin P18
nrfjprog --memwr 0x10001200 --val 0x00000012 --verify
nrfjprog --memwr 0x10001204 --val 0x00000012 --verify
nrfjprog --reset
pause

