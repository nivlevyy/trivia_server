
import logging
import socket 
import requests
from utilities import chatlib
from logger_manager import LoggerManager
import select
import random
import json
import os


ERROR_MSG = "Error! "
SERVER_PORT = 5678
SERVER_IP = "0.0.0.0"
#globals
##users:dictionry of |username (keys): dictionry (value) | holds data about user
# (values in the inner dic are password ,score,num of questions asked )
users={}
#logged_users:dictionry of |socket adress (key):username str (value) 
#we will get the socket address tuple by using .getpeername()
logged_users={}
questions={}
pending_questions = {}
LoggerManager.setup_logging(logging.DEBUG,logging.ERROR,'server.log')
base_path=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
class server:

    def __init__( self, host=SERVER_IP, port=SERVER_PORT):
        self.name="Trivia server"
        self.host=host
        self.port=port
        self.server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client_sockets=[]
        self.data=""
        
        self.server_massages_to_send=[]
        self.user_names_and_passwords_db={}
        
        self.logger =LoggerManager.get_logger('server_logger')
        self.logger.debug('server initilized')
        
    @property
    def get_name(self):
        return self.NAME
    
    def setup_socket(self):
        
        """
        Creates new listening socket and returns it
        Recieves: -
        Returns: the socket object
        """
        try:
            global users
            global questions
            
            self.server_socket.bind((SERVER_IP,SERVER_PORT))
            server_address=(SERVER_IP,SERVER_PORT)
            
            self.logger.info(("starting up on {} port {}".format)(*server_address))
            users = self.load_user_database()
            self.logger.info("users data base loaded successfully")
            questions = self.load_questions()
            self.logger.info("questions loaded successfully")
            
            self.server_socket.listen()
            
        except OSError as e:
            self.logger.error(f"Socket setup failed. Error: {str(e)}")
            if self.server_socket and self.server_socket.fileno() != -1:
                self.server_socket.close()
            self.logger.info("Server socket closed due to an error.")
        finally:
            if self.server_socket and self.server_socket.fileno() == -1:
                self.logger.info("Server socket was already closed.")
      
      
    def load_questions(self):
        """
        Loads questions list from a JSON file.
        Returns: questions dictionary.
        """
        ##add more questions to json
        questions_json_path=os.path.join(base_path,'data','questions.json')
        try:
            
            with open(questions_json_path, 'r') as question_file:
                questions = json.load(question_file)
            self.logger.debug("Questions loaded successfully.")
            
        except FileNotFoundError:
            self.logger.error("questions.json not found. Starting with an empty questions bank.")
            questions = {}
            
        return questions
    
    #web service option
    
    def load_questions_from_web (self):
       
        global questions
        
        web_trivia_url= "https://opentdb.com/api.php?amount=50&type=multiple"
        
        try:
            web_server_response=requests.get(web_trivia_url)
            
            if web_server_response.status_code == 200:
                data = web_server_response.json() 
                questions_in_dic = data.get("results",[])
                
                for indx,question in enumerate(questions_in_dic,start=1):
                   
                    question_text = question["question"]
                    correct_answer = question["correct_answer"]
                    incorrect_answers = question["incorrect_answers"]   

                    all_answers = incorrect_answers + [correct_answer]
                    random.shuffle(all_answers)
                    
                    correct_answer_indx=all_answers.index(correct_answer)+1


                    questions[indx]={
                        'question': question_text,
                        'answers': all_answers,
                        'correct': correct_answer_indx
                        }

        except:
             self.logger.error(f"Failed to get questions from the web. Status code: {web_server_response.status_code}")


    def load_user_database(self):
         """
         Loads users list from a JSON file.
         Returns: users dictionary.
         """
         user_json_path=os.path.join(base_path,'data','users.json')
         try:
             with open(user_json_path, 'r') as users_file:
                users = json.load(users_file)
                self.logger.debug("Users database loaded successfully.")
             
         except FileNotFoundError:
            self.logger.error("users.json not found. Starting with an empty users database.")
            users = {}
             
         except json.JSONDecodeError:
            self.logger.error("Error: Failed to decode user database.")
            users = {}
             
         finally:
            self.logger.debug("Finished loading user database.")  
            return users
    
        
    def save_user_database(self,users):
        """
        Saves users list to a JSON file.
        Recieves: users dictionary.
        Returns: None
        """
        try:
            user_json_path=os.path.join(base_path,'data','users.json')

            with open(user_json_path, 'w') as w_users_file:
                json.dump(users, w_users_file, indent=4)
            self.logger.debug("Users database saved successfully.")
            
        except Exception as e:
            self.logger.error(f"Failed to save users database. Error: {str(e)}")
    
