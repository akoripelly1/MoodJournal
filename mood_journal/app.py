
from flask import Flask, render_template, request, redirect, url_for

import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to Mood Journal!"

@app.route("/home")
def home_redirect():
    return render_template("home.html")



@app.route("/log", methods = ["GET", "POST"])
def log_mood():
    if request.method == "POST":
        mood = request.form["mood"]
        note = request.form.get("note", "")

        #saving to database
        conn = sqlite3.connect("mood_journal.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO mood_logs (mood, note) VALUES (?, ?)", (mood, note))
        conn.commit()
        conn.close()
        return redirect(url_for("view_history"))
    return render_template("log_mood.html")


@app.route("/history")
def view_history():
        conn = sqlite3.connect("mood_journal.db")
        cursor = conn.cursor()
        cursor.execute("SELECT mood, note, date FROM mood_logs")
        conn.commit()
        logs = cursor.fetchall()
        conn.close()

        return render_template("history.html", logs = logs)








if __name__ == '__main__':
    app.run(debug = True, port = 5002)