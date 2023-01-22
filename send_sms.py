import os

# for sms
from twilio.rest import Client


def add_to_sms(phone_number):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body="ding dong wake up, you're in the matrix",
        from_="+16044098733",
        to="+1" + str(phone_number),
    )

    print(message.sid)

    return True
