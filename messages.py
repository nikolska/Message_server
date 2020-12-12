import argparse
from models import User, Message
from psycopg2 import connect, OperationalError
from clcrypto import check_password

parser = argparse.ArgumentParser()

parser.add_argument('-u', '--username', help='username')
parser.add_argument('-p', '--password', help='password (min 8 characters)')
parser.add_argument('-t', '--to', help='username to send the message to')
parser.add_argument('-s', '--send', help='message text')
parser.add_argument('-l', '--list', help='list messages', action='store_true')

args = parser.parse_args()


def send_message(cursor, from_id, to_username, message_text):
    '''
    Send the message from  sender to recipient.
    If recipient doesn't exist or message text is longer than 255 characters function informs about that.
    :param cursor: the cursor class object
    :param int from_id: user ID who's send the message
    :param str to_username: user name to send the message to
    :param str message_text: message text
    '''
    to_user = User.load_user_by_username(cursor, to_username)
    if to_user is None:
        print('User does not exist!')
    elif len(message_text) > 255:
        print('The message is longer than 255 characters!')
        return
    else:
        new_message = Message(from_id, to_user.id, message_text)
        new_message.save_to_db(cursor)
        print('Message is sent.')


def messages_list(cursor, user):
    '''
    Prints list of all messages of user in database.
    :param cursor: the cursor class object
    :param user: the user class object
    '''
    list_messages = Message.load_all_messages(cursor, user.id)
    for message in list_messages:
        from_user = User.load_user_by_id(cursor, message.from_id)
        print(f'from: {from_user.username}')
        print(f'date: {message.creation_date}')
        print(message.text)


if __name__ == '__main__':
    try:
        with connect(user='postgres', password='poltava1955', host='localhost', database='server_db') as connection:
            with connection.cursor() as cursor_:
                connection.autocommit = True
                if args.username and args.password:
                    user_ = User.load_user_by_username(cursor_, args.username)
                    if check_password(args.password, user_.hashed_password):
                        if args.list:
                            messages_list(cursor_, user_)
                        elif args.to and args.send:
                            send_message(cursor_, user_.id, args.to, args.send)
                        else:
                            parser.print_help()
                    else:
                        print("Incorrect password or User does not exists!")
                else:
                    print("Username and password are required.")
                    parser.print_help()
    except OperationalError as ex:
        print('Connection error. Check all data and try again.', ex)
