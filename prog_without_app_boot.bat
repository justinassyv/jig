nrfjprog --recover
nrfjprog --eraseall
nrfjprog --program s140_nrf52_7.3.0_softdevice.hex --verify
nrfjprog --program app.hex --verify
nrfjprog --program nrf_boot.hex --verify
nrfjprog --program nrf_settings.hex --verify
:: regout0 set to 3.0V
:: 0xfffffffd 3.3V
:: 0xfffffffc 3.0V
:: 0xfffffff9 2.1V
:: 0xfffffff8 1.8V
nrfjprog --memwr 0x10001304 --val 0xfffffffc --verify
:: reset pin P18
nrfjprog --memwr 0x10001200 --val 0x00000012 --verify
nrfjprog --memwr 0x10001204 --val 0x00000012 --verify
nrfjprog --reset
pause

