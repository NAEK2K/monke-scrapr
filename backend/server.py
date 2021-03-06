# Backend API and routing for monkeScrapr
# By:
#   Hayden Mirza
#   Kyle Poirier-Szekely
#   Nicolas El-Khoury

import sqlite3
from dynaport.dynaport import Dynaport
from flask import Flask, request, session
from dotenv import load_dotenv
from util import generate_config
from flask_cors import CORS

scrapr = Dynaport().get_module(name="scrapr", path="../scrapr.py")
app = Flask(__name__)
CORS(app)
load_dotenv()

import os

app.secret_key = os.environ.get("secret")

# Create tables
tableConn = sqlite3.connect("users.db")
usersTable = """ CREATE TABLE IF NOT EXISTS USERS(
    USERNAME TEXT NOT NULL,
    PASSWORD TEXT NOT NULL,
    EMAIL TEXT NOT NULL,
    PRIMARY KEY(EMAIL)
)"""
configsTable = """ CREATE TABLE IF NOT EXISTS CONFIGS(
    EMAIL TEXT NOT NULL,
    CONFIG_NAME TEXT NOT NULL,
    CONFIG_PATH TEXT NOT NULL,
    PRIMARY KEY(CONFIG_PATH)
)"""
prawConfigsTable = """ CREATE TABLE IF NOT EXISTS PRAWS(
    EMAIL TEXT NOT NULL,
    CONFIG_NAME TEXT NOT NULL,
    CONFIG_PATH TEXT NOT NULL,
    PRIMARY KEY(CONFIG_PATH)
)"""

tableCursor = tableConn.cursor()
tableCursor.execute(usersTable)
tableCursor.execute(configsTable)
tableCursor.execute(prawConfigsTable)
tableConn.commit()
tableConn.close()

# Default landing page
@app.route("/")
def index():
    return "Hello world"


# TODO: Proper authentication. Only pushes data to database for now
# Register user
@app.route("/register", methods=["POST"])
def register():
    request_data = request.get_json()

    username = None
    email = None
    password = None

    if request_data:
        if "username" in request_data:
            username = request_data["username"]
        if "email" in request_data:
            email = request_data["email"]
        if "password" in request_data:
            password = request_data["password"]

        registerConn = sqlite3.connect("users.db")
        registerCursor = registerConn.cursor()
        try:
            registerCursor.execute(
                "INSERT INTO USERS (username, email, password) VALUES(?,?,?)",
                [username, email, password],
            )
        except:
            registerConn.close()
            return {"status": 400}, 400
        registerConn.commit()
        registerConn.close()
        session["email"] = email
        session["loggedIn"] = True
    return {"status": 200}, 200


# Login user
@app.route("/login", methods=["POST"])
def login():
    request_data = request.get_json()
    print(request_data)
    status = 401
    email = None
    password = None

    if request_data:
        if "email" in request_data:
            email = request_data["email"]
        if "password" in request_data:
            password = request_data["password"]

    loginConn = sqlite3.connect("users.db")
    loginCursor = loginConn.cursor()
    loginCursor.execute(
        "SELECT * FROM USERS WHERE email = ? AND password = ?", [email, password]
    )

    if loginCursor.fetchone():
        status = 200
        session["email"] = email
        session["loggedIn"] = True

    loginConn.close()
    print(session)
    return {"status": status}, status


# Logout user
@app.route("/logout", methods=["POST"])
def logout():
    if "loggedIn" in session and session["loggedIn"]:
        session.pop("email", None)
        session.pop("loggedIn", None)
        return {"status": 200}, 200
    else:
        return {"status": 400, "Error": "User not logged in."}, 400


@app.route("/reddit/runScraper", methods=["POST"])
def runRedditScraper():
    request_data = request.get_json()

    # prawconfig, scraperconfig
    prawConfig = None
    scraperConfig = None

    if request_data:
        if "prawConfig" in request_data:
            prawConfig = request_data["prawConfig"]
            conn = sqlite3.connect("users.db")
            c = conn.cursor()
            c.execute(
                "SELECT CONFIG_PATH FROM PRAWS WHERE EMAIL = ? AND CONFIG_NAME = ?",
                [session["email"], prawConfig],
            )
            praw_config_path = c.fetchone()[0]
            conn.close()
            if not praw_config_path:
                return {"status": 400}, 400
        if "scraperConfig" in request_data:
            scraperConfig = request_data["scraperConfig"]
            conn = sqlite3.connect("users.db")
            c = conn.cursor()
            c.execute(
                "SELECT CONFIG_PATH FROM CONFIGS WHERE EMAIL = ? AND CONFIG_NAME = ?",
                [session["email"], prawConfig],
            )
            config_path = c.fetchone()[0]
            conn.close()
            if not config_path:
                return {"status": 400}, 400
        redditScrapr = scrapr.RedditScrapr(config_path, praw_config_path)
        redditScrapr.scrape()
        return {"status": 200}, 200
    else:
        return {"status": 400}, 400


