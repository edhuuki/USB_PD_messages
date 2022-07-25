
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
	'00101':'Reserved',
	
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

fiveBit_4Bit_decoder = {
	'11110':'0000',
	'01001':'0001',
	'10100':'0010',
	'10101':'0011',
	'01000':'0100',
	'01011':'0101',
	'01110':'0110',
	'01111':'0111',
	'10010':'1000',
	'10011':'1001',
	'10110':'1010',
	'10111':'1011',
	'11010':'1100',
	'11011':'1101',
	'11100':'1110',
	'11101':'1111'
	}



# Reference section 6.3 table 6-5
# Key value pairs are 'bit stream':'control message'
control_messages = {
	'00000':'Reserved',
	'00001':'GoodCRC',
	'00010':'GotoMin',
	'00011':'Accept',
	'00100':'Reject',
	'00101':'Ping',
	'00110':'PS_RDY',
	'00111':'Get_Source_Cap',
	'01000':'Get_Sink_Cap',
	'01001':'DR_Swap',
	'01010':'PR_Swap',
	'01011':'Vconn_Swap',
	'01100':'Wait',
	'01101':'Soft_reset',
	'01110':'Data_Reset',
	'01111':'Data_Reset_Complete',
	'10000':'Not_Supported',
	'10001':'Get_source_Cap_extended',
	'10010':'Get_status',
	'10011':'FR_Swap',
	'10100':'Get_PPS_Status',
	'10101':'Get_Country_Codes',
	'10110':'Get_Sink_Cap_extended',
	'10111':'Get_Source_info',
	'11000':'Get_Revision'
	}


for i in range(16,32):		# Instantiates all the bits that map to 'Reserved' in control messages
	control_messages[str(bin(i))[2:]] = 'Reserved'

preamble = ''.join(['01']*32) # preamble starts with 64 alternating bits starting with 0

# Refernce section 6.2.1.1 table 6-1
# Key value pairs are formating of bits for each SOP
# sop:[bit_mappings]

message_header_bit_format={
	'SOP':['Extended', 'no_DOs', 'MessageID', 'Port_Power_Role','Spec_Revision','Port_Data_Role','Message_Type'],
	'SOP\'':['Extended', 'no_DOs', 'MessageID', 'Cable_Plug','Spec_Revision','Reserved','Message_Type'],
	'SOP\'\'':['Extended', 'no_DOs', 'MessageID', 'Cable_Plug','Spec_Revision','Reserved','Message_Type']
}

'''
bit 15		: 	Extended 	(bool if the header is 32 or 16 bits for True/False)
bit 14:12	: 	no_DOs 		(number of 32 bit data objects)
bit 11:9	: 	MessageID 	(Message ID)
bit 8		: 	Port_Power_Role ()
bit 8		: 	Cable_Plug 	()
bit 7:6		:	Spec_revision
bit 4:0		: 	Message_type

'''