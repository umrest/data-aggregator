#!/bin/bash

DIR=/home/pi/rest/data-aggregator
VENV=/home/pi/rest/venv

cd $DIR
source $VENV/bin/activate
while true; do
    #python3 tcp_serial_redirect.py /dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0 115200 -c localhost:8091
    python ser2tcp.py
    echo "TCP Serial Crashed..."
    sleep 2
done