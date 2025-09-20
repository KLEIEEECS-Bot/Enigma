from flask import Flask, render_template, request
from utils import call_gemini_api

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    description = request.form['description']

    # Use Gemini API to generate story and checklist
    response = call_gemini_api(description)

    story = response.get("story", "We couldn't analyze this input well. Please be careful online.")
    checklist = response.get("checklist", [
        "Be cautious of anything unusual online.",
        "Change passwords if you suspect a problem.",
        "Ask a trusted person for help if unsure."
    ])

    message = "We've analyzed your text and generated the following results!"

    return render_template('output.html', story=story, checklist=checklist, message=message)

if __name__ == '__main__':
    app.run(debug=True)
