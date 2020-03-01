import logging

from app.aws_utils.api import get_client


logger = logging.getLogger(__name__)


def send_email(subject, body, html, recipient, sender):
    ses = get_client('ses')
    ses.send_email(
        Source=sender,
        Destination={
            'ToAddresses': [
                recipient,
            ],
            'BccAddresses': [
                sender,
            ]
        },
        Message={
            'Subject': {
                'Data': subject,
            },
            'Body': {
                'Text': {
                    'Data': body,
                },
                'Html': {
                    'Data': html,
                }
            }
        },

    )


