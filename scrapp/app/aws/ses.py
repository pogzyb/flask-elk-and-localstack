from structlog import get_logger

from . import get_client


logger = get_logger(__name__)


def send_email_with_ses(subject, sender, recipient, html):
    ses = get_client('ses')
    ses.send_email(
        Source=sender,
        Destination={
            'ToAddresses': [recipient],
            'BccAddresses': [sender]
        },
        Message={
            'Subject': {
                'Data': subject,
            },
            'Body': {
                'Html': {
                    'Data': html,
                }
            }
        }
    )
    logger.info(f'SES sent email to {recipient}')
