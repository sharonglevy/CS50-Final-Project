# CS50-Final-Project
CS50 Final Project - PB Pandemic Buddy

The project is a webpage where people can ask for help from someone else or donate their time to another person that needs taht help. The idea came from the difficult year that we have passed,
this was specially thought to offer a special help for risk groups that had to stay home and needed someone to do the shopping for them or maybe just someone to talk to for a while.

The idea is simple. When the user registers the passwords need to have 8 characters minimun and at least one number. Beforestoring the password in the database it will be hashed.
Then you can ask for your first Buddy, for that the user will have to fill a form with the following fields:
Full name
Email
Contact number
Country
City
Town
About me (As a presentation to your new buddy)
Adress
Are you a helper or in need of help?
do you need help or offer help, in person or over the phone?

All of this data is going to be stored in a database and SOME of that content then is going to be shared with your Buddy.
Once you finish filling the form we will check in our databases to find you a buddy, that shares your city and town and that needs your help or wants to help you, depending on your needs and preferences regarding the type of help.
When you are matched with someone a Buddy card will appear in your 'My buddy' tab with your new Buddy's Contact information and an 'About me' field, the same but the other way around will appear on your Buddy's 'My buddy' tab.
If later you want to ask for another buddy you can fill a new form, that form will be very short because we already have most of your data, you will only need to tell us if you need help
or want to offer it, and if it's in person or over the phone.
If you later need to change some of your data you can go to change data and whaterver piece of data that you decide to update will be reflected on your profile shared with your buddy.
The user can also decide to change his or her password in the tab 'Change password', that will ask for the current password, the new one and a confirmation of the new one.
If the current password is correct it will check that the same rules that it had in the registration apply for the  new password and that the new password and the confirmation one are the same,
if they are equal the password will be updated in the database and next time the user logs in he or she will have to enter the new password.
Routing
Each route checks if the user is authenticated. It means if correct mail and password were supplied.

How to use
To run the web application use these commands:

$ export FLASK_APP=application.py
$ flask run
