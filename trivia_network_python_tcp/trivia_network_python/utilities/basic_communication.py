

import logging

from utilities import chatlib
class base_comunication:
    
    def __init__(self,debug_name):
        self.name=debug_name
        
    
    
    def recv_message_and_parse(self,conn):
            """
            Recieves a new message from given socket,
            then parses the message using chatlib.
            Paramaters: conn (socket object)
            Returns: cmd (str) and data (str) of the received message. 
            If error occured, will return None, None
            """
            full_msg=None
            try:
               # while full_msg is None:
                full_msg= conn.recv(chatlib.MAX_MSG_LENGTH).decode()
               
                host = conn.getpeername()
                self.logger.debug("[SERVER] ", host, "msg: ", full_msg)
       
                cmd, data = chatlib.parse_message(full_msg)
                return (cmd, data)
            
            except ConnectionResetError  as e:
                self.logger.error(f"Failed to connect to {chatlib.SERVER_IP}:{chatlib.SERVER_PORT}. Error: {str(e)}")    
                self.close_connection(conn)
            
            except TimeoutError:
                self.logger.error("Connection timed out.")
                return None, None
            
            except ValueError as e:  
                self.logger.error(f"Failed to parse message. Error: {str(e)}")
                return None, None
            
            finally:
                if conn.fileno() == -1:  
                    self.logger.error("Socket has been properly closed.")    
            
    def build_and_send_message(self, conn , code, data):
            """
                Builds a new message using chatlib, wanted code and message. 
                Prints debug info, then sends it to the given socket.
                Paramaters: conn (socket object), code (str), data (str)
                Returns: Nothing
            """
            try:
                full_message_data_formated=chatlib.build_message(code,data)
                
                self.logger.debug(f"[CLIENT] sending message: {full_message_data_formated} (Command: {code}, Data: {data})")
                
                conn.send(full_message_data_formated.encode())
                
            except BrokenPipeError as e:
                self.logger.error(f"Failed to send message: Broken pipe. Error: {str(e)}")
                self.close_connection(conn)
                
            except OSError as e:
                self.logger.error(f"Failed to send message due to socket error. Error: {str(e)}")
                
            finally:
                self.logger.info("Attempt to build and send message ended.")
            