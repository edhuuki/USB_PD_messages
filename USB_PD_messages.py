# This is a python script aimed to encode and decode EPR PD messages
# it includes fucntionality to decode saleae binary files of CC lines
# Author: Erik Huuki
# email: edhuuki@gmail.com

# USB power delivery spec, table 6.6 data messages type 

# Directed graph detailing flow of messages
# Keys are messages, values are lists of potential next messages

import array
import struct
import sys
from collections import namedtuple
from PD_messages_binary_mapping import *

EPR_entry_directed_graph = {
    'start':['EPR_mode_enter'],
    'abort_EPR_entry':['SPR_mode'],
    'EPR_mode_enter':['sink_EPR_capable'],
    'sink_EPR_capable':['abort_EPR_entry','source_EPR_capable'],
    'source_EPR_capable':['abort_EPR_entry','source_EPR_capable_now'],
    'source_EPR_capable_now':['abort_EPR_entry','send_EPR_ack'],
    'send_EPR_ack':['recieved_EPR_ack','captive_cable'],
    'recieved_EPR_ack':['received_enter_successful','error_SSR'],# send soft reset (SSR)
    'captive_cable':['is_Vconn_source1','send_enter_successful'],
    'received_enter_successful':['error_SSR','EPR_mode'],
    'is_Vconn_source1':['Vconn_swap','is_Vconn_source2'],
    'Vconn_swap':['is_Vconn_source2'],
    'is_Vconn_source2':['abort_EPR_entry','EPR_cable'],
    'EPR_cable':['abort_EPR_entry','send_enter_successful'],
    'send_enter_successful':['received_enter_successful','EPR_mode'],
    'EPR_mode':[],
    'SPR_mode':[],
    'error_SSR':[]
    }

class epr_message_encode:


    def __init__(self,**kwargs):
        if 'source' in kwargs:
            self.source = kwargs['source']
        
        pass
    
    def control(self,extended, no_of_DOs, id, port_pwr_role, spec_rev, port_data_role, message_type):

        pass

    def data(self):
        pass

    def extended(self):
        pass

class decode_CC_data_file:
    def __init__(self,**kwargs)-> None:

        if 'Saleae_bin' in kwargs:
            with open(kwargs['Saleae_bin'], 'rb') as f:
                data = _parse_saleae_digital(f)

            self.messages = decode_BMC.saleae_data_2_binary_messages(data)  # Path to bin of saleae file
            self.PD_logs = [pd_message_decode(message) for message in self.messages]

    def logs2csv(self,file):
        if '.csv' != file[-4:]:
            raise Exception('File does not end in .csv')

        with open(file,'w') as file:
            
            # header = ['SOP','Header','Extended Header','Data','EOP'] # The eventual goal of decoding

            header = ['SOP','Header']
            file.write(','.join(header))

            for message in self.PD_logs:
                file.write(str(message))

class pd_message_decode:

    def __init__(self,message=None):
        if message==None:
            raise Exception('Message is Nonetype')
        preamble = '01'*32
        if message[:64]!= preamble:
            raise Exception('Message does not start with preamble.')

        self.sop_kcodes,self.SOP = self.parse_sop(message[64:84])

        if len(message)>85:
            self.header = self.parse_header(message[84:104],self.SOP)
        else:
            self.header= None
    
    # parses start of packets on the PD line
    # Section 5.4 details what is and isn't a valid ordered set.
    def parse_sop(self,sop):
        '''
        SOP is 20 bits composed of 4x5bit kcodes that are reversed
        the following code takes in the raw binary 20 bit value,
            - groups it into the reversed 5bit kcodes
            - reverses each 5bit kcode
            - Maps the kCodes via the PD_messages_binary_mapping k_codes5b dict
            - returns the list of decoded Kcodes and which SOP
        '''
        kcode_bin = [sop[i:i+5] for i in range(0,20,5)]                     # 5bit grouping
        kcode_messages = [fiveBit_fourBit_decoder[five_bit] for five_bit in kcode_bin]    # Maps the kcodes to their message
        message_key = ''.join(kcode_messages)                 # Comverts the ordered set to a key
        
        ## Uncommment the line below for debug
        # print(kcode_bin, kcode_messages, sop_mapping_inv[message_key])

        return (kcode_messages,sop_mapping_inv[message_key])
        


    def parse_header(self,raw_bin_header,sop):

        # need to decode 20 bit 5b signal to 4b

        raw_bin_header = [raw_bin_header[i:i+5] for i in range(0,20,5)]
        raw_bin_header = ''.join([fiveBit_fourBit_decoder[fiveB_group] for fiveB_group in raw_bin_header])
        header_format = {
            'Extended':raw_bin_header[15], 
            'no_DOs':raw_bin_header[12:15],
            'MessageID':raw_bin_header[9:12],
            'Spec_Revision':raw_bin_header[6:8]    
            }
        
        if header_format['no_DOs']=='000':
            header_format['Message_Type']=control_messages[raw_bin_header[:5]]
        else:
            header_format['Message_Type']=data_messages[raw_bin_header[:5]]


        if sop=='SOP':
            header_format['Port_Power_Role'] = raw_bin_header[8]
            header_format['Port_Power_Role'] = raw_bin_header[5]
        else:
            header_format['Cable_plug'] = raw_bin_header[8]
            header_format['Reserved'] = raw_bin_header[5]

        return header_format




    def __str__(self):
        header = 'Header: '+str(self.header) if self.header else ''
        return ','.join([self.SOP,header])


# Decode biphase mark code wave_forms
# raw data that can be decoded includes exported binary saleae digital waveforms
class decode_BMC:
    def data2BMC(data,datainvert= False):

        str2bool = lambda c: bool(int(c))       # converts '1' to True and '0' to False
        invertboolstr = lambda c: '0' if c=='1' else '1'
        next_bit = lambda b,b_1: invertboolstr(b) if str2bool(b_1) else b

        biphase_signal = '1' # instantiate the first signal as a 1
        biphase_signal += '0' if data[0]=='1' else '1'

        for bit in data[1:]:
            biphase_signal+= invertboolstr(biphase_signal[-1])
            biphase_signal+= next_bit(bit,biphase_signal[-1])

        if datainvert:
            return ''.join(map(invertboolstr,biphase_signal))

        return biphase_signal

    def BMC2data(bmc_raw):
        f = lambda a: '0' if a[0]==a[1] else '1'
        temp = zip(bmc_raw[:-1:2],bmc_raw[1::2])
        pairs = [a+b for a,b in temp]
        
        return ''.join(map(f,pairs))

    def saleae_data_2_binary_messages(saleae_wave_form,clk_freq = 300e3):
        # Digital edges is a list of pos/neg edges with the respective time at which it occurs
        # Bug detected in this code

        t_n0 = [0]+saleae_wave_form
        t_deltas = [round((t1-t0)*clk_freq*2) for t0,t1 in zip(t_n0,saleae_wave_form)]  # list of timing information in integer amounts of clock cycles
        # print(t_deltas)
        data = ''
        i = 0
        while i<len(t_deltas):
            if t_deltas[i]==2:
                data+='0'
                i+=1

            elif t_deltas[i]==1 and t_deltas[i+1]==1:
                data+='1'
                i+=2
            
            elif t_deltas[i]>2:
                data+=','
                i+=1
            else:
                i+=1

        data = ''.join(data)
        data = data.split(',')
        data = list(filter(lambda x:x!='', data))
        return list(data)

def _parse_saleae_digital(f):
    # Parse header
    
    TYPE_DIGITAL = 0
    TYPE_ANALOG = 1
    expected_version = 0
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

    return list(transition_times)