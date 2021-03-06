# -*- coding: utf-8 -*-

# Enable SHA-256 sum
import hashlib
# Enable random string generator
import random
# Enable to get current datetime
from datetime import datetime
# Import global functions
from global_functions import escape
from global_functions import check_username


#----------------- Common Settings ------------------#


# Do not save the session for the all applications in the "system" controller
session.forget(response)


#----------------- Users Management -----------------#


def users_management():
    """
    Show standard users management page with all users listed in the table.

    :return: Users as the table
    """

    # Get all users join with last login datetime
    users = db(db.users.id == db.users_logins.user_id).select()
    return dict(
        users=users
    )


def add_user():
    """
    Add a new user to the system (into the table users, users_auth, users_logins).

    :return: Users as the table and operation result alert message
    """

    # Default alert
    alert_type = "success"
    alert_message = ""
    error = False

    # Check mandatory inputs
    if not (request.post_vars.username and request.post_vars.name and request.post_vars.organization and request.post_vars.email and
            request.post_vars.role and request.post_vars.password and request.post_vars.password_confirm):
        alert_type = "danger"
        alert_message = "Some mandatory input is missing!"
        error = True

    # Parse inputs
    username = escape(request.post_vars.username) if not error else ""
    name = escape(request.post_vars.name) if not error else ""
    organization = escape(request.post_vars.organization) if not error else ""
    email = escape(request.post_vars.email) if not error else ""
    role = escape(request.post_vars.role) if not error else ""
    password = escape(request.post_vars.password) if not error else ""
    password_confirm = escape(request.post_vars.password_confirm) if not error else ""

    # Check if username exists
    if not error and check_username(db, username):
        alert_type = "danger"
        alert_message = "Given username \"" + username + "\" already exists in the system!"
        error = True

    # Compare passwords
    if not error and (password != password_confirm):
        alert_type = "danger"
        alert_message = "Given passwords are different!"
        error = True

    # Insert user into tables
    if not error:
        # Insert into users table
        db.users.insert(username=username, name=name, organization=organization, email=email, role=role)
        # Get new user id
        user_id = db(db.users.username == username).select(db.users.id)[0].id
        # Generate salt and password
        salt = ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(20))
        hash = hashlib.sha256(salt + password).hexdigest()
        # Insert into users_auth table
        db.users_auth.insert(user_id=user_id, salt=salt, password=hash)
        # Set last login to default
        db.users_logins.insert(user_id=user_id, last_login=datetime.now())
        # Set success message
        alert_message = "User \"" + username + "\" successfully added to the system."

    # Get all users join with last login datetime
    users = db(db.users.id == db.users_logins.user_id).select()
    # Use standard view
    response.view = request.controller + '/users_management.html'
    return dict(
        alert_type=alert_type,
        alert_message=alert_message,
        users=users
    )


def delete_user():
    """
    Delete a given user from the system (from tables users, users_auth, users_logins).

    :return: Users as the table and operation result alert message
    """

    # Default alert
    alert_type = "success"
    alert_message = ""
    error = False

    # Check mandatory inputs
    if not request.post_vars.username:
        alert_type = "danger"
        alert_message = "Username not given!"
        error = True

    # Parse inputs
    username = escape(request.post_vars.username) if not error else ""

    # Check if username exists
    if not error and not check_username(db, username):
        alert_type = "danger"
        alert_message = "Given username \"" + username + "\" not exists in the system!"
        error = True

    # Delete user from all tables
    if not error:
        # Get user id
        user_id = db(db.users.username == username).select(db.users.id)[0].id
        # Delete from all users tables
        db(db.users.id == user_id).delete()
        db(db.users_auth.user_id == user_id).delete()
        db(db.users_logins.user_id == user_id).delete()
        # Set success message
        alert_message = "User \"" + username + "\" successfully deleted from the system."

    # Get all users join with last login datetime
    users = db(db.users.id == db.users_logins.user_id).select()
    # Use standard view
    response.view = request.controller + '/users_management.html'
    return dict(
        alert_type=alert_type,
        alert_message=alert_message,
        users=users
    )


def edit_user():
    """
    Update information about a given user.

    :return: Users as the table and operation result alert message
    """

    # Default alert
    alert_type = "success"
    alert_message = ""
    error = False

    # Check mandatory inputs
    if not (request.post_vars.username and request.post_vars.name and request.post_vars.organization and
            request.post_vars.email and request.post_vars.role):
        alert_type = "danger"
        alert_message = "Some mandatory input is missing!"
        error = True

    # Parse inputs
    username = escape(request.post_vars.username) if not error else ""
    name = escape(request.post_vars.name) if not error else ""
    organization = escape(request.post_vars.organization) if not error else ""
    email = escape(request.post_vars.email) if not error else ""
    role = escape(request.post_vars.role) if not error else ""

    # Check if username exists
    if not error and not check_username(db, username):
        alert_type = "danger"
        alert_message = "Given username \"" + username + "\" not exists in the system!"
        error = True

    # Check if user has correct permisions
    if not error and session.role == "user" and role != "user":
        alert_type = "danger"
        alert_message = "You do not have permission to update role of the user \"" + username + "\"!"
        error = True

    # Edit user in all users tables
    if not error:
        # Update table users
        db(db.users.username == username).update(name=name, organization=organization, email=email, role=role)
        # Set success message
        alert_message = "User \"" + username + "\" successfully updated."

    # Get all users join with last login datetime
    users = db(db.users.id == db.users_logins.user_id).select()
    # Use standard view.
    response.view = request.controller + '/users_management.html'
    return dict(
        alert_type=alert_type,
        alert_message=alert_message,
        users=users
    )


def change_password():
    """
    Set a new password for a given user.

    :return: Users as the table and operation result alert message
    """

    # Default alert
    alert_type = "success"
    alert_message = ""
    error = False

    # Check mandatory inputs
    if not (request.post_vars.username and request.post_vars.password_new and request.post_vars.password_confirm):
        alert_type = "danger"
        alert_message = "Some mandatory input is missing!"
        error = True

    # Parse inputs
    username = escape(request.post_vars.username) if not error else ""
    password_new = escape(request.post_vars.password_new) if not error else ""
    password_confirm = escape(request.post_vars.password_confirm) if not error else ""

    # Compare passwords
    if not error and (password_new != password_confirm):
        alert_type = "danger"
        alert_message = "Given passwords are different!"
        error = True

    # Set new password
    if not error:
        # Get user id
        user_id = db(db.users.username == username).select(db.users.id)[0].id
        # Get salt and generate a new hash
        salt = db(db.users_auth.user_id == user_id).select(db.users_auth.salt)[0].salt
        hash = hashlib.sha256(salt + password_new).hexdigest()
        # Update password
        db(db.users_auth.user_id == user_id).update(password=hash)
        # Set success message
        alert_message = "Password for the user \"" + username + "\" successfully changed."

    # Get all users join with last login datetime
    users = db(db.users.id == db.users_logins.user_id).select()
    # Use standard view
    response.view = request.controller + '/users_management.html'
    return dict(
        alert_type=alert_type,
        alert_message=alert_message,
        users=users
    )


#----------------- About ----------------------------#


def about():
    """
    Show the main page of the About section.

    :return: Empty dictionary
    """
    return dict()