# Create config
@app.route("/reddit/createConfig", methods=["POST"])
def createConfig():
    request_data = request.get_json()
    print(request_data)
    print(session)

    email = session["email"]

    config_name = None
    if request_data:
        if "configName" in request_data:
            config_name = request_data["configName"]

        params = {
            "scrapr_type": "reddit",
            "limit": request_data.get("numPosts"),
            "subreddit": request_data.get("subreddit"),
            "sorting": request_data.get("sorting"),
            "keywords": request_data.get("keywords"),
            "tracked_users": request_data.get("trackedUsers"),
        }
        config_path = generate_config(config_name, "configs", **params)

        configConn = sqlite3.connect("users.db")
        configCursor = configConn.cursor()
        try:
            configCursor.execute(
                "INSERT INTO CONFIGS (EMAIL, CONFIG_NAME, CONFIG_PATH) VALUES(?,?,?)",
                [email, config_name, config_path],
            )
        except:
            configConn.close()
            return {"status": 400}, 400
        configConn.commit()
        configConn.close()
    return {"status": 200}, 200


@app.route("/reddit/getConfigs", methods=["GET"])
def getConfigs():
    email = session["email"]

    conn = sqlite3.connect("users.db")
    c = conn.execute("SELECT CONFIG_NAME FROM CONFIGS WHERE email = ?", [email])
    rows = c.fetchall()
    if not rows:
        conn.close()
        return {"status": 400}, 400

    configs = []
    for row in rows:
        praw_configs.append(row[0])

    return {"status": 200, "data": {"configs": configs}}, 200


# Create config
@app.route("/reddit/createPrawConfig", methods=["POST"])
def createPrawConfig():
    request_data = request.get_json()

    email = session["email"]
    config_name = None
    if request_data:
        if "configName" in request_data:
            config_name = request_data["configName"]

        params = {
            "client_id": request_data.get("clientId"),
            "client_secret": request_data.get("clientSecret"),
            "user_agent": request_data.get("userAgent"),
        }
        config_path = generate_config(config_name, "configs", **params)

        configConn = sqlite3.connect("users.db")
        configCursor = configConn.cursor()
        try:
            configCursor.execute(
                "INSERT INTO PRAWS (EMAIL, CONFIG_NAME, CONFIG_PATH) VALUES(?,?,?)",
                [
                    email,
                    config_name,
                    config_path,
                ],
            )
        except:
            configConn.close()
            return {"status": 400}, 400
        configConn.commit()
        configConn.close()
    return {"status": 200}, 200


# Get reddit all links
@app.route("/reddit/links", methods=["POST"])
def redditLinks():
    request_data = request.get_json()

    config_name = None
    config_path = None
    email = session["email"]

    if request_data:
        if "configName" in request_data:
            config_name = request_data["configName"]
    configConn = sqlite3.connect("users.db")
    configCursor = configConn.cursor()

    try:
        configCursor.execute(
            "SELECT CONFIG_PATH FROM USERS WHERE email = ? AND CONFIG_NAME = ?",
            [email, config_name],
        )
        config_path = configCursor.fetchone()
    except:
        configConn.close()
        return {"status": 400}, 400

    configConn.commit()
    configConn.close()

    return {
        "status": 200,
        "data": {"links": scrapr.RedditScrapr(config_path).get_all_links()},
    }, 200


@app.route("/reddit/getPrawConfigs", methods=["GET"])
def getPrawConfigs():
    prawConn = sqlite3.connect("users.db")
    prawCursor = prawConn.cursor()
    email = session["email"]
    prawCursor.execute("SELECT CONFIG_NAME FROM PRAWS WHERE EMAIL = ?", [email])
    praws = prawCursor.fetchall()
    prawList = []

    for praw in praws:
        prawList.append(praw[0])
    return {"data": {"praws": prawList}, "status": 200}


app.run(debug=True)
