# Task App

Created by Aimee Bowen

Email: bowen126@mail.chapman.edu

#### Description

This is a flask application created to run in local. It includes user login. Users are able to created lists, tasks, and events. Lists and tasks appear on the home page. All three types require dates and populate the calendar page. Tasks can also be exported to CSV.

## Directions to run

- **app.py** run this file using python to run the application.
- **final_project.sql** database for website.
- **__init__.py** holds base information for app functionality. To connect it to the your own database, edit db_connection to your configuration

## Modules used

**flask**
**flask_login**
**flask_bcrypt**
**mysql.connector**

## Sources used

- Base app uses code from [Corey Shafer's](https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/Flask_Blog) Flask Blog tutorial [on YouTube](https://www.youtube.com/playlist?list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH)
- Parts of calendar were pulled from [sukeesh/flask-calendar](https://github.com/sukeesh/flask-calendar)
- Method for datepicker on datetime inputs taken from [miguelgrinberg](https://gist.github.com/miguelgrinberg/5a1b3749dbe1bb254ff7a41e59cf04c9)
