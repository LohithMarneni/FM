from flask import Flask, render_template, request
import google.generativeai as genai
genai.configure(api_key="AIzaSyAl4NDlsCEJxQpBhqa-3IRxxLSMw1gI-Dc")
app = Flask(__name__)
questions = [
    {"id": 1, "question": "What type of meal are you in the mood for?", 
     "options": ["Breakfast", "Lunch", "Dinner", "Snack"]},
    {"id": 2, "question": "What cuisine do you prefer?", 
     "options": ["Italian", "Mexican", "Indian", "Chinese", "American", "Mediterranean"]},
    {"id": 3, "question": "Do you have any dietary preferences or restrictions?", 
     "options": ["Vegetarian", "Non-Vegetarian", "Vegan", "Gluten-Free", "No preference"]},
    {"id": 4, "question": "How much time do you have to prepare the meal?", 
     "options": ["Less than 15 mins", "15-30 mins", "30-60 mins", "More than 60 mins"]},
    {"id": 5, "question": "What type of flavor profile are you in the mood for?", 
     "options": ["Sweet", "Savory", "Spicy", "Tangy", "Mild", "No preference"]},
    {"id": 6, "question": "Are you looking for a light or filling meal?", 
     "options": ["Light", "Filling", "No preference"]}
]

@app.route('/')
def index():
    prompt = """
    Generate eight questions in JSON array format to assess food preferences.
    Each question should be an object with:
    - "id": unique identifier
    - "question": question text
    - "options": an array of answer choices.
    Return only the JSON array without extra text.
    """
    model = genai.GenerativeModel('gemini-pro')
    questions_response = model.generate_content(prompt)
    return render_template('index.html', questions=questions_response.text)

@app.route('/suggest', methods=['POST'])
def suggest_food():
    user_answers = {}
    for question in questions:
        user_answers[question['id']] = request.form.get(str(question['id']))
    prompt = "Suggest three suitable food items based on the following preferences, and return them in an array format:\n"
    for question in questions:
        answer = user_answers[question['id']]
        prompt += f"{question['question']} {answer}\n"
    prompt += "\nReturn only an array of three food items."
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return render_template('suggestion.html', suggestion=response.text)
if __name__ == '__main__':
    app.run(debug=True)