# Bosch Internship Django Polls

This is a project for an application as an intern at Bosch. The task for this project was follow the  
[Django Getting Started Tutorial](https://www.djangoproject.com/start/). The application in this Tutorial
was about creating an application  
where users can vote on polls and create polls.

## Start The Program

Prerequisite: Python 3 has to be installed, as well as Django 3.6

Run the following command to start the application:  
<code>python manage.py runserver</code>

There is already an admin user in the database, but a new one can be created with this command:  
<code>python manage.py createsuperuser</code>  
The creadentials for the current user are for both the username and password "admin".

## Routes

### "/"

This is the homepage where all polls are visible and can be searched after Question and tag.

### "/polls/:id"

This is the page for displaying a specific poll. Here a user can select a displayed answer to vote for it.

### "/polls/:id/delete"

This is the page for removing a specific poll. This page can only be accessed by the creator of the poll.

### "/create-poll"

This is the page for creating a new poll. This form will only create a poll if the current user is logged into  
the system. The number of answers for a poll must be at least 3, but more answers can be added.

### "/login"

This is the page where a user can log into an existing account.

### "/signup"

This is the page where a new user can be created. After creation the user is automatically logged in.
