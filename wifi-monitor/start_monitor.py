#!/usr/bin/python3

import logging
import logging.handlers
import sniffer
import timed_buffer
import mongo_writer
import mongo_dao
import nickname_resolver
import signal
import unique_client_writer

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

    dao = mongo_dao.Mongo_DAO()
    dao.connect()
    
    #writer = mongo_writer.Mongo_Writer(dao)
    #buff = timed_buffer.Timed_Buffer(writer,60)

    unique_writer = unique_client_writer.Unique_Client_Writer()
    unique_writer.set_dao(dao)

    monitor = sniffer.Sniffer()
    monitor.add_writer(unique_writer)
    
    def keyboard_interrupt_handler(signum, frame):
        logger.info('Program terminated by keyboard interrupt')
        monitor.stop()

    signal.signal(signal.SIGINT, keyboard_interrupt_handler)

    monitor.start()

    logger.info('Exiting program')

if (__name__ == '__main__'):
    main()
