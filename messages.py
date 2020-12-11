import argparse
from models import User, Message
from psycopg2 import connect, OperationalError
from psycopg2.errors import UniqueViolation
from clcrypto import check_password

parser = argparse.ArgumentParser()

parser.add_argument('-u', '--username', help='username')
parser.add_argument('-p', '--password', help='password (min 8 characters)')
parser.add_argument('-t', '--to', help='username to send the message to')
parser.add_argument('-s', '--send', help='message text')
parser.add_argument('-l', '--list', help='list messages', action='store_true')

args = parser.parse_args()


def send_message(cursor, username, password, to_username, text):
    user = User.load_user_by_username(cursor, username)
    to_user = User.load_user_by_username(cursor, to_username)
    if user is None:
        print('User does not exist!')
    elif check_password(password, user.hashed_password) is False:
        print('Password is not correct!')
    else:
        if to_user is None:
            print('User does not exist!')
        elif len(text) > 255:
            print('The message is longer than 255 characters!')
        else:
            new_message = Message(user.id, to_user.id, text)
            new_message.save_to_db(cursor)
            print('Message is sent.')


def message_list(cursor, username, password):
    user = User.load_user_by_username(cursor, username)
    if user is None:
        print('User does not exist!')
    elif check_password(password, user.hashed_password) is False:
        print('Password is not correct!')
    else:
        list_messages = Message.load_all_messages(cursor, user.id)
        for message in list_messages:
            from_user = User.load_user_by_id(cursor, message.from_id)
            print(f'from: {from_user}')
            print(f'date: {message.creation_date}')
            print(message.text)

