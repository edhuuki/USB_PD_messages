from USB_PD_messages import *

messages = decode_CC_data_file(Saleae_bin='digital_0.bin')
for log in messages.PD_logs:
    print(log)
