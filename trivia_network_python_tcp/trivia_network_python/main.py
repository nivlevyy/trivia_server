
import argparse
import logging
import client_fol.client_tcp 
import server_fol.server_tcp 
import logger_manager

server_on=False
host='0.0.0.0'
port=5678
def main():
    global server_on

    logger_manager.LoggerManager.setup_logging(logging.DEBUG,logging.INFO,'trivia_main.log')
    logger= logger_manager.LoggerManager.get_logger('Main_App_logger')
    
    role=input("please make a choice server or client")
    parser = argparse.ArgumentParser(description="Trivia Game Application")
    
    parser.add_argument('--role', choices=['server', 'client'],required=True, help="--------> Choose whether to run the server or client")
    parser.add_argument('--port', type=int, default=5678, help="Port number to use for communication. Default is 5678.")
    parser.add_argument('--host', type=str, default='127.0.0.1', help="Host address for client/server. Default is localhost.")

    args = parser.parse_args()
    
    if args.role == 'server' and server_on==False:  
       logger.info("Starting Server...")
       server_fol.server_tcp.server.starting_server(args.host,args.port)
       server_on=True
       
    elif args.role == 'client':
        logger.info("starting new client...")
        client_fol.client_tcp.client.starting_client()
    # if role=='server':
    #     logger.info("Starting Server...")
    #     server_fol.server_tcp.server.starting_server(host,port)
    #     server_on=True
    # elif role =='client':
    #     logger.info("starting new client...")
    #     client_fol.client_tcp.client.starting_client()
    
    
if __name__ == "__main__":
    main()