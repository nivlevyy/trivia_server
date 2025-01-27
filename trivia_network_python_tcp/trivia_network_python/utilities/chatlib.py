# Protocol Constants

from math import e
from shlex import join

CMD_FIELD_LENGTH = 16	# Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4   # Exact length of length field (in bytes)
MAX_DATA_LENGTH = 10**LENGTH_FIELD_LENGTH-1  # Max size of data field according to protocol
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"     # Delimiter character in protocol
DATA_DELIMITER = "#"     # Delimiter in the data part of the message

# Protocol Messages 
# In this dictionary we will have all the client and server command names
#####change to enums affecting in every sending and  recv msg #####
PROTOCOL_CLIENT = {
"login_msg" : ("LOGIN",1),
"logout_msg" : ("LOGOUT",0),

"logged_msg": ("LOGGED",0),

"get_question_msg":("GET_QUESTION",0),
"send_answer_msg":("SEND_ANSWER",1),

"my_score_msg":("MY_SCORE",0),
"high_score_msg":("HIGH_SCORE",0),

} # .. Add more commands if needed


PROTOCOL_SERVER = {
"login_ok_msg" : ("LOGIN_OK",0),
"login_failed_username_msg":("USERNAME_ERROR",0),
"login_failed_password_msg":("PASSWORD_ERROR",0),
"login_failed_msg" : ("ERROR",0),
"login_answer":("LOGGED_ANSWER",),
"send_question":("YOUR_QUESTION",5),
"correct_answer":("CORRECT_ANSWER",0),
"incorrect_answer":("WRONG_ANSWER",0),
"score":("YOUR_SCORE",0),
"all_score":("ALL_SCORE",0),
"error":("ERROR",0),
"no_more_questions":("NO_QUESTIONS",0)
} # ..  Add more commands if needed


# Other constants

ERROR_RETURN = None  # What is returned in case of an error

#@staticmethod
def build_message(cmd, data):
	"""
	Gets:
    command **cmd (str) and **data field (str) and creates a valid protocol message
	Returns:
    **str or **None if error occured
	"""
	str_data=str(data)
	protocol=""
	length_of_data = ''
	full_msg = ""
	
	if not is_cmd_valid(cmd):
		return ERROR_RETURN
	elif(len(str_data)>MAX_DATA_LENGTH):
		return ERROR_RETURN
	else :
		protocol = f"{cmd:<16}"
		length_of_data=str(len(str_data)).zfill(LENGTH_FIELD_LENGTH)
	    	 
	full_msg = '|'.join([protocol,length_of_data,str_data])
	return full_msg

#@staticmethod
def is_cmd_valid(cmd):
    found_in_client = False
    found_in_server = False
    
    # Check in PROTOCOL_CLIENT
    for value in PROTOCOL_CLIENT.values():
        if cmd == value[0]:
            found_in_client = True
            break
    
    # Check in PROTOCOL_SERVER
    for value in PROTOCOL_SERVER.values():
        if cmd == value[0]:
            found_in_server = True
            break

    # New condition logic: if found in either client or server
    if found_in_client or found_in_server:
        return True  # Command is valid
    else:
        return False  # Command is invalid
	
#@staticmethod
def parse_message(data):
	"""
	Parses protocol message and returns command name and data field
	Returns: **cmd (str), **data (str). If some error occured, returns None, None
	"""
	cmd = ''
	msg = ''
	if len(data)<16:
		return ERROR_RETURN,ERROR_RETURN
	cmd = data[0:16].strip()
	if data[16] != '|' or data[21] != '|':
		return ERROR_RETURN,ERROR_RETURN
	if not any(cmd == value[0] for value in PROTOCOL_CLIENT.values())and not any ( cmd == value[0] for value in PROTOCOL_SERVER.values()):
		return ERROR_RETURN,ERROR_RETURN
	if data[17:21].isdigit():
		msg_len = int(data[17:21])
		if(msg_len<0):
			return ERROR_RETURN,ERROR_RETURN
		if msg_len ==len(data[22:]):
			msg = data[22:]	
	else:
		return ERROR_RETURN,ERROR_RETURN
	
	return cmd, msg

#@staticmethod	
def split_data(msg, expected_fields):
	"""
	Helper method. gets a string and number of expected fields in it. Splits the string 
	using protocol's data field delimiter (|#) and validates that there are correct number of fields.
	Returns:
    **list of fields if all ok. If some error occured, returns None
	"""
	msg_new_list = msg.split(DATA_DELIMITER)
	# i turned expected_fields -1 to expected_fields (chek if good)
	if (len(msg_new_list) == expected_fields):
		return msg_new_list
	else:
		return [ERROR_RETURN]
		
	
#@staticmethod
def join_data(msg_fields):
	"""
	Helper method. Gets a list, joins all of it's fields to one string divided by the data delimiter. 
	Returns:
    string that looks like cell1#cell2#cell3
	"""
	return DATA_DELIMITER.join(map(str, msg_fields))


