from flask import Flask, render_template, request, redirect, url_for, session
import json
import random

app = Flask(__name__)
app.secret_key = "quiz_secret_key"

# Load questions from file
with open("questions.json", "r") as f:
    questions = json.load(f)

@app.route("/")
def index():
    topics = list(questions.keys())
    return render_template("index.html", topics=topics)

@app.route("/quiz/<topic>")
def quiz(topic):
    if topic not in questions:
        return "Topic not found", 404

    quiz_questions = random.sample(questions[topic], len(questions[topic]))
    session["quiz"] = quiz_questions
    session["score"] = 0
    session["current"] = 0
    return redirect(url_for("question"))

@app.route("/question", methods=["GET", "POST"])
def question():
    if request.method == "POST":
        selected = request.form.get("option")
        if selected:
            prev_q = session["quiz"][session["current"] - 1]
            if selected == prev_q["answer"]:
                session["score"] += 1

    if session["current"] >= len(session["quiz"]):
        return redirect(url_for("result"))

    q = session["quiz"][session["current"]]
    session["current"] += 1

    return render_template(
        "quiz.html",
        question=q,
        current=session["current"],
        total=len(session["quiz"])
    )

@app.route("/result")
def result():
    score = session.get("score", 0)
    total = len(session.get("quiz", []))
    return render_template("result.html", score=score, total=total)

if __name__ == "__main__":
    app.run(debug=True)
