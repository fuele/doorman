#!/usr/bin/python3

import logging
import logging.handlers
import sniffer
import timed_buffer
#import file_recorder

def create_logger():
    logger = logging.getLogger('wifi-monitor')
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    fh = logging.handlers.RotatingFileHandler('wifi-monitor.log', maxBytes=1024, backupCount=1)
    fh.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s [%(name)s] [%(levelname)s]: %(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger

def main():
    logger = create_logger()
    logger.info('Starting program')

    #recorder = file_recorder.File_Recorder()

    buff = timed_buffer.Timed_Buffer(10)

    monitor = sniffer.Sniffer(buff)
    monitor.start()

    logger.info('Exiting program')

if (__name__ == '__main__'):
    main()
