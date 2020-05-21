# Created by Aimee Bowen
# Student ID: 2277842
# Email: bowen126@mail.chapman.edu
# Description: Student object class that stores data for name, gpa, major, and adviser.
# It includes simple GET functions for returning student variables.


class Task:

    def __init__(self, title, description, list_id):
        self.title = title
        self.description = description
        self.list = list_id

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_list(self):
        return self.list

    def get_list(self):
        return (self.get_title(), self.get_description(), self.get_list())