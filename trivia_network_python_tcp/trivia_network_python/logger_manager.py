import logging

class LoggerManager:
    
    @staticmethod
    def setup_logging(console_level=logging.DEBUG, file_level=logging.ERROR, log_file=None):
        """Setup logging configuration with different levels for console and file output"""
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)  

       
        console_handler = logging.StreamHandler()
        console_handler.setLevel(console_level)
        console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(file_level)
            file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s [File: %(filename)s, Line: %(lineno)d, Function: %(funcName)s]')
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)

    @staticmethod
    def get_logger(name):
        """Returns a logger by name"""
        return logging.getLogger(name)
    
    # help function of logger  for reading the file of a client to see if therer is an errors occured 
    def read_log_file_filtered(self,filename, client_name=None, log_level=None):
        """Reads and filters log messages by client name and/or log level."""
        try:
             with open(filename, 'r') as file:
                 lines = file.readlines()
                  

             filtered_lines = []
             for line in lines:
                 
                 if client_name and f'client_{client_name}' not in line:
                     continue
                 
                 if log_level not in line:
                     continue

                 filtered_lines.append(line.strip())

            
             for line in reversed(filtered_lines):
                  self.logger.info(line) # can print it instead if its easier to read 
                 
        except FileNotFoundError:
                self.logger.error(f"Error: The file '{filename}' was not found.")
        except Exception as e:
                self.logger.error(f"An error occurred while reading the log file: {str(e)}")
        