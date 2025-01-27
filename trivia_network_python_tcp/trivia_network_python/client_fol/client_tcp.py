
from utilities import chatlib
from logger_manager import LoggerManager
import socket
import time
import logging



SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678


#client class
LoggerManager.setup_logging(logging.DEBUG,logging.WARN,'all_clients.log')

class client:
    
    def __init__(self):
        self.client_socket = None
        self.msg=[]
        self.full_message_data_formated=""
        self.logger =LoggerManager.get_logger('client_logger')
        self.logger.info('client initilized')
        
    def error_and_exit(self,error_msg):
        print(error_msg)
       # exit
    #setup a socket in client side 
        
    def connect(self):
        attempts=10
        
        while attempts > 0:  
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((SERVER_IP,SERVER_PORT))
                self.logger.info("Connected to server successfully.")
                return client_socket
            
            except (ConnectionRefusedError,TimeoutError,OSError) as e:
                self.logger.error(f"Connection failed: Error: {str(e)}")
                attempts-=1
                time.sleep(2)
                
        self.logger.info("Failed to connect after multiple attempts.")
        self.client_socket.close()
               
        
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
            self.logger.debug(f"[SERVER] {host} msg: {full_msg}")
   
            cmd, data = chatlib.parse_message(full_msg)
            return (cmd, data)
        
        except ConnectionResetError  as e:
            self.logger.error(f"Failed to connect to {SERVER_IP}:{SERVER_PORT}. Error: {str(e)}")    
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
        
    def build_and_send_message(self, conn : socket, code, data):
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
            


    def register(self):
        if self.client_socket is not None:
           #add regex to password and check if a username exist
           pass 

    def login(self,conn):
        attampts=5
        while attampts>0:
            
            try:
  
                username = input("Please enter username: \n")
                self.msg.append(username)
                password= input("Please enter password: \n")
                self.msg.append(password)
                self.build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["login_msg"][0],chatlib.join_data(self.msg))
                cmd,data = self.recv_message_and_parse(conn)
                
                if cmd == chatlib.PROTOCOL_SERVER["login_ok_msg"][0]:
                    self.logger.info ("login was succsusful")
                    self.logger=LoggerManager.get_logger(f'client_{username}')
                    break
                
                elif cmd == chatlib.PROTOCOL_SERVER["login_failed_username_msg"][0]:
                    self.logger.info("username is incorrect try again")
                       
                elif cmd == chatlib.PROTOCOL_SERVER["login_failed_username_msg"][0]:
                    self.logger.info("username is incorrect try again")
                   
                self.msg=""    
          
            except (ConnectionResetError, ConnectionAbortedError) as e:
                self.logger.error(f"Login failed due to connection error: {str(e)}")
                self.close_connection(conn)
                
            finally:
                attampts-=1
                if attampts==0:
                    self.logger.info("login exceeded maxisum attempts close connection")
                    conn.close()
            
    

    def logout(self,conn:socket):
        try:       
            self.build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["logout_msg"][0],"")
            self.logger.info("Logout sent to server.")
        except OSError as e:
            self.logger.error(f"Logout failed. Error: {str(e)}")    
        finally:
            conn.close()
            self.logger.info("Client socket closed.")
        
    def logged(self,conn:socket):
        self.build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["logged_msg"][0],"")
        cmd,data = self.recv_message_and_parse(conn)
        
        if cmd == chatlib.PROTOCOL_SERVER["login_answer"][0]:
            self.logger.debug(f'[server]: the users login to system are :{data}')
        
    def my_score(self,conn:socket):
        self.build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["my_score_msg"][0],"")
        cmd,data = self.recv_message_and_parse(conn)
        
        if cmd == chatlib.PROTOCOL_SERVER["score"][0]:
            self.logger.info(f'[server]: your score is :{data}')
            
    def high_score(self,conn:socket):
        self.build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["high_score_msg"][0],"")
        cmd,data = self.recv_message_and_parse(conn)
        
        if cmd == chatlib.PROTOCOL_SERVER["all_score"][0]:
            self.logger.info(f'[server]: all users scores :{data}')
            
    def qustion_handaling(self,conn):
        
        answer_list=[]
        
        self.build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["get_question_msg"][0],"")
        cmd,data = self.recv_message_and_parse(conn)
        question_id_str,question=self.question_formater(data) 
        
        while True:
            if cmd == chatlib.PROTOCOL_SERVER["error"][0]:
                self.logger.info("error")
                break
            else:    
                choose_charecter=input(f'{question}'+'''
choose answer from [1-4]
''')
                
                if int(choose_charecter) not in range(1,5):
                    self.logger.info("not in range please try again")
                    continue
                else:
                    answer_list.extend([question_id_str, choose_charecter]) 
                    self.build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["send_answer_msg"][0],chatlib.join_data(answer_list))
                    cmd,data = self.recv_message_and_parse(conn)
                    if cmd == chatlib.PROTOCOL_SERVER["no_more_questions"][0]:
                        break
                    elif cmd == chatlib.PROTOCOL_SERVER["correct_answer"][0]:
                        self.logger.info("correcttt")
                        break
                    elif(cmd == chatlib.PROTOCOL_SERVER["incorrect_answer"][0]):
                        self.logger.info("wronggg")
                        break
                    else:
                        self.error_and_exit("error")
                        
                        
    def question_formater(self,data):
        question_lst = chatlib.split_data(data,6)
        question = f'''
Question number {question_lst[0]}:
{question_lst[1]}
1. {question_lst[2]}
2. {question_lst[3]}
3. {question_lst[4]}
4. {question_lst[5]}
'''
        return question_lst[0], question
    
    def client_communication(self):
        
        client_socket = self.connect()
        
        self.login(client_socket)
        
        while True:
            self.msg = input(f'''
please choose from this game options(1-5):
1.answer a question
2.Get my score
3.Get high score
4.Get logged users
5.Quit
''')
            if(self.msg =="1"):
                self.qustion_handaling(client_socket)
            elif(self.msg =="2"):
                self.my_score(client_socket)
            elif(self.msg =="3"):
                self.high_score(client_socket)   
            elif(self.msg =="4"):
                self.logged(client_socket)
            elif(self.msg =="5"):
                self.logout(client_socket)
                break

    @staticmethod
    def starting_client():
        client_obj = client()
        client_obj.client_communication()
        


def main():
    client_obj = client()
    client_obj.client_communication()
    

if __name__ == "__main__":
    main()
