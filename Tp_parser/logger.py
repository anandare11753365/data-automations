
import logging
import os
from logging.handlers import TimedRotatingFileHandler
import sys

FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")
class Logger:
    def __init__(self, name = __name__, output_path=None):
        self.LOG_FILE = "tp_parser.log"
        self.name= name
        if output_path == None:
            if os.path.isdir("C:\\temp"):
                # pass
                output_path = "C:\\temp"
            else:
                output_path = "C:\\temp"
                os.makedirs(output_path)
        else:
            if os.path.isdir(output_path):
                pass
            else:
                logging.info('%s path does not exist, thus output_path is set to C:\\temp'%(output_path))
                output_path = "C:\\temp"
        self.logger = logging.getLogger(self.name)
        self.output_path = output_path
    
    
    
    

    def get_console_handler(self):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(FORMATTER)
        return console_handler
    def get_file_handler(self):
        file_handler = TimedRotatingFileHandler(os.path.join(self.output_path,self.LOG_FILE), when='midnight')
        file_handler.setFormatter(FORMATTER)
        return file_handler

    def get_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG) # better to have too much log than not enough
        logger.addHandler(self.get_console_handler())
        logger.addHandler(self.get_file_handler())
    # with this pattern, it's rarely necessary to propagate the error up to parent
        logger.propagate = False
        return logger

    
    def loginfo(self,message):
        # self.file_handler().info(message)
        return self.get_logger().info(message)

    def logdebug(self,message):
        # self.file_handler().debug(message)
        return self.get_logger().debug(message)

    def logwarning(self,message):
        # self.file_handler().warning(message)
        return self.get_logger().warning(message)

    def logerror(self,message):
        # self.file_handler().error(message)
        return self.get_logger().error(message)


if __name__ == '__main__':
    log  = Logger()
    # log.test()
    log.logdebug("bla bla")