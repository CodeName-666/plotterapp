import logging


def TestFunc(x,y):
    try: 
        z = x/y
        logging.info("Z = {}".format(z))
    except ZeroDivisionError as e:
        logging.error(e)


logging.basicConfig(filename='example.log', encoding='utf-8',format='%(asctime)s: %(levelname)s - %(message)s', level='ERROR')
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')
logging.error('And non-ASCII stuff, too, like Øresund and Malmö')


TestFunc(4,0)