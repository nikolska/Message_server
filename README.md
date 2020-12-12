# Message_server

Programs are supposed to take parameters from the command line.

<b>Users</b> - adding, modifying non-key information about yourself, deleting your account. The user is to be identified by login (cannot be repeated).

<b>Broadcasting messages</b> - each user can create an unlimited number of messages for any user. The maximum length of an entry is 255 characters.

<b>Receiving messages</b> - each user can read the messages he has received from other users.

<b>The program Users is to take the following parameters:</b>

-u or --username: user login,

-p or --password: user's password, check if it is at least eight characters long,

-n or --new-pass: new user password,

-l or --list: request to list all users,

-d or --delete: user login to be deleted,

-e or --edit: user login to be modified.

<b>The program Messages is to take the following parameters:</b>

-u or --username: user login,

-p or --password: password for identification,

-l or --list: request to list all messages,

-t or --to: set the username to which we want to send the message,

-s or --send: send the message to the user (message text).
