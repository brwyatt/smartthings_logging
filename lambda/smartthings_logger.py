from smartthings_logging.logging import setup_logging
from smartthings_logging import collect_and_log


log = setup_logging()


def run(event, context):
    collect_and_log()
