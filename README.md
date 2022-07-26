# USB PD messages

Currently decodes the headers of the PD messages for the purposes of debugging. Includes decoding headers for EPR messages. 

Decode PD messages, USB Power Delivery Specification Revision 3.1 Version 1.5

- https://www.usb.org/document-library/usb-power-delivery



## Decoding the digital data from a saleae recording the CC line

Raw data of digital_0.bin if of a 5V contract after a hard reset

```python
from USB_PD_messages import decode_CC_data_file as decode

messages = decode(Saleae_bin='digital_0.bin')

print(messages.PD_logs[0])
# HRST,

```





## Decoding BMC

Section 5.8

```python
from USB_PD_messages import decode_BMC

test_BMC = '11010100'

print(decode_BMC.BMC2data(test_BMC))
# 0110

```


