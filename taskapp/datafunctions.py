# Project: Task App (CPSC 408 Final)
# 
# Created by Aimee Bowen
# Student ID: 2277842
# Email: bowen126@mail.chapman.edu
# Description: This file includes all database queries for the app.

from taskapp import db_connection, login_manager
from taskapp.User import User
import csv
import os
import json

cursor = db_connection.cursor()

# given user ID, return User object
@login_manager.user_loader
def load_user(user_id):
    # check if user exists in database
    cursor.execute(""" SELECT deleted FROM Users WHERE UserId = %s """, (user_id,))
    if cursor.fetchone()[0]:
        return None
    else:
        # get user info and return user
        cursor.execute(""" SELECT UserId, Username, Email, Password FROM Users WHERE UserId = %s """, (user_id,))
        user_tuple = cursor.fetchone()
        user = User(user_tuple[0], user_tuple[1], user_tuple[2], user_tuple[3])
        return user


def create_list(title, date, user_id):
    # Use CreateList procedure
    cursor.callproc("CreateList", (title, date, user_id,))
    db_connection.commit()


def update_list(title, date, list_id):
    cursor.execute(""" UPDATE CalendarItems
                    JOIN Lists on Lists.CalendarItem = CalendarItems.ItemId
                    SET Title = %s, Date = %s
                    WHERE Lists.ListId = %s
                    """, (title, date, list_id,))
    db_connection.commit()


# returns an array of list dicts
def get_lists(user):
    cursor.execute("""
                    SELECT ListId, CI.Title, Complete
                    FROM Lists
                    JOIN CalendarItems CI on Lists.CalendarItem = CI.ItemId
                    WHERE Creator = %s AND Deleted IS NULL""",
                   (user,))
    results = cursor.fetchall()
    lists = []
    if results:
        i = 0
        while i < len(results):
            lists.append(
                {
                    'id': results[i][0],
                    'title': results[i][1],
                    'complete': results[i][2],
                    'tasks': get_tasks(results[i][0])
                }
            )
            i += 1
    return lists

# returns a single dict of a list
def get_list(list_id):
    cursor.execute("""
                    SELECT ListId, CI.Title, Complete
                    FROM Lists
                    JOIN CalendarItems CI on Lists.CalendarItem = CI.ItemId
                    WHERE ListId = %s AND Deleted IS NULL""",
                   (list_id,))
    results = cursor.fetchone()
    if not results:
        return None
    else:
        this_list = {
            'id': results[0],
            'title': results[1],
            'complete': results[2],
            'tasks': get_tasks(results[0])
        }
        return this_list


def delete_list(list_id):
    cursor.execute(" UPDATE Lists SET Deleted = NOW() WHERE ListId = %s ", (list_id,))
    db_connection.commit()


def create_task(title, date, description, list_id):
    # use CreateTask procedure
    cursor.callproc("CreateTask", (title, date, description, list_id,))
    db_connection.commit()


# returns an array of task dicts
def get_tasks(list_id):
    cursor.execute("""
                    SELECT TaskId, CI.Title, Description, Complete
                    FROM Tasks
                    JOIN CalendarItems CI on Tasks.CalendarItem = CI.ItemId
                    WHERE List = %s AND Deleted IS NULL""",
                   (list_id,))
    results = cursor.fetchall()
    tasks = []
    if results:
        i = 0
        while (i < len(results)):
            tasks.append(
                {
                    'id': results[i][0],
                    'title': results[i][1],
                    'description': results[i][2],
                    'complete': results[i][3]
                }
            )
            i += 1
    return tasks


# create a CSV of one list
def create_list_csv(list_id):
    # get current path
    path = os.getcwd() + "\\"
    # create filename
    file = str("CSVList" + str(list_id) + ".csv")
    filepath = path + file
    # get tasks
    tasks = get_tasks(list_id)
    # write to csv
    fieldnames = list(tasks[0].keys())
    with open(filepath, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        for task in tasks:
            writer.writerow(task)
    # returns a dict with the path and filename
    return {'path': path, 'filename': file}


# create a CSV with all tasks for a user
def create_alltasks_csv(user_id):
    # get current path
    path = os.getcwd() + "\\"
    # get username for filename
    cursor.execute("SELECT Username FROM Users WHERE UserId = %s", (user_id,))
    username = cursor.fetchone()[0]
    file = str(str(username) + "_alltasks.csv")
    filepath = path + file
    # join CalendarItems, Lists, and Tasks to get all information
    cursor.execute("""
        SELECT lists.title, CI.Title, Tasks.Description, CI.Date
        FROM Tasks
        JOIN CalendarItems CI on Tasks.CalendarItem = CI.ItemId
        JOIN (  SELECT C.Title title, ListId, Creator
                FROM Lists 
                JOIN CalendarItems C ON Lists.CalendarItem = C.ItemId) lists on lists.ListId = Tasks.List
        WHERE lists.Creator = %s
    """, (user_id,))
    results = cursor.fetchall()
    # write to file
    fieldnames = ["List", "Task", "Description", "Due Date"]
    with open(filepath, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if results:
            i = 0
            while (i < len(results)):
                writer.writerow({'List': results[i][0],
                                 'Task': results[i][1],
                                 'Description': results[i][2],
                                 'Due Date': results[i][3]
                                 })
                i += 1
    # returns a dict with the path and filename
    return {'path': path, 'filename': file}


# returns the number of tasks for a user
def count_tasks(user_id):
    cursor.execute(""" 
                        SELECT COUNT(TaskId)
                        FROM Tasks
                        JOIN Lists ON Lists.ListId = Tasks.List
                        WHERE Lists.Creator = %s AND Tasks.Deleted IS NULL
                    """, (user_id,))
    result = cursor.fetchone()[0]
    return result


# returns the number of lists for a user
def count_lists(user_id):
    cursor.execute(""" 
                    SELECT COUNT(ListId) 
                    FROM Lists
                    WHERE Creator = %s AND Deleted IS NULL
                    GROUP BY Creator
                    """, (user_id,))
    result = cursor.fetchone()[0]
    return result


def create_event(title, event_time, user_id):
    # use CreateEvent stored protocol
    cursor.callproc("CreateEvent", (title, event_time, user_id,))
    db_connection.commit()


# returns array of dicts for all valid CalendarItems
def get_events(user_id):
    cursor.execute("""
        SELECT *
        FROM CalendarItems
        WHERE ItemId IN (SELECT CalendarItem FROM Events WHERE Creator = %s)
            OR ItemId IN (SELECT CalendarItem FROM Lists WHERE Creator = %s)
            OR ItemId IN (SELECT Tasks.CalendarItem FROM Tasks JOIN Lists L ON Tasks.List = L.ListId WHERE L.Creator = %s)
        """, (user_id, user_id, user_id))
    results = cursor.fetchall()
    events = []
    if results:
        i = 0
        while i < len(results):
            if results[i][2]:
                events.append(
                    {
                        'id': results[i][0],
                        'title': results[i][1],
                        'start': results[i][2]
                    }
                )
            i += 1
    return events


# returns json of all events
def calendar_json(user_id):
    all_items = []
    events = get_events(user_id)
    for item in events:
        all_items.append({
            'title': item["title"],
            'start': str(item["start"])
        })
    all_items_json = json.dumps(all_items)
    return all_items_json

