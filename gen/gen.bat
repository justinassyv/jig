nrfutil settings generate --family NRF52840 --application app_io.hex --application-version 0x5 --bootloader-version 0x06 --bl-settings-version 0x02 ../nrf_settings.hex
nrfutil pkg generate --hw-version 0x20101 --sd-req 0x123 --application-version 0x010005 --application app_io.hex --key-file railSensor.pem ../railSensor_ota_io.zip
pause

