import argparse
from models import User
from psycopg2 import connect, OperationalError
from psycopg2.errors import UniqueViolation
from clcrypto import check_password
import getpass

parser = argparse.ArgumentParser()

parser.add_argument('-u', '--username', help='username')
parser.add_argument('-l', '--list', help='list users', action='store_true')
parser.add_argument('-e', '--edit', help='edit user', action="store_true")
parser.add_argument('-d', '--delete', help='delete user', action="store_true")

args = parser.parse_args()


def create_user(cursor, username):
    '''
    Create user and save it to database.
    If user exists function returns UniqueViolation error.
    If user password is shorter than 8 characters function informs about that.
    :param cursor: the cursor class object
    :param str username: name of user
    '''
    if User.load_user_by_username(cursor, username) is None:
        password = getpass.getpass('Enter Your Password:')
        if len(password) >= 8:
            new_user = User(username, password)
            new_user.save_to_db(cursor)
            print(f'New user with ID {new_user.id} was created.')
        else:
            print('Password is too short!')
    else:
        raise UniqueViolation


def edit_password(cursor, username):
    '''
    Change user password to new one and save it in database.
    If user doesn't exist or new user password is shorter than 8 characters function informs about that.
    :param cursor:  the cursor class object
    :param str username: name of user
    :param str new_password: new user password to save
    '''
    user = User.load_user_by_username(cursor, username)
    password = getpass.getpass('Enter Your Password:')
    new_password = getpass.getpass('Enter Your New Password:')
    if user is None:
        print('User does not exist!')
    elif check_password(password, user.hashed_password):
        if len(new_password) >= 8:
            user.hashed_password = new_password
            user.save_to_db(cursor)
            print('Password is changed.')
        else:
            print('Password is too short!')
    else:
        print('Password is not correct!')


def delete_user(cursor, username):
    '''
    Delete all information about user in database.
    If user doesn't exist or user password doesn't correct function informs about that.
    :param cursor: the cursor class object
    :param str username: name of user
    '''
    user = User.load_user_by_username(cursor, username)
    password = getpass.getpass('Enter Your Password:')
    if user is None:
        print('User does not exist!')
    elif check_password(password, user.hashed_password):
        user.delete(cursor)
        print(f'User {user.username} was deleted.')
    else:
        print('Password is not correct!')


def users_list(cursor):
    '''
    Prints list of all users in database.
    :param cursor: the cursor class object
    '''
    users = User.load_all_users(cursor)
    for user in users:
        print(user.username)


if __name__ == '__main__':
    try:
        with connect(user='postgres', password='poltava1955', host='localhost', database='server_db') as connection:
            with connection.cursor() as cursor_:
                connection.autocommit = True
                if args.username and args.edit:
                    edit_password(cursor_, args.username)
                elif args.username and args.delete:
                    delete_user(cursor_, args.username)
                elif args.username:
                    create_user(cursor_, args.username)
                elif args.list:
                    users_list(cursor_)
                else:
                    parser.print_help()
    except OperationalError as ex:
        print('Connection error. Check all data and try again.', ex)
