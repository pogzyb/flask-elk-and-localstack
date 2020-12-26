import logging

from app.aws_utils import get_client


logger = logging.getLogger(__name__)


def send_email_with_ses(subject, html, recipient, sender):
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


