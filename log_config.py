import logging

log = logging.getLogger(__name__)
FORMAT = '%(asctime)s  %(message)s'

logging.basicConfig(filename='myapp.log',
                    format=FORMAT,
                    level=logging.INFO)
