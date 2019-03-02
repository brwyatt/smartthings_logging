import logging
import os


def setup_logging():
    logging.basicConfig()  # needed to run outside Lambda
    log = logging.getLogger()

    default_loglevel = 'INFO'
    loglevel = os.environ.get('LOGLEVEL', default_loglevel)

    try:
        log.setLevel(getattr(logging, loglevel))
        log.info('LogLevel set to "{0}"'.format(loglevel))
    except:
        log.setLevel(getattr(logging, default_loglevel))
        log.warning('LogLevel could not be set to "{0}", using default "{1}" '
                    'instead!'.format(loglevel, default_loglevel))

    return log
