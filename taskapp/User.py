# Project: Task App (CPSC 408 Final)
# 
# Created by Aimee Bowen
# Student ID: 2277842
# Email: bowen126@mail.chapman.edu
# Description: User class for handling user login and registration. Extends UserMixin.

from flask_login import UserMixin


class User(UserMixin):

    def __init__(self, user_id, username, email, password):
        if user_id:
            self.id = user_id
        self.username = username
        self.email = email
        self.password = password
        super().__init__()

    def get_username(self):
        return self.username

    def get_email(self):
        return self.email

    def get_password(self):
        return self.password

    def get_user(self):
        return (self.get_username, self.get_email, self.get_password,)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

