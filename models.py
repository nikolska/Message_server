from clcrypto import hash_password


class User:
    '''
    A class used to represent a User.

    ...

    Attributes
    ----------
    _id : int
       user ID
    username : str
        user name
    _hashed_password : str
        user hashed password


    Methods
    -------
    set_password:
        Set user password (used hashed function).
    save_to_db:
        Save data to database.
    load_user_by_id:
        Load user by user ID.
    load_user_by_username:
        Load user by user name.
    load_all_users:
        Load all users in database.
    delete:
        Delete all information about user from database.
    '''
    def __init__(self, username='', password='', salt=''):
        '''
        :param str username: user name
        :param str password: user password
        :param str salt: cryptographic salt, default=None
        '''
        self._id = -1
        self.username = username
        self._hashed_password = hash_password(password, salt)

    @property
    def id(self):
        '''
        :return: object ID
        '''
        return self._id

    @property
    def hashed_password(self):
        '''
        :return: object hashed password
        '''
        return self._hashed_password

    def set_password(self, password, salt=''):
        '''
        Set user password (used hashed function).
        :param str password: user password
        :param str salt: cryptographic salt, default=None
        '''
        self._hashed_password = hash_password(password, salt)

    @hashed_password.setter
    def hashed_password(self, password):
        '''
        :param str password: user password
        :return: user hashed password
        '''
        self.set_password(password)

    def save_to_db(self, cursor):
        '''
        Create new user and save it to database or update user's information if user is exist.
        :param cursor: the cursor class object
        :return: True if saving was successful, False if not.
        '''
        if self._id == -1:
            sql = 'INSERT INTO users(username, hashed_password) VALUES(%s, %s) RETURNING id;'
            values = (self.username, self._hashed_password)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]
            return True
        else:
            sql = """UPDATE Users SET username=%s, hashed_password=%s WHERE id=%s"""
            values = (self.username, self.hashed_password, self.id)
            cursor.execute(sql, values)
            return True

    @staticmethod
    def load_user_by_id(cursor, id_):
        '''
        Load user by user ID.
        :param cursor: the cursor class object
        :param int id_: user ID
        :return: class User object if user is exist or None if doesn't.
        '''
        sql = 'SELECT id, username, hashed_password FROM users WHERE id=%s;'
        cursor.execute(sql, (id_,))
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user
        else:
            return None

    @staticmethod
    def load_user_by_username(cursor, username):
        '''
        Load user by user name.
        :param cursor: the cursor class object
        :param str username: user name
        :return: class User object if user is exist or None if doesn't.
        '''
        sql = 'SELECT id, username, hashed_password FROM users WHERE username=%s;'
        cursor.execute(sql, (username,))
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user
        else:
            return None

    @staticmethod
    def load_all_users(cursor):
        '''
        Load all users in database.
        :param cursor: the cursor class object
        :return: list of users
        '''
        sql = "SELECT id, username, hashed_password FROM users;"
        users = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            id_, username, hashed_password = row
            loaded_user = User()
            loaded_user._id = id_
            loaded_user.username = username
            loaded_user._hashed_password = hashed_password
            users.append(loaded_user)
        return users

    def delete(self, cursor):
        '''
        Delete user from database.
        :param cursor: the cursor class object
        :return: True if deleting was successful, False if not.
        '''
        sql = "DELETE FROM Users WHERE id=%s"
        cursor.execute(sql, (self.id,))
        self._id = -1
        return True


class Message:
    '''
        A class used to represent a Message.

        ...

        Attributes
        ----------
        _id : int
           message ID
        from_id : int
            user ID who's send the message
        to_id : int
            user ID to send the message to
        text : str
            message text
        _creation_date : date
            date of message creation


        Methods
        -------
        save_to_db:
            Save data to database.
        load_all_messages:
            Load all user messages in database.
        '''
    def __init__(self, from_id, to_id, text):
        '''
        :param int from_id: user ID who's send the message
        :param int to_id: user ID to send the message to
        :param str text: message text
        '''
        self._id = -1
        self.from_id = from_id
        self.to_id = to_id
        self.text = text
        self._creation_date = None

    @property
    def id(self):
        '''
        :return: message ID
        '''
        return self._id

    @property
    def creation_date(self):
        '''
        :return: message creation date
        '''
        return self._creation_date

    def save_to_db(self, cursor):
        '''
        Creates new message or update it if message exist.
        :param cursor: the cursor class object
        :return: True if saving was successful, False if not.
        '''
        if self._id == -1:
            sql = 'INSERT INTO messages(from_id, to_id, text) VALUES(%s, %s, %s) RETURNING id, creation_date'
            values = (self.from_id, self.to_id, self.text)
            cursor.execute(sql, values)
            self._id, self._creation_date = cursor.fetchone()
            return True
        else:
            sql = """UPDATE messages SET from_id=%s, to_id=%s, text=%s WHERE id=%s"""
            values = (self.from_id, self.to_id, self.text, self.id)
            cursor.execute(sql, values)
            return True

    @staticmethod
    def load_all_messages(cursor, user_id=None):
        '''
        Returns list of all messages of user in database.
        :param cursor: the cursor class object
        :param user_id: user ID
        :return: messages list
        '''
        if user_id:
            sql = 'SELECT id, from_id, to_id, text, creation_date FROM messages;'
            cursor.execute(sql, (user_id,))
        else:
            sql = "SELECT id, from_id, to_id, text, creation_date FROM messages"
            cursor.execute(sql)
        messages = []
        for row in cursor.fetchall():
            id_, from_id, to_id, text, creation_date = row
            loaded_message = Message(from_id, to_id, text)
            loaded_message._id = id_
            loaded_message._creation_date = creation_date
            messages.append(loaded_message)
        return messages

