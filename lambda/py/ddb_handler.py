import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """

    :param event: the event that this function will process
    :param context: context object for the function
    :return:
    """
    logger.info(f'EVENT: {event}')
    if event['eventName'] == 'MODIFY':
        return
