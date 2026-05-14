#! /bin/bash
echo SUBSYSTEM==\"tty\", ATTRS{idVendor}==\"0403\", ATTRS{idProduct}==\"6001\", ATTRS{serial}==\"A501HUV2\", SYMLINK+=\"3dprinter ttyUSB99\" | sudo tee /etc/udev/rules.d/99-usb-serial.rules -a