# HELPER SOCKET METHODS

    def build_and_send_message(self, conn , code, data):
        """
            Builds a new message using chatlib, wanted code and message. 
            Prints debug info, then sends it to the given socket.
            Paramaters: conn (socket object), code (str), data (str)
            Returns: Nothing
        """
        full_message_data_formated=chatlib.build_message(code,data)
        # Debug print
        self.logger.debug(f"[SERVER] sending message: {full_message_data_formated} (Command: {code}, Data: {data})")
        
        conn.send(full_message_data_formated.encode())  

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
          #  self.logger.debug("[CLIENT] ", host, "msg: ", full_msg)
            self.logger.debug(f"{full_msg}")
            cmd, data = chatlib.parse_message(str(full_msg))
            return (cmd, data)
        
        except Exception as e:
            self.logger.error(f"Failed to connect to {host[0]}:{host[1]}. Error: {str(e)}")    
            return	
    
    #server comunication
    ##add more 
    
    def send_error(self,conn, error_msg):
        """
        Send error message with given message
        Recieves: socket, message error string from called function
        Returns: None
        """
        self.build_and_send_message(conn,chatlib.PROTOCOL_SERVER["error"][0],error_msg)
	
        
    ##### MESSAGE HANDLING
        
    def handle_login_message(self,conn, data):
        """
        Gets socket and message data of login message. Checks  user and pass exists and match.
        If not - sends error and finished. If all ok, sends OK message and adds user and address to logged_users
        Recieves: socket and data
        Returns: None (sends answer to client)
        """
        global users  # This is needed to access the same users dictionary from all functions
        global logged_users								# To be used later
        client_address = conn.getpeername()
        
        username,password=chatlib.split_data(data,2)
        
        if username not in users.keys():
            self.build_and_send_message(conn,chatlib.PROTOCOL_SERVER["login_failed_username_msg"][0],"")
            return 
        
        if password != users[username]["password"]:
            self.build_and_send_message(conn,chatlib.PROTOCOL_SERVER["login_failed_password_msg"][0],"")
            return
        else:
            logged_users[client_address]=username
            self.build_and_send_message(conn,chatlib.PROTOCOL_SERVER["login_ok_msg"][0],"")
    
    def server_socket_handaling(self):
        """
        main server scaning for active sockets in each list using select func
        Recieves: None
        Returns: None
        """
        while True:
            ready_to_read, ready_to_write, in_error = select.select([self.server_socket]+self.client_sockets,self.client_sockets, [])
        
            for current_socket in ready_to_read :
                if current_socket is self.server_socket:
                    (client_socket,client_address) = self.server_socket.accept()
                    
                    self.logger.info(f"New client joined! {client_address}")
                    self.client_sockets.append(client_socket)
                    self.logger.debug("add to the active clients list ")
                 
                else:
                    try:
                        self.logger.info(f"Waiting to receive a message from client {current_socket.getpeername()}")  # Debug print
                        cmd, data = self.recv_message_and_parse(current_socket)
                        self.handle_client_message(current_socket,cmd, data)
                        
                    except (ConnectionResetError, BrokenPipeError) as e:
                        self.client_sockets.remove(client_socket)
                        client_socket.close()  
                        self.logger.error("client socket has been currapted and was closed")
                      
                        
            for messages in self.server_massages_to_send:
                # itrating on all messages in the queue if there is 
                curr_client_socket,data =messages
                if curr_client_socket in ready_to_write:
                    # improve to send only if a socket is in ready to write 
                     client_socket.send(data.encode())
                    # debug.print_client_connected(self.client_sockets)
                     self.server_massages_to_send.remove(data)
            
        
        

    def handle_logout_message(self,conn:socket):
        """
        Closes the given socket (in laster chapters, also remove user from logged_users dictioary)
        Recieves: socket
        Returns: None
        """
        global logged_users
        client_address =conn.getpeername()
        if client_address in logged_users.keys():
            self.logger.info(f" user in ip: {client_address[0]} ,port:{client_address[1]} is going to be disconected ")
        del logged_users[client_address]
        self.client_sockets.remove(conn)
        conn.close()
        
    def handle_logged_message(self,conn):
        """
        """
        
        global logged_users
        
        formated_msg = " ,".join(logged_users.values())
        self.build_and_send_message(conn,chatlib.PROTOCOL_SERVER["login_answer"][0],formated_msg)


    def handle_getscore_message(self,conn, username):
        """
        Sends to the socket YOURSCORE message with the user's score.
        Recieves: socket and username (str)
        Returns: None (sends answer to client)
        """
        global users
        
        score= users[username]["score"]
        self.build_and_send_message(conn,chatlib.PROTOCOL_SERVER["score"][0],score)
    
    def handle_highscore_message(self,conn):
        """
        """
        
        global users
        all_score_msg = "\n"+self.build_user_score_data_msg()
        self.build_and_send_message(conn,chatlib.PROTOCOL_SERVER["all_score"][0],all_score_msg)
        
    def build_user_score_data_msg(self):
        """
        build msg(str) with all users formated include
        """
        global users
        sorted_users_by_score= sorted(users.items(),key=lambda x:x[1]["score"],reverse=True)
        list_of_users_str =[f'{i+1}. {username}:{data["score"]}' for i, (username ,data) in enumerate( sorted_users_by_score)]
        all_score_msg = "\n".join(list_of_users_str)
        return all_score_msg
    ## can be updated to friends logged in after sending friend request msg
    # and extand communications via server management    
    
    def handle_question_message(self,conn,username):
        """
        """
        
        question=self.create_random_question(username)
        if question is None:
            self.build_and_send_message(conn,chatlib.PROTOCOL_SERVER["no_more_questions"][0],"")
        else:
            self.build_and_send_message(conn,chatlib.PROTOCOL_SERVER["send_question"][0],question)
            #add function to add questions to questions that already asked in users
    

    def create_random_question(self,username):
        """
        Returns a string representing a YOUR_QUESTION command, using random picked question
        Example: id|question|answer1|answer2|answer3|answer4
        """
        
        global questions
        global users
        global pending_questions
        
        full_msg_list=[]
        
        questions_asked =set(users[username]["questions_asked"])
        reamaining_questions= set(questions.keys()) - questions_asked
        
        if not reamaining_questions:
            return None
        
        random_question_key = random.choice(list(reamaining_questions))
        
        pending_questions[username]= int(random_question_key)
        
        full_msg_list.append(str(random_question_key))
        
        selected_question = questions[random_question_key]
        
        question,answers = selected_question["question"],selected_question["answers"]
        full_msg_list.append(question)
        full_msg_list.extend(answers)
        msg_str=chatlib.join_data(full_msg_list)
        
        return msg_str
    
    
    def handle_answer_message(self,conn,username,data):
        
        global users
        global pending_questions
        
        Identifier_and_answer=chatlib.split_data(data,2)
        question_id=Identifier_and_answer[0]
        
        if int(Identifier_and_answer[0]) == pending_questions[username]:
            if int(Identifier_and_answer[1]) == questions[question_id]['correct']:
              users[username]["score"] += 5  
              (users[username]["questions_asked"]).append(Identifier_and_answer[0])
              self.save_user_database(users)
              self.build_and_send_message(conn,chatlib.PROTOCOL_SERVER["correct_answer"][0],"")
            else:
                self.build_and_send_message(conn,chatlib.PROTOCOL_SERVER["incorrect_answer"][0],"")
        else:
            self.send_error(conn,ERROR_MSG)	
            
    def handle_client_message(self,conn, cmd, data):
        """
        Gets message code and data and calls the right function to handle command
        Recieves: socket(conn), message code(command for the server) and data (content of the message)
        Returns: None
        """
        global logged_users	 # To be used later
        
        try:
            client_address = conn.getpeername()
            client_logged = client_address in logged_users.keys()
            if (not client_logged ) or (cmd == chatlib.PROTOCOL_CLIENT["login_msg"][0]):
                self.handle_login_message(conn,data)
            else:
            	
                username = logged_users[client_address]
            	
                if cmd == chatlib.PROTOCOL_CLIENT["logout_msg"][0]:
                    self.handle_logout_message(conn)
                elif (cmd == chatlib.PROTOCOL_CLIENT["logged_msg"][0]):  
                    self.handle_logged_message(conn)
                elif (cmd == chatlib.PROTOCOL_CLIENT["my_score_msg"][0]):
                    self.handle_getscore_message (conn,username)
                elif (cmd == chatlib.PROTOCOL_CLIENT["high_score_msg"][0]):
                    self.handle_highscore_message(conn)
                elif (cmd == chatlib.PROTOCOL_CLIENT["get_question_msg"][0]):
                    self.handle_question_message(conn,username)
                elif (cmd == chatlib.PROTOCOL_CLIENT["send_answer_msg"][0]):
                    self.handle_answer_message(conn,username,data)
                else:
                    self.send_error(conn,ERROR_MSG)
                    
        except KeyError as e:
            self.send_error(conn, f"Invalid command received: {str(e)}")
            
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            self.send_error(conn, ERROR_MSG)
    @staticmethod
    def starting_server(host='0.0.0.0',port=5678):
        game_server=server(host,port) 
        game_server.setup_socket()
        game_server.server_socket_handaling()

def main():
    # Initializes global users and questions dicionaries using load functions, will be used later

    game_server=server() 
   
    game_server.setup_socket()
    game_server.server_socket_handaling()
   
	
	



if __name__ == '__main__':
	main()        
