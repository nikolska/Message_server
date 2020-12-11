import argparse
from models import User, Message, csr
from psycopg2.errors import UniqueViolation
from clcrypto import check_password

parser = argparse.ArgumentParser()

parser.add_argument('-u', '--username', help='username')
parser.add_argument('-p', '--password', help='password (min 8 characters)')
parser.add_argument('-n', '--new_password', help='new_password (min 8 characters)')
parser.add_argument('-l', '--list', help='list users', action='store_true')
parser.add_argument('-e', '--edit', help='edit user', action="store_true")
parser.add_argument('-d', '--delete', help='delete user', action="store_true")

args = parser.parse_args()


def create_user(cursor, username, password):
    if User.load_user_by_username(csr, username) is None:
        if len(password) >= 8:
            new_user = User(username, password)
            new_user.save_to_db(cursor)
            print(f'New user with ID {new_user.id} was created.')
        else:
            print('Password is too short!')
    else:
        raise UniqueViolation


def edit_password(cursor, username, password, new_password):
    user = User.load_user_by_username(cursor, username)
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


def delete_user(cursor, username, password):
    user = User.load_user_by_username(cursor, username)
    if user is None:
        print('User does not exist!')
    elif check_password(password, user.hashed_password):
        user.delete(cursor)
        print(f'User {user.username} was deleted.')
    else:
        print('Password is not correct!')


def users_list(cursor):
    users = User.load_all_users(cursor)
    for user in users:
        print(user.username)


# create_user(csr, 'Billie', 'green_day_ps')
# create_user(csr, 'Sherlock', 'my+hArd*_paSSw0rd')
# create_user(csr, 'Harry', 'h_potter')
# edit_password(csr, 'Ann', 'easy_password', 'new_password*327')
# delete_user(csr, 'Billie', 'green_day_ps')
# users_list(csr)
