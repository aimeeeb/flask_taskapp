# Created by Aimee Bowen
# Student ID: 2277842
# Email: bowen126@mail.chapman.edu
# Description: Student object class that stores data for name, gpa, major, and adviser.
# It includes simple GET functions for returning student variables.


class List:

    def __init__(self, title, user_id):
        self.title = title
        self.user = user_id

    def get_title(self):
        return self.title

    def get_user(self):
        return self.user

    def get_list(self):
        return (self.get_title(), self.get_user(),)

