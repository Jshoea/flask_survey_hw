from flask import Flask, request, session, redirect, flash, render_template
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

RESPONSE_KEY = "responses"
debug = DebugToolbarExtension(app)
app = Flask(__name__)
app.config['SECRET KEY'] = "dont-tell"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
#we do not want strict redirects from the debugger

@app.route("/")
def show_survey_start():
    """Select the survey"""

    return render_template("survey_start.html", survey=survey)

@app.route("/begin", methods=["POST"])
def start_survey():
    session[RESPONSE_KEY]= []
    return redirect("/questions/0")
    #this will reset the session of responses

@app.route("/answer", methods["POST"])
def handle_question():
    """Savee responses and redirect to next questions"""

    choice = request.form['answer']

    #add responses to session
    responses = session[RESPONSE_KEY]
    responses.append(choice)
    session[RESPONSE_KEY] = responses 

    #if the response numbers are the same as the question
    if(len(responses) == len(survey.questions)):
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(responses)}")
    
@app.route("/questions/<int:qid>")
def show_questions(qid):
    """Display the current Question"""
    responses = session.get(RESPONSE_KEY)

    if(responses is None):
        return redirect("/")

    if(len(responses) == len(survey.questions)):
        return redirect("/complete")

    if (len(responses != qid)):
        flash(f"Invalid Question Id: {qid}.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.question[qid]
    return render_template( "question.html", question_num = qid,
        question=question)


#app route for finished survey
@app.route("/complete")
def complete():
    """Show completion page"""

    return render_template("completion.html")


