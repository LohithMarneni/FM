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
    {"id": 4, "question": "What type of flavor profile are you in the mood for?", 
     "options": ["Sweet", "Savory", "Spicy", "Tangy", "Mild", "No preference"]},
    {"id": 5, "question": "Are you looking for a light or filling meal?", 
     "options": ["Light", "Filling", "No preference"]}
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/question', methods=['POST', 'GET'])
def question():
    return render_template('question.html', questions=questions)

@app.route('/suggest', methods=['POST'])
def suggest_food():
    # Gather user's survey responses
    user_answers = {}
    for question in questions:
        user_answers[question['id']] = request.form.get(str(question['id']))
    prompt = "Suggest six suitable food items based on the following preferences, and return them in an array format:\n"
    for question in questions:
        answer = user_answers[question['id']]
        prompt += f"{question['question']} {answer}\n"
    prompt += "\nReturn only an array of six food items in the format ['','','','','','']."
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    
    
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    print(latitude)
    print(longitude)
    prompt = "Suggest ten restaurants near the location provided, "
    prompt += f"Location: Latitude {latitude}, Longitude {longitude}\n"
    prompt += "\nReturn only an array of ten restaurant names in this format: ['','','','','','','','','','']." 
    model = genai.GenerativeModel('gemini-pro')
    res_response = model.generate_content(prompt)
    return render_template('suggestion.html', suggestion=response.text , ress = res_response.text)

if __name__ == '__main__':
    app.run(debug=True)