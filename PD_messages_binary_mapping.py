
## Inverts a dictionary. 
def invert_dict(dictionary):
	temp = {}

	for key, val in dictionary.items():
		temp[''.join(val)] = key

	return temp


# Reference section 5.6
# key value pairs are 'SOP type':[message order]
sop_mapping = {
	'SOP':['SYNC1','SYNC1','SYNC1','SYNC2'],
	'SOP\'':['SYNC1','SYNC1','SYNC3','SYNC3'],
	'SOP\'\'':['SYNC1','SYNC3','SYNC1','SYNC3'],
	'SOP\'_Debug':['SYNC1','RST2','RST2','SYNC3'],
	'SOP\'\'_Debug':['SYNC1','RST2','SYNC3','SYNC2'],
	'HRST':['RST1', 'RST1', 'RST1','RST2'],			# Hard reset
	'CRST':['RST1','SYNC1','RST1','SYNC3']			# Cable reset
	}
sop_mapping_inv = invert_dict(sop_mapping)


# Section 5.3 table 5-1
# Key value pairs are 'bit stream':'message'
k_codes5b = {
	'11110':'0',
	'01001':'1',
	'10100':'2',
	'10101':'3',
	'01000':'4',
	'01011':'5',
	'01110':'6',
	'01111':'7',
	'10010':'8',
	'10011':'9',
	'10110':'A',
	'10111':'B',
	'11010':'C',
	'11011':'D',
	'11100':'E',
	'11101':'F',
	'11000':'SYNC1',
	'10001':'SYNC2',
	'00111':'RST1',
	'11001':'RST2',
	'01101':'EOP',		# End of packet 
	'00110':'SYNC3',
	'00000':'Reserved',
	'00001':'Reserved',
	'00010':'Reserved',
	'00011':'Reserved',
	'00100':'Reserved',
	'00101':'Reserved'
	}
k_codes4b = {
	'0000':'0',
	'0001':'1',
	'0010':'2',
	'0011':'3',
	'0100':'4',
	'0101':'5',
	'0110':'6',
	'0111':'7',
	'1000':'8',
	'1001':'9',
	'1010':'A',
	'1011':'B',
	'1100':'C',
	'1101':'D',
	'1110':'E',
	'1111':'F'
	}
# Table 5-1 pg 95
# Values are reversed so that indexes matches the bit encoding 
fiveBit_fourBit_decoder = {
	'01111':'0000',		# 0
	'10010':'1000',		# 1
	'00101':'0100',		# 2
	'10101':'1100',		# 3
	'01010':'0010',		# 4
	'11010':'1010',		# 5
	'01110':'0110',		# 6
	'11110':'1110',		# 7
	'01001':'0001',		# 8
	'11001':'1001',		# 9
	'01101':'0101',		# A
	'11101':'1101',		# B
	'01011':'0011',		# C
	'11011':'1011',		# D
	'00111':'0111',		# E
	'10111':'1111',		# F
	'00011':'SYNC1',
	'10001':'SYNC2',
	'11100':'RST1',
	'10011':'RST2',
	'10110':'EOP',		# End of packet 
	'01100':'SYNC3'
	}



# Reference section 6.3 table 6-5
# Key value pairs are 'bit stream':'control message'
control_messages = {
	'00000':'Reserved',
	'10000':'GoodCRC',
	'01000':'GotoMin',
	'11000':'Accept',
	'00100':'Reject',
	'10100':'Ping',
	'01100':'PS_RDY',
	'11100':'Get_Source_Cap',
	'00010':'Get_Sink_Cap',
	'10010':'DR_Swap',
	'01010':'PR_Swap',
	'11010':'Vconn_Swap',
	'00110':'Wait',
	'10110':'Soft_reset',
	'01110':'Data_Reset',
	'11110':'Data_Reset_Complete',
	'00001':'Not_Supported',
	'10001':'Get_source_Cap_extended',
	'01001':'Get_status',
	'11001':'FR_Swap',
	'00101':'Get_PPS_Status',
	'10101':'Get_Country_Codes',
	'01101':'Get_Sink_Cap_extended',
	'11101':'Get_Source_info',
	'00011':'Get_Revision'
	}

# for i in range(16,32):		# Instantiates all the bits that map to 'Reserved' in control messages
# 	control_messages[str(bin(i))[3:]] = 'Reserved'



data_messages = {
	'00000':'Reserved',
	'10000':'Source_Capabilities',
	'01000':'Request',
	'11000':'BIST',						# Built in self test
	'00100':'Sink_Capabilities',
	'10100':'Battery_Status',
	'01100':'Alert',
	'11100':'Get_Country_Info',
	'00010':'Enter_USB',
	'10010':'EPR_Request',
	'01010':'EPR_Mode',
	'11010':'Source_Info',
	'00110':'Revision',
	'10110':'Reserved',
	'01110':'Reserved',
	'11110':'Vendor_Defined'
}
# for i in range(16,32):
# 	data_messages[bin(i)[-1:1:-1]] = 'Reserved'

# print(data_messages)



preamble = ''.join(['01']*32) # preamble starts with 64 alternating bits starting with 0

# Refernce section 6.2.1.1 table 6-1
# Key value pairs are formating of bits for each SOP
# sop:[bit_mappings]

message_header_bit_format={
	'SOP':['Extended', 'no_DOs', 'MessageID', 'Port_Power_Role','Spec_Revision','Port_Data_Role','Message_Type'],
	'SOP\'':['Extended', 'no_DOs', 'MessageID', 'Cable_Plug','Spec_Revision','Reserved','Message_Type'],
	'SOP\'\'':['Extended', 'no_DOs', 'MessageID', 'Cable_Plug','Spec_Revision','Reserved','Message_Type']
}



# EPR mode data objects
# pg. 200
# table 6-50

epr_action = {
	bin(0)[-1:1:-1]: 'Reserved',
	bin(1)[-1:1:-1]: 'Enter',
	bin(2)[-1:1:-1]: 'Enter Acknowledge',
	bin(3)[-1:1:-1]: 'Enter Succ',
	bin(4)[-1:1:-1]: 'Reserved',
	bin(5)[-1:1:-1]: 'Reserved',
	bin(6)[-1:1:-1]: 'Reserved'
}