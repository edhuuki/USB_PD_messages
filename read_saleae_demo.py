from epr_PD_messages import *
import array
import struct
import sys
from collections import namedtuple


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
    return DigitalData(initial_state, begin_time, end_time, num_transitions, transition_times)

filename = 'digital_6.bin'

with open(filename, 'rb') as f:
    data = parse_digital(f)


sample = decode_BMC.saleae_data_2_binary_messages(data)


with open('test.txt','w') as file:

    for message in sample:
        # print(message)
        temp = epr_message_decode(message)
        print(temp,'\n')


        file.write(message+'\n\n')

        

