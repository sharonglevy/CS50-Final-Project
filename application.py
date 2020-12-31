import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///buddy.db")


@app.route("/")
@login_required
def index():
    """something will be here"""
    return render_template("main.html")
#fullname=fullname, adress=adress, country=country, city=city, town=town, email=email, number=number

@app.route("/newForm", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        userName = db.execute("SELECT userName FROM users WHERE id = :userid", userid=session["user_id"])
        userName = userName[0]
        userName = userName["username"]
        buddydata = db.execute("SELECT * FROM buddies WHERE username = :username", username = userName)
        if len(buddydata) > 0:
            return render_template("newForm.html")
        else:
            return render_template("main.html", message = "It looks like it's your first buddy, if you haven't already, please go to 'My first Buddy' tab to start the process.")
    elif request.method == "POST":
        print("in post")
        userName = db.execute("SELECT userName FROM users WHERE id = :userid", userid=session["user_id"])
        userName = userName[0]
        userName = userName["username"]
        userdata = db.execute("SELECT * FROM profile WHERE username = :username", username = userName)
        userdata = userdata[0]
        fullname = userdata["fullname"]
        adress = userdata["adress"]
        country = userdata["country"]
        city = userdata["city"]
        town = userdata["town"]
        email = userdata["email"]
        cellNum = userdata["cellNum"]
        aboutMe = userdata["aboutMe"]
        helperORhelp = request.form.get("HorN")
        phoneORperson = request.form.get("Person/Phone")
        db.execute("INSERT INTO profile (username, fullname, email, cellNum, adress, country, city, town, PorP, HorH, aboutMe) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", userName, fullname, email, cellNum, adress, country, city, town, phoneORperson, helperORhelp, aboutMe)
        print("added the new value to profile")
        if helperORhelp == "Need help":
            need = "Helper"
        if helperORhelp == "Helper":
            need = "Need help"
        print("need ", need)
        match = db.execute("SELECT * FROM profile WHERE city = :city AND country = :country AND town = :town AND HorH = :need AND PorP = :PorP AND BUDDY = :negative", city=city, country=country, town=town, need=need, PorP=phoneORperson, negative="NO")
        print(match)
        if len(match) > 0:
            match = match[0]
            print (type(match))
            usernamematch = match["username"]
            emailmatch = match["email"]
            nummatch = match["cellNum"]
            citymatch = match["city"]
            aboutMeMatch = match["aboutMe"]

            db.execute("UPDATE profile SET BUDDY = :positive WHERE username = :username", positive = "YES", username=userName)
            db.execute("UPDATE profile SET BUDDY = :positive WHERE username = :username", positive = "YES", username=usernamematch)
            #new lines on db buddies for each buddy, this will show the respective profiles so they can connect
            db.execute("INSERT INTO buddies (username, BUDDY, email, city, number, aboutMe) VALUES (?, ?, ?, ?, ?, ?)", userName, usernamematch, emailmatch, citymatch, nummatch, aboutMeMatch)
            db.execute("INSERT INTO buddies (username, BUDDY, email, city, number, aboutMe) VALUES (?, ?, ?, ?, ?, ?)", usernamematch, userName, email, city, cellNum, aboutMe)
            rows = db.execute("SELECT * FROM buddies WHERE username = :username", username = userName)
            # a for now return statement
            return render_template("main.html", rows = rows)
        else:
            print("could'n find a match")
            return render_template("apology.html")
            return render_template("main.html", message = "We couldnt find a match for you, when we do a it will appear in your profile")
        return render_template("main.html")

@app.route("/FirstBuddy", methods=["GET", "POST"])
@login_required
def FirstBuddy():
    """Show first form and explain how this works"""
    if request.method == "POST":
        email = request.form.get("Email")
        cellNum = request.form.get("Contact Num")
        helperORhelp = request.form.get("HorN")
        name = request.form.get("FullName")
        phoneORperson = request.form.get("Person/Phone")
        adress = request.form.get("Adress")
        aboutMe = request.form.get("aboutMe")
        country = request.form.get("country")
        city = request.form.get("city")
        town = request.form.get("town")
        userName = db.execute("SELECT userName FROM users WHERE id = :userid", userid=session["user_id"])
        userName = userName[0]
        userName = userName["username"]
        rows = db.execute("SELECT * FROM profile WHERE username = :username", username=userName)
        if len(rows) > 0:
            return apology("Sorry, you have already created your profile, if you want another buddy, go to 'get another buddy', thanks!")
        else:
            db.execute("INSERT INTO profile (username, fullname, email, cellNum, adress, country, city, town, PorP, HorH, aboutMe) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", userName, name, email, cellNum, adress, country, city, town, phoneORperson, helperORhelp, aboutMe)

        if helperORhelp == "Need help":
            need = "Helper"
        if helperORhelp == "Helper":
            need = "Need help"
        print("need ", need)
        match = db.execute("SELECT * FROM profile WHERE city = :city AND country = :country AND town = :town AND HorH = :need AND PorP = :PorP AND BUDDY = :negative", city=city, country=country, town=town, need=need, PorP=phoneORperson, negative="NO")
        print(match)
        if len(match) > 0:
            match = match[0]
            print (type(match))
            usernamematch = match["username"]
            emailmatch = match["email"]
            nummatch = match["cellNum"]
            citymatch = match["city"]
            aboutMeMatch = match["aboutMe"]

            db.execute("UPDATE profile SET BUDDY = :positive WHERE username = :username", positive = "YES", username=userName)
            db.execute("UPDATE profile SET BUDDY = :positive WHERE username = :username", positive = "YES", username=usernamematch)
            #new lines on db buddies for each buddy, this will show the respective profiles so they can connect
            db.execute("INSERT INTO buddies (username, BUDDY, email, city, number, aboutMe) VALUES (?, ?, ?, ?, ?, ?)", userName, usernamematch, emailmatch, citymatch, nummatch, aboutMeMatch)
            db.execute("INSERT INTO buddies (username, BUDDY, email, city, number, aboutMe) VALUES (?, ?, ?, ?, ?, ?)", usernamematch, userName, email, city, cellNum, aboutMe)
            rows = db.execute("SELECT * FROM buddies WHERE username = :username", username = userName)
            # a for now return statement
            return render_template("apology.html")
            return render_template("main.html", rows = rows)
        else:
            print("could'n find a match")
            return render_template("apology.html")
            return render_template("main.html", message = "We couldnt find a match for you, when we do a it will appear in your profile")
    else:
        userName = db.execute("SELECT userName FROM users WHERE id = :userid", userid=session["user_id"])
        userName = userName[0]
        userName = userName["username"]
        userdata = db.execute("SELECT * FROM profile WHERE username = :username", username = userName)
        if len(userdata) > 0:
            userdata = userdata[0]
            print(userdata)
            return render_template("main.html", message = "It looks like you have already requested your first Buddy, as soon as a you match your new buddy will appear in 'My buddies' tab.")
        else:
            return render_template("FirstBuddy.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/changeMyData", methods=["GET", "POST"])
@login_required
def changeMyData():
    """Change data."""
    userName = db.execute("SELECT userName FROM users WHERE id = :userid", userid=session["user_id"])
    userName = userName[0]
    userName = userName["username"]
    if request.method == "GET":
        userdata = db.execute("SELECT * FROM profile WHERE username = :username", username = userName)
        userdata = userdata[0]
        fullname = str(userdata["fullname"])
        adress = str(userdata["adress"])
        country = userdata["country"]
        city = userdata["city"]
        town = userdata["town"]
        email = userdata["email"]
        cellNum = userdata["cellNum"]
        aboutMe = userdata["aboutMe"]
        return render_template("changeMyData.html", userName = userName, fullname=fullname, email=email, cellNum=cellNum, adress=adress, country=country, city=city, town=town, aboutMe=aboutMe)
    elif request.method == "POST":
        newemail = request.form.get("Email")
        newnum = request.form.get("Contact Num")
        newadress = request.form.get("Adress")
        newcountry = request.form.get("country")
        newcity = request.form.get("city")
        newtown = request.form.get("town")
        newaboutme = request.form.get("aboutMe")
        rowsprofile = db.execute("SELECT * FROM profile WHERE username = :username", username = userName)
        rowsbuddy = db.execute("SELECT * FROM buddies WHERE BUDDY = :username", username = userName)
        for row in rowsprofile:
            db.execute("UPDATE profile SET email = :email WHERE username = :username", email = newemail, username = userName)
            db.execute("UPDATE profile SET cellNum = :number WHERE username = :username", number = newnum, username = userName)
            db.execute("UPDATE profile SET adress = :adress WHERE username = :username", adress = newadress, username = userName)
            db.execute("UPDATE profile SET country = :country WHERE username = :username", country = newcountry, username = userName)
            db.execute("UPDATE profile SET city = :city WHERE username = :username", city = newcity, username = userName)
            db.execute("UPDATE profile SET town = :town WHERE username = :username", town = newtown, username = userName)
            db.execute("UPDATE profile SET aboutMe = :aboutme WHERE username = :username", aboutme = newaboutme, username = userName)
        for row in rowsbuddy:
            db.execute("UPDATE buddies SET email = :email WHERE BUDDY = :username", email = newemail, username = userName)
            db.execute("UPDATE buddies SET number = :number WHERE BUDDY = :username", number = newnum, username = userName)
            db.execute("UPDATE buddies SET city = :city WHERE BUDDY = :username", city = newcity, username = userName)
            db.execute("UPDATE buddies SET aboutMe = :aboutme WHERE BUDDY = :username", aboutme = newaboutme, username = userName)
        return render_template("main.html", message = "Your data has been updated, it will reflect in the data that we pass on to your buddies")


@app.route("/myBuddies")
@login_required
def myBuddies():
    """Get buddies list."""
    userName = db.execute("SELECT userName FROM users WHERE id = :userid", userid=session["user_id"])
    userName = userName[0]
    userName = userName["username"]
    rows = db.execute("SELECT * FROM buddies WHERE username = :username", username = userName)
    if len(rows) > 0:
        return render_template("myBuddies.html", rows = rows)
    else:
        return render_template("myBuddies.html", message = "You don't have a buddy yet, we'll find one for you soon!")

@app.route("/changePassword", methods=["GET", "POST"])
@login_required
def changePassword():
    """Get buddies list."""
    if request.method == "GET":
        return render_template("changePassword.html")
    elif request.method == "POST":
        userName = db.execute("SELECT userName FROM users WHERE id = :userid", userid=session["user_id"])
        userName = userName[0]
        userName = userName["username"]
        rows = db.execute("SELECT * FROM users WHERE username = :username", username = userName)
        if not check_password_hash(rows[0]["hash"], request.form.get("passwordnow")):
            return render_template("index.html", message = "Password was incorrect")
        else:
            newpassword = request.form.get("newpassword")
            connewpassword = request.form.get("confpass")
            print(newpassword)
            print(connewpassword)

            if len(newpassword) >= 8:
                dig = any(char.isdigit() for char in newpassword)
                if dig == True:
                    if str(newpassword) == str(connewpassword):
                        newpassword = generate_password_hash(newpassword)
                        db.execute("UPDATE users SET hash = :newpassword WHERE username = :username", newpassword = newpassword, username = userName)
                    else:
                    #message = "The passwords do not match, please re enter them"
                        return render_template("main.html", message = "The passwords do not match, please try again")
            else:
                return render_template("main.html", message = "The password does not have any number, try again.")

        return render_template("main.html", message = "Password has been updated")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
    if request.method == "GET":
            return render_template("register.html")


    # User reached route via POST (as by submitting a form via POST)
    elif request.method == "POST":
        name = request.form.get("username")
        password = request.form.get("password")
        confpass = request.form.get("confpassword")

        #check password and confpassword are the same(or in script?)
        counter = 0

        #check password has at least 8 characters
        if len(password) >= 8:
            dig = any(char.isdigit() for char in password)
            print(dig)
            if dig == True:
                if str(password) == str(confpass):

                    # Query database for username
                    rows = db.execute("SELECT * FROM users WHERE username = :username",
                                  username=request.form.get("username"))

                    # Ensure username exists and password is correct
                    if len(rows) == 1:
                        return render_template("apology.html", message = "Please use another user name, this one is already in use")

                    elif counter == 0:
                        password = generate_password_hash(password)
                        db.execute("INSERT INTO users(username, hash) values(:name, :password)", name = name, password = password)
                        #message = "you were succesuflly registered, please login into your account."
                        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
                        session["user_id"] = rows[0]["id"]
                        return render_template("index.html", message = "Registered successfully!")

                else:
                    #message = "The passwords do not match, please re enter them"
                    return render_template("apology.html", message = "The passwords do not match, please re enter them")
            else:
                return render_template("apology.html", message = "The password does not have any number, please re enter it.")
        else:
            return render_template("apology.html", message = "The password does not have 8 characters or more, please enter another password.")

    return apology("TODO")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
