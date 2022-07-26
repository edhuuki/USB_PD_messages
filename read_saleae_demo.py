from epr_PD_messages import *
import array
import struct
import sys
from collections import namedtuple
from PD_messages_binary_mapping import *


def parse_digital(f):
    TYPE_DIGITAL = 0
    TYPE_ANALOG = 1
    expected_version = 0

    DigitalData = namedtuple('DigitalData', ('initial_state', 'begin_time', 'end_time', 'num_transitions', 'transition_times'))

    # Parse header
    identifier = f.read(8)
    if identifier != b"<SALEAE>":
        raise Exception("Not a saleae file")

    version, datatype = struct.unpack('=ii', f.read(8))

    if version != expected_version or datatype != TYPE_DIGITAL:
        raise Exception("Unexpected data type: {}".format(datatype))

    # Parse digital-specific data
    initial_state, begin_time, end_time, num_transitions = struct.unpack('=iddq', f.read(28))

    # Parse transition times
    transition_times = array.array('d')
    transition_times.fromfile(f, num_transitions)

    return transition_times

filename = 'digital_0.bin'

with open(filename, 'rb') as f:
    data = parse_digital(f)


sample = decode_BMC.saleae_data_2_binary_messages(data)

# for i,message in enumerate(sample):
#     print(len(message))
#     try:
#         temp = epr_message_decode(message)
#         print(i,temp,'\n')
#     except:
#         print('error\n')

i = 0
messages = sample
for message in messages:
    test = epr_message_decode(message)
    print(test.SOP)
    if test.header:
        print(message[84:104])
        try:
            print(control_messages[test.header['Message_Type'][::-1]])
        except:
            print('\nERROR\n')
    print('\n')

        

