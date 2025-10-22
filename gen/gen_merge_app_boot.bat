mergehex --merge app_boot.hex app_io.hex --output ../app.hex
nrfutil settings generate --family NRF52840 --application ../app.hex --application-version 0x5 --bootloader-version 0x06 --bl-settings-version 0x02 ../nrf_settings.hex
nrfutil pkg generate --hw-version 0x20101 --sd-req 0x123 --application-version 0x010005 --application ../app.hex --key-file railSensor.pem ../railSensor_ota.zip
pause

