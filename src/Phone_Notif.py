from twilio.rest import Client

account_sid = 'AC5dab613b3f3707eb4034157c415b4e83'
auth_token = 'e1c3d26e72fffa181b92ba01fcb0bf9b'


def send_message(text):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        messaging_service_sid='MG2114c2fc78be4d9840464da37209c8f1',
        body=text,
        to='+33679717090'
    )

    return


if __name__ == '__main__':
    send_message('hello Mathilde')
